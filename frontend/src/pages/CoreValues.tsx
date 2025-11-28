import { useEffect, useState } from 'react';
import { coreValuesApi } from '../services/api';
import type { CoreValuesAssessment } from '../types';
import { DocumentArrowDownIcon } from '@heroicons/react/24/outline';

export default function CoreValues() {
  const [assessments, setAssessments] = useState<CoreValuesAssessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const response = await coreValuesApi.list();
      setAssessments(response.data);
    } catch (error) {
      console.error('Error loading assessments:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAlignmentColor = (level?: string) => {
    const colors: Record<string, string> = {
      strong_fit: 'bg-green-100 text-green-800',
      good_fit: 'bg-blue-100 text-blue-800',
      partial_fit: 'bg-yellow-100 text-yellow-800',
      poor_fit: 'bg-red-100 text-red-800',
    };
    return colors[level || ''] || 'bg-gray-100 text-gray-800';
  };

  const getAlignmentLabel = (level?: string) => {
    const labels: Record<string, string> = {
      strong_fit: 'Strong Cultural Fit',
      good_fit: 'Good Cultural Fit',
      partial_fit: 'Partial Cultural Fit',
      poor_fit: 'Poor Cultural Fit',
    };
    return labels[level || ''] || 'Unknown';
  };

  const getRatingColor = (score: number) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 50) return 'text-yellow-600';
    if (score >= 30) return 'text-orange-600';
    return 'text-red-600';
  };

  const handleExportPdf = async (id: string) => {
    try {
      const response = await coreValuesApi.exportPdf(id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `core_values_${id}.pdf`;
      a.click();
    } catch (error) {
      console.error('Error exporting PDF:', error);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Core Values Assessment</h1>
        <p className="mt-2 text-gray-600">
          Evaluate cultural fit based on organizational core values
        </p>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Our Five Core Values</h2>
        <div className="space-y-3">
          <div className="p-4 bg-blue-50 rounded-md">
            <h3 className="font-medium text-blue-900">1. Personal Growth</h3>
            <p className="text-sm text-blue-700 mt-1">
              We pursue mastery, learn continuously, and improve our capabilities every
              day.
            </p>
          </div>
          <div className="p-4 bg-purple-50 rounded-md">
            <h3 className="font-medium text-purple-900">2. Harmonious Relationships</h3>
            <p className="text-sm text-purple-700 mt-1">
              We foster trust, communicate with respect, and collaborate effectively.
            </p>
          </div>
          <div className="p-4 bg-green-50 rounded-md">
            <h3 className="font-medium text-green-900">3. Problem Solving</h3>
            <p className="text-sm text-green-700 mt-1">
              We face challenges with clarity, creativity, and discipline, always fixing
              root causes.
            </p>
          </div>
          <div className="p-4 bg-orange-50 rounded-md">
            <h3 className="font-medium text-orange-900">4. Positive Impact</h3>
            <p className="text-sm text-orange-700 mt-1">
              We aim to elevate every person we serve—clients, colleagues, and
              communities.
            </p>
          </div>
          <div className="p-4 bg-indigo-50 rounded-md">
            <h3 className="font-medium text-indigo-900">5. Financial Stewardship</h3>
            <p className="text-sm text-indigo-700 mt-1">
              We create value, drive revenue, and build long-term financial strength.
            </p>
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
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold">
                      {assessment.assessment_type.toUpperCase()} Assessment
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${getAlignmentColor(
                        assessment.alignment_level
                      )}`}
                    >
                      {getAlignmentLabel(assessment.alignment_level)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {new Date(assessment.assessment_date).toLocaleDateString()}
                  </p>
                  {assessment.assessor_name && (
                    <p className="text-sm text-gray-600">
                      Assessor: {assessment.assessor_name}
                    </p>
                  )}
                </div>
                <div className="flex gap-2">
                  <div className="text-right">
                    <div
                      className={`text-3xl font-bold ${getRatingColor(
                        assessment.overall_alignment_score
                      )}`}
                    >
                      {assessment.overall_alignment_score.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">out of 100</div>
                  </div>
                  <button
                    onClick={() => handleExportPdf(assessment.id)}
                    className="btn btn-secondary flex items-center gap-2 h-fit"
                  >
                    <DocumentArrowDownIcon className="h-4 w-4" />
                    PDF
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div className="text-center p-3 bg-blue-50 rounded">
                  <div className="text-xs font-medium text-gray-700">
                    Personal Growth
                  </div>
                  <div
                    className={`text-lg font-bold ${getRatingColor(
                      assessment.personal_growth_score
                    )}`}
                  >
                    {assessment.personal_growth_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-purple-50 rounded">
                  <div className="text-xs font-medium text-gray-700">
                    Relationships
                  </div>
                  <div
                    className={`text-lg font-bold ${getRatingColor(
                      assessment.harmonious_relationships_score
                    )}`}
                  >
                    {assessment.harmonious_relationships_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-green-50 rounded">
                  <div className="text-xs font-medium text-gray-700">
                    Problem Solving
                  </div>
                  <div
                    className={`text-lg font-bold ${getRatingColor(
                      assessment.problem_solving_score
                    )}`}
                  >
                    {assessment.problem_solving_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-orange-50 rounded">
                  <div className="text-xs font-medium text-gray-700">
                    Positive Impact
                  </div>
                  <div
                    className={`text-lg font-bold ${getRatingColor(
                      assessment.positive_impact_score
                    )}`}
                  >
                    {assessment.positive_impact_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-indigo-50 rounded">
                  <div className="text-xs font-medium text-gray-700">
                    Financial Stewardship
                  </div>
                  <div
                    className={`text-lg font-bold ${getRatingColor(
                      assessment.financial_stewardship_score
                    )}`}
                  >
                    {assessment.financial_stewardship_score.toFixed(1)}
                  </div>
                </div>
              </div>

              {assessment.notes && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-sm text-gray-600">{assessment.notes}</p>
                </div>
              )}
            </div>
          ))}
          {assessments.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-500 mb-4">No Core Values assessments yet.</p>
              <p className="text-sm text-gray-400">
                Create assessments to evaluate how well candidates align with your
                organizational values.
              </p>
            </div>
          )}
        </div>
      )}

      <div className="mt-6 card bg-indigo-50 border-indigo-200">
        <h3 className="text-sm font-semibold text-indigo-900 mb-2">
          About Core Values Assessment
        </h3>
        <p className="text-sm text-indigo-800">
          Core Values assessment helps ensure cultural fit by evaluating candidates
          against your organization's fundamental principles. Strong alignment leads to
          better performance, higher retention, and stronger team cohesion.
        </p>
      </div>
    </div>
  );
}
