import { motion } from "framer-motion";

export function SurrealCollage() {
    return (
        <div className="relative h-[400px] w-full overflow-hidden bg-[#e6e1d6] text-black p-8 rounded-xl isolate">
            {/* Background Texture Effect */}
            <div className="absolute inset-0 opacity-20 pointer-events-none" style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/crumpled-paper.png")' }}></div>

            <motion.div
                className="absolute top-10 left-10 w-48 h-64 bg-black overflow-hidden shadow-2xl rotate-[-6deg] z-10 border-4 border-white"
                initial={{ y: 50, opacity: 0 }}
                whileInView={{ y: 0, opacity: 1, rotate: -6 }}
                transition={{ duration: 0.8 }}
            >
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cG9ydHJhaXR8ZW58MHx8MHx8fDA%3D" alt="Portrait" className="w-full h-full object-cover sepia-[.5] grayscale-[.5]" />
            </motion.div>

            <motion.div
                className="absolute bottom-10 right-20 w-56 h-40 bg-purple-600 z-20 mix-blend-multiply opacity-80 rotate-[12deg] flex items-center justify-center p-4 text-white font-bold text-center leading-none shadow-xl"
                initial={{ scale: 0.8, opacity: 0 }}
                whileInView={{ scale: 1, opacity: 0.8, rotate: 12 }}
                transition={{ delay: 0.2, duration: 0.5 }}
            >
                DIGITAL<br />DREAMS
                <div className="absolute -top-4 -left-4 w-12 h-12 bg-yellow-400 rounded-full mix-blend-normal z-30" />
            </motion.div>

            <motion.div
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-8xl font-black text-transparent stroke-text-black z-30 pointer-events-none"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 5, repeat: Infinity }}
            >
                VISION
            </motion.div>

            {/* Tape Effect */}
            <div className="absolute top-4 left-32 w-24 h-8 bg-white/40 rotate-12 backdrop-blur-sm shadow-sm z-40 transform skew-x-12"></div>

            <style>{`
        .stroke-text-black {
            -webkit-text-stroke: 2px black;
        }
      `}</style>
        </div>
    );
}
