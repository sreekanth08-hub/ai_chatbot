const API = "http://127.0.0.1:5000";
const chatBox = document.getElementById("chatBox");
const micAnim = document.getElementById("micAnimation");
const recordStatus = document.getElementById("recordStatus");

function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = "message";
    div.innerHTML = `<span class="${sender}">${sender === "user" ? "You" : "Bot"}:</span> ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function initBot() {
    addMessage("bot", "Hi 👋 I am your AI Disease Analyzer. Choose an input mode from the sidebar.");
}

/* SIDEBAR NAVIGATION */
function showSection(type) {
    document.getElementById("textSection").classList.add("hidden");
    document.getElementById("voiceSection").classList.add("hidden");
    document.getElementById("imageSection").classList.add("hidden");

    document.getElementById(type + "Section").classList.remove("hidden");
}

/* TEXT INPUT */
function sendText() {
    const text = document.getElementById("textInput").value.trim();
    if (!text) return;

    addMessage("user", text);

    fetch(API + "/predict/text", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ symptoms: text })
    })
    .then(res => res.json())
    .then(data => showBotResult(data));
}

/* VOICE INPUT */
function startVoice() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Voice input not supported");
        return;
    }

    micAnim.classList.add("recording");
    recordStatus.innerText = "Recording... Speak now";

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        micAnim.classList.remove("recording");
        recordStatus.innerText = "Recording stopped";

        const text = event.results[0][0].transcript;
        addMessage("user", text);

        fetch(API + "/predict/text", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ symptoms: text })
        })
        .then(res => res.json())
        .then(data => showBotResult(data));
    };
}

/* IMAGE INPUT */
function sendImage() {
    const img = document.getElementById("imageInput").files[0];
    if (!img) return;

    addMessage("user", "📷 Image uploaded");

    const fd = new FormData();
    fd.append("image", img);

    fetch(API + "/predict/image", {
        method: "POST",
        body: fd
    })
    .then(res => res.json())
    .then(data => {
        addMessage("bot", `<b>Disease:</b> ${data.disease}`);
    });
}

/* BOT RESPONSE FORMAT */
function showBotResult(data) {
    let remedies = "<ul>";
    data.recommendations.forEach(r => remedies += `<li>${r}</li>`);
    remedies += "</ul>";

    addMessage(
        "bot",
        `<b>Disease Identified:</b> ${data.disease}<br><b>Recommended Remedies:</b>${remedies}`
    );
}
