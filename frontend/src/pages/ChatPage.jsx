import { useState } from "react";
import ChatBox from "../components/ChatBox";
import InputBar from "../components/InputBar";
import AgeInput from "../components/AgeInput";
import LanguageSelector from "../components/LanguageSelector";
import { sendMessageToBot } from "../api/chatService";
import "../styles/chat.css";

const ChatPage = () => {
  const [chat, setChat] = useState([]);
  const [message, setMessage] = useState("");
  const [age, setAge] = useState("");
  const [lang, setLang] = useState("en");
  const [loading, setLoading] = useState(false);

  // ------------------ VOICE INPUT ------------------
  const startListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Voice input not supported in this browser");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = lang;
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = (event) => {
      const speechText = event.results[0][0].transcript;
      setMessage(speechText);
    };

    recognition.onerror = () => {
      alert("Voice recognition failed. Try again.");
    };
  };

  // ------------------ SEND MESSAGE ------------------
  const sendMessage = async () => {
  if (!message.trim() || !age) return;

  // show user message
  setChat((prev) => [...prev, { sender: "user", text: message }]);
  setLoading(true);

  try {
    const data = await sendMessageToBot(message, age, lang);

    // ✅ CLARIFICATION CASE
    if (data.status === "clarification") {
      setChat((prev) => [
        ...prev,
        { sender: "bot", text: "🤖 " + data.message },
      ]);
      setLoading(false);
      setMessage("");
      return;
    }

    // ✅ FINAL RESPONSE CASE
    const botText =
      `🩺 Disease: ${data.disease}\n` +
      `📝 Advice: ${data.advice}\n` +
      `💊 Medicines: ${data.medicine}\n` +
      `${data.warning ? "⚠️ " + data.warning + "\n" : ""}`;

    setChat((prev) => [...prev, { sender: "bot", text: botText }]);
  } catch (err) {
    setChat((prev) => [
      ...prev,
      { sender: "bot", text: "⚠️ Server not reachable. Please try again." },
    ]);
  }

  setLoading(false);
  setMessage("");
};
  // ------------------ UI ------------------
  return (
    <div className="container">
      <h2>MedSpeaking Bot</h2>

      <div className="top-controls">
        <AgeInput age={age} setAge={setAge} />
        <LanguageSelector lang={lang} setLang={setLang} />
      </div>

      <ChatBox chat={chat} lang={lang} />

      {loading && <p className="typing">Analyzing your symptoms…</p>}

      <InputBar
        message={message}
        setMessage={setMessage}
        sendMessage={sendMessage}
        startListening={startListening}
      />

      <p className="footer-note">
        ⚠️ This chatbot provides general health information only. If symptoms
        are serious or continue, please consult a doctor.
      </p>
    </div>
  );
};

export default ChatPage;