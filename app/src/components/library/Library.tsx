import { useState } from 'react';
import { mockTracks, musicGenres, mockVideos } from '../../lib/musicData';
import { TrackItem } from '../library/TrackItem';
import { VideoCard } from '../library/VideoCard';
import { Button } from '../ui/button';
import { Play, Shuffle, Sparkles, Clock } from 'lucide-react';
import { usePlayerStore } from '../../store/playerStore';
import { cn } from '../../lib/utils';

export function Library() {
    const { setQueue, play } = usePlayerStore();
    const [tracks] = useState(mockTracks);

    const handlePlayAll = () => {
        setQueue(tracks, 0);
        play();
    };

    const handleShuffle = () => {
        const shuffled = [...tracks].sort(() => Math.random() - 0.5);
        setQueue(shuffled, 0);
        play();
    };

    return (
        <div className="flex-1 min-h-screen bg-black text-white pb-32">
            {/* Dynamic Header */}
            <div className="relative pt-20 px-8 pb-12 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-900/30 to-black pointer-events-none" />

                <div className="relative z-10 container mx-auto">
                    <div className="flex items-center gap-2 mb-4">
                        <Sparkles className="w-5 h-5 text-purple-400" />
                        <span className="text-xs font-bold uppercase tracking-[0.2em] text-purple-400">Curated Paradise</span>
                    </div>
                    <h1 className="text-7xl font-black text-white mb-4 tracking-tight">Your Library</h1>
                    <p className="text-gray-400 text-lg mb-8 max-w-xl">
                        A personalized collection of your Suno AI masterpieces and favorite tracks.
                    </p>

                    <div className="flex gap-4">
                        <Button
                            onClick={handlePlayAll}
                            className="bg-white hover:bg-gray-200 text-black rounded-full px-10 h-14 font-bold text-base shadow-xl shadow-white/5 transition-transform hover:scale-105"
                        >
                            <Play className="w-5 h-5 mr-3" fill="currentColor" />
                            Play All
                        </Button>
                        <Button
                            onClick={handleShuffle}
                            variant="outline"
                            className="border-white/20 hover:border-white hover:bg-white/5 rounded-full px-10 h-14 font-bold text-base backdrop-blur-sm transition-transform hover:scale-105"
                        >
                            <Shuffle className="w-5 h-5 mr-3" />
                            Shuffle
                        </Button>
                    </div>
                </div>
            </div>

            {/* Genre Section */}
            <div className="container mx-auto px-8 mb-16 relative z-10">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    Explore Genres
                    <div className="h-px flex-1 bg-white/5" />
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {musicGenres.map((genre) => (
                        <div
                            key={genre.id}
                            onClick={() => {
                                const genreTracks = tracks.filter(t => t.genre?.toLowerCase() === genre.id || t.genre === genre.title.split(' ')[0]);
                                if (genreTracks.length > 0) {
                                    setQueue(genreTracks, 0);
                                    play();
                                }
                            }}
                            className={cn(
                                "group relative h-48 rounded-2xl overflow-hidden cursor-pointer transition-all hover:scale-[1.02]",
                                genre.color
                            )}
                        >
                            <img
                                src={genre.image}
                                alt={genre.title}
                                className="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-60 group-hover:scale-110 transition-transform duration-500"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                            <div className="absolute bottom-6 left-6">
                                <h3 className="text-xl font-black">{genre.title}</h3>
                            </div>
                            <div className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center shadow-lg">
                                    <Play className="w-5 h-5 ml-0.5" fill="currentColor" />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Video Section */}
            <div className="container mx-auto px-8 mb-16 relative z-10">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    Featured Music Videos
                    <div className="h-px flex-1 bg-white/5" />
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    {mockVideos.map((video) => (
                        <VideoCard key={video.id} video={video} />
                    ))}
                </div>
            </div>

            {/* Track List */}
            <div className="container mx-auto px-8 relative z-10">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    Your Tracks
                    <div className="h-px flex-1 bg-white/5" />
                </h2>
                <div className="grid grid-cols-[16px_4fr_2fr_80px] gap-4 px-6 pb-4 text-xs font-bold uppercase tracking-widest text-gray-500 border-b border-white/5 mb-4">
                    <div>#</div>
                    <div>Title</div>
                    <div>Album</div>
                    <div className="flex justify-end pr-2"><Clock className="w-4 h-4" /></div>
                </div>

                <div className="space-y-1">
                    {tracks.map((track, index) => (
                        <TrackItem
                            key={track.id}
                            track={track}
                            index={index}
                            showIndex
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
