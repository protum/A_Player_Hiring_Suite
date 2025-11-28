import { useEffect, useState } from 'react';
import { scorecardsApi } from '../services/api';
import type { Scorecard } from '../types';
import { DocumentArrowDownIcon } from '@heroicons/react/24/outline';

export default function Scorecards() {
  const [scorecards, setScorecards] = useState<Scorecard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadScorecards();
  }, []);

  const loadScorecards = async () => {
    try {
      const response = await scorecardsApi.list();
      setScorecards(response.data);
    } catch (error) {
      console.error('Error loading scorecards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPdf = async (id: string, title: string) => {
    try {
      const response = await scorecardsApi.exportPdf(id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `scorecard_${title}.pdf`;
      a.click();
    } catch (error) {
      console.error('Error exporting PDF:', error);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">A-Method Scorecards</h1>
        <p className="mt-2 text-gray-600">
          Define roles with mission, outcomes, and competencies
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {scorecards.map((scorecard) => (
            <div key={scorecard.id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-bold text-gray-900">
                    {scorecard.role_title}
                  </h2>
                  {scorecard.department && (
                    <p className="text-sm text-gray-500">{scorecard.department}</p>
                  )}
                </div>
                <button
                  onClick={() => handleExportPdf(scorecard.id, scorecard.role_title)}
                  className="btn btn-secondary flex items-center gap-2"
                >
                  <DocumentArrowDownIcon className="h-4 w-4" />
                  Export PDF
                </button>
              </div>

              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Mission</h3>
                <p className="text-gray-900">{scorecard.mission}</p>
              </div>

              {scorecard.outcomes.length > 0 && (
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">
                    Key Outcomes ({scorecard.outcomes.length})
                  </h3>
                  <ul className="space-y-2">
                    {scorecard.outcomes.slice(0, 3).map((outcome, idx) => (
                      <li key={idx} className="text-sm text-gray-600">
                        • {outcome.description}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {scorecard.competencies.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2">
                    Competencies ({scorecard.competencies.length})
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {scorecard.competencies.map((comp, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                      >
                        {comp.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {scorecards.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-500">
                No scorecards yet. Create your first A-Method scorecard to define role
                expectations.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
