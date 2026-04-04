import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'

export default function ScoreGauge({ score, label, color }) {
  const data = [{ value: score, fill: color }]
  const scoreColor = score >= 70 ? '#16a34a' : score >= 40 ? '#d97706' : '#dc2626'

  return (
    <div className="flex flex-col items-center bg-white rounded-2xl p-6 shadow-sm">
      <div className="relative">
        <RadialBarChart width={140} height={140} innerRadius={50} outerRadius={70}
          data={data} startAngle={90} endAngle={-270}>
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar background dataKey="value" cornerRadius={10} />
        </RadialBarChart>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold" style={{ color: scoreColor }}>
            {score}%
          </span>
        </div>
      </div>
      <p className="text-gray-600 font-medium mt-2 text-sm">{label}</p>
      <p className="text-xs mt-1"
        style={{ color: scoreColor }}>
        {score >= 70 ? 'Good' : score >= 40 ? 'Needs work' : 'Poor'}
      </p>
    </div>
  )
}