import React, { useState } from "react";

import { saveSession } from "../services/sessionStorage";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import VoiceRecorder from "../components/VoiceRecorder";
import { evaluateSession, sendMessage } from "../services/api";

export default function ConversationPage({
  session,
  setSession,
  onReport,
  onHome,
}) {
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState("");

  async function handleSend(
    message,
    inputType = "text"
  ) {
    const trimmed = message.trim();

    if (!trimmed || loading) return;

    setLoading(true);
    setError("");

    try {
      const result = await sendMessage(
        session.session_id,
        trimmed,
        session.messages,
        inputType
      );

      setSession((currentSession) => ({
        ...currentSession,
        messages: result.history,
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleEndSession() {
    if (evaluating) return;

    setEvaluating(true);
    setError("");

    try {
      const report = await evaluateSession(
        session.messages
      );

      const completedSession = {
        ...session,
        ended_at: new Date().toISOString(),
        status: "completed",
        report,
      };

      setSession(completedSession);
      saveSession(completedSession);
      onReport(report);
    } catch (err) {
      setError(err.message);
    } finally {
      setEvaluating(false);
    }
  }

  return (
    <main className="conversation-page">
      <div className="conversation-shell">

        <header className="conversation-header">
          <div>
            <div className="brand-row">
              <div className="brand-icon">💬</div>
              <span>AI Language Coach</span>
            </div>

            <p className="eyebrow">
              Conversation Session
            </p>

            <h1>Practice naturally</h1>

            <p className="conversation-subtitle">
              Speak or type in English and keep the
              conversation going.
            </p>
          </div>

          <button
            className="home-button"
            onClick={onHome}
          >
            ← Home
          </button>
        </header>

        <section className="conversation-card">

          <div className="today-label">
            Today
          </div>

          <ChatWindow
            history={session.messages}
            loading={loading}
          />

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

          <div className="message-composer">

            <ChatInput
              onSend={handleSend}
              disabled={loading}
            />

            <VoiceRecorder
              onTranscript={handleSend}
              disabled={loading}
            />

          </div>

          <div className="conversation-actions">

            <span className="conversation-tip">
              💡 Try to speak naturally. You can use
              text or voice.
            </span>

            <button
              className="end-session-button"
              onClick={handleEndSession}
              disabled={evaluating}
            >
              {evaluating
                ? "Evaluating Session..."
                : "▥  End Session & View Report"}
            </button>

          </div>

        </section>
      </div>
    </main>
  );
}