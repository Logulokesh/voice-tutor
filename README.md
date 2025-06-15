# 🎓 KinAI-Mentor

<div align="center">

### *Open-Source, Offline Educational Assistant Powered by Local LLM*

---

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai)
[![MIT License](https://img.shields.io/badge/License-MIT-00C851?style=for-the-badge)](LICENSE)
[![100% Offline](https://img.shields.io/badge/100%25-OFFLINE-9C27B0?style=for-the-badge)](https://github.com)

**🌟 A 100% offline, open-source, voice-driven tutor that's free, flexible, and aligned with the Victorian Curriculum F–10 Version 2.0 🌟**
<p align="center">
  <img src="https://raw.githubusercontent.com/Logulokesh/KinAI-Mentor/refs/heads/main/screenshots/Logo-4.gif" alt="KinAi-Nexpatrol" width="100%" />
</p>
</div>

---

## 🚀 **The Vision**

<!-- Row 1: Identify the Challenge --> <table style="width: 100%; border-collapse: collapse; font-family: sans-serif;"> <tr> <td style="width: 500px; text-align: center; vertical-align: top; padding: 80px;"> <img src="identify.png" width="220" alt="Identify" /> </td> <td style="padding: 40px; vertical-align: top;"> <h2 style="color: #2563eb; display: flex; align-items: center; gap: 10px; margin-top: 0;"> <span style="font-size: 24px;">🔍</span> 1. Identify the Challenge </h2> <p> Modern education lacks personalized support due to time and resource limits. KinAI-Mentor solves this with an <strong>offline 🌐, open-source 🤖 AI tutor</strong>, aligned with the <strong>Victorian Curriculum F–10 Version 2.0 🎓</strong>, offering accessible, flexible learning for all students 🎯. </p> </td> </tr> </table> <!-- Row 2: Engineer the Approach --> <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; background-color: #f9f9f9;"> <tr> <td style="padding: 40px; vertical-align: top;"> <h2 style="color: #16a34a; display: flex; align-items: center; gap: 10px; margin-top: 0;"> <span style="font-size: 24px;">⚙️</span> 2. Engineer the Approach </h2> <p> KinAI-Mentor uses a <strong>local LLM 🧠 via Ollama</strong> for real-time responses without internet 🌐. It combines <strong>speech-to-text 🎙️</strong> and <strong>text-to-speech 🔊 AI</strong> for hands-free interaction 💬. </p> <p> Fully offline, it ensures <strong>privacy 🔒</strong>, <strong>speed ⚡</strong>, and <strong>customizability</strong>, supporting both voice and text input/output 📱. </p> </td> <td style="width: 220px; text-align: center; vertical-align: top; padding: 40px;"> <img src="support.png" width="220" alt="Support" /> </td> </tr> </table> <!-- Row 3: Implement the Outcome --> <table style="width: 100%; border-collapse: collapse; font-family: sans-serif;"> <tr> <td style="width: 220px; text-align: center; vertical-align: top; padding: 40px;"> <img src="empower.png" width="220" alt="Empower" /> </td> <td style="padding: 40px; vertical-align: top;"> <h2 style="color: #dc2626; display: flex; align-items: center; gap: 10px; margin-top: 0;"> <span style="font-size: 24px;">✅</span> 3. Implement the Outcome </h2> <p> A fully functional, <strong>AI-driven tutoring system 🚀</strong> that runs locally on any device 📱. Students learn at their own pace using <strong>voice commands 🎙️</strong> or <strong>chat input 💬</strong>. </p> <p> Built with <strong>on-device AI</strong>, it supports diverse learners ♿—ideal for those with disabilities or limited digital access. An empowering, joyful step forward in education 🎉. </p> </td> </tr> </table>

**💬 Interactive** • **📱 Cross-Platform** • **♿ Accessible** • **🚀 Performance** • **🎉 Engaging**

</div>

---

## 🌟 **Overview**

> **Why KinAI-Mentor?** While tech giants focus on enterprise AI tools, we're solving something fundamental: helping kids learn when life gets busy. 

**KinAI-Mentor** isn't just another educational app—it's a **100% offline, open-source, voice-driven tutor** that's:
- 🆓 **Completely Free** - No subscriptions, no hidden costs
- 🔧 **Fully Customizable** - Open-source and hackable
- 📚 **Curriculum-Aligned** - Victorian Curriculum F–10 Version 2.0
- 🎤 **Voice & Text Ready** - Multiple interaction modes

---

## ⭐ **Key Features**

<div align="center">

| 🎤 **Voice Input** | 💬 **Chat Input** | 🗣️ **Voice Output** | 📃 **Text Display** |
|:---:|:---:|:---:|:---:|
| Speak your questions naturally | Type queries traditionally | Answers read aloud via TTS | Visual responses on screen |

| 🎓 **Curriculum-Aligned** | 💻 **100% Offline** | 🛠️ **Open-Source** | 🔊 **Multilingual** |
|:---:|:---:|:---:|:---:|
| Victorian Curriculum F–10 V2.0 | No internet dependency | Free to modify & extend | Optional language models |

</div>

---

## 🏗️ **System Architecture**

```mermaid
graph TB
    subgraph "🎯 User Interaction"
        A[👤 User]
        A -->|🎤 Voice| B[Microphone]
        A -->|💬 Text| C[Text Input]
    end
    
    subgraph "🔄 Input Processing"
        B --> D[🎧 Speech-to-Text]
        C --> E[⚙️ Query Processor]
        D --> E
    end
    
    subgraph "🧠 AI Core"
        E --> F[🤖 Ollama LLM]
        F <--> G[💾 Knowledge Base]
        F <--> H[📚 Curriculum Data]
    end
    
    subgraph "📤 Output Generation"
        F --> I[🔧 Response Formatter]
        I --> J[🖥️ Text Display]
        I --> K[🔊 Text-to-Speech]
        K --> L[🎶 Audio Output]
    end
    
    J --> A
    L --> A
    
    style A fill:#e1f5fe
    style F fill:#f3e5f5
    style G fill:#e8f5e8
    style H fill:#fff3e0
```

### 📋 **How It Works**

<details>
<summary><b>🔍 Click to expand architecture details</b></summary>

| Component | Function | Technology |
|-----------|----------|------------|
| **👤 User Interface** | Voice/text input handling | Streamlit + Speech Recognition |
| **🎧 Speech Processing** | Voice-to-text conversion | Offline speech recognition |
| **🧠 AI Engine** | Query processing & responses | Ollama LLM (local) |
| **💾 Knowledge Base** | General learning content | JSON database |
| **📚 Curriculum** | Victorian Curriculum alignment | Structured JSON |
| **🔊 Audio Output** | Text-to-speech synthesis | Local TTS engine |

</details>

---

## 🎯 **Why Choose KinAI-Mentor?**

<div align="center">

| **🌟 Benefit** | **🔥 Why It Matters** |
|:---|:---|
| **♿ Accessible Design** | Supports auditory, visual, and diverse learners |
| **🧠 Curriculum-Focused** | Aligned with Victorian Curriculum F–10 V2.0 |
| **🔁 Multi-Modal** | Seamless voice ↔ text switching |
| **📱 Hands-Free Learning** | Perfect for multitasking or accessibility needs |
| **🌍 Privacy-First** | 100% offline - your data never leaves your device |
| **🔧 Developer-Friendly** | Open-source, customizable, and extensible |
| **⚡ No Dependencies** | Works without internet, subscriptions, or accounts |

</div>

---

## 🛠️ **Quick Start**

### 📋 **Prerequisites**

<div align="center">

| Requirement | Version | Purpose |
|:---:|:---:|:---:|
| 🐍 **Python** | 3.8+ | Core runtime |
| 🤖 **Ollama** | Latest | Local LLM |
| 🎤 **Microphone** | Any | Voice input |
| 🔊 **Audio Output** | Any | Voice responses |

</div>

### ⚡ **Installation**

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Logulokesh/kinai-mentor.git
cd kinai-mentor

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Setup Ollama
# Download from https://ollama.ai
ollama pull llama3

# 5️⃣ Launch KinAI-Mentor
streamlit run ui.py
```

### 🚀 **Launch Commands**

```bash
# Start Ollama server
ollama run llama3

# Launch KinAI-Mentor interface
streamlit run ui.py
```

---

## 📁 **Project Structure**

<div align="center">

| File | Purpose | Icon |
|:---|:---|:---:|
| `core_tutor.py` | Core AI logic & processing | ⚙️ |
| `ui.py` | Streamlit user interface | 🖥️ |
| `syllabus.json` | Victorian Curriculum data | 📚 |
| `voicetutor_db.json` | Knowledge base | 📂 |
| `requirements.txt` | Python dependencies | 📋 |
| `README.md` | Documentation | 📖 |

</div>

---

## 🛠️ **Tech Stack**

<div align="center">

### **Core Technologies**

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai)

### **AI & Audio**

![Speech Recognition](https://img.shields.io/badge/Speech_Recognition-00D4AA?style=for-the-badge&logo=google&logoColor=white)
![Text to Speech](https://img.shields.io/badge/Text_to_Speech-4285F4?style=for-the-badge&logo=google&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

</div>

---

## 🤝 **Contributing**

<div align="center">

**🌟 Help us make learning more accessible! 🌟**

[![Contribute](https://img.shields.io/badge/Contribute-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/badge/Issues-Open-red?style=for-the-badge)](https://github.com/Logulokesh/kinai-mentor/issues)
[![PRs](https://img.shields.io/badge/PRs-Welcome-blue?style=for-the-badge)](https://github.com/Logulokesh/kinai-mentor/pulls)

</div>

### 🔧 **How to Contribute**

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. ✅ **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 🚀 **Push** to the branch (`git push origin feature/amazing-feature`)
5. 📬 **Open** a Pull Request

---

## 📜 **License**

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Free to use, modify, and distribute under the MIT License**

</div>

---

## 📸 **Screenshots**

<div align="center">

### 🖥️ **Main Interface**
*Clean, intuitive design for seamless learning*

![KinAI-Mentor Main Interface](https://raw.githubusercontent.com/Logulokesh/VICTutorAI-Offline-Educational-Assistant-Voice/refs/heads/main/screenshots/001%20-%20VoiceTutor%20Online%20Classroom%20-%20%5Blocalhost%5D.png)

---

### 💬 **Interactive Learning**
*Real-time conversations with AI tutor*

![Interactive Learning](https://raw.githubusercontent.com/Logulokesh/VICTutorAI-Offline-Educational-Assistant-Voice/refs/heads/main/screenshots/002%20-%20VoiceTutor%20Online%20Classroom%20-%20%5Blocalhost%5D.png)

---

### 🎤 **Voice Interaction**
*Hands-free learning experience*

![Voice Interaction](https://raw.githubusercontent.com/Logulokesh/VICTutorAI-Offline-Educational-Assistant-Voice/refs/heads/main/screenshots/003%20-%20VoiceTutor%20Online%20Classroom%20-%20%5Blocalhost%5D.png)

---

### 📚 **Curriculum Content**
*Victorian Curriculum F–10 Version 2.0 aligned*

![Curriculum Content](https://raw.githubusercontent.com/Logulokesh/VICTutorAI-Offline-Educational-Assistant-Voice/refs/heads/main/screenshots/005%20-%20VoiceTutor%20Online%20Classroom%20-%20%5Blocalhost%5D.png)

---

### 🎯 **Learning Dashboard**
*Track progress and engagement*

![Learning Dashboard](https://raw.githubusercontent.com/Logulokesh/VICTutorAI-Offline-Educational-Assistant-Voice/refs/heads/main/screenshots/006%20-%20VoiceTutor%20Online%20Classroom%20-%20%5Blocalhost%5D.png)

</div>

---

**Made with ❤️ for accessible education**

---

*KinAI-Mentor - Empowering learners through intelligent, offline AI tutoring*

</div>
