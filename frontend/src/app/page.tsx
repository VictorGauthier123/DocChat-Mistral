"use client";

import { useState } from "react";
import axios from "axios";
import ChatUI from "../components/ChatUI";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function HomePage() {
  const [sessionId, setSessionId] = useState<string | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSessionId(res.data.session_id);
    } catch (err) {
      console.error("Erreur upload:", err);
    }
  };

  return (
    <main className="h-screen bg-gray-100 flex items-center justify-center">
      {!sessionId ? (
        <div className="p-6 border rounded-xl shadow bg-white text-center">
          <label className="px-4 py-2  text-black rounded-lg cursor-pointer hover:bg-blue-700">
          Choisir un PDF
          <input
            type="file"
            accept="application/pdf"
            onChange={handleUpload}
            className="hidden"
          />
        </label>

        </div>
      ) : (
        <ChatUI sessionId={sessionId} />
      )}
    </main>
  );
}


