import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./Chat.css";

const API_URL = "http://localhost:8000";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async (text) => {
    if (!text) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { role: "user", content: text, ts: time };
    // add user message and a typing placeholder for assistant
    setMessages((prev) => [...prev, userMsg, { role: "assistant", content: "", typing: true, ts: null }]);
    setInput("");

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        message: text,
      });

      const time2 = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages((prev) => {
        const copy = prev.slice();
        for (let i = copy.length - 1; i >= 0; i--) {
          if (copy[i].role === 'assistant' && copy[i].typing) {
            copy[i] = { role: 'assistant', content: res.data.response, typing: false, ts: time2 };
            break;
          }
        }
        return copy;
      });
    } catch (err) {
      console.error(err);
      setMessages((prev) => {
        const copy = prev.slice();
        for (let i = copy.length - 1; i >= 0; i--) {
          if (copy[i].role === 'assistant' && copy[i].typing) {
            copy[i] = { role: 'assistant', content: 'Error: failed to get response', typing: false, ts: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
            break;
          }
        }
        return copy;
      });
    }
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser");
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

    recognition.start();
  };

  // voice output removed: assistant responses are text-only

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-app">
      <header className="chat-header">
        <div className="title">Chat Agent</div>
        <div className="controls">
          <button
            className={`icon-btn mic ${listening ? "listening" : ""}`}
            onClick={startListening}
            title="Start voice input"
          >
            {listening ? "🎙" : "🎤"}
          </button>
        </div>
      </header>

      <main className="chat-box">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.role === "user" ? "user" : "assistant"}`}
          >
            <div className="avatar" aria-hidden>
              {msg.role === 'user' ? 'U' : 'A'}
            </div>
            <div className="bubble-wrap">
              <div className={`bubble ${msg.typing ? 'typing' : ''}`}>
                {msg.typing ? <span className="dots"><em></em><em></em><em></em></span> : msg.content}
              </div>
              {msg.ts && <div className="ts">{msg.ts}</div>}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </main>

      <form
        className="chat-input"
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage(input);
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message or press the mic"
          aria-label="Message"
        />
        <button className="send-btn" type="submit">
          Send
        </button>
      </form>
    </div>
  );
}