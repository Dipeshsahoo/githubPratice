import { useQuery } from '@tanstack/react-query'
import { Sparkles, User } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const Mentorship = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['mentorship'],
    queryFn: async () => {
      const res = await api.get('/mentorship?approved_only=true')
      return res.data
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Mentorship</h1>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.posts && data.posts.length > 0 ? (
        <div className="grid md:grid-cols-2 gap-6">
          {data.posts.map((post) => (
            <div key={post.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-start mb-4">
                <Sparkles className="w-6 h-6 text-primary-600 mr-3" />
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
                  {post.expertise_area && (
                    <span className="inline-block bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded mb-2">
                      {post.expertise_area}
                    </span>
                  )}
                  <p className="text-gray-600 mb-4">{post.description}</p>
                  {post.user && (
                    <div className="flex items-center text-sm text-gray-500">
                      <User className="w-4 h-4 mr-1" />
                      {post.user.profile?.first_name} {post.user.profile?.last_name}
                    </div>
                  )}
                  <span className={`inline-block mt-2 text-xs px-2 py-1 rounded ${
                    post.availability_status === 'available' ? 'bg-green-100 text-green-700' :
                    post.availability_status === 'limited' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {post.availability_status}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">No mentorship posts found.</div>
      )}
    </div>
  )
}

export default Mentorship
