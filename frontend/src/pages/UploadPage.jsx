// src/pages/UploadPage.jsx
const BASE_URL = import.meta.env.VITE_API_URL;
import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        setError('');
      }
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a resume PDF');
      return;
    }
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('jd_text', jobDescription);

      const API_URL = import.meta.env.VITE_API_URL || 'BASE_URL';
      
      const response = await axios.post(`${API_URL}/resume/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Navigate to results page with data
      navigate('/results', { 
        state: { analysisResult: response.data } 
      });
      
    } catch (err) {
      console.error('Analysis failed:', err);
      setError(
        err.response?.data?.error || 
        'Analysis failed. Please check that the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-12 pt-8">
          <div className="inline-block mb-6">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center transform rotate-6 shadow-2xl shadow-purple-500/50">
              <svg className="w-12 h-12 text-white transform -rotate-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
          <h1 className="text-5xl font-black text-white mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            CareerBuddy AI
          </h1>
          <p className="text-xl text-purple-200 font-medium">
            AI-powered career guidance that gets you hired
          </p>
          <p className="text-purple-400 mt-2">
            Upload your resume and job description for personalized insights
          </p>
        </div>

        {/* Main Form Card */}
        <div className="bg-gray-800/50 backdrop-blur-xl border border-purple-500/30 rounded-3xl p-8 md:p-12 shadow-2xl">
          
          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-900/30 border-2 border-red-500/50 rounded-xl flex items-start gap-3">
              <svg className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-200 font-medium">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            
            {/* File Upload Section */}
            <div>
              <label className="block text-purple-300 font-semibold mb-3 text-lg">
                📄 Upload Your Resume
              </label>
              <div
                {...getRootProps()}
                className={`border-3 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
                  isDragActive
                    ? 'border-purple-400 bg-purple-900/30 scale-105'
                    : file
                    ? 'border-green-500 bg-green-900/20'
                    : 'border-purple-500/50 bg-gray-900/30 hover:border-purple-400 hover:bg-purple-900/20'
                }`}
              >
                <input {...getInputProps()} />
                
                {file ? (
                  <div className="space-y-3">
                    <svg className="w-16 h-16 text-green-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p className="text-green-300 font-semibold text-xl">{file.name}</p>
                    <p className="text-green-400 text-sm">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        setFile(null);
                      }}
                      className="mt-3 text-sm text-purple-400 hover:text-purple-300 underline"
                    >
                      Remove and upload a different file
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <svg className="w-16 h-16 text-purple-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-purple-200 font-semibold text-lg">
                      {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
                    </p>
                    <p className="text-purple-400 text-sm">or click to browse</p>
                    <p className="text-purple-500 text-xs">PDF format, max 10MB</p>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description Section */}
            <div>
              <label className="block text-purple-300 font-semibold mb-3 text-lg">
                💼 Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the complete job description here...

Example:
We're looking for a Senior Software Engineer with 5+ years of experience in React, Node.js, and cloud platforms (AWS/Azure). You'll lead frontend architecture decisions and mentor junior developers..."
                className="w-full h-64 px-6 py-4 bg-gray-900/50 border-2 border-purple-500/30 rounded-2xl text-white placeholder-purple-500/50 focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all resize-none text-base leading-relaxed"
              />
              <p className="mt-2 text-purple-400 text-sm">
                💡 Tip: Include the full job posting with requirements, responsibilities, and qualifications for best results
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !file || !jobDescription.trim()}
              className={`w-full py-5 rounded-2xl font-bold text-lg transition-all transform shadow-xl ${
                loading || !file || !jobDescription.trim()
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white hover:scale-105 shadow-purple-500/50 hover:shadow-2xl'
              }`}
            >
              {loading ? (
                <div className="flex items-center justify-center gap-3">
                  <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Analyzing Resume...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center gap-3">
                  <span>Analyze My Resume</span>
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </div>
              )}
            </button>
          </form>

          {/* Features List */}
          <div className="mt-10 pt-8 border-t border-purple-500/20">
            <p className="text-purple-300 font-semibold mb-4 text-center">What you'll get:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="text-white font-medium">ATS Compatibility Score</p>
                  <p className="text-purple-400 text-sm">See if your resume passes screening</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="text-white font-medium">Job Match Analysis</p>
                  <p className="text-purple-400 text-sm">How well you fit the role</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="text-white font-medium">Skill Gap Report</p>
                  <p className="text-purple-400 text-sm">What skills you're missing</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="text-white font-medium">Personalized Roadmap</p>
                  <p className="text-purple-400 text-sm">Week-by-week learning path</p>
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <p className="text-center text-purple-400 mt-8 text-sm">
          QUANT 4 • Hacksagon 2026
        </p>
      </div>
    </div>
  );
}