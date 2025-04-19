import streamlit as st
import atexit
from core_tutor import VoiceTutorCore
import datetime
import ollama

# Set page config as the first Streamlit command
st.set_page_config(page_title="VoiceTutor Online Classroom", page_icon="🎓", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-container {
        background-color: #1e2130;  /* Dark background with blue-gray tone */
        color: #e0e6f0;  /* Light text for contrast */
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #121421;  /* Deeper dark background */
    }
    .sidebar .sidebar-content {
        background-color: #1e2130;  /* Dark sidebar */
        color: #e0e6f0;  /* Light text */
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background-color: #4e73df;  /* Preserved bright blue */
        color: white;
        border: none;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a5fc4;
        transform: scale(1.05);
    }
    .stSelectbox, .stTextInput>div>div>input {
        background-color: #2c3347;  /* Dark input background */
        color: #e0e6f0;  /* Light text */
        border-radius: 6px;
        border: 1px solid #3e4660;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2130;  /* Dark tab background */
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
        border-radius: 8px;
        color: #e0e6f0;  /* Light text for tabs */
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2c3347;  /* Slightly lighter dark background on hover */
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #4e73df;
        color: white;
    }
    /* Ensure text visibility in various Streamlit elements */
    .stMarkdown, .stText, .stInfo, .stWarning, .stError {
        color: #e0e6f0;
    }
    .stDataFrame, .stTable {
        background-color: #2c3347;
        color: #e0e6f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "core" not in st.session_state:
    st.session_state.user_uuid = None
    st.session_state.core = None
    st.session_state.nickname = ""
    st.session_state.subject = None
    st.session_state.level = None

def cleanup():
    core = st.session_state.get("core")
    if core and core.recording:
        core.stop_recording()

atexit.register(cleanup)

st.title("🎓 VoiceTutor Online Learning")
st.markdown("*Intelligent Voice-Powered Education*")

# User setup
with st.sidebar:
    st.header("User Setup")
    if st.session_state.user_uuid is None:
        if st.button("New User"):
            st.session_state.core = VoiceTutorCore()
            st.session_state.user_uuid = st.session_state.core.user_uuid
            new_nickname = st.text_input("Enter your nickname", value="Student", key="new_nickname")
            if new_nickname:
                st.session_state.nickname = new_nickname
                st.session_state.core.db.update(
                    {'nickname': st.session_state.nickname},
                    st.session_state.core.user_query.uuid == st.session_state.user_uuid
                )
            st.success(f"Your UUID: {st.session_state.user_uuid} (Save this!)")

        existing_uuid = st.text_input("Enter existing UUID", key="existing_uuid")
        if st.button("Load User") and existing_uuid:
            try:
                st.session_state.core = VoiceTutorCore(user_uuid=existing_uuid)
                st.session_state.user_uuid = existing_uuid
                user_data = st.session_state.core.db.search(st.session_state.core.user_query.uuid == existing_uuid)
                if user_data and "nickname" in user_data[0] and user_data[0]["nickname"]:
                    st.session_state.nickname = user_data[0]["nickname"]
                else:
                    st.session_state.nickname = "Student"
                    st.session_state.core.db.update(
                        {'nickname': st.session_state.nickname},
                        st.session_state.core.user_query.uuid == st.session_state.user_uuid
                    )
                st.success(f"Loaded user: {st.session_state.nickname}")
            except Exception as e:
                st.error(f"Invalid UUID: {e}")
    else:
        st.info(f"Logged in as {st.session_state.nickname} (UUID: {st.session_state.user_uuid})")

if st.session_state.core:
    # Set default subject and level
    subjects = sorted(st.session_state.core.syllabus.keys())
    if st.session_state.subject is None:
        st.session_state.subject = subjects[0]
    if st.session_state.level is None:
        st.session_state.level = sorted(st.session_state.core.syllabus[st.session_state.subject].keys())[0]

    tab1, tab_syllabus, tab2, tab_progress = st.tabs(["Classroom", "Syllabus Topics", "Audio Settings", "Progress Report"])

    with tab1:
        with st.sidebar:
            st.header("Classroom Setup")
            st.selectbox("Subject", options=subjects, key="subject")
            levels = sorted(st.session_state.core.syllabus[st.session_state.subject].keys())
            st.selectbox("Level", options=levels, key="level")
            input_name = dict(st.session_state.core.available_devices["input"]).get(st.session_state.core.audio_settings["input_device"], "None")
            output_name = dict(st.session_state.core.available_devices["output"]).get(st.session_state.core.audio_settings["output_device"], "None")
            st.subheader("Audio Status")
            st.info(f"Mic: {input_name}")
            st.info(f"Speaker: {output_name}")

        left_col, right_col = st.columns([1, 3])
        with left_col:
            st.header("🎮 Classroom Controls")
            class_status = st.empty()
            if not st.session_state.core.recording:
                class_status.warning("⏸️ Not recording")
            else:
                class_status.success("🎙️ Recording...")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎙️ Start Recording"):
                    success, message = st.session_state.core.start_recording()
                    if success:
                        class_status.success(message)
                    else:
                        st.error(message)
            with col2:
                if st.button("🛑 Stop Recording"):
                    success, message = st.session_state.core.stop_recording()
                    if success:
                        class_status.warning("⏸️ Not recording")
                        st.success(message)
                    else:
                        st.error(message)

            if st.button("📤 Send to Tutor", use_container_width=True):
                with st.spinner("Processing..."):
                    success, result = st.session_state.core.send_to_tutor(
                        st.session_state.nickname,
                        st.session_state.subject,
                        st.session_state.level,
                        topic_code=st.session_state.get("selected_topic_code")
                    )
                if success:
                    st.success(f"Heard: {result['recognized_text']}")
                else:
                    st.error(result)

        with right_col:
            st.header(f"📚 {st.session_state.subject.capitalize()} {st.session_state.level}")
            # Select a Topic
            syllabus_content = st.session_state.core.get_syllabus_content(st.session_state.subject, st.session_state.level)
            topic_options = [f"{code}: {desc.split('.')[0]}..." for code, desc in syllabus_content.items()]
            completed_topics = st.session_state.core.get_completed_topics(st.session_state.subject, st.session_state.level)
            st.subheader("📋 Select a Topic")
            selected_topic = st.selectbox("Choose a syllabus topic", options=topic_options, key="topic_select")
            selected_topic_code = selected_topic.split(":")[0].strip() if selected_topic else None
            st.session_state.selected_topic_code = selected_topic_code
            if selected_topic_code in completed_topics:
                st.warning(f"Topic {selected_topic_code} already completed!")
            else:
                st.info(f"Selected: {selected_topic_code}")

            # Chat with Tutor (moved above Discussion)
            st.subheader("💬 Chat with Tutor")
            chat_input = st.text_input("Type your message here", key="chat_input")
            if st.button("Send Chat", key="send_chat"):
                if chat_input:
                    with st.spinner("Processing..."):
                        syllabus_content = st.session_state.core.get_syllabus_content(st.session_state.subject, st.session_state.level)
                        topic_desc = syllabus_content.get(selected_topic_code, "General topic") if selected_topic_code else "General topic"
                        syllabus_str = f"{selected_topic_code}: {topic_desc}" if selected_topic_code else ", ".join(syllabus_content.keys())
                        context = (
                            f"Student: {st.session_state.nickname}, Subject: {st.session_state.subject}, Level: {st.session_state.level}, Selected Topic: {syllabus_str}\n"
                            f"Student says: {chat_input}\n"
                        )
                        ollama_response = ollama.generate(
                            model=st.session_state.core.llm_model,
                            prompt=(
                                f"You are a classroom teacher speaking directly to a student. "
                                f"Based on the student's latest input and the selected syllabus topic ({syllabus_str}), "
                                f"teach a short, practical lesson or provide a clear, helpful answer to their question or concern. "
                                f"Focus on the specific topic provided and the student's input—do not stray into unrelated areas "
                                f"unless the student explicitly asks. Keep your response concise, engaging, and like a real teacher "
                                f"giving a lesson or support. If the student's input is unrelated to the topic, gently guide them back. "
                                f"Context:\n{context}"
                            )
                        )
                        response = ollama_response["response"].strip()
                        st.session_state.core.update_lesson(st.session_state.subject, st.session_state.level, chat_input, response)
                        if selected_topic_code:
                            st.session_state.core.mark_topic_completed(st.session_state.subject, st.session_state.level, selected_topic_code)
                        st.session_state.core.speak_text(response)
                        st.success("Message sent and response spoken!")
                        st.rerun()  # Assumes modern Streamlit version

            # Discussion
            st.subheader("📜 Discussion")
            user_data = st.session_state.core.db.search(st.session_state.core.user_query.uuid == st.session_state.user_uuid)[0]
            lessons = user_data["lessons"]
            if not lessons:
                st.info("No conversation yet.")
            else:
                for lesson in lessons[-5:]:
                    st.markdown(f"**{st.session_state.nickname} ({lesson['timestamp']}):** {lesson['user_input']}")
                    st.markdown(f"**Tutor:** {lesson['tutor_response']}")
                    st.write("---")

    with tab_syllabus:
        st.header("📚 Syllabus Topics")
        syllabus_content = st.session_state.core.get_syllabus_content(st.session_state.subject, st.session_state.level)
        for code, desc in syllabus_content.items():
            st.write(f"- **{code}**: {desc.split('.')[0]}...")

    with tab2:
        st.header("🔊 Audio Settings")
        if st.button("🔄 Refresh Audio Devices"):
            st.session_state.core.refresh_audio_devices()
            st.success("Devices refreshed!")
        
        input_devices = st.session_state.core.available_devices["input"]
        if input_devices:
            input_labels = [f"{i}: {name}" for i, name in input_devices]
            selected_input = st.selectbox("Microphone", input_labels, index=0)
            st.session_state.core.audio_settings["input_device"] = int(selected_input.split(":")[0])
        else:
            st.error("No input devices detected.")

        output_devices = st.session_state.core.available_devices["output"]
        if output_devices:
            output_labels = [f"{i}: {name}" for i, name in output_devices]
            selected_output = st.selectbox("Speaker", output_labels, index=0)
            st.session_state.core.audio_settings["output_device"] = int(selected_output.split(":")[0])
        else:
            st.error("No output devices detected.")

        st.session_state.core.audio_settings["sample_rate"] = st.selectbox("Sample Rate", st.session_state.core.SAMPLE_RATES)

    with tab_progress:
        st.header("📊 Progress Report")
        if st.button("Generate Report"):
            report = st.session_state.core.generate_progress_report(st.session_state.nickname)
            st.text_area("Your Progress", value=report, height=400)