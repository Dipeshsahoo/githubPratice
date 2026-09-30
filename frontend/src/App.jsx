import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import AlumniDirectory from './pages/AlumniDirectory'
import Events from './pages/Events'
import EventDetail from './pages/EventDetail'
import News from './pages/News'
import Gallery from './pages/Gallery'
import Mentorship from './pages/Mentorship'
import Jobs from './pages/Jobs'
import Donations from './pages/Donations'
import Profile from './pages/Profile'
import AdminDashboard from './pages/AdminDashboard'
import JubileePage from './pages/JubileePage'
import ProtectedRoute from './components/ProtectedRoute'
import Chatbot from './components/Chatbot'

function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/alumni" element={<AlumniDirectory />} />
          <Route path="/events" element={<Events />} />
          <Route path="/events/:id" element={<EventDetail />} />
          <Route path="/news" element={<News />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/mentorship" element={<Mentorship />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/donations" element={<Donations />} />
          <Route path="/jubilee" element={<JubileePage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute requireAdmin>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
        <Chatbot />
      </Layout>
    </AuthProvider>
  )
}

export default App
