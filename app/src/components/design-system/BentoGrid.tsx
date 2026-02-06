import { motion } from "framer-motion";
import { ArrowRight, Box, Image, Music, Zap } from "lucide-react";

const items = [
    {
        title: "Smart Videos",
        description: "Seamlessly integrated video content that reacts to user interaction.",
        icon: <Box className="w-6 h-6" />,
        colSpan: "col-span-12 md:col-span-8",
        bg: "bg-gradient-to-br from-purple-900/50 to-indigo-900/50",
    },
    {
        title: "Macro Animations",
        description: "Large scale motion for impact.",
        icon: <Zap className="w-6 h-6" />,
        colSpan: "col-span-12 md:col-span-4",
        bg: "bg-white/5",
    },
    {
        title: "3D Graphics",
        description: "Immersive 3D experiences directly in the browser.",
        icon: <Box className="w-6 h-6" />,
        colSpan: "col-span-12 md:col-span-4",
        bg: "bg-pink-900/20",
    },
    {
        title: "Audio Visualization",
        description: "Real-time frequency analysis.",
        icon: <Music className="w-6 h-6" />,
        colSpan: "col-span-12 md:col-span-4",
        bg: "bg-blue-900/20",
    },
    {
        title: "Blending Modes",
        description: "Advanced CSS blending.",
        icon: <Image className="w-6 h-6" />,
        colSpan: "col-span-12 md:col-span-4",
        bg: "bg-white/5",
    },
];

export function BentoGrid() {
    return (
        <div className="grid grid-cols-12 gap-4 auto-rows-[200px]">
            {items.map((item, i) => (
                <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: i * 0.1 }}
                    viewport={{ once: true }}
                    className={`${item.colSpan} ${item.bg} relative rounded-3xl p-6 border border-white/10 overflow-hidden group hover:border-white/20 transition-colors`}
                >
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent pointer-events-none" />

                    <div className="absolute top-6 right-6 p-2 rounded-full bg-white/10 group-hover:bg-white/20 transition-colors">
                        {item.icon}
                    </div>

                    <div className="absolute bottom-6 left-6 right-6">
                        <h3 className="text-xl font-bold mb-2 text-white group-hover:text-purple-300 transition-colors">
                            {item.title}
                        </h3>
                        <p className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors">
                            {item.description}
                        </p>

                        <div className="mt-4 flex items-center gap-2 text-xs font-medium text-white/50 opacity-0 group-hover:opacity-100 transition-opacity translate-y-2 group-hover:translate-y-0">
                            EXPLORE <ArrowRight className="w-3 h-3" />
                        </div>
                    </div>
                </motion.div>
            ))}
        </div>
    );
}
