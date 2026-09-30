import { useQuery } from '@tanstack/react-query'
import { Newspaper, Calendar } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const News = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['news'],
    queryFn: async () => {
      const res = await api.get('/news?published_only=true')
      return res.data
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">News & Announcements</h1>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.news && data.news.length > 0 ? (
        <div className="space-y-6">
          {data.news.map((article) => (
            <Link
              key={article.id}
              to={`/news/${article.id}`}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
            >
              <div className="flex items-start">
                <Newspaper className="w-8 h-8 text-primary-600 mr-4 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">{article.title}</h3>
                  {article.category && (
                    <span className="inline-block bg-primary-100 text-primary-700 text-xs px-2 py-1 rounded mb-2">
                      {article.category}
                    </span>
                  )}
                  <p className="text-gray-600 mb-3 line-clamp-2">{article.content}</p>
                  {article.published_at && (
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(article.published_at).toLocaleDateString()}
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">No news articles found.</div>
      )}
    </div>
  )
}

export default News
