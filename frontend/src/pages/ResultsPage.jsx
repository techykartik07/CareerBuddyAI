import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
 
export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Chat state
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [showChat, setShowChat] = useState(false);
 
  useEffect(() => {
    // Get data from navigation state (passed from UploadPage)
    const analysisData = location.state?.analysisResult;
    
    if (analysisData) {
      setData(analysisData);
      setLoading(false);
      
      // Add initial AI greeting message
      setMessages([{
        role: 'assistant',
        content: `Hi! I've analyzed your resume and job match. I can help you with:
 
• Understanding your skill gaps
• Creating a study plan for missing skills
• Advice on improving your ATS score
• Career guidance and next steps
 
What would you like to know?`,
        timestamp: new Date().toISOString()
      }]);
    } else {
      // No data - redirect back to upload
      navigate('/');
    }
  }, [location, navigate]);
 
  const sendChatMessage = async () => {
    if (!chatInput.trim() || chatLoading) return;
 
    const userMessage = {
      role: 'user',
      content: chatInput,
      timestamp: new Date().toISOString()
    };
 
    setMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);
 
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const response = await axios.post(`${API_URL}/ai/chat`, {
        message: chatInput,
        context: {
          ats_score: data.ats?.ats_score,
          job_match: data.match?.match_percentage,
          skill_gaps: data.skill_gap,
          roadmap: data.roadmap
        }
      });
 
      const aiMessage = {
        role: 'assistant',
        content: response.data.reply,
        timestamp: new Date().toISOString()
      };
 
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
    }
  };
 
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-center">
          <div className="relative w-24 h-24 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-purple-500/30 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-transparent border-t-purple-500 rounded-full animate-spin"></div>
          </div>
          <p className="text-xl text-purple-200 font-medium">Analyzing your resume...</p>
          <p className="text-sm text-purple-400 mt-2">This may take a few moments</p>
        </div>
      </div>
    );
  }
 
  if (!data) return null;
 
  const getScoreColor = (score) => {
    if (score >= 75) return 'from-green-500 to-emerald-600';
    if (score >= 50) return 'from-yellow-500 to-orange-600';
    return 'from-red-500 to-rose-600';
  };
 
  const getVerdictConfig = (score) => {
    if (score >= 75) return {
      icon: '✓',
      title: 'Strong Resume',
      desc: 'Your resume is well-optimized for ATS systems and matches the job requirements.',
      gradient: 'from-green-500/20 to-emerald-500/20',
      border: 'border-green-500',
      text: 'text-green-400'
    };
    if (score >= 50) return {
      icon: '⚠',
      title: 'Needs Improvement',
      desc: 'Your resume has potential but needs keyword optimization and skill enhancement.',
      gradient: 'from-yellow-500/20 to-orange-500/20',
      border: 'border-yellow-500',
      text: 'text-yellow-400'
    };
    return {
      icon: '✗',
      title: 'Significant Gaps',
      desc: 'Your resume needs major improvements to pass ATS screening and match job requirements.',
      gradient: 'from-red-500/20 to-rose-500/20',
      border: 'border-red-500',
      text: 'text-red-400'
    };
  };
 
  const verdict = getVerdictConfig(data.ats?.ats_score || 0);
 
  // Parse roadmap into structured weeks
  const parseRoadmap = (roadmapText) => {
    const weeks = [];
    const lines = roadmapText.split('\n');
    let currentWeek = null;
 
    lines.forEach(line => {
      const weekMatch = line.match(/##\s+(Week\s+\d+-?\d*):?\s+(.+)/i);
      if (weekMatch) {
        if (currentWeek) weeks.push(currentWeek);
        currentWeek = {
          period: weekMatch[1],
          title: weekMatch[2].replace(/\*\*/g, '').trim(),
          items: []
        };
      } else if (currentWeek && line.trim().startsWith('-')) {
        const item = line.replace(/^-\s*/, '').replace(/\*\*/g, '').trim();
        if (item) currentWeek.items.push(item);
      }
    });
    if (currentWeek) weeks.push(currentWeek);
    return weeks;
  };
 
  const roadmapWeeks = parseRoadmap(data.roadmap);
 
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-8">
          <button 
            onClick={() => navigate('/')}
            className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-2 mb-4"
          >
            <span>←</span> Back to Upload
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">Analysis Results</h1>
          <p className="text-purple-300">Your personalized career development insights</p>
        </div>
 
        {/* Verdict Banner */}
        <div className={`mb-8 p-6 rounded-2xl border-2 ${verdict.border} bg-gradient-to-r ${verdict.gradient} backdrop-blur-sm`}>
          <div className="flex items-start gap-4">
            <div className={`text-4xl ${verdict.text}`}>{verdict.icon}</div>
            <div className="flex-1">
              <h2 className={`text-2xl font-bold ${verdict.text} mb-2`}>{verdict.title}</h2>
              <p className="text-gray-300 text-lg">{verdict.desc}</p>
            </div>
          </div>
        </div>
 
        {/* Scores Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* ATS Score Card */}
          <div className="bg-gray-800/50 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-8 hover:border-purple-500/50 transition-all">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-purple-300">ATS Compatibility</h2>
              <svg className="w-8 h-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className={`text-7xl font-black bg-gradient-to-r ${getScoreColor(data.ats?.ats_score || 0)} bg-clip-text text-transparent mb-3`}>
              {data.ats?.ats_score || 0}%
            </div>
            <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className={`h-full bg-gradient-to-r ${getScoreColor(data.ats?.ats_score || 0)} transition-all duration-1000`}
                style={{ width: `${data.ats?.ats_score || 0}%` }}
              ></div>
            </div>
            <p className="text-gray-400 mt-3 text-sm">
              {(data.ats?.ats_score || 0) >= 75 ? 'Excellent - Your resume will pass most ATS filters' : 
               (data.ats?.ats_score || 0) >= 50 ? 'Moderate - Some improvements needed' : 
               'Low - Significant optimization required'}
            </p>
          </div>
 
          {/* Job Match Card */}
          <div className="bg-gray-800/50 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-8 hover:border-blue-500/50 transition-all">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-blue-300">Job Match Score</h2>
              <svg className="w-8 h-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div className={`text-7xl font-black bg-gradient-to-r ${getScoreColor(data.match?.match_percentage || 0)} bg-clip-text text-transparent mb-3`}>
              {data.match?.match_percentage || 0}%
            </div>
            <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className={`h-full bg-gradient-to-r ${getScoreColor(data.match?.match_percentage || 0)} transition-all duration-1000`}
                style={{ width: `${data.match?.match_percentage || 0}%` }}
              ></div>
            </div>
            <p className="text-gray-400 mt-3 text-sm">
              {(data.match?.match_percentage || 0) >= 75 ? 'Strong fit for this position' : 
               (data.match?.match_percentage || 0) >= 50 ? 'Moderate fit with some gaps' : 
               'Significant skill development needed'}
            </p>
          </div>
        </div>
 
        {/* Missing Keywords Section */}
        {data.ats.missing_keywords?.length > 0 && (
          <div className="bg-gradient-to-r from-amber-900/30 to-orange-900/30 border-2 border-amber-500/50 rounded-2xl p-8 mb-8 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-4">
              <svg className="w-8 h-8 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <h2 className="text-2xl font-bold text-amber-300">Resume Improvement Tips</h2>
            </div>
            <p className="text-amber-200 mb-5 text-lg">
              Add these keywords to boost your ATS compatibility:
            </p>
            <div className="flex flex-wrap gap-3">
              {data.ats.missing_keywords.map((kw, idx) => (
                <span 
                  key={idx}
                  className="px-5 py-2.5 bg-amber-500/20 border border-amber-400/40 text-amber-200 rounded-xl text-base font-semibold hover:bg-amber-500/30 hover:border-amber-400/60 transition-all cursor-default"
                >
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}
 
        {/* Skill Gaps */}
        <div className="bg-gray-800/50 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <svg className="w-8 h-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <h2 className="text-2xl font-bold text-white">Critical Skill Gaps</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(data.skill_gap?.missing_skills || []).map((skill, idx) => (
              <div 
                key={idx} 
                className="bg-gray-900/50 border border-gray-700 rounded-xl p-5 hover:border-purple-500/50 transition-all group"
              >
                <div className="flex items-start gap-3 mb-2">
                  <span className="px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider bg-red-500/20 text-red-300 border border-red-500/40">
                    High
                  </span>
                  <h3 className="font-bold text-white text-lg flex-1 group-hover:text-purple-300 transition-colors">
                    {skill}
                  </h3>
                </div>
                <p className="text-gray-400 text-sm leading-relaxed ml-0">
                  This skill was identified as missing based on the job requirements.
                </p>
              </div>
            ))}
          </div>
        </div>
 
        {/* AI CHAT PANEL - NEW SECTION */}
        <div className="bg-gray-800/50 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <svg className="w-8 h-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <h2 className="text-2xl font-bold text-white">AI Career Assistant</h2>
            </div>
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all text-sm font-medium"
            >
              {showChat ? 'Hide Chat' : 'Show Chat'}
            </button>
          </div>
 
          {showChat && (
            <>
              {/* Chat Messages */}
              <div className="bg-gray-900/50 rounded-xl p-4 mb-4 h-96 overflow-y-auto space-y-4">
                {messages.map((msg, idx) => (
                  <div 
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[80%] rounded-xl p-4 ${
                      msg.role === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-700 text-gray-100'
                    }`}>
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                      <p className="text-xs mt-2 opacity-70">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-700 rounded-xl p-4">
                      <div className="flex gap-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
 
              {/* Chat Input */}
              <div className="flex gap-3">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                  placeholder="Ask me anything about your career path..."
                  className="flex-1 px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  disabled={chatLoading}
                />
                <button
                  onClick={sendChatMessage}
                  disabled={!chatInput.trim() || chatLoading}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl transition-all font-medium flex items-center gap-2"
                >
                  <span>Send</span>
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>
              </div>
 
              {/* Suggested Questions */}
              <div className="mt-4 flex flex-wrap gap-2">
                <p className="w-full text-sm text-gray-400 mb-1">Suggested questions:</p>
                {[
                  "What should I focus on first?",
                  "How can I improve my ATS score?",
                  "Explain my skill gaps",
                  "Best resources for learning Docker?"
                ].map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => setChatInput(suggestion)}
                    className="px-3 py-1.5 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 text-gray-300 rounded-lg text-xs transition-all"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
 
        {/* Career Roadmap - Flowchart Style */}
        <div className="bg-gray-800/50 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-8">
          <div className="flex items-center gap-3 mb-8">
            <svg className="w-8 h-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            <h2 className="text-2xl font-bold text-white">Your Career Roadmap</h2>
          </div>
 
          {/* Roadmap Timeline */}
          <div className="relative">
            {/* Vertical Line */}
            <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-blue-500 to-green-500"></div>
            
            <div className="space-y-8">
              {roadmapWeeks.map((week, idx) => (
                <div key={idx} className="relative pl-16">
                  {/* Timeline Node */}
                  <div className="absolute left-0 top-0 w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 border-4 border-gray-900 flex items-center justify-center">
                    <span className="text-white font-bold text-sm">{idx + 1}</span>
                  </div>
                  
                  {/* Week Card */}
                  <div className="bg-gray-900/70 border-2 border-purple-500/30 rounded-xl p-6 hover:border-purple-500/60 transition-all group">
                    <div className="mb-4">
                      <span className="text-purple-400 text-sm font-semibold uppercase tracking-wider">
                        {week.period}
                      </span>
                      <h3 className="text-xl font-bold text-white mt-1 group-hover:text-purple-300 transition-colors">
                        {week.title}
                      </h3>
                    </div>
                    
                    <ul className="space-y-2">
                      {week.items.map((item, itemIdx) => (
                        <li key={itemIdx} className="flex items-start gap-3 text-gray-300">
                          <svg className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          <span className="leading-relaxed">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
 
                  {/* Connector Line to Next */}
                  {idx < roadmapWeeks.length - 1 && (
                    <div className="absolute left-6 -bottom-4 w-0.5 h-8 bg-gradient-to-b from-transparent via-purple-500 to-transparent"></div>
                  )}
                </div>
              ))}
            </div>
          </div>
 
          {/* Success Message */}
          <div className="mt-10 p-6 bg-gradient-to-r from-green-900/30 to-emerald-900/30 border-2 border-green-500/50 rounded-xl">
            <div className="flex items-center gap-3">
              <svg className="w-8 h-8 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
              <div>
                <h4 className="text-green-300 font-bold text-lg">You've Got This! 🚀</h4>
                <p className="text-green-200 text-sm mt-1">
                  Follow this roadmap consistently, build projects, and you'll be ready for the role in {roadmapWeeks.length} weeks.
                </p>
              </div>
            </div>
          </div>
        </div>
 
        {/* Action Buttons */}
        <div className="mt-8 flex gap-4 justify-center">
          <button 
            onClick={() => navigate('/')}
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-semibold rounded-xl transition-all transform hover:scale-105 shadow-lg shadow-purple-500/50"
          >
            Analyze Another Resume
          </button>
          {/* <button 
            onClick={() => window.print()}
            className="px-8 py-4 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all border border-gray-600"
          >
            Print / Save PDF
          </button> */}
        </div>
 
      </div>
    </div>
  );
}