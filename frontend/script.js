// CHATBOT SCRIPT
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messagesContainer = document.getElementById("messages");
const newChatBtn = document.getElementById("new-chat");
const suggestionBtns = document.querySelectorAll(".suggestion-btn");
const clearAllBtn = document.getElementById("clear-all");
const clearChatBtn = document.getElementById("clear-chat");
const temperatureSlider = document.getElementById("temperature");
const tempValue = document.getElementById("temp-value");
const chatHistoryList = document.getElementById("chat-history-list");

// Lấy lịch sử chat từ localStorage của trình duyệt (Trúc bảo 10 nhưng t thịk 15 :))))
let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [[]];
let currentChatIndex = 0;

// Đoạn này để khi reload sẽ thấy lun cái lịch sử chat mà không cần chat hay nhấn newchat
if (chatHistory && chatHistory.length > 0) {
    renderChatHistory();
}

// Thêm tin nhắn
function addMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(sender);
    msgDiv.textContent = text;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Hiển thị nội dung chat at the mô mần
function renderChat() {
    messagesContainer.innerHTML = "";
    chatHistory[currentChatIndex].forEach((msg) => {
        addMessage(msg.sender, msg.text);
    });
}

// Hiển thị danh sách lịch sử chat
function renderChatHistory() {
    chatHistoryList.innerHTML = "";
    chatHistory.forEach((chat, index) => {
        const li = document.createElement("li");
        if (chat.length === 0) {
            li.textContent = `Đây là lần thứ ${index + 1} m bỏ trống chat này nha Trúc ~~`;
        } else {
            // Lấy tin nhắn đầu tiên làm tiêu đề
            const firstUserMsg = chat.find((m) => m.sender === "user");
            li.textContent = firstUserMsg ? firstUserMsg.text : "Chat một mình như tự kỉ ~~";
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

// Cập nhật giao diện chat đang chọn
function updateActiveChat() {
    const items = chatHistoryList.querySelectorAll("li");
    items.forEach((item, idx) => {
        item.classList.toggle("active", idx === currentChatIndex);
    });
}

// Hiệu ứng bot đang gõ
function showTypingEffect() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("bot");
    typingDiv.textContent = "Đợi xí đang rặn 2 giây nhanh lắm xong liền";
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingDiv;
}

// Bot giả lập
function botReply(userText) {
    const responses = [
        "ko tốn thời gian hả trrrr",
        "hú hú ẹc ech",
        "ghi đại đại nè",
        "blablabagvaegfaeg",
        "úm ba la xì bùa m đã bị troll ^^",
        "(NHÉT CHỮ ZÀO MỒM) Ánh kêu trả lời tiếng việt mới ngầu :v"
    ];
    const reply = responses[Math.floor(Math.random() * responses.length)];
    const typing = showTypingEffect();
    setTimeout(() => {
        typing.remove();
        addMessage("bot", reply);
        chatHistory[currentChatIndex].push({ sender: "bot", text: reply });
        saveChatHistory();
    }, 2000);
}

// Gửi tin nhắn user
chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const userText = messageInput.value.trim();
    if (userText === "") return;
    addMessage("user", userText);
    chatHistory[currentChatIndex].push({ sender: "user", text: userText });
    messageInput.value = "";
    saveChatHistory();
    botReply(userText);
    renderChatHistory();
});

// Nút New Chat
newChatBtn.addEventListener("click", () => {
    chatHistory.unshift([]);
    if (chatHistory.length > 20) chatHistory.pop(); // này giớn hạn 20 caht nè
    currentChatIndex = 0;
    renderChat();
    renderChatHistory();
    saveChatHistory();
});

// Xóa toàn bộ lịch sử
clearAllBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (confirm("Xoá lịch sử hả chắc chx?")) {
        chatHistory = [[]];
        currentChatIndex = 0;
        localStorage.removeItem("chatHistory");
        renderChat();
        renderChatHistory();
    }
});

// Xóa lịch sử chat hiện tại
clearChatBtn.addEventListener("click", () => {
    if (confirm("Xoá lịch sử hả chắc chx?")) {
        chatHistory[currentChatIndex] = [];
        saveChatHistory();
        renderChat();
        renderChatHistory();
    }
});

// Hiển thị giá trị temperature
temperatureSlider.addEventListener("input", () => {
    tempValue.textContent = temperatureSlider.value;
});

// Vectorstore buttons
document.getElementById("create-vectorstore").addEventListener("click", () => {
    alert("Chức năng Vectorstore triển khai ở đây nè");
});
document.getElementById("open-vectorstore").addEventListener("click", () => {
    alert("Chức năng Open Vectorstore triển khai ở đây nè");
});

// Thêm tin nhắn mẫu khi trang được tải
window.addEventListener("DOMContentLoaded", () => {
    // Reload lại vẫn hiện thanh lịch sử nếu có dữ liệu cũ trc đoá
    if (!chatHistory || chatHistory.length === 0) {
        chatHistory = [[]];
    }

    if (chatHistory[0].length === 0) {
        addMessage("robot đây", "cần giúp gì?");
        chatHistory[0] = [{ sender: "robot đây", text: "Cần giúp gì?" }];
        saveChatHistory();
    } else {
        renderChat();
    }

    // Đảm bảo luôn hiển thị thanh lịch sử khi có dữ liệu cũ chứ ko cần nhấn newchat để xem thanh lịch sử nè
    renderChatHistory();
});

// Hàm lưu lại toàn bộ chat vào localStorage
function saveChatHistory() {
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
}