import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { User, Save } from 'lucide-react'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const Profile = () => {
  const { user, setUser } = useAuth()
  const queryClient = useQueryClient()
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    first_name: user?.profile?.first_name || '',
    last_name: user?.profile?.last_name || '',
    batch_year: user?.profile?.batch_year || '',
    profession: user?.profile?.profession || '',
    company: user?.profile?.company || '',
    location: user?.profile?.location || '',
    bio: user?.profile?.bio || '',
    linkedin_url: user?.profile?.linkedin_url || '',
    website_url: user?.profile?.website_url || ''
  })

  const { data: profileData } = useQuery({
    queryKey: ['profile', user?.id],
    queryFn: async () => {
      const res = await api.get(`/alumni/${user.id}`)
      return res.data
    },
    enabled: !!user
  })

  const updateMutation = useMutation({
    mutationFn: async (data) => {
      const res = await api.put(`/alumni/${user.id}`, data)
      return res.data
    },
    onSuccess: (data) => {
      setUser(data.profile?.user || user)
      queryClient.invalidateQueries(['profile', user.id])
      setEditing(false)
    }
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    updateMutation.mutate(formData)
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  if (!user) {
    return <div>Please log in to view your profile</div>
  }

  const profile = profileData?.profile || user.profile

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">My Profile</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        {!editing ? (
          <>
            <div className="flex items-center mb-6">
              {profile?.profile_picture ? (
                <img
                  src={profile.profile_picture}
                  alt="Profile"
                  className="w-24 h-24 rounded-full object-cover"
                />
              ) : (
                <div className="w-24 h-24 rounded-full bg-primary-100 flex items-center justify-center">
                  <User className="w-12 h-12 text-primary-600" />
                </div>
              )}
              <div className="ml-6">
                <h2 className="text-2xl font-semibold">
                  {profile?.first_name} {profile?.last_name}
                </h2>
                <p className="text-gray-600">{user.email}</p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4 mb-6">
              {profile?.batch_year && (
                <div>
                  <p className="text-sm text-gray-500">Batch Year</p>
                  <p className="font-medium">{profile.batch_year}</p>
                </div>
              )}
              {profile?.profession && (
                <div>
                  <p className="text-sm text-gray-500">Profession</p>
                  <p className="font-medium">{profile.profession}</p>
                </div>
              )}
              {profile?.company && (
                <div>
                  <p className="text-sm text-gray-500">Company</p>
                  <p className="font-medium">{profile.company}</p>
                </div>
              )}
              {profile?.location && (
                <div>
                  <p className="text-sm text-gray-500">Location</p>
                  <p className="font-medium">{profile.location}</p>
                </div>
              )}
            </div>

            {profile?.bio && (
              <div className="mb-6">
                <p className="text-sm text-gray-500 mb-2">Bio</p>
                <p className="text-gray-700">{profile.bio}</p>
              </div>
            )}

            <button
              onClick={() => setEditing(true)}
              className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700"
            >
              Edit Profile
            </button>
          </>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                <input
                  type="text"
                  name="first_name"
                  required
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                <input
                  type="text"
                  name="last_name"
                  required
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Batch Year *</label>
                <input
                  type="number"
                  name="batch_year"
                  required
                  value={formData.batch_year}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Profession *</label>
                <input
                  type="text"
                  name="profession"
                  required
                  value={formData.profession}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Company</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
              <textarea
                name="bio"
                rows="4"
                value={formData.bio}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={updateMutation.isLoading}
                className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
              >
                <Save className="w-4 h-4 mr-2" />
                Save
              </button>
              <button
                type="button"
                onClick={() => setEditing(false)}
                className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default Profile
