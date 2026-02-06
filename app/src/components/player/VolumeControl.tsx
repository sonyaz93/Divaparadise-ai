import { usePlayerStore } from '../../store/playerStore';
import { Volume2, VolumeX } from 'lucide-react';
import { Slider } from '../ui/slider';
import { Button } from '../ui/button';

export function VolumeControl() {
    const { volume, isMuted, setVolume, toggleMute } = usePlayerStore();

    const handleVolumeChange = (value: number[]) => {
        setVolume(value[0]);
    };

    const displayVolume = isMuted ? 0 : volume;

    return (
        <div className="flex items-center gap-2 w-32">
            <Button
                variant="ghost"
                size="icon"
                onClick={toggleMute}
                className="h-8 w-8 text-gray-400 hover:text-white"
            >
                {isMuted || volume === 0 ? (
                    <VolumeX className="h-4 w-4" />
                ) : (
                    <Volume2 className="h-4 w-4" />
                )}
            </Button>

            <Slider
                value={[displayVolume]}
                max={1}
                step={0.01}
                onValueChange={handleVolumeChange}
                className="flex-1"
            />
        </div>
    );
}
