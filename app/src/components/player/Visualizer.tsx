import { useEffect, useRef, useState } from 'react';
import { usePlayerStore } from '../../store/playerStore';
import { useAudioEngine } from '../../hooks/useAudioEngine';

interface VisualizerProps {
    barCount?: number;
}

export function Visualizer({ barCount = 32 }: VisualizerProps) {
    const { howl, isPlaying } = usePlayerStore();
    const { getSpectrum, isLoaded } = useAudioEngine();
    const [bars, setBars] = useState<number[]>(new Array(barCount).fill(0));
    const requestRef = useRef<number>(null);
    const analyserRef = useRef<AnalyserNode | null>(null);

    useEffect(() => {
        if (!howl || !isLoaded) return;

        // Connect Howler to Web Audio Analyser
        // Howler.js internal: howl._sounds[0]._node is the BufferSource or MediaElementSource
        try {
            // @ts-ignore - Accessing howler internals to connect analyser
            const audioCtx = (window.Howler as any).ctx;
            if (!audioCtx) return;

            const analyser = audioCtx.createAnalyser();
            analyser.fftSize = 256;
            analyserRef.current = analyser;

            // Connect Howler master gain to our analyser
            // @ts-ignore
            const masterGain = (window.Howler as any).masterGain;
            if (masterGain) {
                masterGain.connect(analyser);
            }

            const update = () => {
                if (!isPlaying) {
                    setBars(prev => prev.map(b => b * 0.9)); // Smooth fade out
                    requestRef.current = requestAnimationFrame(update);
                    return;
                }

                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);
                analyser.getByteFrequencyData(dataArray);

                // Use Rust Engine to process spectrum data
                const spectrum = getSpectrum(dataArray, barCount);
                setBars(Array.from(spectrum));

                requestRef.current = requestAnimationFrame(update);
            };

            requestRef.current = requestAnimationFrame(update);
        } catch (e) {
            console.error('Visualizer connection error:', e);
        }

        return () => {
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
        };
    }, [howl, isPlaying, isLoaded, getSpectrum, barCount]);

    return (
        <div className="flex items-end justify-center gap-1 h-12 w-full px-4 overflow-hidden">
            {bars.map((height, i) => (
                <div
                    key={i}
                    className="w-1 bg-gradient-to-t from-purple-600 via-indigo-500 to-purple-400 rounded-full transition-all duration-75"
                    style={{
                        height: `${Math.max(10, height * 100)}%`,
                        opacity: 0.3 + (height * 0.7),
                        boxShadow: height > 0.5 ? '0 0 10px rgba(168, 85, 247, 0.4)' : 'none'
                    }}
                />
            ))}
        </div>
    );
}
