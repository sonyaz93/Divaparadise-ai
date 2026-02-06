import { motion } from "framer-motion";

export function TypographyShowcase() {
    return (
        <div className="space-y-12">
            {/* 1. Gradient Hero Text */}
            <div className="space-y-4">
                <p className="text-sm uppercase tracking-[0.3em] text-gray-500">Expressive Typography</p>
                <h2 className="text-8xl font-black tracking-tighter mix-blend-overlay text-white opacity-20 select-none">
                    IMPACT
                </h2>
                <h2 className="text-7xl font-bold tracking-tight bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400 bg-clip-text text-transparent -mt-20 ml-2">
                    Meaningful<br />Motion.
                </h2>
            </div>

            {/* 2. Negative Space Text */}
            <div className="bg-white text-black p-12 rounded-3xl overflow-hidden relative cursor-hover group">
                <h3 className="text-6xl font-bold relative z-10 mix-blend-difference text-white">
                    Negative<br />SPACE
                </h3>
                <motion.div
                    className="absolute top-0 right-0 w-64 h-64 bg-black rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 opacity-20 group-hover:scale-150 transition-transform duration-700"
                />
                <p className="relative z-10 mt-6 max-w-sm text-lg font-medium">
                    Using whitespace as an active design element to create focus and breath.
                </p>
            </div>

            {/* 3. Experimental Stroke/Fill */}
            <div className="relative h-40 flex items-center overflow-hidden">
                <div className="absolute whitespace-nowrap text-9xl font-black text-transparent stroke-text opacity-30 animate-marquee">
                    BRUTALISM • BOLD • RAW •
                </div>
            </div>

            <style>{`
        .stroke-text {
            -webkit-text-stroke: 1px rgba(255, 255, 255, 0.5);
        }
        @keyframes marquee {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        .animate-marquee {
            animation: marquee 20s linear infinite;
        }
      `}</style>
        </div>
    );
}
