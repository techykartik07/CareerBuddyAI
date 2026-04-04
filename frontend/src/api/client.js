import axios from 'axios'

// Switch this to Render URL when Ajay deploys:
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const analyzeResume = async (pdfFile, jdText) => {
  const form = new FormData()
  form.append('file', pdfFile)
  form.append('jd_text', jdText)
  const res = await axios.post(`${API_BASE}/resume/analyze`, form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data
}

export const sendChatMessage = async (message, context) => {
  const res = await axios.post(`${API_BASE}/ai/chat`, { message, context })
  return res.data
}
// In api/client.js, add a mock function for testing:
export const analyzeResumeMock = async () => ({
  contact: { name: "Test User", email: "test@email.com" },
  ats: { ats_score: 62, matched_keywords: ["python","ml"], missing_keywords: ["docker","fastapi"] },
  match: { match_percentage: 71.4, verdict: "Moderate match" },
  skill_gap: { missing_skills: ["docker","fastapi","tensorflow"], present_skills: ["python","numpy"] },
  roadmap: "## Week 1\nLearn FastAPI basics...\n## Week 2\nDocker fundamentals..."
})

// Switch back to real analyzeResume() once M1's backend is ready