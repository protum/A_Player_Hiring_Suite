import { useQuery } from '@tanstack/react-query'
import { leadershipAPI } from '@/services/api'
import { TrendingUp, Plus } from 'lucide-react'

export default function LeadershipAssessments() {
  const { data: assessments, isLoading } = useQuery({
    queryKey: ['leadershipAssessments'],
    queryFn: leadershipAPI.list,
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <TrendingUp className="mr-3 text-primary-600" size={36} />
            Leadership Assessments
          </h1>
          <p className="text-gray-600 mt-2">
            360-degree assessment of the 4 CEO behaviors from The CEO Next Door
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus size={20} className="mr-2" />
          New Assessment
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="card bg-blue-50 border-2 border-blue-200">
          <h3 className="font-bold text-blue-900 mb-3">The 4 CEO Behaviors</h3>
          <div className="grid grid-cols-2 gap-3 text-sm text-blue-800">
            <div>
              <div className="font-semibold mb-1">1. Decisiveness</div>
              <div className="text-xs">Speed, quality, cutting losses</div>
            </div>
            <div>
              <div className="font-semibold mb-1">2. Reliability</div>
              <div className="text-xs">Predictability, commitments</div>
            </div>
            <div>
              <div className="font-semibold mb-1">3. Bold Adaptation</div>
              <div className="text-xs">Pivoting, inflection points</div>
            </div>
            <div>
              <div className="font-semibold mb-1">4. Engaging for Impact</div>
              <div className="text-xs">Influence, alignment, vision</div>
            </div>
          </div>
        </div>

        <div className="card bg-green-50 border-2 border-green-200">
          <h3 className="font-bold text-green-900 mb-3">Assessment Features</h3>
          <ul className="space-y-2 text-sm text-green-800">
            <li>✓ 360-degree feedback from multiple raters</li>
            <li>✓ Evidence-based behavior capture</li>
            <li>✓ Individual development plans</li>
            <li>✓ Executive dashboards</li>
          </ul>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      ) : assessments && assessments.length > 0 ? (
        <div className="space-y-4">
          {assessments.map((assessment) => (
            <div key={assessment.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">{assessment.assessment_period}</h3>
                <span
                  className={`px-3 py-1 rounded text-sm font-medium ${
                    assessment.status === 'completed'
                      ? 'bg-green-100 text-green-700'
                      : assessment.status === 'in_progress'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {assessment.status}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <ScoreBadge
                  label="Decisiveness"
                  score={assessment.decisiveness_score}
                  color="blue"
                />
                <ScoreBadge
                  label="Reliability"
                  score={assessment.reliability_score}
                  color="green"
                />
                <ScoreBadge
                  label="Bold Adaptation"
                  score={assessment.bold_adaptation_score}
                  color="purple"
                />
                <ScoreBadge
                  label="Engaging Impact"
                  score={assessment.engaging_impact_score}
                  color="orange"
                />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <TrendingUp className="mx-auto text-gray-400 mb-4" size={64} />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Assessments Yet</h3>
          <p className="text-gray-600 mb-4">Create your first leadership assessment</p>
          <button className="btn btn-primary">Create First Assessment</button>
        </div>
      )}
    </div>
  )
}

function ScoreBadge({ label, score, color }: { label: string; score?: number; color: string }) {
  return (
    <div className={`p-3 rounded-lg bg-${color}-50 border border-${color}-200`}>
      <div className="text-xs text-gray-600 mb-1">{label}</div>
      <div className={`text-2xl font-bold text-${color}-700`}>{score?.toFixed(1) || 'N/A'}</div>
    </div>
  )
}
