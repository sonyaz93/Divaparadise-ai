import { usePlayerStore } from '../../store/playerStore';
import { Slider } from '../ui/slider';
import { formatTime } from '../../lib/musicData';

export function ProgressBar() {
    const { currentTime, duration, seek } = usePlayerStore();

    const handleSeek = (value: number[]) => {
        seek(value[0]);
    };

    return (
        <div className="w-full flex items-center gap-2">
            <span className="text-xs text-gray-400 w-10 text-right">
                {formatTime(currentTime)}
            </span>

            <Slider
                value={[currentTime]}
                max={duration || 100}
                step={0.1}
                onValueChange={handleSeek}
                className="flex-1 cursor-pointer"
            />

            <span className="text-xs text-gray-400 w-10">
                {formatTime(duration)}
            </span>
        </div>
    );
}
