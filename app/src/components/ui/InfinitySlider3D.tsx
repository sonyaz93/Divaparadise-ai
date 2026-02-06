import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface InfinitySlider3DProps {
    children?: React.ReactNode;
    duration?: number;
    reverse?: boolean;
    className?: string;
    depth?: boolean; // Toggle 3D skew effect
}

export const InfinitySlider3D: React.FC<InfinitySlider3DProps> = ({
    children,
    duration = 20,
    reverse = false,
    className,
    depth = true, // Default to 3D mode
}) => {
    return (
        <div className={cn(
            "relative flex overflow-hidden w-full group",
            depth && "perspective-[1000px]",
            className
        )}>
            {/* 3D Container Wrapper if depth is enabled */}
            <div className={cn(
                "flex w-full",
                depth && "transform-style-3d rotate-y-[-10deg] rotate-z-[5deg] scale-110" // Simple default 3D tilt
            )}>
                <motion.div
                    className="flex gap-4 min-w-full flex-shrink-0"
                    initial={{ x: reverse ? "-100%" : "0%" }}
                    animate={{ x: reverse ? "0%" : "-100%" }}
                    transition={{
                        duration: duration,
                        ease: "linear",
                        repeat: Infinity,
                    }}
                >
                    {children}
                </motion.div>
                <motion.div
                    className="flex gap-4 min-w-full flex-shrink-0"
                    initial={{ x: reverse ? "-100%" : "0%" }}
                    animate={{ x: reverse ? "0%" : "-100%" }}
                    transition={{
                        duration: duration,
                        ease: "linear",
                        repeat: Infinity,
                    }}
                >
                    {children}
                </motion.div>
            </div>

            {/* Side Fades */}
            <div className="absolute inset-y-0 left-0 w-20 bg-gradient-to-r from-black via-transparent to-transparent z-10 pointer-events-none" />
            <div className="absolute inset-y-0 right-0 w-20 bg-gradient-to-l from-black via-transparent to-transparent z-10 pointer-events-none" />
        </div>
    );
};

// Helper for image cards
export const SliderImageCard = ({ src, alt }: { src: string; alt?: string }) => (
    <div className="relative w-[300px] h-[200px] rounded-2xl overflow-hidden shrink-0 shadow-2xl border border-white/10 group/card">
        <img
            src={src}
            alt={alt || "Slider Image"}
            className="w-full h-full object-cover transform transition-transform duration-500 group-hover/card:scale-110"
        />
        <div className="absolute inset-0 bg-black/20 group-hover/card:bg-transparent transition-colors" />
    </div>
);
