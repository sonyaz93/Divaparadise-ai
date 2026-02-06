// Track data types
export interface Track {
    id: string;
    title: string;
    artist: string;
    artistId?: string;
    album?: string;
    albumId?: string;
    duration: number; // in seconds
    audioUrl: string;
    coverImage: string;
    genre?: string;
    releaseDate?: string;
    lyrics?: string;
}

export interface Video {
    id: string;
    title: string;
    artist: string;
    videoUrl: string;
    thumbnailUrl?: string;
    duration?: number;
}

export interface Playlist {
    id: string;
    name: string;
    description?: string;
    coverImage?: string;
    tracks: Track[];
    createdAt: Date;
    updatedAt: Date;
}

export interface Artist {
    id: string;
    name: string;
    bio?: string;
    profileImage: string;
    coverImage?: string;
    genres: string[];
}

// Player state types
export type RepeatMode = 'off' | 'one' | 'all';

export interface PlayerState {
    currentTrack: Track | null;
    isPlaying: boolean;
    volume: number;
    isMuted: boolean;
    currentTime: number;
    duration: number;
    queue: Track[];
    currentIndex: number;
    repeat: RepeatMode;
    shuffle: boolean;
    originalQueue: Track[]; // for shuffle
}
