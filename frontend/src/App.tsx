import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from '@/pages/Dashboard'
import Login from '@/pages/Login'
import Scorecards from '@/pages/Scorecards'
import CEOScorecards from '@/pages/CEOScorecards'
import Interviews from '@/pages/Interviews'
import LeadershipAssessments from '@/pages/LeadershipAssessments'
import PowerScores from '@/pages/PowerScores'
import Layout from '@/components/Layout'

function App() {
  const isAuthenticated = !!localStorage.getItem('access_token')

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Layout>
                <Dashboard />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/scorecards"
          element={
            isAuthenticated ? (
              <Layout>
                <Scorecards />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/ceo-scorecards"
          element={
            isAuthenticated ? (
              <Layout>
                <CEOScorecards />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/interviews"
          element={
            isAuthenticated ? (
              <Layout>
                <Interviews />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/leadership"
          element={
            isAuthenticated ? (
              <Layout>
                <LeadershipAssessments />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/power-scores"
          element={
            isAuthenticated ? (
              <Layout>
                <PowerScores />
              </Layout>
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </Router>
  )
}

export default App
