import React from "react";
export default function FeedbackCard({ mistake }) {
  return (
    <article className="feedback-card">
      <span className="tag">{mistake.category}</span>
      <p><strong>Original:</strong> {mistake.original}</p>
      <p><strong>Corrected:</strong> {mistake.corrected}</p>
      {mistake.natural_alternative && (
        <p><strong>Natural alternative:</strong> {mistake.natural_alternative}</p>
      )}
      <p><strong>Why:</strong> {mistake.explanation}</p>
    </article>
  );
}
