import { Leaf } from "lucide-react";
import { motion } from "framer-motion";

export function EcoStyle() {
    return (
        <div className="relative bg-[#2c3325] rounded-tl-[80px] rounded-br-[80px] p-12 overflow-hidden shadow-2xl">
            {/* Texture */}
            <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(#4a5d3f 1px, transparent 1px)', backgroundSize: '16px 16px' }}></div>

            <div className="relative z-10 grid md:grid-cols-2 gap-8 items-center">
                <div className="space-y-6">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#8f9e83] text-[#bfccb5] text-xs tracking-wider uppercase">
                        <Leaf className="w-3 h-3" /> Sustainable Design
                    </div>
                    <h2 className="text-5xl font-serif text-[#e3e8df] leading-tight">
                        Rugged &<br />
                        <span className="italic text-[#8f9e83]">Organic.</span>
                    </h2>
                    <p className="text-[#a4b09b] leading-relaxed">
                        Reconnecting digital spaces with natural textures, earth tones, and softened geometry.
                    </p>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-8 py-4 bg-[#e3e8df] text-[#2c3325] rounded-full font-semibold hover:bg-[#8f9e83] hover:text-white transition-colors"
                    >
                        Explore Nature
                    </motion.button>
                </div>

                <div className="relative">
                    <motion.div
                        className="w-full aspect-square rounded-full border border-[#8f9e83]/30 flex items-center justify-center p-8"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 60, ease: "linear", repeat: Infinity }}
                    >
                        <div className="w-full h-full rounded-full border border-[#8f9e83]/50 border-dashed" />
                    </motion.div>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-32 h-48 bg-[#4a5d3f] rounded-t-[100px] rounded-b-2xl shadow-lg" />
                    </div>
                </div>
            </div>
        </div>
    );
}
