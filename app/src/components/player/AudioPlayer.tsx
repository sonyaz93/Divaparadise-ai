import { usePlayerStore } from '../../store/playerStore';
import { PlayerControls } from './PlayerControls';
import { ProgressBar } from './ProgressBar';
import { VolumeControl } from './VolumeControl';
import { Visualizer } from './Visualizer';
import { Music2 } from 'lucide-react';

export function AudioPlayer() {
    const { currentTrack } = usePlayerStore();

    if (!currentTrack) {
        return null; // Or show a minimal player
    }

    return (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 w-[95%] max-w-[1400px] bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl z-50 shadow-2xl shadow-purple-900/40 overflow-hidden">
            <div className="px-6 py-4">
                <div className="flex items-center justify-between gap-8">
                    {/* Left: Track Info */}
                    <div className="flex items-center gap-4 w-[30%]">
                        <div className="relative group">
                            <div className="w-14 h-14 rounded-xl bg-gray-900 overflow-hidden flex-shrink-0 shadow-lg group-hover:scale-105 transition-transform duration-300">
                                {currentTrack.coverImage ? (
                                    <img
                                        src={currentTrack.coverImage}
                                        alt={currentTrack.title}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center">
                                        <Music2 className="w-6 h-6 text-gray-400" />
                                    </div>
                                )}
                            </div>
                            <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-500 rounded-full border-2 border-black animate-pulse shadow-sm" />
                        </div>
                        <div className="min-w-0">
                            <div className="text-sm font-bold text-white truncate hover:text-purple-400 cursor-pointer transition-colors">
                                {currentTrack.title}
                            </div>
                            <div className="text-[10px] font-bold uppercase tracking-widest text-gray-500 truncate mt-0.5">
                                {currentTrack.artist}
                            </div>
                        </div>
                    </div>

                    {/* Center: Player Controls & Progress */}
                    <div className="flex-1 flex flex-col gap-1 max-w-[600px]">
                        <div className="flex justify-center items-center gap-4">
                            <PlayerControls />
                        </div>
                        <div className="px-12">
                            <Visualizer barCount={48} />
                        </div>
                        <ProgressBar />
                    </div>

                    {/* Right: Volume */}
                    <div className="w-[30%] flex justify-end">
                        <VolumeControl />
                    </div>
                </div>
            </div>
            {/* Ambient Purple Glow */}
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-purple-500/50 to-transparent opacity-50" />
        </div>
    );
}
