function highlightSearchText(text, searchQuery) {
  if (!searchQuery || !text) return text;

  const query = searchQuery.toLowerCase();
  const parts = text.split(new RegExp(`(${searchQuery})`, "gi"));

  return parts.map((part, i) =>
    part.toLowerCase() === query ? (
      <mark key={i} className="bg-yellow-300 font-semibold text-gray-900">
        {part}
      </mark>
    ) : (
      part
    )
  );
}

export default function MessageBubble({ message, currentRole, searchQuery }) {
  const isCurrentUser = message.role === currentRole;

  return (
    <div className={`flex ${isCurrentUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-2 rounded-lg ${
          isCurrentUser
            ? "bg-indigo-600 text-white"
            : "bg-gray-200 text-gray-900"
        }`}
      >
        {message.isLoading ? (
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
            <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
          </div>
        ) : (
          <>
            <div className="flex justify-between items-start gap-2 mb-1">
              <p className="text-sm font-semibold">{message.role}</p>
              {message.timestamp && (
                <p className={`text-xs ${isCurrentUser ? "text-indigo-200" : "text-gray-500"}`}>
                  {message.timestamp}
                </p>
              )}
            </div>
            <p className="text-sm mb-2">{highlightSearchText(message.original_text, searchQuery)}</p>
            {message.translated_text && (
              <>
                <hr className={isCurrentUser ? "border-indigo-400" : "border-gray-300"} />
                <p className={`text-xs mt-2 ${isCurrentUser ? "text-indigo-100" : "text-gray-600"}`}>
                  <strong>Translation:</strong> {highlightSearchText(message.translated_text, searchQuery)}
                </p>
              </>
            )}
            {message.audio_path && (
              <audio controls className="mt-2 w-full">
                <source src={`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/${message.audio_path}`} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            )}
            {message.error && (
              <p className="text-xs mt-2 text-red-400">{message.error}</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
