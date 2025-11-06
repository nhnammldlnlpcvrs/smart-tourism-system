// DOM elements
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messagesContainer = document.getElementById("messages");
const newChatBtn = document.getElementById("new-chat");
const clearAllBtn = document.getElementById("clear-all");
const chatHistoryList = document.getElementById("chat-history-list");
const temperatureSlider = document.getElementById("temperature");
const tempValue = document.getElementById("temp-value");

// Lịch sử chat: mỗi phần tử là 1 cuộc chat, mảng message {sender, text}
let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [[]];
let currentChatIndex = 0;

// Render lịch sử chat khi load
if (chatHistory && chatHistory.length > 0) {
    renderChatHistory();
    renderChat();
}

// Thêm tin nhắn vào giao diện
function addMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(sender);
    msgDiv.textContent = text;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Hiển thị toàn bộ chat hiện tại
function renderChat() {
    messagesContainer.innerHTML = "";
    chatHistory[currentChatIndex].forEach(msg => addMessage(msg.sender, msg.text));
}

// Hiển thị danh sách lịch sử chat
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

// Cập nhật chat đang active
function updateActiveChat() {
    const items = chatHistoryList.querySelectorAll("li");
    items.forEach((item, idx) => {
        item.classList.toggle("active", idx === currentChatIndex);
    });
}

// Hiệu ứng bot đang "typing..."
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
        const res = await fetch("http://.0.0.1:8000/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        });
        console.log("Status:", res.status);
        const data = await res.json();
        console.log("JSON:", data);
        addMessage("bot", data.reply || "Không có phản hồi");
    } catch (e) {
        console.error("Fetch lỗi:", e);
        addMessage("bot", "Lỗi khi gọi backend");
    }
}

// Submit form gửi tin nhắn
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

// Tạo chat mới
newChatBtn.addEventListener("click", () => {
    chatHistory.unshift([]);
    if (chatHistory.length > 20) chatHistory.pop(); // Giới hạn 20 chat
    currentChatIndex = 0;
    renderChat();
    renderChatHistory();
    saveChatHistory();
});

// Xóa tất cả lịch sử chat
clearAllBtn.addEventListener("click", () => {
    if (confirm("Xóa toàn bộ lịch sử chat?")) {
        chatHistory = [[]];
        currentChatIndex = 0;
        localStorage.removeItem("chatHistory");
        renderChat();
        renderChatHistory();
    }
});

// Cập nhật giá trị temperature (nếu cần cho backend)
temperatureSlider.addEventListener("input", () => {
    tempValue.textContent = temperatureSlider.value;
});

// Lưu chatHistory vào localStorage
function saveChatHistory() {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
}

// Khi load trang lần đầu
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
