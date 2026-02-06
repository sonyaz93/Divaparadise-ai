export function GrainyGradients() {
    return (
        <div className="relative w-full h-64 rounded-3xl overflow-hidden flex items-center justify-center">
            {/* SVG Noise Filter */}
            <svg className="hidden">
                <filter id="noiseFilter">
                    <feTurbulence type="fractalNoise" baseFrequency="0.6" stitchTiles="stitch" />
                </filter>
            </svg>

            {/* Gradient Backgrounds */}
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500" />
            <div className="absolute top-0 -left-20 w-96 h-96 bg-yellow-300 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" />
            <div className="absolute -bottom-32 right-0 w-96 h-96 bg-cyan-300 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000" />

            {/* Grain Overlay */}
            <div className="absolute inset-0 opacity-40 mix-blend-soft-light" style={{ filter: 'url(#noiseFilter)' }} />

            <div className="relative z-10 text-center">
                <h3 className="text-4xl font-bold text-white drop-shadow-md mb-2">Grainy Gradients</h3>
                <p className="text-white/80 font-medium tracking-wide">Noise + Color + Blur</p>
            </div>

            <style>{`
            @keyframes blob {
                0% { transform: translate(0px, 0px) scale(1); }
                33% { transform: translate(30px, -50px) scale(1.1); }
                66% { transform: translate(-20px, 20px) scale(0.9); }
                100% { transform: translate(0px, 0px) scale(1); }
            }
            .animate-blob {
                animation: blob 7s infinite;
            }
            .animation-delay-2000 {
                animation-delay: 2s;
            }
        `}</style>
        </div>
    );
}
