import { motion } from "framer-motion";
import { useState } from "react";

export function FramerDemo() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="p-8 flex flex-col items-center gap-8 bg-black/20 rounded-xl backdrop-blur-sm border border-white/10">

            <div className="space-y-2 text-center">
                <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
                    Framer Motion Demo
                </h2>
                <p className="text-muted-foreground">Examples of animations you can now use</p>
            </div>

            {/* 1. Scale & Hover Effect */}
            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold shadow-lg hover:shadow-purple-500/50 transition-shadow"
            >
                Hover & Click Me!
            </motion.button>

            {/* 2. Toggle Animation */}
            <div className="flex flex-col items-center gap-4">
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="text-sm text-purple-300 hover:text-purple-200 underline"
                >
                    Toggle Reveal
                </button>

                <motion.div
                    layout
                    initial={{ opacity: 0, height: 0 }}
                    animate={{
                        opacity: isOpen ? 1 : 0,
                        height: isOpen ? "auto" : 0
                    }}
                    transition={{ duration: 0.3 }}
                    className="bg-white/10 p-4 rounded-lg overflow-hidden max-w-xs text-center"
                >
                    <p>
                        ✨ This content animates in and out smoothly using Framer Motion!
                    </p>
                </motion.div>
            </div>

            {/* 3. Drag Gesture */}
            <div className="relative w-full h-32 bg-white/5 rounded-xl flex items-center justify-center overflow-hidden border border-white/10 group">
                <p className="absolute text-xs text-white/30 pointer-events-none">Drag the circle</p>
                <motion.div
                    drag
                    dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
                    className="w-12 h-12 bg-pink-500 rounded-full shadow-lg cursor-grab active:cursor-grabbing"
                    whileDrag={{ scale: 1.2, boxShadow: "0px 0px 20px rgba(236, 72, 153, 0.5)" }}
                />
            </div>

        </div>
    );
}
