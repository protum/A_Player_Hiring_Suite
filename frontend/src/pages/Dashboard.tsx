import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { systemApi } from '../services/api';
import { ArrowTrendingUpIcon, DocumentTextIcon, UserGroupIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await systemApi.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      name: 'Candidates',
      value: stats?.candidates || 0,
      icon: UserGroupIcon,
      color: 'bg-blue-500',
      link: '/candidates',
    },
    {
      name: 'Scorecards',
      value: stats?.scorecards || 0,
      icon: DocumentTextIcon,
      color: 'bg-green-500',
      link: '/scorecards',
    },
    {
      name: 'Interviews',
      value: stats?.interviews || 0,
      icon: UserGroupIcon,
      color: 'bg-purple-500',
      link: '/interviews',
    },
    {
      name: 'Assessments',
      value: (stats?.ceo_assessments || 0) + (stats?.power_score_assessments || 0),
      icon: ChartBarIcon,
      color: 'bg-orange-500',
      link: '/ceo-assessments',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Evidence-based hiring and leadership assessment platform
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {statCards.map((stat) => (
              <Link
                key={stat.name}
                to={stat.link}
                className="card hover:shadow-md transition-shadow"
              >
                <div className="flex items-center">
                  <div className={`${stat.color} p-3 rounded-lg`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <Link
                  to="/candidates"
                  className="block p-4 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors"
                >
                  <h3 className="font-medium text-gray-900">Add New Candidate</h3>
                  <p className="text-sm text-gray-600">Start evaluating a new candidate</p>
                </Link>
                <Link
                  to="/scorecards"
                  className="block p-4 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors"
                >
                  <h3 className="font-medium text-gray-900">Create Scorecard</h3>
                  <p className="text-sm text-gray-600">Define A-Method scorecard for a role</p>
                </Link>
                <Link
                  to="/interviews"
                  className="block p-4 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors"
                >
                  <h3 className="font-medium text-gray-900">Schedule Interview</h3>
                  <p className="text-sm text-gray-600">
                    Create biographical interview session
                  </p>
                </Link>
              </div>
            </div>

            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Assessment Methodologies
              </h2>
              <div className="space-y-3">
                <div className="p-4 bg-blue-50 rounded-md">
                  <h3 className="font-medium text-blue-900">A-Method Scorecards</h3>
                  <p className="text-sm text-blue-700">Based on "Who" by Geoff Smart</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-md">
                  <h3 className="font-medium text-purple-900">
                    Biographical Interviewing
                  </h3>
                  <p className="text-sm text-purple-700">Topgrading methodology</p>
                </div>
                <div className="p-4 bg-green-50 rounded-md">
                  <h3 className="font-medium text-green-900">CEO Behaviors</h3>
                  <p className="text-sm text-green-700">
                    Based on "The CEO Next Door"
                  </p>
                </div>
                <div className="p-4 bg-orange-50 rounded-md">
                  <h3 className="font-medium text-orange-900">Power Score</h3>
                  <p className="text-sm text-orange-700">
                    Leadership effectiveness assessment
                  </p>
                </div>
              </div>
            </div>
          </div>

          {stats && (
            <div className="mt-6 text-center text-sm text-gray-500">
              Database size: {stats.database_size_mb} MB | All data stored locally
            </div>
          )}
        </>
      )}
    </div>
  );
}
