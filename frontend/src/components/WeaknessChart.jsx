import React from "react";
export default function WeaknessChart({ scores = {} }) {
  return (
    <section className="panel">
      <h2>Skill Scores</h2>
      <div className="score-list">
        {Object.entries(scores).map(([name, value]) => (
          <div className="score-row" key={name}>
            <span>{name.replaceAll("_", " ")}</span>
            <div className="bar">
              <div className="bar-fill" style={{ width: `${value}%` }} />
            </div>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
