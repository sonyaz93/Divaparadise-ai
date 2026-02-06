import { useRef, type MouseEvent } from "react";
import { motion, useMotionTemplate, useMotionValue, useSpring } from "framer-motion";
import { Disc, Play, Heart, Share2 } from "lucide-react";

export function AlbumCard3D() {
    const ref = useRef<HTMLDivElement>(null);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    const xSpring = useSpring(x, { stiffness: 300, damping: 20 });
    const ySpring = useSpring(y, { stiffness: 300, damping: 20 });

    const transform = useMotionTemplate`rotateX(${xSpring}deg) rotateY(${ySpring}deg)`;

    const handleMouseMove = (e: MouseEvent) => {
        if (!ref.current) return;

        const rect = ref.current.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;

        const mouseX = (e.clientX - rect.left) * 32.5;
        const mouseY = (e.clientY - rect.top) * 32.5;

        const rX = (mouseY / height - 32.5 / 2) * -1;
        const rY = mouseX / width - 32.5 / 2;

        x.set(rX);
        y.set(rY);
    };

    const handleMouseLeave = () => {
        x.set(0);
        y.set(0);
    };

    return (
        <div className="flex items-center justify-center p-12 perspective-1000">
            <motion.div
                ref={ref}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                style={{
                    transformStyle: "preserve-3d",
                    transform,
                }}
                className="relative w-80 h-80 group cursor-pointer"
            >
                {/* Vinyl Record (Slides out) */}
                <div
                    className="absolute top-2 left-2 right-2 bottom-2 rounded-full bg-black flex items-center justify-center shadow-xl transition-transform duration-700 ease-out group-hover:translate-x-32 group-hover:rotate-[360deg]"
                    style={{ transform: "translateZ(-10px)" }}
                >
                    <div className="absolute inset-0 rounded-full border border-white/10"
                        style={{ background: 'repeating-radial-gradient(#111 0, #111 2px, #222 3px, #222 4px)' }}
                    />
                    {/* Record Label */}
                    <div className="w-1/3 h-1/3 bg-gradient-to-tr from-pink-500 to-purple-500 rounded-full flex items-center justify-center z-10 border-4 border-black">
                        <Disc className="w-6 h-6 text-white animate-spin-slow" />
                    </div>
                </div>

                {/* Album Cover (Top Layer) */}
                <div
                    className="absolute inset-0 bg-white rounded-lg shadow-2xl overflow-hidden border border-white/10"
                    style={{ transform: "translateZ(20px)" }}
                >
                    <img
                        src="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=500&auto=format&fit=crop&q=60"
                        alt="Album Art"
                        className="w-full h-full object-cover"
                    />

                    {/* Dark Overlay on Hover */}
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4 backdrop-blur-[2px]">
                        <button className="p-3 bg-white/20 rounded-full hover:bg-white hover:text-black transition-colors backdrop-blur-md">
                            <Heart className="w-6 h-6" />
                        </button>
                        <button className="p-4 bg-purple-600 rounded-full hover:scale-110 transition-transform shadow-lg shadow-purple-500/50">
                            <Play className="w-8 h-8 text-white fill-current" />
                        </button>
                        <button className="p-3 bg-white/20 rounded-full hover:bg-white hover:text-black transition-colors backdrop-blur-md">
                            <Share2 className="w-6 h-6" />
                        </button>
                    </div>

                    {/* Album Info Pinned */}
                    <div className="absolute bottom-4 left-4 right-4 z-20 translate-y-2 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-500">
                        <div className="bg-black/60 backdrop-blur-md p-3 rounded-lg border border-white/10">
                            <h3 className="text-white font-bold truncate">Neon Paradise</h3>
                            <p className="text-gray-300 text-xs">Synthwave Collection</p>
                        </div>
                    </div>
                </div>

                {/* 3D Reflection/Sheen */}
                <div
                    className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/10 to-white/0 rounded-lg pointer-events-none mix-blend-overlay z-50"
                    style={{ transform: "translateZ(30px)" }}
                />
            </motion.div>

            <style>{`
        .perspective-1000 {
            perspective: 1000px;
        }
        .animate-spin-slow {
            animation: spin 3s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
      `}</style>
        </div>
    );
}
