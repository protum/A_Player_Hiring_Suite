import { useEffect, useState } from 'react';
import { interviewsApi } from '../services/api';
import type { Interview } from '../types';

export default function Interviews() {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInterviews();
  }, []);

  const loadInterviews = async () => {
    try {
      const response = await interviewsApi.list();
      setInterviews(response.data);
    } catch (error) {
      console.error('Error loading interviews:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      scheduled: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      completed: 'bg-green-100 text-green-800',
      cancelled: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Biographical Interviews</h1>
        <p className="mt-2 text-gray-600">
          Topgrading-style chronological interviews
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {interviews.map((interview) => (
            <div key={interview.id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold">
                    Interview #{interview.id.slice(0, 8)}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Candidate ID: {interview.candidate_id}
                  </p>
                  {interview.interviewer_name && (
                    <p className="text-sm text-gray-600">
                      Interviewer: {interview.interviewer_name}
                    </p>
                  )}
                </div>
                <span className={`px-3 py-1 rounded-full text-sm ${getStatusColor(interview.status)}`}>
                  {interview.status}
                </span>
              </div>
              {interview.job_history.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600">
                    {interview.job_history.length} job(s) in history
                  </p>
                </div>
              )}
            </div>
          ))}
          {interviews.length === 0 && (
            <div className="card text-center py-12">
              <p className="text-gray-500">No interviews scheduled yet.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
