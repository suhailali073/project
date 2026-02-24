from flask import Flask, jsonify, render_template_string
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

# ─────────────────────────────────────────────
# SECTION-BASED CHECKLIST (ORDERED)
# ─────────────────────────────────────────────

checklist_sections = [
    {
        "section": "Before Induction of Anaesthesia",
        "questions": [
            "Has the patient confirmed identity, site, procedure, and consent?",
            "Is the site marked?",
            "Is the anaesthesia machine and medication check complete?",
            "Is the pulse oximeter functioning?",
            "Does the patient have a known allergy?",
            "Does the patient have a difficult airway or aspiration risk?",
            "Is there risk of more than 500ml blood loss?"
        ]
    },
    {
        "section": "Before Skin Incision",
        "questions": [
            "Have all team members introduced themselves?",
            "Has the patient's name and procedure been confirmed?",
            "Has antibiotic prophylaxis been given?",
            "What are the anticipated critical events?",
            "Is essential imaging displayed?"
        ]
    },
    {
        "section": "Before Patient Leaves Operating Room",
        "questions": [
            "Has instrument, sponge and needle count been completed?",
            "Have specimens been labeled correctly?",
            "Have equipment problems been addressed?",
            "What are the key concerns for recovery and management?"
        ]
    }
]

# Initialize status
status = []
for section in checklist_sections:
    section_data = {
        "section": section["section"],
        "questions": []
    }
    for q in section["questions"]:
        section_data["questions"].append({
            "question": q,
            "yes": False,
            "no": False
        })
    status.append(section_data)

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def run_checklist():
    for section in status:
        speak(section["section"])

        for i, item in enumerate(section["questions"]):
            speak(item["question"])

            while True:
                with sr.Microphone(device_index=1) as source:
                    audio = recognizer.listen(source)

                try:
                    command = recognizer.recognize_google(audio).lower()

                    if "confirm" in command or "done" in command or "yes" in command:
                        section["questions"][i]["yes"] = True
                        section["questions"][i]["no"] = False
                        speak("Marked yes")
                        break
                    else:
                        section["questions"][i]["no"] = True
                        section["questions"][i]["yes"] = False
                        speak("Marked no")
                        break

                except:
                    speak("Repeat please")

    speak("Checklist completed")

# ─────────────────────────────────────────────
# MODERN HTML TEMPLATE (OPTIONS VISIBLE)
# ─────────────────────────────────────────────

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Surgical Safety Checklist</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f4f6f9;
            margin: 0;
        }

        header {
            background: #1f3c88;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .container {
            padding: 30px;
            max-width: 1000px;
            margin: auto;
        }

        button {
            background: #1f3c88;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover { background: #163172; }

        .progress-bar {
            width: 100%;
            height: 10px;
            background: #ddd;
            border-radius: 5px;
            margin: 20px 0;
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: #28a745;
            border-radius: 5px;
            transition: 0.3s;
        }

        .section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        .section h3 {
            margin-top: 0;
            color: #1f3c88;
        }

        .item {
            margin: 15px 0;
            padding: 10px;
            border-left: 4px solid #ccc;
            background: #fafafa;
        }

        .item.yes {
            border-left-color: #28a745;
            background: #eaf7ee;
        }

        .item.no {
            border-left-color: #dc3545;
            background: #fdecea;
        }

        .options {
            margin-top: 8px;
        }

        .yes-option {
            color: #28a745;
            font-weight: bold;
            margin-right: 20px;
        }

        .no-option {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
</head>

<body>

<header>
    <h2>Checklist for Surgery</h2>
</header>

<div class="container">

    <button onclick="startChecklist()">Start Checklist</button>

    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>

    <div id="checklist"></div>

</div>

<script>
function startChecklist() {
    fetch("/start");
}

function loadChecklist() {
    fetch("/api/status")
    .then(res => res.json())
    .then(data => {

        let html = "";
        let total = 0;
        let completed = 0;

        data.forEach(section => {
            html += `<div class="section"><h3>${section.section}</h3>`;

            section.questions.forEach(item => {

                total++;

                let itemClass = "";
                if (item.yes) {
                    itemClass = "yes";
                    completed++;
                }
                else if (item.no) {
                    itemClass = "no";
                    completed++;
                }

                html += `
                    <div class="item ${itemClass}">
                        <div>${item.question}</div>
                        <div class="options">
                            <span class="yes-option">
                                ${item.yes ? "✔ Yes" : "Yes"}
                            </span>
                            <span class="no-option">
                                ${item.no ? "✖ No" : "No"}
                            </span>
                        </div>
                    </div>
                `;
            });

            html += "</div>";
        });

        document.getElementById("checklist").innerHTML = html;

        let progress = total === 0 ? 0 : (completed / total) * 100;
        document.getElementById("progressFill").style.width = progress + "%";
    });
}

setInterval(loadChecklist, 1000);
</script>

</body>
</html>
"""

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/status")
def get_status():
    return jsonify(status)

@app.route("/start")
def start():
    threading.Thread(target=run_checklist).start()
    return jsonify({"message": "Checklist started"})

if __name__ == "__main__":
    app.run(debug=True)