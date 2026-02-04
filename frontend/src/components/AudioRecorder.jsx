import { useRef, useState } from "react";
import { api } from "../services/api";

export default function AudioRecorder({ conversationId, role, sourceLanguage, targetLanguage }) {
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      chunks.current = [];

      mediaRecorder.current.ondataavailable = (e) => {
        chunks.current.push(e.data);
      };

      mediaRecorder.current.onstop = async () => {
        const blob = new Blob(chunks.current, { type: "audio/webm" });
        chunks.current = [];

        const formData = new FormData();
        formData.append("audio", blob, "recording.webm");
        formData.append("conversation_id", conversationId);
        formData.append("role", role);
        formData.append("source_language", sourceLanguage);
        formData.append("target_language", targetLanguage);

        setIsTranscribing(true);
        try {
          await api.post("/audio", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        } catch (error) {
          console.error("Error uploading audio:", error);
        } finally {
          setIsTranscribing(false);
        }
      };

      mediaRecorder.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Unable to access microphone. Please check permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="flex gap-2">
      <button
        onClick={startRecording}
        disabled={isRecording || isTranscribing}
        className="bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition flex items-center gap-2"
      >
        🎙️ {isRecording ? "Recording..." : "Start"}
      </button>
      <button
        onClick={stopRecording}
        disabled={!isRecording || isTranscribing}
        className="bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition flex items-center gap-2"
      >
        ⏹️ {isTranscribing ? "Processing..." : "Stop"}
      </button>
    </div>
  );
}
