const InputBar = ({ message, setMessage, sendMessage, startListening }) => {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="input-area">
      <input
        type="text"
        placeholder="Type or speak your symptoms…"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button onClick={startListening} title="Voice input">🎤</button>
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default InputBar;