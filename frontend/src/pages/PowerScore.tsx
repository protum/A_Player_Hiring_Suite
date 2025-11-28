import { useEffect, useState } from 'react';
import { powerScoreApi } from '../services/api';
import type { PowerScoreAssessment } from '../types';

export default function PowerScore() {
  const [assessments, setAssessments] = useState<PowerScoreAssessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const response = await powerScoreApi.list();
      setAssessments(response.data);
    } catch (error) {
      console.error('Error loading assessments:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRatingLabel = (score: number) => {
    if (score >= 85) return 'Exceptional';
    if (score >= 70) return 'Strong';
    if (score >= 50) return 'Adequate';
    if (score >= 30) return 'Needs Development';
    return 'Critical Gap';
  };

  const getRatingColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 50) return 'text-yellow-600';
    if (score >= 30) return 'text-orange-600';
    return 'text-red-600';
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Power Score Assessment</h1>
        <p className="mt-2 text-gray-600">
          Leadership effectiveness across Results, Relationships, and Role Model
        </p>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Power Score Dimensions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 rounded-md">
            <h3 className="font-medium text-blue-900">Results</h3>
            <p className="text-sm text-blue-700 mt-1">Business outcomes delivered</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-md">
            <h3 className="font-medium text-purple-900">Relationships</h3>
            <p className="text-sm text-purple-700 mt-1">Team and stakeholder trust</p>
          </div>
          <div className="p-4 bg-green-50 rounded-md">
            <h3 className="font-medium text-green-900">Role Model</h3>
            <p className="text-sm text-green-700 mt-1">Values and integrity</p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {assessments.map((assessment) => (
            <div key={assessment.id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">Power Score Assessment</h3>
                  <p className="text-sm text-gray-600">
                    {new Date(assessment.assessment_date).toLocaleDateString()}
                  </p>
                </div>
                <div className="text-right">
                  <div className={`text-3xl font-bold ${getRatingColor(assessment.overall_power_score)}`}>
                    {assessment.overall_power_score.toFixed(1)}
                  </div>
                  <div className="text-sm font-medium text-gray-500">
                    {getRatingLabel(assessment.overall_power_score)}
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-3 bg-blue-50 rounded">
                  <div className="text-sm font-medium text-gray-700">Results</div>
                  <div className={`text-xl font-bold ${getRatingColor(assessment.results_score)}`}>
                    {assessment.results_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-purple-50 rounded">
                  <div className="text-sm font-medium text-gray-700">Relationships</div>
                  <div className={`text-xl font-bold ${getRatingColor(assessment.relationships_score)}`}>
                    {assessment.relationships_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-green-50 rounded">
                  <div className="text-sm font-medium text-gray-700">Role Model</div>
                  <div className={`text-xl font-bold ${getRatingColor(assessment.role_model_score)}`}>
                    {assessment.role_model_score.toFixed(1)}
                  </div>
                </div>
              </div>
              {assessment.development_plans.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Development Plans ({assessment.development_plans.length})
                  </h4>
                  {assessment.development_plans.slice(0, 2).map((plan, idx) => (
                    <div key={idx} className="text-sm text-gray-600 mb-1">
                      • {plan.goal}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
          {assessments.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-500">No Power Score assessments yet.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
