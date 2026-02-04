import { useState } from "react";
import ChatPage from "./pages/ChatPage";
import "./index.css";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <ChatPage />
    </div>
  );
}

export default App;
