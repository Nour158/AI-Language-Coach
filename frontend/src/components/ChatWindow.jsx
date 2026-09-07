import React from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({
  history,
  loading,
}) {
  return (
    <div className="chat-window">

      {history.map((message, index) => (
        <MessageBubble
          key={index}
          message={message}
        />
      ))}

      {loading && (
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      )}

    </div>
  );
}