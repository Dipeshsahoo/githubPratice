import { Link } from 'react-router-dom'
import { Users, Calendar, Newspaper, Briefcase, Heart, Sparkles } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Home = () => {
  const { user } = useAuth()

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Welcome to Alumni Portal
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Celebrating 75 Years of Excellence - Platinum Jubilee
            </p>
            <div className="flex justify-center space-x-4">
              {!user ? (
                <>
                  <Link
                    to="/register"
                    className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition"
                  >
                    Join Us
                  </Link>
                  <Link
                    to="/login"
                    className="bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-600 transition"
                  >
                    Login
                  </Link>
                </>
              ) : (
                <Link
                  to="/jubilee"
                  className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition flex items-center"
                >
                  <Sparkles className="w-5 h-5 mr-2" />
                  Jubilee Events
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Connect, Celebrate, Contribute</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Link to="/alumni" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Users className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Alumni Directory</h3>
            <p className="text-gray-600">
              Find and connect with fellow alumni from different batches and professions.
            </p>
          </Link>

          <Link to="/events" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Calendar className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Events & Reunions</h3>
            <p className="text-gray-600">
              Stay updated with upcoming events and register for Platinum Jubilee celebrations.
            </p>
          </Link>

          <Link to="/news" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Newspaper className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">News & Updates</h3>
            <p className="text-gray-600">
              Read the latest announcements and news from the alumni community.
            </p>
          </Link>

          <Link to="/mentorship" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Sparkles className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Mentorship</h3>
            <p className="text-gray-600">
              Connect with mentors or offer mentorship to fellow alumni.
            </p>
          </Link>

          <Link to="/jobs" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Briefcase className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Career Opportunities</h3>
            <p className="text-gray-600">
              Explore job postings and internship opportunities shared by alumni.
            </p>
          </Link>

          <Link to="/donations" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
            <Heart className="w-12 h-12 text-primary-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Donations</h3>
            <p className="text-gray-600">
              Support the school and alumni initiatives through donations.
            </p>
          </Link>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary-50 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Join the Platinum Jubilee Celebration</h2>
          <p className="text-lg text-gray-700 mb-8">
            Be part of this historic milestone. Register for events, connect with alumni, and celebrate 75 years of excellence together.
          </p>
          <Link
            to="/jubilee"
            className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition inline-block"
          >
            View Jubilee Schedule
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Home
