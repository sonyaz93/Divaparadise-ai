import React from 'react';
import Tilt from 'react-parallax-tilt';
import { cn } from '@/lib/utils';

interface HolographicTiltProps {
    children: React.ReactNode;
    className?: string;
}

export const HolographicTilt: React.FC<HolographicTiltProps> = ({ children, className }) => {
    return (
        <Tilt
            glareEnable={true}
            glareMaxOpacity={0.45}
            scale={1.05}
            perspective={1000}
            transitionSpeed={1500}
            className={cn("transform-style-3d", className)}
        >
            <div className="relative w-full h-full transform-style-3d">
                {children}
                {/* Simple Holographic Overlay for extra style */}
                <div className="absolute inset-0 bg-gradient-to-tr from-white/10 to-transparent opacity-20 pointer-events-none rounded-xl" />
            </div>
        </Tilt>
    );
};
