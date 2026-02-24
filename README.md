# 🏥 AI Voice-Controlled Surgical Safety Checklist

A voice-driven, real-time surgical safety checklist web application built using **Python (Flask)** and **Speech Recognition**.

This system allows medical teams to complete the WHO Surgical Safety Checklist hands-free using voice commands, improving workflow efficiency and reducing human error.

---

## 🚀 Features

* 🎤 Voice-controlled checklist (Say “confirm”, “done”, or “yes”)
* 📋 Section-based WHO surgical workflow
* ✅ Real-time Yes/No marking
* 📊 Live progress tracking
* 🌐 Web-based interface
* 🔁 Real-time UI updates via API polling
* 🧠 Backend voice processing with multithreading

---

## 🏗 Architecture Overview

The system consists of three main components:

### 1️⃣ Voice Processing Layer

* `speech_recognition` for speech-to-text
* Google Speech Recognition API
* `pyttsx3` for text-to-speech
* Runs in a background thread to prevent server blocking

### 2️⃣ Backend API Layer (Flask)

* `/` → Renders the web interface
* `/start` → Starts the checklist process
* `/api/status` → Returns checklist status as JSON

### 3️⃣ Frontend Layer

* HTML + CSS (Modern UI design)
* JavaScript Fetch API
* Real-time polling (updates every second)

---

## 📋 Surgical Checklist Sections

The checklist follows the WHO Surgical Safety structure:

1. **Before Induction of Anaesthesia**
2. **Before Skin Incision**
3. **Before Patient Leaves Operating Room**

Each question supports:

* ✔ Yes (voice: confirm / done / yes)
* ✖ No (any other response)

---

## 🛠 Tech Stack

* Python 3.x
* Flask
* SpeechRecognition
* pyttsx3
* HTML / CSS / JavaScript

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/suhailali073/project.git
cd project
```

### 2️⃣ Install Dependencies

```bash
pip install flask SpeechRecognition pyttsx3 pyaudio
```

> ⚠ If PyAudio installation fails on Windows:
> Use a precompiled wheel or install via:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

Click **Start Checklist** and begin speaking.

---

## 🎤 How It Works

1. The system speaks the section name.
2. The system reads each question aloud.
3. User responds:

   * “confirm” / “done” / “yes” → Marks **Yes**
   * Any other response → Marks **No**
4. UI updates automatically.
5. Progress bar fills as checklist progresses.

---

## 💡 Why This Matters

* Reduces human error in surgical procedures
* Enforces standardized protocol
* Hands-free sterile operation
* Encourages team communication
* Can be extended for logging, compliance, and analytics

---

## 🔮 Future Improvements

* Database logging (SQLite / PostgreSQL)
* Authentication system
* Multi-user support
* PDF report generation
* Cloud deployment
* WebSocket real-time updates
* Hospital system integration

---

## ⚠ Limitations

* Requires microphone access
* Dependent on internet for Google speech recognition
* Prototype-level implementation (not medically certified)

---

## 📜 License

This project is built for educational and hackathon purposes.
Not certified for clinical use.