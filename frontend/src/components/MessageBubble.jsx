import React from "react";

export default function MessageBubble({
  message,
}) {
  const isUser = message.role === "user";

  return (
    <div
      className={
        isUser
          ? "message-row user-message-row"
          : "message-row assistant-message-row"
      }
    >
      {!isUser && (
        <div className="coach-avatar">
          🤖
        </div>
      )}

      <div className="message-content">

        <span className="message-name">
          {isUser ? "You" : "AI Coach"}
        </span>

        <div
          className={
            isUser
              ? "message-bubble user-bubble"
              : "message-bubble assistant-bubble"
          }
        >
          {message.content}
        </div>

      </div>
    </div>
  );
}