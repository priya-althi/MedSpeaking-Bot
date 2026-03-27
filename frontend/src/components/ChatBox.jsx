import { useEffect, useRef } from "react";
import Message from "./Message";

const ChatBox = ({ chat = [], lang = "en" }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  return (
    <div className="chat-box">
      {chat.length === 0 && (
        <div className="empty-state">
          <span className="empty-icon">🩺</span>
          <p>Describe your symptoms and I'll help identify what it might be.</p>
        </div>
      )}
      {chat.map((c, i) => (
        <Message key={i} sender={c.sender} text={c.text} lang={lang} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default ChatBox;