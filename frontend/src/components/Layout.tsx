import { Link, useNavigate } from 'react-router-dom'
import { Home, FileText, Users, Award, TrendingUp, BarChart } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-20 border-b">
            <h1 className="text-2xl font-bold text-primary-600">A-Player Suite</h1>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <NavLink to="/" icon={<Home size={20} />} label="Dashboard" />
            <NavLink to="/scorecards" icon={<FileText size={20} />} label="Scorecards" />
            <NavLink to="/ceo-scorecards" icon={<Award size={20} />} label="CEO Scorecards" />
            <NavLink to="/interviews" icon={<Users size={20} />} label="Interviews" />
            <NavLink to="/leadership" icon={<TrendingUp size={20} />} label="Leadership" />
            <NavLink to="/power-scores" icon={<BarChart size={20} />} label="Power Scores" />
          </nav>

          {/* User menu */}
          <div className="p-4 border-t">
            <button
              onClick={handleLogout}
              className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="ml-64">
        <main className="p-8">{children}</main>
      </div>
    </div>
  )
}

interface NavLinkProps {
  to: string
  icon: React.ReactNode
  label: string
}

function NavLink({ to, icon, label }: NavLinkProps) {
  return (
    <Link
      to={to}
      className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-700 transition-colors"
    >
      {icon}
      <span className="ml-3 font-medium">{label}</span>
    </Link>
  )
}
