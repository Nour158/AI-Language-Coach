import React from "react";
export default function ScoreCard({ title, score, suffix = "" }) {
  return (
    <section className="panel score-card">
      <p>{title}</p>
      <strong>
        {score}
        {suffix}
      </strong>
    </section>
  );
}
