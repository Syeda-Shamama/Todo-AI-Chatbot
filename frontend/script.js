// frontend/script.js
// Task: TASK-008 | Spec: REQ-05

const API_BASE = "http://localhost:8000";
const USER_ID = "user1"; // hardcoded for now; can be replaced with auth later

let conversationId = null;

const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

// Append a message bubble to the chat
function appendMessage(role, text, type = "") {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message", role);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  if (type) bubble.classList.add(type);
  bubble.textContent = text;

  wrapper.appendChild(bubble);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return bubble;
}

// Show animated loading dots while waiting for response
function showLoading() {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message", "assistant");
  wrapper.id = "loadingMsg";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble", "loading");
  bubble.innerHTML = "<span></span><span></span><span></span>";

  wrapper.appendChild(bubble);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeLoading() {
  const el = document.getElementById("loadingMsg");
  if (el) el.remove();
}

// Send message to backend
async function sendMessage() {
  const text = messageInput.value.trim();
  if (!text) return;

  appendMessage("user", text);
  messageInput.value = "";
  sendBtn.disabled = true;
  showLoading();

  try {
    const res = await fetch(`${API_BASE}/api/${USER_ID}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conversation_id: conversationId,
        message: text,
      }),
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    const data = await res.json();
    conversationId = data.conversation_id;

    removeLoading();
    appendMessage("assistant", data.response);
  } catch (err) {
    removeLoading();
    appendMessage("assistant", "Something went wrong. Please try again.", "error");
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    messageInput.focus();
  }
}

// Send on button click
sendBtn.addEventListener("click", sendMessage);

// Send on Enter key
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
