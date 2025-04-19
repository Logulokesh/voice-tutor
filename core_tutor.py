import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import time
import logging
import json
from vosk import Model, KaldiRecognizer
from melo.api import TTS as MeloTTS
import ollama
import pygame.mixer
from tinydb import TinyDB, Query
import uuid
from functools import lru_cache
import threading
import queue

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class VoiceTutorCore:
    SAMPLE_RATES = [44100, 48000, 16000, 96000]  # Adjusted order to prioritize common rates

    def __init__(self, user_uuid=None):
        self.audio_settings = {
            "input_device": None,
            "output_device": None,
            "sample_rate": 44100,  # Changed to 44100 Hz to avoid ALSA issues
            "audio_system": "pygame"
        }
        self.recording = False
        self.audio_data = None
        self.available_devices = {"input": [], "output": []}
        self.refresh_audio_devices()

        self.db = TinyDB('voicetutor_db.json')
        self.user_query = Query()
        if user_uuid is None:
            self.user_uuid = str(uuid.uuid4())
            self.db.insert({'uuid': self.user_uuid, 'nickname': '', 'lessons': [], 'progress': {}, 'completed_topics': []})
            logger.info(f"New user created with UUID: {self.user_uuid}")
        else:
            self.user_uuid = user_uuid
            if not self.db.search(self.user_query.uuid == user_uuid):
                self.db.insert({'uuid': self.user_uuid, 'nickname': '', 'lessons': [], 'progress': {}, 'completed_topics': []})
            else:
                # Ensure 'completed_topics' exists for existing users
                user_data = self.db.search(self.user_query.uuid == user_uuid)[0]
                if 'completed_topics' not in user_data:
                    self.db.update({'completed_topics': []}, self.user_query.uuid == user_uuid)
            logger.info(f"Loaded user with UUID: {self.user_uuid}")

        syllabus_path = "syllabus.json"
        if os.path.exists(syllabus_path):
            with open(syllabus_path, "r") as f:
                self.syllabus = json.load(f)
        else:
            raise FileNotFoundError(f"syllabus.json not found at {syllabus_path}")

        model_path = "models/vosk-model-small-en-us-0.15"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Download Vosk model to {model_path}")
        self.vosk_model = Model(model_path)
        self.tts = None
        self.init_audio_system()
        self.llm_model = "granite3.2:latest"

    def refresh_audio_devices(self):
        devices = sd.query_devices()
        self.available_devices["input"] = [(i, d["name"]) for i, d in enumerate(devices) if d["max_input_channels"] > 0]
        self.available_devices["output"] = [(i, d["name"]) for i, d in enumerate(devices) if d["max_output_channels"] > 0]
        if not self.audio_settings["input_device"] and self.available_devices["input"]:
            self.audio_settings["input_device"] = self.available_devices["input"][0][0]
        if not self.audio_settings["output_device"] and self.available_devices["output"]:
            self.audio_settings["output_device"] = self.available_devices["output"][0][0]

    def init_tts(self):
        self.tts = MeloTTS(language="EN", device="cpu")

    def init_audio_system(self):
        pygame.mixer.init(frequency=self.audio_settings["sample_rate"])

    def start_recording(self):
        if self.recording:
            return False, "Already recording"
        try:
            self.audio_data = None
            sd.default.device = self.audio_settings["input_device"]
            sd.default.samplerate = self.audio_settings["sample_rate"]
            sd.default.channels = 2
            self.recording = True
            self.audio_data = sd.rec(int(10 * self.audio_settings["sample_rate"]), blocking=False)
            logger.info(f"Recording started with sample rate: {self.audio_settings['sample_rate']}")
            return True, "Recording started"
        except Exception as e:
            logger.error(f"Recording error: {e}")
            self.recording = False
            return False, f"Error: {e}"

    def stop_recording(self):
        if not self.recording:
            return False, "Not recording"
        self.recording = False
        sd.stop()
        sd.wait()
        logger.info("Recording stopped")
        return True, "Recording stopped"

    @lru_cache(maxsize=128)
    def get_syllabus_content(self, subject, level):
        return self.syllabus.get(subject.lower(), {}).get(level, {})

    def update_lesson(self, subject, level, user_input, tutor_response):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        lesson = {
            "subject": subject,
            "level": level,
            "user_input": user_input,
            "tutor_response": tutor_response,
            "timestamp": timestamp
        }
        user_data = self.db.search(self.user_query.uuid == self.user_uuid)[0]
        user_data["lessons"].append(lesson)
        self.db.update({'lessons': user_data["lessons"]}, self.user_query.uuid == self.user_uuid)
        logger.info(f"Lesson added for {self.user_uuid}: {subject} - {level}")

    def mark_topic_completed(self, subject, level, topic_code):
        """Mark a syllabus topic as completed in TinyDB."""
        user_data = self.db.search(self.user_query.uuid == self.user_uuid)[0]
        completed_topics = user_data.get("completed_topics", [])
        topic_key = f"{subject}_{level}_{topic_code}"
        if topic_key not in completed_topics:
            completed_topics.append(topic_key)
            self.db.update({'completed_topics': completed_topics}, self.user_query.uuid == self.user_uuid)
            logger.info(f"Marked {topic_key} as completed for user {self.user_uuid}")
        return True

    def get_completed_topics(self, subject, level):
        """Retrieve completed topics for a specific subject and level."""
        user_data = self.db.search(self.user_query.uuid == self.user_uuid)[0]
        completed_topics = user_data.get("completed_topics", [])
        return [t.split('_')[2] for t in completed_topics if t.startswith(f"{subject}_{level}_")]

    def generate_progress_report(self, nickname):
        user_data = self.db.search(self.user_query.uuid == self.user_uuid)[0]
        lessons = user_data["lessons"]
        
        report = f"Progress Report for {nickname} (UUID: {self.user_uuid})\n"
        report += "====================\n\n"
        covered = {}
        for lesson in lessons:
            subj = lesson["subject"]
            lvl = lesson["level"]
            if subj not in covered:
                covered[subj] = set()
            covered[subj].add(lvl)
        
        report += "Covered Subjects and Levels:\n"
        if not covered:
            report += "- No subjects covered yet.\n"
        else:
            for subject, levels in covered.items():
                report += f"- {subject.capitalize()}: {', '.join(sorted(levels))}\n"

        report += "\nRecent Lessons (Last 5):\n"
        if not lessons:
            report += "- No lessons yet.\n"
        else:
            for lesson in lessons[-5:]:
                report += f"- [{lesson['timestamp']}] You: {lesson['user_input']}\n"
                report += f"  Tutor: {lesson['tutor_response']}\n"

        total_topics = sum(len(self.syllabus[s][l]) for s in self.syllabus for l in self.syllabus[s])
        covered_topics = len(set((l["subject"], l["level"]) for l in lessons))
        progress_percentage = (covered_topics / total_topics * 100) if total_topics > 0 else 0
        report += f"\nProgress: Covered {covered_topics} unique subject-level pairs out of {total_topics} topics ({progress_percentage:.2f}%)\n"
        return report

    def recognize_speech(self, temp_file, result_queue):
        try:
            recognizer = KaldiRecognizer(self.vosk_model, self.audio_settings["sample_rate"])
            with open(temp_file, "rb") as wf:
                wf.read(44)
                while True:
                    data = wf.read(4096)
                    if len(data) == 0:
                        break
                    recognizer.AcceptWaveform(data)
            result = json.loads(recognizer.FinalResult()).get("text", "")
            result_queue.put(result)
        except Exception as e:
            result_queue.put(f"Recognition error: {e}")

    def send_to_tutor(self, nickname, subject, level, topic_code=None):
        if not self.recording or self.audio_data is None:
            return False, "Not recording"
        try:
            logger.info("Stopping recording for processing")
            sd.stop()
            sd.wait()
            if np.all(np.isnan(self.audio_data)):
                return False, "No audio recorded"

            audio_data = np.mean(self.audio_data, axis=1) if self.audio_data.shape[1] > 1 else self.audio_data.flatten()
            audio_data = np.clip(audio_data, -1.0, 1.0)
            if np.max(np.abs(audio_data)) <= 0.01:
                return False, "No audio detected"

            audio_data = (audio_data * 32767).astype(np.int16)
            temp_file = "temp.wav"
            write(temp_file, self.audio_settings["sample_rate"], audio_data)
            logger.info(f"Wrote temp.wav: {os.path.getsize(temp_file)} bytes")

            logger.info("Starting speech recognition")
            result_queue = queue.Queue()
            recognition_thread = threading.Thread(target=self.recognize_speech, args=(temp_file, result_queue))
            recognition_thread.start()

            recognition_thread.join(timeout=30)
            if recognition_thread.is_alive():
                logger.error("Speech recognition timed out after 30 seconds")
                return False, "Speech recognition took too long"
            
            result = result_queue.get()
            if os.path.exists(temp_file):
                os.remove(temp_file)
            logger.info(f"Recognized text: {result}")

            if not result:
                return False, "No speech detected"
            if result.startswith("Recognition error:"):
                return False, result

            syllabus_content = self.get_syllabus_content(subject, level)
            topic_desc = syllabus_content.get(topic_code, "General topic") if topic_code else "General topic"
            syllabus_str = f"{topic_code}: {topic_desc}" if topic_code else ", ".join(syllabus_content.keys())
            context = (
                f"Student: {nickname}, Subject: {subject}, Level: {level}, Selected Topic: {syllabus_str}\n"
                f"Student says: {result}\n"
            )
            logger.info("Generating tutor response")
            ollama_response = ollama.generate(
                model=self.llm_model,
                prompt=(
                    f"You are a classroom teacher speaking directly to a student. "
                    f"Based on the student's latest input and the selected syllabus topic ({syllabus_str}), "
                    f"teach a short, practical lesson or provide a clear, helpful answer to their question or concern. "
                    f"Focus on the specific topic provided and the student's input—do not stray into unrelated areas "
                    f"unless the student explicitly asks. Keep your response concise, engaging, and like a real teacher "
                    f"giving a lesson or support. If the student’s input is unrelated to the topic, gently guide them back. "
                    f"Context:\n{context}"
                )
            )
            response = ollama_response["response"].strip()
            logger.info(f"Tutor response: {response}")

            self.update_lesson(subject, level, result, response)
            if topic_code:
                self.mark_topic_completed(subject, level, topic_code)
            logger.info("Speaking response")
            self.speak_text(response)
            return True, {"recognized_text": result, "tutor_response": response}
        except Exception as e:
            logger.error(f"Error in send_to_tutor: {e}", exc_info=True)
            if os.path.exists("temp.wav"):
                os.remove("temp.wav")
            return False, f"Error: {e}"

    def speak_text(self, text):
        if not self.tts:
            self.init_tts()
        temp_audio = "temp_tts.wav"
        self.tts.tts_to_file(text, speaker_id=0, output_path=temp_audio)
        if self.audio_settings["audio_system"] == "pygame":
            pygame.mixer.music.load(temp_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        else:
            os.system(f"aplay {temp_audio}")
        os.remove(temp_audio)