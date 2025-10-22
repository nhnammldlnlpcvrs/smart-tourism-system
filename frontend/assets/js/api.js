/**
 * api.js
 * ---------------------
 * Xử lý việc gọi API tới backend (FastAPI hoặc Flask)
 * TODO: cập nhật URL thực tế sau khi backend chạy.
 */

const API_URL = "http://127.0.0.1:8000/chat";

export async function sendMessageToBackend(message) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: message }),
        });
        const data = await response.json();
        return data.answer || "Xin lỗi, tôi chưa hiểu câu hỏi của bạn 😅";
    } catch (error) {
        console.error("Error calling backend:", error);
        return "Lỗi kết nối đến máy chủ.";
    }
}