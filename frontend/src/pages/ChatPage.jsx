import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import AudioRecorder from "../components/AudioRecorder";
import RoleSelector from "../components/RoleSelector";
import LanguageSelector from "../components/LanguageSelector";
import SearchBar from "../components/SearchBar";
import SummaryPanel from "../components/SummaryPanel";

export default function ChatPage() {
  const [role, setRole] = useState("doctor");
  const [sourceLanguage, setSourceLanguage] = useState("English");
  const [targetLanguage, setTargetLanguage] = useState("Hindi");
  const [conversationId] = useState(`conv-${Date.now()}`);
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🏥 Healthcare Conversation Translator
          </h1>
          <p className="text-gray-600">Real-time translation for doctor-patient conversations</p>
        </div>

        {/* Controls Panel */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Your Role</label>
              <RoleSelector role={role} setRole={setRole} />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">From Language</label>
              <LanguageSelector language={sourceLanguage} setLanguage={setSourceLanguage} />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">To Language</label>
              <LanguageSelector language={targetLanguage} setLanguage={setTargetLanguage} />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">Search Conversations</label>
            <SearchBar onSearch={handleSearch} />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Voice Input</label>
            <AudioRecorder
              conversationId={conversationId}
              role={role}
              sourceLanguage={sourceLanguage}
              targetLanguage={targetLanguage}
            />
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Window */}
          <div className="lg:col-span-2">
            <ChatWindow
              sourceLanguage={sourceLanguage}
              targetLanguage={targetLanguage}
              role={role}
              searchQuery={searchQuery}
            />
          </div>

          {/* Summary Panel */}
          <div className="lg:col-span-1">
            <SummaryPanel conversationId={conversationId} targetLanguage={targetLanguage} />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-600 text-sm">
          <p>Powered by Google Generative AI | Secure HIPAA-compliant conversations</p>
        </div>
      </div>
    </div>
  );
}
