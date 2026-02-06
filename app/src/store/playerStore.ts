import { create } from 'zustand';
import { Howl } from 'howler';
import type { Track, PlayerState, RepeatMode } from '../types/music';

interface PlayerStore extends PlayerState {
    // Internal
    howl: Howl | null;

    // Actions
    setTrack: (track: Track) => void;
    play: () => void;
    pause: () => void;
    togglePlay: () => void;
    next: () => void;
    previous: () => void;
    seek: (time: number) => void;
    setVolume: (volume: number) => void;
    toggleMute: () => void;
    setRepeat: (mode: RepeatMode) => void;
    toggleShuffle: () => void;
    setQueue: (tracks: Track[], startIndex?: number) => void;
    addToQueue: (track: Track) => void;
    removeFromQueue: (index: number) => void;
    clearQueue: () => void;
    updateTime: (time: number) => void;
    updateDuration: (duration: number) => void;
}

export const usePlayerStore = create<PlayerStore>((set, get) => ({
    // Initial state
    currentTrack: null,
    isPlaying: false,
    volume: 0.7,
    isMuted: false,
    currentTime: 0,
    duration: 0,
    queue: [],
    currentIndex: -1,
    repeat: 'off',
    shuffle: false,
    originalQueue: [],
    howl: null,

    // Set track and load audio
    setTrack: (track: Track) => {
        const { howl, volume } = get();

        // Stop and unload previous track
        if (howl) {
            howl.stop();
            howl.unload();
        }

        // Create new Howl instance
        const extension = track.audioUrl.split('.').pop()?.toLowerCase() || 'mp3';
        const format = extension === '3gpp' || extension === '3gp' ? '3gp' : (extension === 'mp4' ? 'mp4' : extension);

        const newHowl = new Howl({
            src: [track.audioUrl],
            html5: true,
            format: [format as string],
            volume: volume,
            onplay: () => set({ isPlaying: true }),
            onpause: () => set({ isPlaying: false }),
            onend: () => {
                const { repeat, next } = get();
                if (repeat === 'one') {
                    get().play();
                } else {
                    next();
                }
            },
            onload: () => {
                set({ duration: newHowl.duration() });
            },
            onloaderror: (_id, error) => {
                console.error('❌ Howler Load Error:', error);
                set({ isPlaying: false });
            },
            onplayerror: (_id, error) => {
                console.error('❌ Howler Play Error:', error);
                set({ isPlaying: false });
                howl?.unload();
            },
            onseek: () => {
                set({ currentTime: newHowl.seek() as number });
            },
        });

        set({
            currentTrack: track,
            howl: newHowl,
            currentTime: 0,
            isPlaying: false,
        });
    },

    // Playback controls
    play: () => {
        const { howl } = get();
        if (howl && !howl.playing()) {
            howl.play();
        }
    },

    pause: () => {
        const { howl } = get();
        if (howl && howl.playing()) {
            howl.pause();
        }
    },

    togglePlay: () => {
        const { isPlaying, play, pause } = get();
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    },

    next: () => {
        const { queue, currentIndex, repeat, setTrack, play } = get();

        if (queue.length === 0) return;

        let nextIndex = currentIndex + 1;

        // Handle repeat all
        if (nextIndex >= queue.length) {
            if (repeat === 'all') {
                nextIndex = 0;
            } else {
                return; // End of queue
            }
        }

        set({ currentIndex: nextIndex });
        setTrack(queue[nextIndex]);
        play();
    },

    previous: () => {
        const { queue, currentIndex, currentTime, setTrack, play, seek } = get();

        if (queue.length === 0) return;

        // If more than 3 seconds played, restart track
        if (currentTime > 3) {
            seek(0);
            return;
        }

        let prevIndex = currentIndex - 1;

        // Handle repeat all
        if (prevIndex < 0) {
            prevIndex = queue.length - 1;
        }

        set({ currentIndex: prevIndex });
        setTrack(queue[prevIndex]);
        play();
    },

    seek: (time: number) => {
        const { howl } = get();
        if (howl) {
            howl.seek(time);
            set({ currentTime: time });
        }
    },

    setVolume: (volume: number) => {
        const { howl } = get();
        const clampedVolume = Math.max(0, Math.min(1, volume));

        if (howl) {
            howl.volume(clampedVolume);
        }

        set({ volume: clampedVolume, isMuted: false });
    },

    toggleMute: () => {
        const { howl, isMuted, volume } = get();

        if (howl) {
            howl.volume(isMuted ? volume : 0);
        }

        set({ isMuted: !isMuted });
    },

    setRepeat: (mode: RepeatMode) => {
        set({ repeat: mode });
    },

    toggleShuffle: () => {
        const { shuffle, queue, currentTrack, originalQueue } = get();

        if (!shuffle) {
            // Enable shuffle: save original queue and shuffle
            const shuffled = [...queue];

            // Keep current track at its position
            const currentIndex = queue.findIndex(t => t.id === currentTrack?.id);

            // Shuffle remaining tracks
            for (let i = shuffled.length - 1; i > currentIndex + 1; i--) {
                const j = Math.floor(Math.random() * (i - currentIndex)) + currentIndex + 1;
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }

            set({
                shuffle: true,
                originalQueue: queue,
                queue: shuffled,
            });
        } else {
            // Disable shuffle: restore original queue
            set({
                shuffle: false,
                queue: originalQueue,
                originalQueue: [],
            });
        }
    },

    setQueue: (tracks: Track[], startIndex = 0) => {
        const { setTrack } = get();

        set({
            queue: tracks,
            currentIndex: startIndex,
            originalQueue: [],
            shuffle: false,
        });

        if (tracks.length > 0 && startIndex >= 0) {
            setTrack(tracks[startIndex]);
        }
    },

    addToQueue: (track: Track) => {
        const { queue } = get();
        set({ queue: [...queue, track] });
    },

    removeFromQueue: (index: number) => {
        const { queue, currentIndex } = get();
        const newQueue = queue.filter((_, i) => i !== index);

        set({
            queue: newQueue,
            currentIndex: index < currentIndex ? currentIndex - 1 : currentIndex,
        });
    },

    clearQueue: () => {
        const { howl } = get();

        if (howl) {
            howl.stop();
            howl.unload();
        }

        set({
            queue: [],
            currentIndex: -1,
            currentTrack: null,
            isPlaying: false,
            currentTime: 0,
            duration: 0,
            howl: null,
        });
    },

    updateTime: (time: number) => {
        set({ currentTime: time });
    },

    updateDuration: (duration: number) => {
        set({ duration });
    },
}));

// Time update loop
if (typeof window !== 'undefined') {
    setInterval(() => {
        const { howl, isPlaying } = usePlayerStore.getState();
        if (howl && isPlaying) {
            const currentTime = howl.seek() as number;
            usePlayerStore.getState().updateTime(currentTime || 0);
        }
    }, 100);
}
