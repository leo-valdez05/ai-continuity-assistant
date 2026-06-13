let conversationId = null;
let inChat = false;

function getInput() {
    return inChat
        ? document.getElementById("userMessageChat")
        : document.getElementById("userMessage");
}

async function sendMessage() {
    const input = getInput();
    const message = input.value.trim();
    if (!message) return;

    if (input.disabled) return;
    input.disabled = true;
    setTimeout(() => input.disabled = false, 1000);

    if (!inChat) {
        await switchToChat();
    }

    input.value = "";
    addMessage(message, "user");


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
    document.getElementById("chatArea").appendChild(thinking);
    scrollToBottom();

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({message: message, conversation_id: conversationId})
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
        scrollToBottom();
        if (data.leaving) {
        endConversation();
        loadSidebar();
    }
    }, 900);

    const emotion = (data.emotion || "neutral").toLowerCase();
    const auroraColors = {
        happy: "linear-gradient(90deg, transparent, #4e3a0a, transparent)",
        excited: "linear-gradient(90deg, transparent, #4e3a0a, transparent)",
        joy: "linear-gradient(90deg, transparent, #4e3a0a, transparent)",
        sad: "linear-gradient(90deg, transparent, #0a0a3e, transparent)",
        anxious: "linear-gradient(90deg, transparent, #3e0a0a, transparent)",
        stressed: "linear-gradient(90deg, transparent, #3e0a0a, transparent)",
        angry: "linear-gradient(90deg, transparent, #3e0a0a, transparent)",
        calm: "linear-gradient(90deg, transparent, #0a2e2a, transparent)",
        neutral: "linear-gradient(90deg, transparent, #3a3060, transparent)"
    };

    const aurora = document.getElementById("auroraLine");
    if (aurora) {
        aurora.style.background = auroraColors[emotion] || auroraColors.neutral;
    }
}

async function switchToChat() {

    const response = await fetch("/new_conversation", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title: "New Chat"})
    });
    const data = await response.json();
    conversationId = data.conversation_id;
    localStorage.setItem("lastConversationId", conversationId);



    inChat = true;
    const landing = document.getElementById("landing");
    const chatView = document.getElementById("chatView");
    landing.style.opacity = "0";
    landing.style.transition = "opacity 0.4s ease";
    setTimeout(() => {
        landing.style.display = "none";
        chatView.classList.add("active");
        document.getElementById("userMessageChat").focus();
    }, 400);
}

function addMessage(text, sender) {
    const chatArea = document.getElementById("chatArea");
    const bubble = document.createElement("div");
    bubble.classList.add("bubble", sender);
    if (sender === "ai") {
        bubble.innerHTML = marked.parse(text);
    } else {
        bubble.textContent = text;
    }
    chatArea.appendChild(bubble);
    scrollToBottom();
}

function scrollToBottom() {
    const chatArea = document.getElementById("chatArea");
    chatArea.scrollTop = chatArea.scrollHeight;
}

document.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});
async function loadSidebar() {
    const response = await fetch("/conversations");
    const conversations = await response.json();

    const list = document.getElementById("sidebarList");
    list.innerHTML = "";

    conversations.forEach(conv => {
        const item = document.createElement("div");
        item.classList.add("sidebar-item");
        item.textContent = conv[1];
        item.onclick = () => loadConversation(conv[0]);
        list.appendChild(item);
    });
}

loadSidebar();

async function loadConversation(convId) {
    conversationId = convId;
    localStorage.setItem("lastConversationId", convId);

    // switch to chat view if not already there
    if (!inChat) {
        inChat = true;
        document.getElementById("landing").style.display = "none";
        document.getElementById("chatView").classList.add("active");
    }

    // clear current messages
    document.getElementById("chatArea").innerHTML = "";

    // load messages for this conversation
    const response = await fetch(`/messages/${convId}`);
    const messages = await response.json();

    messages.forEach(msg => {
        addMessage(msg[1], msg[0]);
    });

    // mark active in sidebar
    document.querySelectorAll(".sidebar-item").forEach(item => {
        item.classList.remove("active");
    });
    document.querySelectorAll(".sidebar-item").forEach(item => {
    if (item.onclick.toString().includes(convId)) {
        item.classList.add("active");
    }
});
    scrollToBottom();
}

function newChat() {
    conversationId = null;
    inChat = false;
    document.getElementById("chatArea").innerHTML = "";
    document.getElementById("chatView").classList.remove("active");
    document.getElementById("landing").style.display = "flex";
    document.querySelectorAll(".sidebar-item").forEach(i => i.classList.remove("active"));
}
async function endConversation() {
    if (!conversationId) return;
    const messages = Array.from(document.querySelectorAll(".bubble")).map(b => ({
        role: b.classList.contains("user") ? "user" : "assistant",
        content: b.textContent
    }));
    await fetch("/end_conversation", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({conversation_id: conversationId, messages: messages})
    });
}

window.addEventListener("beforeunload", endConversation);
window.addEventListener("load", async () => {
    await loadSidebar();
    const lastId = localStorage.getItem("lastConversationId");
    if (lastId) {
        conversationId = parseInt(lastId);
        await loadConversation(conversationId);
    }
});
document.querySelectorAll("textarea").forEach(textarea => {
    textarea.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
    textarea.addEventListener("keypress", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (this === getInput()) {
            sendMessage();
            }
        }
    });
});
async function logout() {
    await fetch("/logout", {method: "POST"});
    localStorage.removeItem("lastConversationId");
    location.reload();
}