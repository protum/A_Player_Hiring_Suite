import { useQuery } from '@tanstack/react-query'
import { powerScoresAPI } from '@/services/api'
import { BarChart, Plus } from 'lucide-react'

export default function PowerScores() {
  const { data: powerScores, isLoading } = useQuery({
    queryKey: ['powerScores'],
    queryFn: powerScoresAPI.list,
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <BarChart className="mr-3 text-primary-600" size={36} />
            Power Scores
          </h1>
          <p className="text-gray-600 mt-2">
            Executive effectiveness assessment: Power Score = P × W × R
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus size={20} className="mr-2" />
          New Power Score
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card bg-purple-50 border-2 border-purple-200">
          <h3 className="font-bold text-purple-900 mb-3">P - Priorities</h3>
          <ul className="space-y-1 text-sm text-purple-800">
            <li>• Clarity of priorities</li>
            <li>• Focus maintenance</li>
            <li>• Team alignment</li>
            <li>• Resource consistency</li>
          </ul>
        </div>

        <div className="card bg-blue-50 border-2 border-blue-200">
          <h3 className="font-bold text-blue-900 mb-3">W - Who</h3>
          <ul className="space-y-1 text-sm text-blue-800">
            <li>• Bench strength</li>
            <li>• A-player ratio</li>
            <li>• Team gaps</li>
            <li>• Delegation efficiency</li>
          </ul>
        </div>

        <div className="card bg-green-50 border-2 border-green-200">
          <h3 className="font-bold text-green-900 mb-3">R - Relationships</h3>
          <ul className="space-y-1 text-sm text-green-800">
            <li>• Board alignment</li>
            <li>• Cross-team collaboration</li>
            <li>• Market trust</li>
            <li>• Culture health</li>
          </ul>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      ) : powerScores && powerScores.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {powerScores.map((powerScore) => (
            <div
              key={powerScore.id}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="mb-4">
                <div className="text-3xl font-bold text-primary-600 mb-1">
                  {powerScore.total_power_score?.toFixed(1) || 'N/A'}
                </div>
                <div className="text-sm text-gray-600">
                  {new Date(powerScore.assessment_date).toLocaleDateString()}
                </div>
              </div>

              <div className="space-y-3">
                <DimensionBar
                  label="Priorities (P)"
                  score={powerScore.priorities_score}
                  color="purple"
                />
                <DimensionBar label="Who (W)" score={powerScore.who_score} color="blue" />
                <DimensionBar
                  label="Relationships (R)"
                  score={powerScore.relationships_score}
                  color="green"
                />
              </div>

              {powerScore.weakest_dimension && (
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
                  <div className="text-xs font-medium text-yellow-900 mb-1">Weakest Link</div>
                  <div className="text-sm text-yellow-800">{powerScore.weakest_dimension}</div>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <BarChart className="mx-auto text-gray-400 mb-4" size={64} />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Power Scores Yet</h3>
          <p className="text-gray-600 mb-4">Create your first Power Score assessment</p>
          <button className="btn btn-primary">Create First Assessment</button>
        </div>
      )}
    </div>
  )
}

function DimensionBar({ label, score, color }: { label: string; score?: number; color: string }) {
  const percentage = score ? (score / 10) * 100 : 0

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-gray-600">{label}</span>
        <span className="text-sm font-bold text-gray-900">{score?.toFixed(1) || 'N/A'}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`bg-${color}-600 h-2 rounded-full transition-all`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
    </div>
  )
}
