import { motion } from "framer-motion";
import { Play, Heart, Music, Plus, ShoppingCart } from "lucide-react";

interface SongCardProps {
    image: string;
    title: string;
    artist: string;
    bpm: string;
    genre: string;
    price: string;
    color: string;
}

export function SongCard3D({ image, title, artist, bpm, genre, price, color }: SongCardProps) {
    return (
        <div className="group h-[420px] w-full [perspective:1000px] cursor-pointer">
            <div className="relative h-full w-full rounded-2xl shadow-xl transition-all duration-700 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">

                {/* Front Side */}
                <div className="absolute inset-0 h-full w-full rounded-2xl bg-black border border-white/10 overflow-hidden flex flex-col [backface-visibility:hidden]">
                    {/* Parallax Image Background */}
                    <div className="relative h-3/4 overflow-hidden">
                        <img src={image} alt="Album Art" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent" />

                        {/* Floating 3D Elements */}
                        <motion.div
                            className="absolute top-4 right-4 bg-white/10 backdrop-blur-md p-2 rounded-full border border-white/20"
                            animate={{ y: [0, -10, 0], rotate: [0, 10, 0] }}
                            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                        >
                            <Music className="w-5 h-5 text-white" />
                        </motion.div>

                        <motion.div
                            className="absolute bottom-4 left-4 bg-white/10 backdrop-blur-md px-3 py-1 rounded-full border border-white/20"
                            animate={{ x: [0, 5, 0] }}
                            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                        >
                            <span className="text-xs font-bold text-white uppercase tracking-wider">New Release</span>
                        </motion.div>
                    </div>

                    <div className="h-1/4 p-4 flex justify-between items-center bg-zinc-900/50 backdrop-blur-md">
                        <div>
                            <h3 className="text-lg font-bold text-white truncate w-40">{title}</h3>
                            <p className="text-sm text-gray-400">{artist}</p>
                        </div>
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${color}`}>
                            <Play className="w-5 h-5 text-white fill-current" />
                        </div>
                    </div>
                </div>

                {/* Back Side */}
                <div className="absolute inset-0 h-full w-full rounded-2xl bg-zinc-900 p-6 flex flex-col justify-between [transform:rotateY(180deg)] [backface-visibility:hidden] border border-white/10 relative overflow-hidden">
                    {/* Background Blob */}
                    <div className={`absolute -top-20 -right-20 w-60 h-60 ${color} opacity-20 blur-3xl rounded-full`} />

                    <div>
                        <div className="flex justify-between items-start mb-6">
                            <div className="flex gap-2">
                                <span className="bg-white/10 px-2 py-1 rounded-md text-[10px] text-white/70 uppercase border border-white/5">{genre}</span>
                                <span className="bg-white/10 px-2 py-1 rounded-md text-[10px] text-white/70 uppercase border border-white/5">{bpm} BPM</span>
                            </div>
                            <Heart className="w-6 h-6 text-gray-400 hover:text-red-500 transition-colors" />
                        </div>

                        <div className="space-y-4 mb-6">
                            <h3 className="text-2xl font-black text-white leading-none">{title}</h3>
                            <div className="h-16 flex items-end gap-1 opacity-50">
                                {/* Fake Waveform */}
                                {[40, 70, 30, 80, 50, 90, 20, 60, 40, 80, 30, 70].map((h, i) => (
                                    <motion.div
                                        key={i}
                                        initial={{ height: 10 }}
                                        animate={{ height: `${h}%` }}
                                        transition={{ duration: 0.5, repeat: Infinity, repeatType: 'mirror', delay: i * 0.05 }}
                                        className={`w-1 ${color} rounded-t-full`}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="space-y-3">
                        <button className={`w-full py-3 ${color} rounded-xl font-bold text-white flex items-center justify-center gap-2 hover:brightness-110 transition-all shadow-lg`}>
                            <ShoppingCart className="w-4 h-4" />
                            <span>BUY {price}</span>
                        </button>
                        <button className="w-full py-3 bg-white/5 rounded-xl font-bold text-white border border-white/10 flex items-center justify-center gap-2 hover:bg-white/10 transition-all">
                            <Plus className="w-4 h-4" />
                            <span>ADD TO LIBRARY</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
