import React, { useState } from "react";

import HomePage from "./pages/HomePage";
import ConversationPage from "./pages/ConversationPage";
import ReportPage from "./pages/ReportPage";
import SessionHistoryPage from "./pages/SessionHistoryPage";
import PastConversationPage from "./pages/PastConversationPage";

export default function App() {
  const [page, setPage] = useState("home");
  const [session, setSession] = useState(null);
  const [report, setReport] = useState(null);

  function startSession() {
    const newSession = {
      session_id: crypto.randomUUID(),
      started_at: new Date().toISOString(),
      ended_at: null,
      status: "active",

      messages: [
        {
          role: "assistant",
          content:
            "Hi! I'm your AI Language Coach. What would you like to talk about today?",
          metadata: {
            source: "system_greeting",
          },
        },
      ],
    };

    setSession(newSession);
    setReport(null);
    setPage("conversation");
  }

  // HOME PAGE
  if (page === "home") {
    return (
      <HomePage
        onStart={startSession}
        onHistory={() => setPage("history")}
      />
    );
  }

  // REPORT PAGE
  if (page === "report") {
    return (
      <ReportPage
        report={report}
        onRestart={startSession}
        onHome={() => setPage("home")}
      />
    );
  }

  // SESSION HISTORY PAGE
  if (page === "history") {
    return (
      <SessionHistoryPage
        onHome={() => setPage("home")}

        onOpenSession={(savedSession) => {
          setSession(savedSession);
          setReport(savedSession.report);
          setPage("report");
        }}

        onOpenConversation={(savedSession) => {
          setSession(savedSession);
          setPage("past-conversation");
        }}
      />
    );
  }

  // PAST CONVERSATION PAGE
  if (page === "past-conversation") {
    return (
      <PastConversationPage
        session={session}

        onBack={() => {
          setPage("history");
        }}

        onViewReport={(savedSession) => {
          setSession(savedSession);
          setReport(savedSession.report);
          setPage("report");
        }}
      />
    );
  }

  // ACTIVE CONVERSATION PAGE
  return (
    <ConversationPage
      session={session}
      setSession={setSession}

      onReport={(newReport) => {
        setReport(newReport);
        setPage("report");
      }}

      onHome={() => {
        setPage("home");
      }}
    />
  );
}