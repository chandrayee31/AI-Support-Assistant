import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! Upload a sales file with the **+** button, then ask things like:\n\n- What is the total revenue?\n- Which products are top selling?\n- What should I restock tomorrow?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [activeFile, setActiveFile] = useState("");
  const fileInputRef = useRef(null);

  const fetchUploadedFiles = async () => {
    try {
      const res = await fetch("http://localhost:8000/uploaded-files");
      const data = await res.json();

      setUploadedFiles(data.files || []);
      setActiveFile(data.active_file || "");
    } catch (err) {
      console.error("Failed to fetch uploaded files");
    }
  };

  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading || uploading) return;

    const currentInput = input;
    const userMessage = { role: "user", content: currentInput };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: currentInput }),
      });

      const data = await res.json();

      const aiMessage = {
        role: "assistant",
        content: data.answer || "No answer returned.",
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error connecting to backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const openFilePicker = () => {
    if (!uploading && !loading) {
      fileInputRef.current?.click();
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: `📎 Uploaded file: **${file.name}**`,
      },
    ]);

    try {
      const res = await fetch("http://localhost:8000/upload-sales", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `⚠️ Upload failed: ${data.detail || "Unknown error"}`,
          },
        ]);
        return;
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `✅ File uploaded successfully: **${data.filename || file.name}**\n\nYou can now ask questions about this dataset.`,
        },
      ]);

      await fetchUploadedFiles();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error uploading file.",
        },
      ]);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const handleActiveFileChange = async (event) => {
    const filename = event.target.value;
    setActiveFile(filename);

    if (!filename) return;

    try {
      const res = await fetch("http://localhost:8000/set-active-file", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `⚠️ Failed to switch active file: ${data.detail || "Unknown error"}`,
          },
        ]);
        return;
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `📂 Active dataset switched to **${filename}**`,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Error switching active file.",
        },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header branded-header">
        <div className="logo">
          <div className="logo-icon">📦</div>
          <div className="logo-text">
            <div className="title">StockSense AI</div>
            <div className="subtitle">Smarter stocking. Better decisions.</div>
          </div>
        </div>
      </header>

      <div className="toolbar">
        <div className="dataset-selector">
          <label htmlFor="activeFile">Active Dataset:</label>
          <select
            id="activeFile"
            value={activeFile}
            onChange={handleActiveFileChange}
            disabled={loading || uploading || uploadedFiles.length === 0}
          >
            <option value="">Select a file</option>
            {uploadedFiles.map((file) => (
              <option key={file} value={file}>
                {file}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.role === "user" ? "user" : "assistant"}`}
          >
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}

        {uploading && (
          <div className="chat-bubble assistant thinking">Uploading file…</div>
        )}

        {loading && (
          <div className="chat-bubble assistant thinking">Thinking…</div>
        )}
      </div>

      {activeFile && (
        <div className="uploaded-file-banner">
          Active file: <strong>{activeFile}</strong>
        </div>
      )}

      <div className="chat-input">
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />

        <button
          className="icon-button"
          onClick={openFilePicker}
          title="Upload file"
          type="button"
          disabled={loading || uploading}
        >
          +
        </button>

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something about your store..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading || uploading}
        />

        <button onClick={sendMessage} disabled={loading || uploading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;