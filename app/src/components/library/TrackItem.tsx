import { usePlayerStore } from '../../store/playerStore';
import { Play } from 'lucide-react';
import { Button } from '../ui/button';
import { formatDuration } from '../../lib/musicData';
import type { Track } from '../../types/music';
import { cn } from '../../lib/utils';

interface TrackItemProps {
    track: Track;
    index?: number;
    isActive?: boolean;
    showIndex?: boolean;
}

export function TrackItem({ track, index, isActive, showIndex = true }: TrackItemProps) {
    const { currentTrack, isPlaying, setTrack, togglePlay, play } = usePlayerStore();

    const isCurrentTrack = currentTrack?.id === track.id;
    const isCurrentlyPlaying = isCurrentTrack && isPlaying;

    const handleClick = () => {
        if (isCurrentTrack) {
            togglePlay();
        } else {
            setTrack(track);
            play();
        }
    };

    return (
        <div
            className={cn(
                'group grid grid-cols-[16px_4fr_2fr_80px] gap-4 px-4 py-2 rounded-md hover:bg-gray-800/50 transition-colors cursor-pointer',
                isActive && 'bg-gray-800/30'
            )}
            onClick={handleClick}
        >
            {/* Index / Play button */}
            <div className="flex items-center justify-center text-gray-400">
                {isCurrentlyPlaying ? (
                    <div className="flex gap-0.5">
                        <div className="w-0.5 h-3 bg-purple-500 animate-pulse" />
                        <div className="w-0.5 h-3 bg-purple-500 animate-pulse" style={{ animationDelay: '0.2s' }} />
                        <div className="w-0.5 h-3 bg-purple-500 animate-pulse" style={{ animationDelay: '0.4s' }} />
                    </div>
                ) : (
                    <>
                        <span className="group-hover:hidden text-sm">
                            {showIndex && index !== undefined ? index + 1 : ''}
                        </span>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 hidden group-hover:flex"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleClick();
                            }}
                        >
                            <Play className="h-4 w-4" fill="currentColor" />
                        </Button>
                    </>
                )}
            </div>

            {/* Track info */}
            <div className="flex items-center gap-3 min-w-0">
                <div className="w-10 h-10 rounded bg-gray-700 overflow-hidden flex-shrink-0">
                    {track.coverImage && (
                        <img
                            src={track.coverImage}
                            alt={track.title}
                            className="w-full h-full object-cover"
                        />
                    )}
                </div>
                <div className="min-w-0">
                    <div className={cn(
                        'text-sm font-medium truncate',
                        isCurrentTrack ? 'text-purple-400' : 'text-white'
                    )}>
                        {track.title}
                    </div>
                    <div className="text-sm text-gray-400 truncate">
                        {track.artist}
                    </div>
                </div>
            </div>

            {/* Album */}
            <div className="flex items-center text-sm text-gray-400 truncate">
                {track.album || '—'}
            </div>

            {/* Duration */}
            <div className="flex items-center justify-end text-sm text-gray-400">
                {formatDuration(track.duration)}
            </div>
        </div>
    );
}
