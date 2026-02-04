import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    onSearch(query);
  };

  const handleClear = () => {
    setQuery("");
    onSearch("");
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && handleSearch()}
        placeholder="Search conversations..."
        className="flex-1 border border-gray-300 rounded-lg p-2 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
      />
      <button
        onClick={handleSearch}
        disabled={!query.trim()}
        className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
      >
        🔍 Search
      </button>
      {query && (
        <button
          onClick={handleClear}
          className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition"
        >
          ✕ Clear
        </button>
      )}
    </div>
  );
}
