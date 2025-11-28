import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { HomeIcon, DocumentTextIcon, UserGroupIcon, ChartBarIcon, TrophyIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';
import Dashboard from './pages/Dashboard';
import Candidates from './pages/Candidates';
import Scorecards from './pages/Scorecards';
import Interviews from './pages/Interviews';
import CEOAssessments from './pages/CEOAssessments';
import PowerScore from './pages/PowerScore';
import Settings from './pages/Settings';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Candidates', href: '/candidates', icon: UserGroupIcon },
  { name: 'Scorecards', href: '/scorecards', icon: DocumentTextIcon },
  { name: 'Interviews', href: '/interviews', icon: UserGroupIcon },
  { name: 'CEO Behaviors', href: '/ceo-assessments', icon: ChartBarIcon },
  { name: 'Power Score', href: '/power-score', icon: TrophyIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

function Navigation() {
  const location = useLocation();

  return (
    <nav className="bg-primary-800 h-screen w-64 fixed left-0 top-0 overflow-y-auto">
      <div className="p-6">
        <h1 className="text-white text-xl font-bold mb-8">A-Player Hiring Suite</h1>
        <div className="space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-900 text-white'
                    : 'text-primary-100 hover:bg-primary-700'
                }`}
              >
                <item.icon className="h-5 w-5" />
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-primary-700">
        <p className="text-primary-300 text-xs">
          Evidence-Based Hiring & Leadership Assessment
        </p>
        <p className="text-primary-400 text-xs mt-1">v1.0.0 - Local Mode</p>
      </div>
    </nav>
  );
}

function AppContent() {
  return (
    <div className="flex">
      <Navigation />
      <main className="ml-64 flex-1 p-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/candidates" element={<Candidates />} />
          <Route path="/scorecards" element={<Scorecards />} />
          <Route path="/interviews" element={<Interviews />} />
          <Route path="/ceo-assessments" element={<CEOAssessments />} />
          <Route path="/power-score" element={<PowerScore />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
