import React from "react";
import { getSessions } from "../services/sessionStorage";

export default function SessionHistoryPage({
  onHome,
  onOpenSession,
  onOpenConversation,
}) {
  const sessions = getSessions().reverse();

  return (
    <main className="history-page">
      <div className="history-shell">

        <header className="history-header">
          <div>
            <p className="eyebrow">
              Your Progress
            </p>

            <h1>Session History</h1>

            <p className="history-subtitle">
              Review your previous English practice
              sessions, conversations, and learning reports.
            </p>
          </div>

          <button
            className="report-home-button"
            onClick={onHome}
          >
            ← Home
          </button>
        </header>

        {sessions.length === 0 ? (
          <div className="history-empty">
            <div className="history-empty-icon">
              📚
            </div>

            <h2>No sessions yet</h2>

            <p>
              Complete your first practice session and
              your progress will appear here.
            </p>

            <button
              className="primary-button"
              onClick={onHome}
            >
              Back to Home
            </button>
          </div>
        ) : (
          <div className="history-grid">

            {sessions.map((session, index) => {
              const learnerMessages =
                session.messages?.filter(
                  (message) =>
                    message.role === "user"
                ).length || 0;

              const score =
                session.report?.overall_score ?? 0;

              return (
                <article
                  className="history-card"
                  key={session.session_id}
                >

                  <div className="history-card-top">

                    <div className="history-session-icon">
                      💬
                    </div>

                    <div>
                      <p className="history-session-number">
                        Session {sessions.length - index}
                      </p>

                      <h2>
                        Practice Session
                      </h2>
                    </div>

                  </div>

                  <div className="history-details">

                    <div className="history-detail">
                      <span className="detail-label">
                        Date
                      </span>

                      <strong>
                        {new Date(
                          session.started_at
                        ).toLocaleDateString()}
                      </strong>
                    </div>

                    <div className="history-detail">
                      <span className="detail-label">
                        Time
                      </span>

                      <strong>
                        {new Date(
                          session.started_at
                        ).toLocaleTimeString(
                          [],
                          {
                            hour: "2-digit",
                            minute: "2-digit",
                          }
                        )}
                      </strong>
                    </div>

                    <div className="history-detail">
                      <span className="detail-label">
                        Messages
                      </span>

                      <strong>
                        {learnerMessages}
                      </strong>
                    </div>

                  </div>

                  <div className="history-score-row">

                    <div>
                      <span className="detail-label">
                        Overall Score
                      </span>

                      <div className="history-score">
                        {score}
                        <span>/100</span>
                      </div>
                    </div>

                    <div
                      className={
                        score >= 75
                          ? "score-badge good-score"
                          : score >= 50
                          ? "score-badge average-score"
                          : "score-badge low-score"
                      }
                    >
                      {score >= 75
                        ? "Great work"
                        : score >= 50
                        ? "Keep improving"
                        : "Keep practicing"}
                    </div>

                  </div>

                  <div className="history-card-actions">

                    <button
                      className="view-conversation-button"
                      onClick={() =>
                        onOpenConversation(session)
                      }
                    >
                      View Conversation
                    </button>

                    <button
                      className="view-report-button"
                      onClick={() =>
                        onOpenSession(session)
                      }
                    >
                      View Report
                    </button>

                  </div>

                </article>
              );
            })}

          </div>
        )}

      </div>
    </main>
  );
}
