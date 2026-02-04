import { useState, useRef, useEffect } from "react";
import { api } from "../services/api";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ sourceLanguage, targetLanguage, role, searchQuery }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId] = useState(`conv-${Date.now()}`);
  const [filteredMessages, setFilteredMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Load messages from localStorage on component mount
  useEffect(() => {
    const savedMessages = localStorage.getItem(`conv-${conversationId}`);
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (error) {
        console.error("Error loading saved messages:", error);
      }
    }
  }, [conversationId]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(`conv-${conversationId}`, JSON.stringify(messages));
  }, [messages, conversationId]);

  // Filter messages based on search query
  useEffect(() => {
    if (searchQuery && searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      const filtered = messages.filter(
        (msg) =>
          msg.original_text.toLowerCase().includes(query) ||
          msg.translated_text.toLowerCase().includes(query)
      );
      setFilteredMessages(filtered);
    } else {
      setFilteredMessages(messages);
    }
  }, [messages, searchQuery]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [filteredMessages]);

  const sendMessage = async () => {
    if (!text.trim()) return;

    const timestamp = new Date().toLocaleString();
    const userMessage = {
      id: `msg-${Date.now()}`,
      role,
      original_text: text,
      translated_text: "",
      isLoading: true,
      timestamp,
    };

    setMessages((prev) => [...prev, userMessage]);
    setText("");
    setLoading(true);

    try {
      const response = await api.post("/messages", {
        conversation_id: conversationId,
        role,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        text,
      });

      const messageData = response.data.message || response.data;
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === userMessage.id
            ? {
                ...msg,
                ...messageData,
                id: msg.id,
                timestamp,
                isLoading: false,
              }
            : msg
        )
      );
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = error.response?.data?.detail || "Failed to send message";
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === userMessage.id
            ? {
                ...msg,
                isLoading: false,
                error: errorMessage,
              }
            : msg
        )
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {filteredMessages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <p>{searchQuery ? "No messages match your search." : "No messages yet. Start a conversation!"}</p>
          </div>
        ) : (
          filteredMessages.map((msg) => (
            <MessageBubble 
              key={msg.id} 
              message={msg} 
              currentRole={role}
              searchQuery={searchQuery}
            />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex gap-2">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Type your message as ${role}...`}
            className="flex-1 border border-gray-300 rounded-lg p-3 resize-none focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 max-h-24"
            rows="2"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !text.trim()}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center gap-2"
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
