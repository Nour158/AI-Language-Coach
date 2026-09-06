import React from "react";
import ChatWindow from "../components/ChatWindow";

export default function PastConversationPage({
  session,
  onBack,
  onViewReport,
}) {
  return (
    <main className="conversation-page">
      <div className="conversation-shell">

        <header className="conversation-header">
          <div>
            <p className="eyebrow">
              Previous Session
            </p>

            <h1>Past Conversation</h1>

            <p className="conversation-subtitle">
              Review what you discussed during this
              practice session.
            </p>
          </div>

          <button
            className="home-button"
            onClick={onBack}
          >
            ← Session History
          </button>
        </header>

        <section className="conversation-card">

          <div className="past-session-info">
            <span>
              {new Date(
                session.started_at
              ).toLocaleString()}
            </span>

            <span>
              Score:{" "}
              {session.report?.overall_score ?? "N/A"}
              /100
            </span>
          </div>

          <ChatWindow
            history={session.messages || []}
            loading={false}
          />

          <div className="past-conversation-footer">
            <button
              className="primary-button"
              onClick={() =>
                onViewReport(session)
              }
            >
              View Learning Report
            </button>
          </div>

        </section>
      </div>
    </main>
  );
}