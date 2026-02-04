export default function LanguageSelector({ language, setLanguage }) {
  return (
    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className="border border-gray-300 p-2 rounded-lg bg-white text-gray-700 font-medium hover:border-indigo-400 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
    >
      <option value="English">🇬🇧 English</option>
      <option value="Hindi">🇮🇳 Hindi</option>
      <option value="Spanish">🇪🇸 Spanish</option>
      <option value="French">🇫🇷 French</option>
    </select>
  );
}
