"use client";

import { useState } from "react";
import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function ChatBox({ sessionId }: { sessionId: string }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/query`, {
        session_id: sessionId,
        question: question,
      });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error("Erreur:", err);
      setAnswer("Impossible d’obtenir une réponse");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-xl shadow-md bg-white">
      <h2 className="text-lg font-bold mb-2">Pose une question sur ton document</h2>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Ex: Quelle est mon expérience pro ?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 border rounded px-2 py-1"
        />
        <button
          onClick={askQuestion}
          className="px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "..." : "Envoyer"}
        </button>
      </div>
      {answer && (
        <div className="mt-2 p-2 border rounded bg-gray-100">
          <p><strong>Réponse :</strong></p>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
