import { useEffect, useState } from 'react';
import { ceoAssessmentsApi } from '../services/api';
import type { CEOAssessment } from '../types';

export default function CEOAssessments() {
  const [assessments, setAssessments] = useState<CEOAssessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const response = await ceoAssessmentsApi.list();
      setAssessments(response.data);
    } catch (error) {
      console.error('Error loading assessments:', error);
    } finally {
      setLoading(false);
    }
  };

  const behaviorLabels: Record<string, string> = {
    decisiveness: 'Decide with Speed & Conviction',
    reliability: 'Relentless Reliability',
    adaptation: 'Adapt Boldly',
    engagement: 'Engage for Impact',
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">CEO Behaviors Assessment</h1>
        <p className="mt-2 text-gray-600">
          Based on "The CEO Next Door" - Four key leadership behaviors
        </p>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">The Four CEO Behaviors</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(behaviorLabels).map(([key, label]) => (
            <div key={key} className="p-4 bg-gray-50 rounded-md">
              <h3 className="font-medium text-gray-900">{label}</h3>
              <p className="text-sm text-gray-600 mt-1">
                {key === 'decisiveness' && 'Make tough calls quickly with confidence'}
                {key === 'reliability' && 'Consistently deliver on commitments'}
                {key === 'adaptation' && 'Navigate change and ambiguity effectively'}
                {key === 'engagement' && 'Build strong stakeholder relationships'}
              </p>
            </div>
          ))}
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
                  <h3 className="text-lg font-semibold">
                    {assessment.assessment_type.toUpperCase()} Assessment
                  </h3>
                  <p className="text-sm text-gray-600">
                    {new Date(assessment.assessment_date).toLocaleDateString()}
                  </p>
                  {assessment.assessor_name && (
                    <p className="text-sm text-gray-600">
                      Assessor: {assessment.assessor_name}
                    </p>
                  )}
                </div>
                {assessment.overall_score && (
                  <div className="text-right">
                    <div className="text-2xl font-bold text-primary-600">
                      {assessment.overall_score.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">out of 5.0</div>
                  </div>
                )}
              </div>
              <div className="grid grid-cols-2 gap-3">
                {assessment.behavior_ratings.map((rating) => (
                  <div key={rating.behavior} className="p-3 bg-gray-50 rounded">
                    <div className="text-sm font-medium text-gray-700">
                      {behaviorLabels[rating.behavior]}
                    </div>
                    <div className="text-lg font-bold text-primary-600">
                      {rating.score}/5
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
          {assessments.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-500">No CEO assessments yet.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
