import { useState, useRef, useEffect, useCallback } from "react";
import "./App.css";

const API = import.meta.env.VITE_API_URL || "https://careerbuddyai-wof2.onrender.com";

// ─── helpers ─────────────────────────────────────────────────────────────────
function scoreColor(n) {
  if (n >= 70) return "emerald";
  if (n >= 40) return "violet";
  return "blue";
}

// ─── sub-components ──────────────────────────────────────────────────────────
function ScoreCard({ label, value, unit = "%", verdict, color }) {
  const pct = Math.min(100, Math.max(0, Number(value) || 0));
  return (
    <div className={`score-card ${color}`}>
      <div className="score-label">{label}</div>
      <div className="score-number">
        {pct}
        <span style={{ fontSize: "1.25rem", fontWeight: 500 }}>{unit}</span>
      </div>
      {verdict && <div className="score-verdict">{verdict}</div>}
      <div className="progress-bar-wrap">
        <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function SkillTags({ skills, variant }) {
  if (!skills || skills.length === 0)
    return <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>—</span>;
  return (
    <div className="skill-tags">
      {skills.map((s) => (
        <span key={s} className={`skill-tag ${variant}`}>
          {s}
        </span>
      ))}
    </div>
  );
}

function ContactGrid({ contact }) {
  const fields = [
    { key: "name", label: "Name" },
    { key: "email", label: "Email" },
    { key: "phone", label: "Phone" },
    { key: "linkedin", label: "LinkedIn" },
    { key: "github", label: "GitHub" },
    { key: "location", label: "Location" },
  ];
  return (
    <div className="contact-grid">
      {fields.map(({ key, label }) =>
        contact?.[key] ? (
          <div key={key} className="contact-item">
            <span className="contact-item-label">{label}</span>
            <span className="contact-item-value" title={contact[key]}>
              {contact[key]}
            </span>
          </div>
        ) : null
      )}
    </div>
  );
}

// ─── main App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");
  const [backendOk, setBackendOk] = useState(null);

  // Chat
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm CareerBuddy AI 👋 Analyze your resume first, then ask me anything about your career!",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef(null);

  // ── ping backend on mount ─────────────────────────────────────────────────
  useEffect(() => {
    fetch(`${API}/health`)
      .then((r) => r.json())
      .then(() => setBackendOk(true))
      .catch(() => setBackendOk(false));
  }, []);

  // ── auto-scroll chat ──────────────────────────────────────────────────────
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // ── file handlers ─────────────────────────────────────────────────────────
  const handleFile = useCallback((f) => {
    if (!f) return;
    if (!f.name.endsWith(".pdf")) {
      setError("Please upload a PDF file.");
      return;
    }
    setFile(f);
    setError("");
    setResults(null);
  }, []);

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      handleFile(e.dataTransfer.files[0]);
    },
    [handleFile]
  );

  // ── analyze ───────────────────────────────────────────────────────────────
  const analyze = async () => {
    if (!file) {
      setError("Please upload a resume PDF.");
      return;
    }
    setLoading(true);
    setError("");
    setResults(null);

    try {
      const form = new FormData();
      form.append("file", file);
      form.append("jd_text", jdText);

      const res = await fetch(`${API}/resume/analyze`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server error ${res.status}`);
      }

      const data = await res.json();
      setResults(data);
      setActiveTab("overview");
      setChatMessages([
        {
          role: "assistant",
          text: `✅ Resume analyzed! Your ATS score is **${data.ats?.ats_score ?? "?"}%** and job match is **${data.match?.match_percentage ?? "?"}%**. Ask me anything about your results!`,
        },
      ]);
    } catch (e) {
      setError(e.message || "Failed to analyze resume. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  // ── chat ──────────────────────────────────────────────────────────────────
  const sendChat = async () => {
    if (!chatInput.trim() || chatLoading) return;
    const message = chatInput.trim();
    setChatInput("");
    setChatMessages((m) => [...m, { role: "user", text: message }]);
    setChatLoading(true);

    try {
      const context = results
        ? {
            resume_text: results.text || "",
            jd_text: jdText,
            ats_score: results.ats?.ats_score ?? 0,
            match_percentage: results.match?.match_percentage ?? 0,
            missing_skills: results.skill_gap?.missing_skills ?? [],
          }
        : {};

      const res = await fetch(`${API}/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, context }),
      });

      const data = await res.json();
      setChatMessages((m) => [...m, { role: "assistant", text: data.reply }]);
    } catch {
      setChatMessages((m) => [
        ...m,
        { role: "assistant", text: "Sorry, I couldn't reach the backend right now." },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const onChatKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendChat();
    }
  };

  // ── render ────────────────────────────────────────────────────────────────
  return (
    <div className="app">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-brand">
          <span className="navbar-brand-icon">🚀</span>
          CareerBuddy AI
        </div>
        <div className="navbar-status">
          <span
            className="status-dot"
            style={{ background: backendOk === false ? "var(--accent-rose)" : "var(--accent-emerald)" }}
          />
          {backendOk === null ? "Connecting…" : backendOk ? "Backend Connected" : "Backend Offline"}
        </div>
      </nav>

      {/* Hero */}
      <section className="hero">
        <div className="hero-badge">✨ AI-Powered Career Analysis</div>
        <h1 className="hero-title">
          Land Your <span>Dream Job</span>
          <br />
          Smarter & Faster
        </h1>
        <p className="hero-subtitle">
          Upload your resume, paste a job description, and get instant ATS scoring,
          skill gap analysis, and a personalised career roadmap — powered by AI.
        </p>
      </section>

      <main className="main-content">
        {/* Error banner */}
        {error && (
          <div className="error-banner">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Input Panel */}
        <div className="card" style={{ marginBottom: "1.5rem" }}>
          <div className="input-panel">
            {/* Upload */}
            <div>
              <label className="jd-label">📄 Resume (PDF)</label>
              <div
                className={`upload-zone ${dragOver ? "drag-over" : ""}`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={onDrop}
                onClick={() => document.getElementById("resume-file-input").click()}
              >
                <input
                  id="resume-file-input"
                  type="file"
                  accept=".pdf"
                  className="upload-zone-input"
                  style={{ display: "none" }}
                  onChange={(e) => handleFile(e.target.files[0])}
                />
                <div className="upload-icon">📂</div>
                <div className="upload-label">
                  {file ? "Change Resume" : "Drop PDF here or click to browse"}
                </div>
                <div className="upload-hint">PDF only · Max 5 MB</div>
                {file && (
                  <div className="upload-file-name">
                    ✅ {file.name}
                  </div>
                )}
              </div>
            </div>

            {/* Job Description */}
            <div style={{ display: "flex", flexDirection: "column" }}>
              <label className="jd-label">💼 Job Description (optional but recommended)</label>
              <textarea
                className="jd-textarea"
                placeholder="Paste the job description here to get ATS score, job match %, and skill gap analysis tailored to this role…"
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                style={{ flex: 1 }}
              />
            </div>
          </div>

          <button
            id="analyze-button"
            className="analyze-btn"
            onClick={analyze}
            disabled={loading || !file}
          >
            {loading ? (
              <>
                <div className="spinner" />
                Analyzing Resume…
              </>
            ) : (
              <>🔍 Analyze My Resume</>
            )}
          </button>
        </div>

        {/* Results */}
        {results ? (
          <>
            {/* Tabs */}
            <div className="tabs">
              {["overview", "skills", "roadmap", "chat"].map((t) => (
                <button
                  key={t}
                  id={`tab-${t}`}
                  className={`tab-btn ${activeTab === t ? "active" : ""}`}
                  onClick={() => setActiveTab(t)}
                >
                  {t === "overview" && "📊 Overview"}
                  {t === "skills" && "🧠 Skills"}
                  {t === "roadmap" && "🗺️ Roadmap"}
                  {t === "chat" && "💬 AI Chat"}
                </button>
              ))}
            </div>

            {/* Overview Tab */}
            {activeTab === "overview" && (
              <>
                {/* Score cards */}
                <div className="results-grid">
                  <ScoreCard
                    label="ATS Score"
                    value={results.ats?.ats_score ?? 0}
                    verdict={`${results.ats?.matched_keywords?.length ?? 0} / ${results.ats?.total_keywords_checked ?? 0} keywords matched`}
                    color={scoreColor(results.ats?.ats_score ?? 0)}
                  />
                  <ScoreCard
                    label="Job Match"
                    value={results.match?.match_percentage ?? 0}
                    verdict={results.match?.verdict}
                    color={scoreColor(results.match?.match_percentage ?? 0)}
                  />
                  <ScoreCard
                    label="Skill Gap"
                    value={(() => {
                      const missing = results.skill_gap?.gap_count ?? 0;
                      const total   = results.skill_gap?.total_jd_skills
                                      ?? ((results.skill_gap?.present_skills?.length ?? 0) + missing);
                      return total > 0 ? Math.round((missing / total) * 100) : 0;
                    })()}
                    verdict={`${results.skill_gap?.gap_count ?? 0} missing skill${results.skill_gap?.gap_count === 1 ? "" : "s"} out of ${results.skill_gap?.total_jd_skills ?? (results.skill_gap?.gap_count ?? 0) + (results.skill_gap?.present_skills?.length ?? 0)}`}
                    color="violet"
                  />
                </div>

                {/* Contact + Role prediction */}
                <div className="sections-grid">
                  <div className="card">
                    <div className="card-title">👤 Contact Info</div>
                    <ContactGrid contact={results.contact} />
                    <div className="section-divider" />
                    <div className="card-title" style={{ marginBottom: "0.5rem" }}>
                      📋 Resume Stats
                    </div>
                    <div style={{ fontSize: "0.875rem", color: "var(--text-secondary)" }}>
                      <span style={{ color: "var(--accent-blue)", fontWeight: 700 }}>
                        {results.word_count}
                      </span>{" "}
                      words &nbsp;·&nbsp;
                      <span style={{ color: "var(--accent-violet)", fontWeight: 700 }}>
                        {results.resume_skills?.length ?? 0}
                      </span>{" "}
                      skills detected
                    </div>
                  </div>

                  <div className="card">
                    <div className="card-title">🎯 Role Prediction</div>
                    {results.role_prediction ? (
                      <>
                        <div style={{ marginBottom: "0.75rem" }}>
                          <div className="keywords-label">Best Fit Role</div>
                          <div
                            style={{
                              fontSize: "1.2rem",
                              fontWeight: 700,
                              fontFamily: "Outfit, sans-serif",
                              color: "var(--accent-blue)",
                              marginTop: "0.25rem",
                            }}
                          >
                            {results.role_prediction.predicted_role}
                          </div>
                          <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: "0.2rem" }}>
                            {results.role_prediction.confidence}% confidence
                          </div>
                        </div>
                        {results.role_prediction.top_3_matches?.map((r, i) => (
                          <div
                            key={r.role}
                            className={`role-prediction-row ${i === 0 ? "top" : ""}`}
                          >
                            <span className="role-name">
                              #{i + 1} {r.role}
                            </span>
                            <span className="role-confidence">{r.confidence}%</span>
                          </div>
                        ))}
                      </>
                    ) : (
                      <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                        Role prediction not available. Train the classifier first.
                      </div>
                    )}
                  </div>
                </div>

                {/* Matched / Missing keywords */}
                {results.ats && (
                  <div className="card">
                    <div className="card-title">🔑 ATS Keywords</div>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
                      <div>
                        <div className="keywords-label">✅ Matched</div>
                        <SkillTags skills={results.ats.matched_keywords} variant="present" />
                      </div>
                      <div>
                        <div className="keywords-label">❌ Missing</div>
                        <SkillTags skills={results.ats.missing_keywords} variant="missing" />
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Skills Tab */}
            {activeTab === "skills" && (
              <div className="card">
                <div className="card-title">🧠 Skill Gap Analysis</div>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                    gap: "1.5rem",
                  }}
                >
                  <div>
                    <div className="keywords-label" style={{ marginBottom: "0.625rem" }}>
                      ✅ Skills You Have (matched JD)
                    </div>
                    <SkillTags skills={results.skill_gap?.present_skills} variant="present" />
                  </div>
                  <div>
                    <div className="keywords-label" style={{ marginBottom: "0.625rem" }}>
                      ❌ Missing Skills (in JD, not resume)
                    </div>
                    <SkillTags skills={results.skill_gap?.missing_skills} variant="missing" />
                  </div>
                  <div>
                    <div className="keywords-label" style={{ marginBottom: "0.625rem" }}>
                      ⭐ Bonus Skills (resume extras)
                    </div>
                    <SkillTags skills={results.skill_gap?.bonus_skills} variant="bonus" />
                  </div>
                  <div>
                    <div className="keywords-label" style={{ marginBottom: "0.625rem" }}>
                      📌 All Resume Skills
                    </div>
                    <SkillTags skills={results.resume_skills} variant="neutral" />
                  </div>
                </div>
              </div>
            )}

            {/* Roadmap Tab */}
            {activeTab === "roadmap" && (
              <div className="card">
                <div className="card-title">🗺️ Personalised Career Roadmap</div>
                {results.roadmap ? (
                  <div className="roadmap-text">{results.roadmap}</div>
                ) : (
                  <div style={{ fontSize: "0.875rem", color: "var(--text-muted)" }}>
                    Paste a job description and re-analyze to generate a roadmap.
                  </div>
                )}
              </div>
            )}

            {/* Chat Tab */}
            {activeTab === "chat" && (
              <div className="card chat-section">
                <div className="card-title">💬 AI Career Assistant</div>
                <div className="chat-messages">
                  {chatMessages.map((m, i) => (
                    <div key={i} className={`chat-bubble ${m.role}`}>
                      {m.text}
                    </div>
                  ))}
                  {chatLoading && (
                    <div className="chat-bubble typing">CareerBuddy is thinking…</div>
                  )}
                  <div ref={chatEndRef} />
                </div>
                <div className="chat-input-row">
                  <input
                    id="chat-input-field"
                    className="chat-input"
                    placeholder="Ask me about your resume, skills, salary, interviews…"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={onChatKey}
                    disabled={chatLoading}
                  />
                  <button
                    id="chat-send-button"
                    className="chat-send-btn"
                    onClick={sendChat}
                    disabled={chatLoading || !chatInput.trim()}
                  >
                    {chatLoading ? <div className="spinner" style={{ borderTopColor: "#020617" }} /> : "Send ➤"}
                  </button>
                </div>
              </div>
            )}
          </>
        ) : (
          /* Empty state */
          !loading && (
            <div className="card">
              <div className="empty-state">
                <div className="empty-state-icon">📋</div>
                <div className="empty-state-title">Ready to analyze your resume</div>
                <div className="empty-state-hint">
                  Upload a PDF and optionally paste a job description above, then hit{" "}
                  <strong style={{ color: "var(--accent-blue)" }}>Analyze My Resume</strong>.
                  You'll get ATS score, job match %, skill gap, AI roadmap, and a career chatbot — all connected to the backend.
                </div>
              </div>
            </div>
          )
        )}
      </main>

      <footer className="footer">
        CareerBuddy AI &nbsp;·&nbsp; Backend at{" "}
        <a href="https://careerbuddyai-wof2.onrender.com/docs" target="_blank" rel="noreferrer">
          careerbuddyai-wof2.onrender.com/docs
        </a>
      </footer>
    </div>
  );
}