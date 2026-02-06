import { useEffect, useState, useRef } from 'react';
import init, { AudioEngine } from '../wasm/core_engine';

export function useAudioEngine() {
    const [isLoaded, setIsLoaded] = useState(false);
    const engineRef = useRef<AudioEngine | null>(null);

    useEffect(() => {
        const loadWasm = async () => {
            try {
                // Initialize the wasm module
                await init();

                // Create a new instance of our Rust AudioEngine
                const engine = new AudioEngine();
                engineRef.current = engine;

                setIsLoaded(true);
                console.log('🦀 Rust Audio Engine Loaded Successfully');
            } catch (err) {
                console.error('❌ Failed to load Rust Audio Engine:', err);
            }
        };

        loadWasm();

        return () => {
            if (engineRef.current) {
                engineRef.current.free();
            }
        };
    }, []);

    const processAudio = (audioData: Float32Array) => {
        if (engineRef.current && isLoaded) {
            engineRef.current.process_audio(audioData);
            return engineRef.current.get_peak();
        }
        return 0;
    };

    const getSpectrum = (freqData: Uint8Array, numBars: number) => {
        if (engineRef.current && isLoaded) {
            return engineRef.current.calculate_spectrum(freqData, numBars);
        }
        return new Float32Array(numBars).fill(0);
    };

    const setGain = (value: number) => {
        if (engineRef.current && isLoaded) {
            engineRef.current.set_gain(value);
        }
    };

    return {
        isLoaded,
        processAudio,
        getSpectrum,
        setGain,
        peak: engineRef.current?.get_peak() || 0
    };
}
