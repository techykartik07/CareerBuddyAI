import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'https://careerbuddyai-wof2.onrender.com'

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