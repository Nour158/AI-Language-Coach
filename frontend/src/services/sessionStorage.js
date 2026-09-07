const STORAGE_KEY = "ai_language_coach_sessions";


export function getSessions() {
  const saved = localStorage.getItem(STORAGE_KEY);

  if (!saved) {
    return [];
  }

  try {
    return JSON.parse(saved);
  } catch {
    return [];
  }
}


export function saveSession(session) {
  const sessions = getSessions();

  const existingIndex = sessions.findIndex(
    (item) => item.session_id === session.session_id
  );

  if (existingIndex >= 0) {
    sessions[existingIndex] = session;
  } else {
    sessions.push(session);
  }

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(sessions)
  );
}


export function getSession(sessionId) {
  const sessions = getSessions();

  return sessions.find(
    (session) => session.session_id === sessionId
  );
}


export function deleteSession(sessionId) {
  const sessions = getSessions().filter(
    (session) => session.session_id !== sessionId
  );

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(sessions)
  );
}