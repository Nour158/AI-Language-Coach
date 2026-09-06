import React from "react";

export default function ReportPage({
  report,
  onRestart,
  onHome,
}) {
  const scores = report?.scores || {};

  const scoreItems = [
    ["Grammar", scores.grammar ?? 0],
    ["Vocabulary", scores.vocabulary ?? 0],
    ["Fluency", scores.fluency ?? 0],
    ["Coherence", scores.coherence ?? 0],
    ["Sentence Structure", scores.sentence_structure ?? 0],
  ];

  return (
    <main className="report-page">
      <div className="report-shell">

        {/* HEADER */}
        <header className="report-header">
          <div>
            <p className="eyebrow">
              Session Complete
            </p>

            <h1>Your Learning Report</h1>

            <p className="report-subtitle">
              Here is your personalized English
              performance summary.
            </p>
          </div>

          <div className="report-header-actions">
            <button
              className="report-home-button"
              onClick={onHome}
            >
              ← Home
            </button>

            <button
              className="primary-button"
              onClick={onRestart}
            >
              Start New Session
            </button>
          </div>
        </header>


        {/* TOP SUMMARY */}
        <section className="report-summary-grid">

          <div className="overall-score-card">
            <p className="score-label">
              Overall Score
            </p>

            <div className="big-score">
              {report?.overall_score ?? 0}
              <span>/100</span>
            </div>

            <p className="score-description">
              Your performance across all evaluated
              language skills.
            </p>
          </div>


          <div className="skill-card">
            <h2>Skill Scores</h2>

            <div className="skill-list">
              {scoreItems.map(([name, value]) => (
                <div
                  className="skill-row"
                  key={name}
                >
                  <div className="skill-heading">
                    <span>{name}</span>
                    <strong>{value}/100</strong>
                  </div>

                  <div className="score-track">
                    <div
                      className="score-fill"
                      style={{
                        width: `${Math.min(
                          value,
                          100
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

        </section>


        {/* STRENGTHS + WEAKNESSES */}
        <section className="feedback-grid">

          <div className="feedback-card strength-card">
            <div className="feedback-title">
              <span className="feedback-icon">
                ✓
              </span>

              <h2>Strengths</h2>
            </div>

            {report?.strengths?.length ? (
              <ul>
                {report.strengths.map(
                  (item, index) => (
                    <li key={index}>
                      {item}
                    </li>
                  )
                )}
              </ul>
            ) : (
              <p className="empty-text">
                No strengths were identified yet.
              </p>
            )}
          </div>


          <div className="feedback-card weakness-card">
            <div className="feedback-title">
              <span className="feedback-icon">
                !
              </span>

              <h2>Areas to Improve</h2>
            </div>

            {report?.weaknesses?.length ? (
              <ul>
                {report.weaknesses.map(
                  (item, index) => (
                    <li key={index}>
                      {item}
                    </li>
                  )
                )}
              </ul>
            ) : (
              <p className="empty-text">
                No weaknesses were identified.
              </p>
            )}
          </div>

        </section>


        {/* DETAILED FEEDBACK */}
        <section className="report-section">
          <div className="section-heading">
            <div>
              <p className="section-tag">
                Corrections
              </p>

              <h2>Detailed Feedback</h2>
            </div>
          </div>

          {report?.mistakes?.length ? (
            <div className="mistake-list">
              {report.mistakes.map(
                (mistake, index) => (
                  <div
                    className="mistake-card"
                    key={index}
                  >
                    {typeof mistake === "string" ? (
                      mistake
                    ) : (
                      <>
                        {mistake.original && (
                          <p>
                            <strong>
                              You said:
                            </strong>{" "}
                            {mistake.original}
                          </p>
                        )}

                        {mistake.correction && (
                          <p>
                            <strong>
                              Better:
                            </strong>{" "}
                            {mistake.correction}
                          </p>
                        )}

                        {mistake.explanation && (
                          <p>
                            {
                              mistake.explanation
                            }
                          </p>
                        )}
                      </>
                    )}
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="empty-feedback">
              No specific mistakes were returned.
            </div>
          )}
        </section>


        {/* EXERCISES */}
        <section className="report-section">
          <div className="section-heading">
            <div>
              <p className="section-tag">
                Practice Next
              </p>

              <h2>Personalized Exercises</h2>
            </div>
          </div>

          {report?.exercises?.length ? (
            <div className="exercise-grid">
              {report.exercises.map(
                (exercise, index) => (
                  <div
                    className="exercise-card"
                    key={index}
                  >
                    <div className="exercise-number">
                      {index + 1}
                    </div>

                    <p>
                      {typeof exercise === "string"
                        ? exercise
                        : exercise.instruction ||
                          exercise.prompt ||
                          JSON.stringify(
                            exercise
                          )}
                    </p>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="empty-feedback">
              Complete more conversation practice
              to receive personalized exercises.
            </div>
          )}
        </section>

      </div>
    </main>
  );
}