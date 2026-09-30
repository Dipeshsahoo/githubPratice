import { useQuery } from '@tanstack/react-query'
import { Users, Calendar, Newspaper, Briefcase, Heart, TrendingUp } from 'lucide-react'
import api from '../services/api'

const AdminDashboard = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const res = await api.get('/admin/stats')
      return res.data
    }
  })

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      {stats && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Users</p>
                <p className="text-3xl font-bold">{stats.users.total}</p>
              </div>
              <Users className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.users.pending_approval} pending approval
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Events</p>
                <p className="text-3xl font-bold">{stats.events.total}</p>
              </div>
              <Calendar className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.events.upcoming} upcoming
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">News Articles</p>
                <p className="text-3xl font-bold">{stats.news.total}</p>
              </div>
              <Newspaper className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.news.published} published
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Mentorship Posts</p>
                <p className="text-3xl font-bold">{stats.mentorship.total}</p>
              </div>
              <TrendingUp className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.mentorship.pending} pending approval
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Job Postings</p>
                <p className="text-3xl font-bold">{stats.jobs.total}</p>
              </div>
              <Briefcase className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.jobs.active} active
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Donations</p>
                <p className="text-3xl font-bold">₹{stats.donations.total_amount.toLocaleString()}</p>
              </div>
              <Heart className="w-12 h-12 text-primary-600" />
            </div>
            <p className="text-sm text-gray-500 mt-2">
              {stats.donations.pending} pending
            </p>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <a href="/admin/users" className="bg-primary-50 p-4 rounded-lg hover:bg-primary-100 transition">
            <h3 className="font-semibold mb-2">Manage Users</h3>
            <p className="text-sm text-gray-600">Approve and manage user accounts</p>
          </a>
          <a href="/admin/events" className="bg-primary-50 p-4 rounded-lg hover:bg-primary-100 transition">
            <h3 className="font-semibold mb-2">Manage Events</h3>
            <p className="text-sm text-gray-600">Create and manage events</p>
          </a>
          <a href="/admin/donations" className="bg-primary-50 p-4 rounded-lg hover:bg-primary-100 transition">
            <h3 className="font-semibold mb-2">Manage Donations</h3>
            <p className="text-sm text-gray-600">Review and process donations</p>
          </a>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
