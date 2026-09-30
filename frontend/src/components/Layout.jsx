import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Menu, X, User, LogOut, Settings } from 'lucide-react'
import { useState } from 'react'

const Layout = ({ children }) => {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link to="/" className="flex items-center">
                <span className="text-2xl font-bold text-primary-600">Alumni Portal</span>
              </Link>
              <div className="hidden md:ml-10 md:flex md:space-x-8">
                <Link to="/" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Home
                </Link>
                <Link to="/alumni" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Directory
                </Link>
                <Link to="/events" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Events
                </Link>
                <Link to="/news" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  News
                </Link>
                <Link to="/gallery" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Gallery
                </Link>
                <Link to="/mentorship" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Mentorship
                </Link>
                <Link to="/jobs" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium">
                  Jobs
                </Link>
                <Link to="/jubilee" className="text-primary-600 hover:text-primary-700 px-3 py-2 text-sm font-medium font-semibold">
                  Jubilee
                </Link>
              </div>
            </div>
            <div className="hidden md:flex md:items-center md:space-x-4">
              {user ? (
                <>
                  <Link
                    to="/profile"
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium flex items-center"
                  >
                    <User className="w-4 h-4 mr-1" />
                    Profile
                  </Link>
                  {isAdmin() && (
                    <Link
                      to="/admin"
                      className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium"
                    >
                      Admin
                    </Link>
                  )}
                  <button
                    onClick={handleLogout}
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium flex items-center"
                  >
                    <LogOut className="w-4 h-4 mr-1" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="text-gray-700 hover:text-primary-600"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link to="/" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Home</Link>
              <Link to="/alumni" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Directory</Link>
              <Link to="/events" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Events</Link>
              <Link to="/news" className="block px-3 py-2 text-gray-700 hover:text-primary-600">News</Link>
              <Link to="/gallery" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Gallery</Link>
              <Link to="/mentorship" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Mentorship</Link>
              <Link to="/jobs" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Jobs</Link>
              <Link to="/jubilee" className="block px-3 py-2 text-primary-600 font-semibold">Jubilee</Link>
              {user ? (
                <>
                  <Link to="/profile" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Profile</Link>
                  {isAdmin() && <Link to="/admin" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Admin</Link>}
                  <button onClick={handleLogout} className="block w-full text-left px-3 py-2 text-gray-700 hover:text-primary-600">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="block px-3 py-2 text-gray-700 hover:text-primary-600">Login</Link>
                  <Link to="/register" className="block px-3 py-2 bg-primary-600 text-white rounded-md">Register</Link>
                </>
              )}
            </div>
          </div>
        )}
      </nav>
      <main>{children}</main>
      <footer className="bg-gray-800 text-white mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-400">© 2024 Alumni Portal. All rights reserved.</p>
            <p className="text-gray-500 text-sm mt-2">Platinum Jubilee Celebration</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout
