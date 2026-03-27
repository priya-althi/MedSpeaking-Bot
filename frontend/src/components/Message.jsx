import { useRef, useState } from "react";

const Message = ({ sender = "bot", text = "", lang = "en" }) => {

  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const speakText = async () => {

    // 🔴 If already playing → STOP
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
      setIsPlaying(false);
      return;
    }

    try {
      const res = await fetch("https://medspeaking-bot.onrender.com/speak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, lang })
      });

      const blob = await res.blob();
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);

      audioRef.current = audio;
      setIsPlaying(true);

      audio.play();

      // When finished → reset
      audio.onended = () => {
        audioRef.current = null;
        setIsPlaying(false);
      };

    } catch (err) {
      alert("Voice service failed");
    }
  };

  return (
    <div className={`message ${sender === "user" ? "user" : "bot"}`}>
      <span>{text}</span>

      {sender === "bot" && (
        <div>
          <button className="speak-btn" onClick={speakText}>
            {isPlaying ? "⏹ Stop" : "🔊 Listen"}
          </button>
        </div>
      )}
    </div>
  );
};

export default Message;