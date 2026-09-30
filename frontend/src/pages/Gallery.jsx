import { useQuery } from '@tanstack/react-query'
import { Image as ImageIcon } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const Gallery = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['albums'],
    queryFn: async () => {
      const res = await api.get('/gallery')
      return res.data
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Gallery</h1>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.albums && data.albums.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.albums.map((album) => (
            <Link
              key={album.id}
              to={`/gallery/${album.id}`}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition overflow-hidden"
            >
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                <ImageIcon className="w-16 h-16 text-gray-400" />
              </div>
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">{album.title}</h3>
                {album.description && (
                  <p className="text-gray-600 text-sm line-clamp-2">{album.description}</p>
                )}
                {album.media_count !== null && (
                  <p className="text-sm text-gray-500 mt-2">{album.media_count} items</p>
                )}
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">No albums found.</div>
      )}
    </div>
  )
}

export default Gallery
