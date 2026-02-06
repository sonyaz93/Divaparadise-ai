import { usePlayerStore } from '../../store/playerStore';
import { Play, Pause, SkipForward, SkipBack, Repeat, Repeat1, Shuffle } from 'lucide-react';
import { Button } from '../ui/button';
import { cn } from '../../lib/utils';

export function PlayerControls() {
    const {
        isPlaying,
        togglePlay,
        next,
        previous,
        repeat,
        setRepeat,
        shuffle,
        toggleShuffle,
        currentTrack,
    } = usePlayerStore();

    const handleRepeat = () => {
        if (repeat === 'off') setRepeat('all');
        else if (repeat === 'all') setRepeat('one');
        else setRepeat('off');
    };

    if (!currentTrack) return null;

    return (
        <div className="flex items-center gap-2">
            {/* Shuffle */}
            <Button
                variant="ghost"
                size="icon"
                onClick={toggleShuffle}
                className={cn(
                    'h-8 w-8 transition-colors',
                    shuffle ? 'text-purple-400' : 'text-gray-400 hover:text-white'
                )}
            >
                <Shuffle className="h-4 w-4" />
            </Button>

            {/* Previous */}
            <Button
                variant="ghost"
                size="icon"
                onClick={previous}
                className="h-8 w-8 text-gray-400 hover:text-white"
            >
                <SkipBack className="h-5 w-5" fill="currentColor" />
            </Button>

            {/* Play/Pause */}
            <Button
                variant="default"
                size="icon"
                onClick={togglePlay}
                className="h-10 w-10 rounded-full bg-white hover:bg-gray-200 hover:scale-105 transition-all"
            >
                {isPlaying ? (
                    <Pause className="h-5 w-5 text-black" fill="currentColor" />
                ) : (
                    <Play className="h-5 w-5 text-black ml-0.5" fill="currentColor" />
                )}
            </Button>

            {/* Next */}
            <Button
                variant="ghost"
                size="icon"
                onClick={next}
                className="h-8 w-8 text-gray-400 hover:text-white"
            >
                <SkipForward className="h-5 w-5" fill="currentColor" />
            </Button>

            {/* Repeat */}
            <Button
                variant="ghost"
                size="icon"
                onClick={handleRepeat}
                className={cn(
                    'h-8 w-8 transition-colors',
                    repeat !== 'off' ? 'text-purple-400' : 'text-gray-400 hover:text-white'
                )}
            >
                {repeat === 'one' ? (
                    <Repeat1 className="h-4 w-4" />
                ) : (
                    <Repeat className="h-4 w-4" />
                )}
            </Button>
        </div>
    );
}
