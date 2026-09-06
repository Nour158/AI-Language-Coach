import React, { useState } from "react";

export default function ChatInput({
  onSend,
  disabled,
}) {
  const [message, setMessage] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (!message.trim()) return;

    onSend(message, "text");

    setMessage("");
  }

  return (
    <form
      className="chat-input-form"
      onSubmit={handleSubmit}
    >
      <span className="input-icon">
        ☺
      </span>

      <input
        type="text"
        value={message}
        placeholder="Write your message in English..."
        onChange={(event) =>
          setMessage(event.target.value)
        }
        disabled={disabled}
      />

      <button
        type="submit"
        className="send-button"
        disabled={disabled}
      >
        ➤ Send
      </button>
    </form>
  );
}