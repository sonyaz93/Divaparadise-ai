import { motion } from "framer-motion";
import { ShoppingBag, Star } from "lucide-react";

export function FlipCard3D() {
    return (
        <div className="group h-96 w-72 [perspective:1000px] cursor-pointer">
            <div className="relative h-full w-full rounded-xl shadow-xl transition-all duration-500 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">

                {/* Front Side */}
                <div className="absolute inset-0 h-full w-full rounded-xl bg-gradient-to-br from-gray-900 to-black border border-white/10 p-6 flex flex-col items-center justify-between [backface-visibility:hidden]">
                    <div className="w-full flex justify-between items-start">
                        <div className="bg-white/10 px-3 py-1 rounded-full backdrop-blur-md border border-white/10">
                            <span className="text-[10px] font-bold text-white tracking-widest uppercase">New Arrival</span>
                        </div>
                        <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                    </div>

                    <div className="relative z-10 w-full flex justify-center py-4">
                        {/* Floating Sneaker Effect */}
                        <motion.img
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                            src="https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=60"
                            alt="Nike Shoe"
                            className="w-48 h-48 object-contain drop-shadow-[0_20px_20px_rgba(0,0,0,0.5)] -rotate-[25deg]"
                        />
                        <div className="absolute inset-x-0 bottom-0 h-2 bg-black/50 blur-xl rounded-full" />
                    </div>

                    <div className="w-full">
                        <h3 className="text-2xl font-black text-white italic uppercase tracking-tighter">AIR STRIDE</h3>
                        <p className="text-white/60 text-sm">Next Gen Running</p>
                        <div className="flex justify-between items-end mt-4">
                            <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-cyan-400">$189.00</span>
                            <span className="text-xs text-white/40 mb-1">HOVER TO BUY</span>
                        </div>
                    </div>

                    {/* Shine Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/5 to-white/0 pointer-events-none rounded-xl" />
                </div>

                {/* Back Side */}
                <div className="absolute inset-0 h-full w-full rounded-xl bg-white text-black p-8 flex flex-col [transform:rotateY(180deg)] [backface-visibility:hidden]">
                    <h3 className="text-xl font-bold mb-2">Select Size</h3>
                    <div className="grid grid-cols-4 gap-2 mb-6">
                        {['7', '8', '9', '10', '11', '12'].map((size) => (
                            <button key={size} className="w-full aspect-square rounded-lg border border-gray-200 hover:border-black hover:bg-black hover:text-white transition-colors text-sm font-medium flex items-center justify-center">
                                {size}
                            </button>
                        ))}
                    </div>

                    <h3 className="text-xl font-bold mb-2">Description</h3>
                    <p className="text-xs text-gray-500 leading-relaxed mb-auto">
                        Engineered for speed. Features a breathable mesh upper and our signature responsive cushioning for maximum energy return.
                    </p>

                    <button className="w-full py-4 bg-black text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-gray-800 transition-colors group/btn">
                        <ShoppingBag className="w-4 h-4" />
                        <span>ADD TO CART</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
