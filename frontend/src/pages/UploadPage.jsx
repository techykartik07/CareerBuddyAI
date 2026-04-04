import { useState } from "react"
import { useNavigate } from "react-router-dom"
import DropZone from "../components/DropZone"
import { analyzeResume } from "../api/client"

export default function UploadPage() {
  const navigate = useNavigate()

  const [file, setFile] = useState(null)
  const [jd, setJd] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleAnalyze = async () => {
    if (!file) return setError("Please upload a resume PDF.")
    if (!jd.trim()) return setError("Please enter a job description.")

    setLoading(true)
    setError("")

    try {
      const result = await analyzeResume(file, jd)
      navigate("/results", { state: { result } })
    } catch (e) {
      setError(
        e.response?.data?.detail ||
          "Analysis failed. Check that the backend is running."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* 🔥 Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-white bg-opacity-90 flex flex-col items-center justify-center z-50">
          <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 font-medium">
            Analysing your resume...
          </p>
          <p className="text-gray-400 text-sm mt-1">
            AI is reviewing your profile
          </p>
        </div>
      )}

      {/* 🔷 Main UI */}
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-sm w-full max-w-lg">
          <h1 className="text-2xl font-bold text-purple-700 mb-1">
            CareerBuddy AI
          </h1>
          <p className="text-gray-400 text-sm mb-6">
            AI-powered career guidance
          </p>

          {/* 📂 File Upload */}
          <DropZone onFileSelect={setFile} selectedFile={file} />

          {/* 📝 Job Description */}
          <textarea
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste the job description here..."
            className="w-full mt-4 p-3 border border-gray-200 rounded-xl text-sm resize-none h-32 focus:outline-none focus:border-purple-400"
          />

          {/* ❌ Error */}
          {error && (
            <p className="text-red-500 text-sm mt-2">{error}</p>
          )}

          {/* 🚀 Button */}
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full mt-4 bg-purple-600 text-white py-3 rounded-xl font-medium hover:bg-purple-700 disabled:opacity-50"
          >
            Analyse My Resume →
          </button>
        </div>
      </div>
    </>
  )
}