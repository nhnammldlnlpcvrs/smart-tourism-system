const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messagesContainer = document.getElementById("messages");
const newChatBtn = document.getElementById("new-chat");
const clearAllBtn = document.getElementById("clear-all");
const chatHistoryList = document.getElementById("chat-history-list");
const temperatureSlider = document.getElementById("temperature");
const tempValue = document.getElementById("temp-value");

let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [[]];
let currentChatIndex = 0;

if (chatHistory && chatHistory.length > 0) {
    renderChatHistory();
    renderChat();
}

function addMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(sender);
    msgDiv.textContent = text;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

//toàn bộ chat hiện tại
function renderChat() {
    messagesContainer.innerHTML = "";
    chatHistory[currentChatIndex].forEach(msg => addMessage(msg.sender, msg.text));
}

//lịch sử chat
function renderChatHistory() {
    chatHistoryList.innerHTML = "";
    chatHistory.forEach((chat, index) => {
        const li = document.createElement("li");
        if (chat.length === 0) {
            li.textContent = `Chat trống lần ${index + 1}`;
        } else {
            const firstUserMsg = chat.find(m => m.sender === "user");
            li.textContent = firstUserMsg ? firstUserMsg.text : "Chat không có user message";
        }
        if (index === currentChatIndex) li.classList.add("active");
        li.addEventListener("click", () => {
            currentChatIndex = index;
            renderChat();
            updateActiveChat();
        });
        chatHistoryList.appendChild(li);
    });
}

//chat đang active
function updateActiveChat() {
    const items = chatHistoryList.querySelectorAll("li");
    items.forEach((item, idx) => {
        item.classList.toggle("active", idx === currentChatIndex);
    });
}

//hiệu ứng "typing..."
function showTypingEffect() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("bot");
    typingDiv.textContent = "Bot đang trả lời...";
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingDiv;
}

async function botReply(userText) {
    try {
        const res = await fetch("http://127.0.0.1:8000/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        });

        const data = await res.json();
        addMessage("bot", data.bot_reply || "Không có phản hồi");
        chatHistory[currentChatIndex].push({ sender: "bot", text: data.bot_reply || "Không có phản hồi" });
        saveChatHistory();
    } catch (e) {
        console.error("Fetch lỗi:", e);
        addMessage("bot", "Lỗi khi gọi backend");
    }
}

//submit form
chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const userText = messageInput.value.trim();
    if (!userText) return;

    addMessage("user", userText);
    chatHistory[currentChatIndex].push({ sender: "user", text: userText });
    messageInput.value = "";
    saveChatHistory();

    botReply(userText);
    renderChatHistory();
});

//tạo chat mới
newChatBtn.addEventListener("click", () => {
    chatHistory.unshift([]);
    if (chatHistory.length > 20) chatHistory.pop(); //giới hạn 20 chat
    currentChatIndex = 0;
    renderChat();
    renderChatHistory();
    saveChatHistory();
});

//xóa tất cả lịch sử chat
clearAllBtn.addEventListener("click", () => {
    if (confirm("Xóa toàn bộ lịch sử chat?")) {
        chatHistory = [[]];
        currentChatIndex = 0;
        localStorage.removeItem("chatHistory");
        renderChat();
        renderChatHistory();
    }
});


temperatureSlider.addEventListener("input", () => {
    tempValue.textContent = temperatureSlider.value;
});

//lưu chatHistory
function saveChatHistory() {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
}

//khi load trang lần đầu
window.addEventListener("DOMContentLoaded", () => {
    if (!chatHistory || chatHistory.length === 0) chatHistory = [[]];
    if (chatHistory[0].length === 0) {
        addMessage("bot", "Xin chào! Bạn muốn hỏi gì?");
        chatHistory[0].push({ sender: "bot", text: "Xin chào! Bạn muốn hỏi gì?" });
        saveChatHistory();
    }
    renderChat();
    renderChatHistory();
});