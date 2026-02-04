export default function RoleSelector({ role, setRole }) {
  return (
    <div className="flex gap-4">
      <label className="flex items-center gap-2 cursor-pointer">
        <input
          type="radio"
          name="role"
          value="doctor"
          checked={role === "doctor"}
          onChange={(e) => setRole(e.target.value)}
          className="w-4 h-4 accent-indigo-600"
        />
        <span className="text-gray-700 font-medium">👨‍⚕️ Doctor</span>
      </label>
      <label className="flex items-center gap-2 cursor-pointer">
        <input
          type="radio"
          name="role"
          value="patient"
          checked={role === "patient"}
          onChange={(e) => setRole(e.target.value)}
          className="w-4 h-4 accent-indigo-600"
        />
        <span className="text-gray-700 font-medium">🤒 Patient</span>
      </label>
    </div>
  );
}
