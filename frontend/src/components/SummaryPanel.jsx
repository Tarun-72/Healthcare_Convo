import { useState } from "react";
import { api } from "../services/api";

export default function SummaryPanel({ conversationId, targetLanguage }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/summary?conversation_id=${conversationId}&target_language=${targetLanguage || "English"}`);
      const summaryText = response.data.summary || response.data.content || response.data;
      setSummary(summaryText);
    } catch (err) {
      console.error("Error generating summary:", err);
      setError("Failed to generate summary. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-full flex flex-col">
      <h3 className="font-semibold text-gray-900 mb-4">📋 Conversation Summary</h3>
      
      <button
        onClick={generateSummary}
        disabled={loading}
        className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition mb-4"
      >
        {loading ? "⏳ Generating..." : "📝 Generate Summary"}
      </button>

      <div className="flex-1 overflow-y-auto">
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {summary && (
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-indigo-200">
            <h4 className="font-semibold text-gray-900 mb-3">Summary</h4>
            <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">{summary}</p>
          </div>
        )}

        {!summary && !loading && !error && (
          <div className="text-center py-8">
            <p className="text-gray-400 text-sm">Click "Generate Summary" to create a summary of this conversation</p>
          </div>
        )}
      </div>
    </div>
  );
}
