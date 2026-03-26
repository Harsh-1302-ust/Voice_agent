import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./Chat.css";

const API_URL = "http://localhost:8000";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);

  // 🧠 Get/Create Session
  const getOrCreateSession = () => {
    let session = localStorage.getItem("session_id");

    if (!session) {
      session = crypto.randomUUID();
      localStorage.setItem("session_id", session);
    }

    return session;
  };

  // 🆕 New Chat
  const newChat = () => {
    const newSession = crypto.randomUUID();
    localStorage.setItem("session_id", newSession);
    setMessages([]);
  };

  // 📥 Load History
  useEffect(() => {
    const loadHistory = async () => {
      const session = getOrCreateSession();

      try {
        const res = await axios.get(`${API_URL}/history/${session}`);

        const formatted = res.data.messages.map((msg) => ({
          ...msg,
          ts: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        }));

        setMessages(formatted);
      } catch (err) {
        console.error("Failed to load history", err);
      }
    };

    loadHistory();
  }, []);

  // 📩 Send Message
  const sendMessage = async (text) => {
    if (!text?.trim() || loading) return;

    setLoading(true);

    const session = getOrCreateSession();

    const time = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const userMsg = { role: "user", content: text.trim(), ts: time };

    setMessages((prev) => [
      ...prev,
      userMsg,
      { role: "assistant", content: "", typing: true },
    ]);

    setInput("");

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        message: text,
        session_id: session,
      });

      const time2 = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.typing
            ? {
                role: "assistant",
                content: res.data.response,
                ts: time2,
              }
            : msg
        )
      );
    } catch (err) {
      console.error(err);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.typing
            ? {
                role: "assistant",
                content: "⚠️ Something went wrong. Try again.",
                ts: new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                }),
              }
            : msg
        )
      );
    }

    setLoading(false);
    inputRef.current?.focus();
  };

  // 🎤 Voice Input
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }

    if (listening && recognitionRef.current) {
      recognitionRef.current.stop();
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";

    recognition.onstart = () => setListening(true);

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      sendMessage(text);
    };

    recognition.onend = () => setListening(false);
    recognition.onerror = () => setListening(false);

    recognitionRef.current = recognition;
    recognition.start();
  };

  // ⌨️ Enter to Send
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  // 🔽 Auto Scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🎯 Autofocus
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="chat-app">
      {/* HEADER */}
      <header className="chat-header">
        <div className="title">AI Voice Agent</div>

        <div className="controls">
          <button className="icon-btn" onClick={newChat}>
            ➕ New Chat
          </button>

          <button
            className={`icon-btn mic ${listening ? "listening" : ""}`}
            onClick={startListening}
          >
            {listening ? "🎙" : "🎤"}
          </button>
        </div>
      </header>

      {/* CHAT */}
      <main className="chat-box">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${
              msg.role === "user" ? "user" : "assistant"
            }`}
          >
            <div className="avatar">
              {msg.role === "user" ? "U" : "AI"}
            </div>

            <div className="bubble-wrap">
              <div className={`bubble ${msg.typing ? "typing" : ""}`}>
                {msg.typing ? (
                  <span className="dots">
                    <em></em>
                    <em></em>
                    <em></em>
                  </span>
                ) : (
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                )}
              </div>

              {msg.ts && <div className="ts">{msg.ts}</div>}
            </div>
          </div>
        ))}

        <div ref={chatEndRef} />
      </main>

      {/* INPUT */}
      <form
        className="chat-input"
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage(input);
        }}
      >
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
        />

        <button className="send-btn" disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}