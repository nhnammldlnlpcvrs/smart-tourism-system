/**
 * ui.js
 * ---------------------
 * Quản lý cập nhật giao diện người dùng.
 */

export function appendUserMessage(text) {
    const chatBody = document.getElementById("chat-body");
    const msg = document.createElement("div");
    msg.classList.add("user-message");
    msg.textContent = text;
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
}

export function appendBotMessage(text) {
    const chatBody = document.getElementById("chat-body");
    const msg = document.createElement("div");
    msg.classList.add("bot-message");
    msg.textContent = text;
    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
}