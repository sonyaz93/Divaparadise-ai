import { motion } from 'framer-motion';
import { SongCard3D } from './SongCard3D';

const songs = [
    {
        title: "Midnight Tokyo",
        artist: "Neon Drifter",
        image: "https://images.unsplash.com/photo-1621360841012-3f82bd6d3a74?w=500&auto=format&fit=crop&q=60",
        bpm: "128",
        genre: "Synthwave",
        price: "$1.29",
        color: "bg-purple-600"
    },
    {
        title: "Digital Soul",
        artist: "Cyber Heart",
        image: "https://images.unsplash.com/photo-1619983081593-e2ba5b543e6d?w=500&auto=format&fit=crop&q=60",
        bpm: "90",
        genre: "R&B Future",
        price: "$0.99",
        color: "bg-pink-600"
    },
    {
        title: "Quantum Bass",
        artist: "Low End Theory",
        image: "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?w=500&auto=format&fit=crop&q=60",
        bpm: "174",
        genre: "Drum & Bass",
        price: "$1.49",
        color: "bg-cyan-600"
    },
    {
        title: "Ethereal Dream",
        artist: "Atmosphere",
        image: "https://images.unsplash.com/photo-1514525253440-b393452e8d26?w=500&auto=format&fit=crop&q=60",
        bpm: "110",
        genre: "Ambient",
        price: "$1.29",
        color: "bg-indigo-600"
    }
];

export function MusicProductGrid() {
    return (
        <div className="w-full">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {songs.map((song, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1, duration: 0.5 }}
                        viewport={{ once: true }}
                    >
                        <SongCard3D {...song} />
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
