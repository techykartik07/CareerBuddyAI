export default function SkillGapList({ present = [], missing = [] }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm">
      <h2 className="font-semibold text-gray-800 mb-4">Skill Analysis</h2>
      <div className="mb-4">
        <p className="text-xs font-medium text-gray-400 uppercase mb-2">You have</p>
        <div className="flex flex-wrap gap-2">
          {present.map(s => (
            <span key={s} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
              {s}
            </span>
          ))}
        </div>
      </div>
      <div>
        <p className="text-xs font-medium text-gray-400 uppercase mb-2">Missing skills</p>
        <div className="flex flex-wrap gap-2">
          {missing.map(s => (
            <span key={s} className="px-3 py-1 bg-red-100 text-red-600 rounded-full text-xs font-medium">
              + {s}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}