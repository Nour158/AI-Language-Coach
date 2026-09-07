import React from "react";
import logo from "../assets/logo.png";
export default function HomePage({
  onStart,
  onHistory,
}) {
  return (
    <div className="page">
      <div className="container">
        <div className="home-card">
          <img
           src={logo}
           alt="AI Language Coach"
           className="home-logo"
          />
          <div className="home-badge">
            AI-Powered English Practice
          </div>
             
          <h1 className="home-title">
            Speak Better.
            <br />
            Learn <span>Smarter.</span>
          </h1>

          <p className="home-description">
            Practice natural English conversations using
            text or voice, then receive personalized
            feedback on your grammar, vocabulary,
            fluency, and communication skills.
          </p>

          <div className="home-features">
            <div className="feature-pill">
              🎙 Voice Practice
            </div>

            <div className="feature-pill">
              💬 AI Conversation
            </div>

            <div className="feature-pill">
              📊 Personalized Feedback
            </div>

            <div className="feature-pill">
              📚 Session History
            </div>
          </div>

          <div className="home-actions">
            <button
              className="primary-button"
              onClick={onStart}
            >
              Start Practice Session →
            </button>

            <button
              className="secondary-button"
              onClick={onHistory}
            >
              View Session History
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}