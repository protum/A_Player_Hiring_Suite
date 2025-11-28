import { useQuery } from '@tanstack/react-query'
import { interviewsAPI } from '@/services/api'
import { Users, Plus } from 'lucide-react'

export default function Interviews() {
  const { data: interviews, isLoading } = useQuery({
    queryKey: ['interviews'],
    queryFn: interviewsAPI.list,
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Users className="mr-3 text-primary-600" size={36} />
            Topgrading Interviews
          </h1>
          <p className="text-gray-600 mt-2">
            Chronological in-depth structured interviews with TORC methodology
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus size={20} className="mr-2" />
          New Interview
        </button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading...</div>
        </div>
      ) : interviews && interviews.length > 0 ? (
        <div className="space-y-4">
          {interviews.map((interview) => (
            <div key={interview.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{interview.candidate_name}</h3>
                  {interview.candidate_email && (
                    <p className="text-gray-600 text-sm">{interview.candidate_email}</p>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-primary-600 mb-1">
                    {interview.cqi_score || 'N/A'}
                  </div>
                  <div className="text-xs text-gray-500">CQI Score</div>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span
                  className={`px-3 py-1 rounded text-sm font-medium ${
                    interview.status === 'completed'
                      ? 'bg-green-100 text-green-700'
                      : interview.status === 'in_progress'
                      ? 'bg-blue-100 text-blue-700'
                      : interview.status === 'scheduled'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {interview.status}
                </span>
                {interview.recommendation && (
                  <span className="text-sm text-gray-600">
                    Recommendation: <span className="font-medium">{interview.recommendation}</span>
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <Users className="mx-auto text-gray-400 mb-4" size={64} />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Interviews Yet</h3>
          <p className="text-gray-600 mb-4">Schedule your first Topgrading interview</p>
          <button className="btn btn-primary">Create First Interview</button>
        </div>
      )}
    </div>
  )
}
