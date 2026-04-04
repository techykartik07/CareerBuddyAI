import { useLocation, useNavigate } from 'react-router-dom'
import ScoreGauge    from '../components/ScoreGauge'
import SkillGapList  from '../components/SkillGapList'
import ChatPanel     from '../components/ChatPanel'
import ReactMarkdown from 'react-markdown'

export default function ResultsPage() {
  const { state }  = useLocation()
  const navigate   = useNavigate()
  const result     = state?.result

  if (!result) {
    navigate('/')
    return null
  }

  const { contact, ats, match, skill_gap, roadmap } = result
  const chatContext = { ...ats, ...match, missing_skills: skill_gap.missing_skills }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-xl font-bold text-purple-700">CareerBuddy AI Results</h1>
            {contact?.name && <p className="text-gray-400 text-sm">{contact.name}</p>}
          </div>
          <button onClick={() => navigate('/')}
            className="text-sm text-purple-600 hover:underline">
            ← Analyse another resume
          </button>
        </div>

        {/* Score Cards */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <ScoreGauge score={ats.ats_score}          label="ATS Compatibility"   color="#7F77DD" />
          <ScoreGauge score={match.match_percentage} label="Job Match"            color="#1D9E75" />
        </div>

        {/* Skill Gap */}
        <div className="mb-6">
          <SkillGapList present={skill_gap.present_skills} missing={skill_gap.missing_skills} />
        </div>

        {/* Roadmap */}
        <div className="bg-white rounded-2xl p-6 shadow-sm mb-6">
          <h2 className="font-semibold text-gray-800 mb-4">Your Career Roadmap</h2>
          <div className="prose prose-sm max-w-none text-gray-600">
            <ReactMarkdown>{roadmap}</ReactMarkdown>
          </div>
        </div>

        {/* AI Chat */}
        <ChatPanel context={chatContext} />
      </div>
    </div>
  )
}