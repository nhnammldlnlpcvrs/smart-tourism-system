/**
 * main.js
 * ---------------------
 * Điều khiển luồng chính của chatbot:
 * - Lắng nghe input người dùng
 * - Gọi API backend
 * - Cập nhật UI
 */

import { sendMessageToBackend } from "./api.js";
import { appendUserMessage, appendBotMessage } from "./ui.js";

document.getElementById("send-btn").addEventListener("click", handleSend);
document.getElementById("user-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSend();
});

async function handleSend() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    appendUserMessage(message);
    input.value = "";

    appendBotMessage("⏳ Đang xử lý...");

    const reply = await sendMessageToBackend(message);

    // Xóa dòng "đang xử lý"
    const chatBody = document.getElementById("chat-body");
    chatBody.lastChild.remove();

    appendBotMessage(reply);
}
