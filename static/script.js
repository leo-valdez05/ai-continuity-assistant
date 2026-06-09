async function sendMessage() {
    const input = document.getElementById("userMessage");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    const thinking = document.createElement("div");
    thinking.classList.add("indicator-wrap");
    thinking.innerHTML = `
        <div class="book-stage">
            <div class="ind-page ip1"></div>
            <div class="ind-page ip2"></div>
            <div class="ind-page ip3"></div>
            <div class="book-base"></div>
        </div>
        <span class="label-thinking">looking it up...</span>
    `;
    document.querySelector(".chat-area").appendChild(thinking);

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });

    const data = await response.json();

    thinking.innerHTML = `
        <div class="book-stage">
            <div class="ind-page ip1" style="animation:none;background:#c8e8ff;box-shadow:0 0 18px rgba(100,200,255,0.9);transform:rotate(-18deg) translateY(-28px) translateX(-4px)"></div>
            <div class="ind-page ip2" style="animation:none;background:#d0ecff;box-shadow:0 0 18px rgba(100,200,255,0.85);transform:rotate(10deg) translateY(-32px) translateX(2px)"></div>
            <div class="ind-page ip3" style="animation:none;background:#ccebff;box-shadow:0 0 18px rgba(100,200,255,0.9);transform:rotate(20deg) translateY(-26px) translateX(5px)"></div>
            <div class="book-base" style="background:#2a5a8a"></div>
        </div>
        <span style="color:#4a9eff;font-size:13px;font-family:Georgia,serif">found it!</span>
    `;

    setTimeout(() => {
        thinking.remove();
        addMessage(data.reply, "ai");
    }, 900);
}
function addMessage(text, sender) {
    const chatArea = document.querySelector(".chat-area");
    const bubble = document.createElement("div");
    bubble.classList.add("bubble", sender);
    bubble.textContent = text;
    chatArea.appendChild(bubble);
}

document.getElementById("userMessage").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});