import { useQuery } from '@tanstack/react-query'
import { scorecardsAPI, ceoScorecardsAPI, interviewsAPI } from '@/services/api'
import { FileText, Award, Users, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const { data: scorecards } = useQuery({
    queryKey: ['scorecards'],
    queryFn: scorecardsAPI.list,
  })

  const { data: ceoScorecards } = useQuery({
    queryKey: ['ceoScorecards'],
    queryFn: ceoScorecardsAPI.list,
  })

  const { data: interviews } = useQuery({
    queryKey: ['interviews'],
    queryFn: interviewsAPI.list,
  })

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Welcome to A-Player Hiring Suite - Your comprehensive hiring and leadership assessment platform
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={<FileText className="text-primary-600" size={32} />}
          title="Scorecards"
          value={scorecards?.length || 0}
          subtitle="A-Method scorecards"
        />
        <StatCard
          icon={<Award className="text-green-600" size={32} />}
          title="CEO Scorecards"
          value={ceoScorecards?.length || 0}
          subtitle="Executive assessments"
        />
        <StatCard
          icon={<Users className="text-blue-600" size={32} />}
          title="Interviews"
          value={interviews?.length || 0}
          subtitle="Topgrading interviews"
        />
        <StatCard
          icon={<TrendingUp className="text-purple-600" size={32} />}
          title="Assessments"
          value={0}
          subtitle="Leadership & Power Score"
        />
      </div>

      {/* Framework Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FrameworkCard
          title="Who: A-Method"
          description="Create role scorecards with clear mission, outcomes, and competencies"
          features={['Role mission definition', '3-5 measurable outcomes', '5-8 key competencies']}
        />
        <FrameworkCard
          title="Topgrading"
          description="Chronological in-depth structured interviews with TORC methodology"
          features={['Career-by-career analysis', 'Boss ratings', 'Red flag detection']}
        />
        <FrameworkCard
          title="CEO Next Door"
          description="Assess the 4 CEO behaviors that drive success"
          features={['Decisiveness', 'Reliability', 'Bold Adaptation', 'Engaging for Impact']}
        />
        <FrameworkCard
          title="Power Score"
          description="Executive effectiveness: P × W × R formula"
          features={['Priorities clarity', 'Who (team quality)', 'Relationships health']}
        />
        <FrameworkCard
          title="CEO Scorecard"
          description="Comprehensive executive performance assessment"
          features={[
            'CEO Excellence Index',
            'Behavior + Power Score',
            'Operating metrics',
            'Development recommendations',
          ]}
        />
        <FrameworkCard
          title="Foolproof Hiring"
          description="Evidence-based candidate evaluation"
          features={['CQI scoring', 'Pattern analysis', 'Reference validation']}
        />
      </div>
    </div>
  )
}

interface StatCardProps {
  icon: React.ReactNode
  title: string
  value: number
  subtitle: string
}

function StatCard({ icon, title, value, subtitle }: StatCardProps) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        {icon}
        <span className="text-3xl font-bold text-gray-900">{value}</span>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{subtitle}</p>
    </div>
  )
}

interface FrameworkCardProps {
  title: string
  description: string
  features: string[]
}

function FrameworkCard({ title, description, features }: FrameworkCardProps) {
  return (
    <div className="card hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <ul className="space-y-2">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start">
            <span className="text-primary-600 mr-2">✓</span>
            <span className="text-sm text-gray-700">{feature}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
