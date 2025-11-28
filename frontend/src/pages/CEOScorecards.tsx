import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ceoScorecardsAPI } from '@/services/api'
import { Award, Plus, TrendingUp, Users, Target } from 'lucide-react'
import type { CEOScorecard } from '@/types'

export default function CEOScorecards() {
  const [selectedScorecard, setSelectedScorecard] = useState<string | null>(null)

  const { data: scorecards, isLoading } = useQuery({
    queryKey: ['ceoScorecards'],
    queryFn: ceoScorecardsAPI.list,
  })

  const { data: scorecardDetails } = useQuery({
    queryKey: ['ceoScorecard', selectedScorecard],
    queryFn: () => ceoScorecardsAPI.get(selectedScorecard!),
    enabled: !!selectedScorecard,
  })

  const { data: excellenceIndex } = useQuery({
    queryKey: ['excellenceIndex', selectedScorecard],
    queryFn: () => ceoScorecardsAPI.getExcellenceIndex(selectedScorecard!),
    enabled: !!selectedScorecard,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Award className="mr-3 text-primary-600" size={36} />
            CEO Scorecards
          </h1>
          <p className="text-gray-600 mt-2">
            Comprehensive executive performance assessment combining CEO Next Door + Power Score
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus size={20} className="mr-2" />
          New CEO Scorecard
        </button>
      </div>

      {/* Framework Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200">
          <div className="flex items-center mb-3">
            <TrendingUp className="text-blue-600 mr-3" size={28} />
            <h3 className="text-lg font-bold text-blue-900">4 CEO Behaviors</h3>
          </div>
          <ul className="space-y-1 text-sm text-blue-800">
            <li>• Decisiveness</li>
            <li>• Reliability</li>
            <li>• Bold Adaptation</li>
            <li>• Engaging for Impact</li>
          </ul>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200">
          <div className="flex items-center mb-3">
            <Users className="text-green-600 mr-3" size={28} />
            <h3 className="text-lg font-bold text-green-900">Power Score (P×W×R)</h3>
          </div>
          <ul className="space-y-1 text-sm text-green-800">
            <li>• Priorities (P)</li>
            <li>• Who (W)</li>
            <li>• Relationships (R)</li>
          </ul>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200">
          <div className="flex items-center mb-3">
            <Target className="text-purple-600 mr-3" size={28} />
            <h3 className="text-lg font-bold text-purple-900">Operating Metrics</h3>
          </div>
          <ul className="space-y-1 text-sm text-purple-800">
            <li>• Goals & Revenue</li>
            <li>• Strategy Execution</li>
            <li>• People & Culture</li>
          </ul>
        </div>
      </div>

      {/* Scorecards List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Your CEO Scorecards</h2>
          {scorecards && scorecards.length > 0 ? (
            <div className="space-y-4">
              {scorecards.map((scorecard) => (
                <ScorecardCard
                  key={scorecard.id}
                  scorecard={scorecard}
                  isSelected={selectedScorecard === scorecard.id}
                  onClick={() => setSelectedScorecard(scorecard.id)}
                />
              ))}
            </div>
          ) : (
            <div className="card text-center py-12">
              <Award className="mx-auto text-gray-400 mb-4" size={64} />
              <h3 className="text-lg font-semibold text-gray-700 mb-2">No CEO Scorecards Yet</h3>
              <p className="text-gray-600 mb-4">
                Create your first CEO scorecard to start tracking executive performance
              </p>
              <button className="btn btn-primary">Create First Scorecard</button>
            </div>
          )}
        </div>

        {/* Scorecard Details */}
        <div>
          {selectedScorecard && scorecardDetails ? (
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-4">Scorecard Details</h2>
              <div className="card">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{scorecardDetails.period}</h3>
                  <div className="flex items-center">
                    <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                      {scorecardDetails.status}
                    </span>
                  </div>
                </div>

                {excellenceIndex && (
                  <div className="mb-6">
                    <div className="text-center p-6 bg-gradient-to-br from-primary-50 to-primary-100 rounded-xl">
                      <div className="text-5xl font-bold text-primary-700 mb-2">
                        {excellenceIndex.excellence_index?.toFixed(1) || 'N/A'}
                      </div>
                      <div className="text-sm font-medium text-primary-600">CEO Excellence Index</div>
                    </div>
                  </div>
                )}

                <div className="space-y-4">
                  <ScoreItem label="Behavior Score" value={excellenceIndex?.behavior_score} max={10} />
                  <ScoreItem label="Power Score" value={excellenceIndex?.power_score} max={1000} />
                  <ScoreItem label="Operating Score" value={excellenceIndex?.operating_score} max={100} />
                </div>

                {excellenceIndex?.weakest_area && (
                  <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <h4 className="font-semibold text-yellow-900 mb-1">Focus Area</h4>
                    <p className="text-sm text-yellow-800">Weakest: {excellenceIndex.weakest_area}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="card text-center py-12">
              <Award className="mx-auto text-gray-300 mb-4" size={64} />
              <p className="text-gray-500">Select a scorecard to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

interface ScorecardCardProps {
  scorecard: CEOScorecard
  isSelected: boolean
  onClick: () => void
}

function ScorecardCard({ scorecard, isSelected, onClick }: ScorecardCardProps) {
  return (
    <div
      onClick={onClick}
      className={`card cursor-pointer transition-all ${
        isSelected ? 'ring-2 ring-primary-500 bg-primary-50' : 'hover:shadow-lg'
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-bold text-gray-900">{scorecard.period}</h3>
        {scorecard.ceo_excellence_index && (
          <div className="text-2xl font-bold text-primary-600">
            {scorecard.ceo_excellence_index.toFixed(1)}
          </div>
        )}
      </div>
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-600">
          {new Date(scorecard.created_at).toLocaleDateString()}
        </span>
        <span
          className={`px-2 py-1 rounded text-xs font-medium ${
            scorecard.status === 'finalized'
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
  )
}

interface ScoreItemProps {
  label: string
  value?: number
  max: number
}

function ScoreItem({ label, value, max }: ScoreItemProps) {
  const percentage = value ? (value / max) * 100 : 0

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-bold text-gray-900">{value?.toFixed(1) || 'N/A'}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-primary-600 h-2 rounded-full transition-all"
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
    </div>
  )
}
