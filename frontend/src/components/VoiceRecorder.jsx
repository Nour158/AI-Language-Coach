import React, { useRef, useState } from "react";
import { transcribeAudio } from "../services/api";

export default function VoiceRecorder({ onTranscript, disabled }) {
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const [recording, setRecording] = useState(false);
  const [working, setWorking] = useState(false);

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    chunksRef.current = [];
    const recorder = new MediaRecorder(stream);
    mediaRecorderRef.current = recorder;

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
      }
    };

    recorder.onstop = async () => {
      setWorking(true);

      try {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const result = await transcribeAudio(blob);

        if (result.transcript) {
          onTranscript(
  result.transcript,
  "voice"
);
        }
      } catch (error) {
        alert(error.message);
      } finally {
        setWorking(false);
        stream.getTracks().forEach((track) => track.stop());
      }
    };

    recorder.start();
    setRecording(true);
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  if (recording) {
    return (
      <button className="voice-button recording" onClick={stopRecording}>
        Stop
      </button>
    );
  }

  return (
    <button
      className="voice-button"
      onClick={startRecording}
      disabled={disabled || working}
    >
      {working ? "Transcribing..." : "Voice"}
    </button>
  );
}
