import { useQuery } from '@tanstack/react-query'
import { scorecardsAPI } from '@/services/api'
import { FileText, Plus } from 'lucide-react'

export default function Scorecards() {
  const { data: scorecards, isLoading } = useQuery({
    queryKey: ['scorecards'],
    queryFn: scorecardsAPI.list,
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <FileText className="mr-3 text-primary-600" size={36} />
            A-Method Scorecards
          </h1>
          <p className="text-gray-600 mt-2">
            Define role mission, outcomes, and competencies using the Who: A Method framework
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus size={20} className="mr-2" />
          New Scorecard
        </button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      ) : scorecards && scorecards.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {scorecards.map((scorecard) => (
            <div key={scorecard.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <h3 className="text-xl font-bold text-gray-900 mb-2">{scorecard.role_title}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{scorecard.role_mission}</p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">
                  {new Date(scorecard.created_at).toLocaleDateString()}
                </span>
                <span
                  className={`px-2 py-1 rounded ${
                    scorecard.status === 'active'
                      ? 'bg-green-100 text-green-700'
                      : scorecard.status === 'draft'
                      ? 'bg-gray-100 text-gray-700'
                      : 'bg-yellow-100 text-yellow-700'
                  }`}
                >
                  {scorecard.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <FileText className="mx-auto text-gray-400 mb-4" size={64} />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Scorecards Yet</h3>
          <p className="text-gray-600 mb-4">Create your first A-Method scorecard to get started</p>
          <button className="btn btn-primary">Create First Scorecard</button>
        </div>
      )}
    </div>
  )
}
