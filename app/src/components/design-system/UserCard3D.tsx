import { useRef, type MouseEvent } from "react";
import { motion, useMotionTemplate, useMotionValue, useSpring } from "framer-motion";
import { Sparkles, Trophy, Music } from "lucide-react";

export function UserCard3D() {
    const ref = useRef<HTMLDivElement>(null);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    const xSpring = useSpring(x);
    const ySpring = useSpring(y);

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
                className="relative h-96 w-72 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 p-8 shadow-2xl overflow-hidden group border border-white/20"
            >
                {/* Holographic Glare Effect */}
                <div
                    className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none mix-blend-overlay z-50"
                    style={{
                        backgroundImage: 'linear-gradient(105deg, transparent 20%, rgba(255,255,255,0.4) 25%, transparent 30%)',
                        backgroundSize: '200% 200%',
                        animation: 'shine 2s infinite linear'
                    }}
                />

                {/* Floating Content Layer 1 (Base) */}
                <div
                    style={{ transform: "translateZ(20px)" }}
                    className="absolute inset-4 rounded-lg bg-black/20 backdrop-blur-sm border border-white/10 p-6 flex flex-col items-center gap-4"
                >
                    {/* Avatar */}
                    <div
                        style={{ transform: "translateZ(50px)" }}
                        className="w-24 h-24 rounded-full border-4 border-white/20 shadow-xl overflow-hidden relative"
                    >
                        <img src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=500&auto=format&fit=crop&q=60" alt="Avatar" className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/50 to-transparent mix-blend-overlay"></div>
                    </div>

                    <div style={{ transform: "translateZ(40px)" }} className="text-center">
                        <h2 className="text-2xl font-bold text-white drop-shadow-md">Songya Diva</h2>
                        <p className="text-white/60 text-sm">Pro Member</p>
                    </div>

                    <div style={{ transform: "translateZ(30px)" }} className="flex gap-4 mt-auto">
                        <div className="flex flex-col items-center gap-1 text-white/80">
                            <div className="p-2 bg-white/10 rounded-full"><Trophy className="w-4 h-4 text-yellow-300" /></div>
                            <span className="text-[10px] font-bold">LVL 99</span>
                        </div>
                        <div className="flex flex-col items-center gap-1 text-white/80">
                            <div className="p-2 bg-white/10 rounded-full"><Sparkles className="w-4 h-4 text-purple-300" /></div>
                            <span className="text-[10px] font-bold">VIP</span>
                        </div>
                        <div className="flex flex-col items-center gap-1 text-white/80">
                            <div className="p-2 bg-white/10 rounded-full"><Music className="w-4 h-4 text-pink-300" /></div>
                            <span className="text-[10px] font-bold">ARTIST</span>
                        </div>
                    </div>
                </div>
            </motion.div>

            <style>{`
        .perspective-1000 {
            perspective: 1000px;
        }
        @keyframes shine {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
      `}</style>
        </div>
    );
}
