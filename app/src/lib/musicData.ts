import type { Track, Video } from '../types/music';

// Genres with premium images
export const musicGenres = [
    { id: 'lofi', title: 'Lo-Fi Chill', image: '/images/Genre/lofi.png', color: 'bg-purple-900/40' },
    { id: 'acoustic', title: 'Acoustic Soul', image: '/images/Genre/acoustic.png', color: 'bg-amber-900/40' },
    { id: 'jazz', title: 'Midnight Jazz', image: '/images/Genre/jazz.png', color: 'bg-blue-900/40' },
    { id: 'electronic', title: 'Electric Night', image: '/genre_electronic.jpg', color: 'bg-indigo-900/40' },
];

// Mock Suno tracks - อัปเดตการใช้ภาพ Placeholder และ Genre Images
export const mockTracks: Track[] = [
    {
        id: '1',
        title: 'Careless Whisper (Karaoke)',
        artist: 'Tamia',
        album: 'Favorities',
        duration: 300,
        audioUrl: '/video/mp4/Careless Whisper - by Tamia  FEMALE KEY (Karaoke Version).mp4',
        coverImage: '/images/Genre/jazz.png',
        genre: 'Jazz',
        releaseDate: '2024-02-01',
    },
    {
        id: '2',
        title: 'Más Allá (Beyond)',
        artist: 'Gloria Estefan',
        album: 'Favorities',
        duration: 240,
        audioUrl: '/video/3GPP/Más Allá (Beyond).3gpp',
        coverImage: '/images/Genre/acoustic.png',
        genre: 'Acoustic',
        releaseDate: '2024-02-05',
    },
];

export const mockVideos: Video[] = [
    {
        id: 'v1',
        title: 'Careless Whisper (Karaoke)',
        artist: 'Tamia (Female Key)',
        videoUrl: '/video/mp4/Careless Whisper - by Tamia  FEMALE KEY (Karaoke Version).mp4',
        thumbnailUrl: '/images/Genre/jazz.png', // Temporary thumbnail
    },
    {
        id: 'v2',
        title: 'Más Allá (Beyond)',
        artist: 'Gloria Estefan',
        videoUrl: '/video/3GPP/Más Allá (Beyond).3gpp',
        thumbnailUrl: '/images/Genre/acoustic.png', // Temporary thumbnail
    }
];

// Helper function to format duration
export function formatDuration(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Helper to format time for display
export function formatTime(seconds: number): string {
    if (isNaN(seconds) || !isFinite(seconds)) return '0:00';
    return formatDuration(seconds);
}
