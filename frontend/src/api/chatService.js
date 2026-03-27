export const sendMessageToBot = async (message, age, lang) => {
  try {
    const res = await fetch("https://medspeaking-bot.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, age, lang })
    });

    if (!res.ok) throw new Error("Server error");

    return await res.json();
  } catch (err) {
    return { error: "Unable to connect to server" };
  }
};
