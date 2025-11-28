import { useEffect, useState } from 'react';
import { idealTeamPlayerApi } from '../services/api';
import type { IdealTeamPlayerAssessment } from '../types';
import { DocumentArrowDownIcon } from '@heroicons/react/24/outline';

export default function IdealTeamPlayer() {
  const [assessments, setAssessments] = useState<IdealTeamPlayerAssessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const response = await idealTeamPlayerApi.list();
      setAssessments(response.data);
    } catch (error) {
      console.error('Error loading assessments:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category?: string) => {
    const colors: Record<string, string> = {
      ideal_team_player: 'bg-green-100 text-green-800',
      accidental_mess_maker: 'bg-yellow-100 text-yellow-800',
      lovable_slacker: 'bg-blue-100 text-blue-800',
      skillful_politician: 'bg-red-100 text-red-800',
      pawn: 'bg-gray-100 text-gray-800',
      bulldozer: 'bg-red-100 text-red-800',
      charmer: 'bg-purple-100 text-purple-800',
      ideal_mismatch: 'bg-red-100 text-red-800',
    };
    return colors[category || ''] || 'bg-gray-100 text-gray-800';
  };

  const getCategoryLabel = (category?: string) => {
    const labels: Record<string, string> = {
      ideal_team_player: 'Ideal Team Player',
      accidental_mess_maker: 'Accidental Mess-Maker',
      lovable_slacker: 'Lovable Slacker',
      skillful_politician: 'Skillful Politician',
      pawn: 'Pawn',
      bulldozer: 'Bulldozer',
      charmer: 'Charmer',
      ideal_mismatch: 'Ideal Mismatch',
    };
    return labels[category || ''] || 'Unknown';
  };

  const handleExportPdf = async (id: string, category: string) => {
    try {
      const response = await idealTeamPlayerApi.exportPdf(id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ideal_team_player_${category}_${id}.pdf`;
      a.click();
    } catch (error) {
      console.error('Error exporting PDF:', error);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          Ideal Team Player Assessment
        </h1>
        <p className="mt-2 text-gray-600">
          Based on Patrick Lencioni's three virtues: Humble, Hungry, and Smart
        </p>
      </div>

      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">The Three Virtues</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 rounded-md">
            <h3 className="font-medium text-blue-900">Humble</h3>
            <p className="text-sm text-blue-700 mt-1">
              Lacks excessive ego, shares credit, defines success collectively
            </p>
          </div>
          <div className="p-4 bg-green-50 rounded-md">
            <h3 className="font-medium text-green-900">Hungry</h3>
            <p className="text-sm text-green-700 mt-1">
              Self-motivated, diligent, always looking to do more
            </p>
          </div>
          <div className="p-4 bg-purple-50 rounded-md">
            <h3 className="font-medium text-purple-900">Smart (People Smart)</h3>
            <p className="text-sm text-purple-700 mt-1">
              Has common sense about people and good emotional intelligence
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
                      className={`px-3 py-1 rounded-full text-sm ${getCategoryColor(
                        assessment.category
                      )}`}
                    >
                      {getCategoryLabel(assessment.category)}
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
                    <div className="text-2xl font-bold text-primary-600">
                      {assessment.overall_score.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">out of 5.0</div>
                  </div>
                  <button
                    onClick={() =>
                      handleExportPdf(assessment.id, assessment.category || 'assessment')
                    }
                    className="btn btn-secondary flex items-center gap-2 h-fit"
                  >
                    <DocumentArrowDownIcon className="h-4 w-4" />
                    PDF
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 bg-blue-50 rounded">
                  <div className="text-sm font-medium text-gray-700">Humble</div>
                  <div className="text-xl font-bold text-blue-600">
                    {assessment.humble_score.toFixed(2)}
                  </div>
                </div>
                <div className="p-3 bg-green-50 rounded">
                  <div className="text-sm font-medium text-gray-700">Hungry</div>
                  <div className="text-xl font-bold text-green-600">
                    {assessment.hungry_score.toFixed(2)}
                  </div>
                </div>
                <div className="p-3 bg-purple-50 rounded">
                  <div className="text-sm font-medium text-gray-700">
                    Smart
                  </div>
                  <div className="text-xl font-bold text-purple-600">
                    {assessment.smart_score.toFixed(2)}
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
              <p className="text-gray-500 mb-4">
                No Ideal Team Player assessments yet.
              </p>
              <p className="text-sm text-gray-400">
                Create assessments to evaluate candidates across the three key
                virtues: humble, hungry, and smart.
              </p>
            </div>
          )}
        </div>
      )}

      <div className="mt-6 card bg-blue-50 border-blue-200">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">
          About the Ideal Team Player Framework
        </h3>
        <p className="text-sm text-blue-800">
          Based on Patrick Lencioni's research, the Ideal Team Player possesses three
          essential virtues. Candidates strong in all three make exceptional team
          members, while those lacking one or more create predictable challenges.
        </p>
      </div>
    </div>
  );
}
