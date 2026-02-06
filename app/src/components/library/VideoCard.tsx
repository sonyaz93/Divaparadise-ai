import { Play, Film } from 'lucide-react';
import type { Video, Track } from '../../types/music';
import { usePlayerStore } from '../../store/playerStore';

interface VideoCardProps {
    video: Video;
}

export function VideoCard({ video }: VideoCardProps) {
    const { setTrack, play } = usePlayerStore();

    const handleClick = () => {
        // Map Video to Track format for playing
        const trackFromVideo: Track = {
            id: video.id,
            title: video.title,
            artist: video.artist,
            audioUrl: video.videoUrl, // Use video URL as audio source
            coverImage: video.thumbnailUrl || '/images/UI/placeholders/album.png',
            duration: video.duration || 0,
            genre: 'Video'
        };

        setTrack(trackFromVideo);
        play();
    };

    return (
        <div
            onClick={handleClick}
            className="group relative bg-[#181818] hover:bg-[#282828] p-4 rounded-xl transition-all duration-300 cursor-pointer shadow-lg hover:shadow-purple-900/20"
        >
            <div className="relative aspect-video mb-4 rounded-lg overflow-hidden shadow-md">
                <img
                    src={video.thumbnailUrl || '/images/UI/placeholders/album.png'}
                    alt={video.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-12 h-12 rounded-full bg-purple-500 text-white flex items-center justify-center translate-y-4 group-hover:translate-y-0 transition-all duration-300 shadow-xl">
                        <Play className="w-6 h-6 ml-1" fill="currentColor" />
                    </div>
                </div>
                <div className="absolute bottom-2 right-2 bg-black/60 backdrop-blur-md px-2 py-0.5 rounded text-[10px] font-bold text-white flex items-center gap-1">
                    <Film className="w-3 h-3" />
                    VIDEO
                </div>
            </div>
            <h3 className="text-sm font-bold text-white truncate mb-1 group-hover:text-purple-400 transition-colors">
                {video.title}
            </h3>
            <p className="text-xs text-gray-400 font-medium truncate">
                {video.artist}
            </p>
        </div>
    );
}
