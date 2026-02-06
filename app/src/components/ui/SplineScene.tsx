import React, { Suspense } from 'react';
import Spline from '@splinetool/react-spline';
import { cn } from '@/lib/utils';

interface SplineSceneProps {
    sceneUrl?: string; // Default to a cool demo info if none provided
    className?: string;
}

export const SplineScene: React.FC<SplineSceneProps> = ({
    sceneUrl = "https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode", // Common demo URL
    className
}) => {
    return (
        <div className={cn("w-full h-[500px] relative rounded-2xl overflow-hidden bg-black/20 border border-white/10", className)}>
            <div className="absolute inset-0 flex items-center justify-center text-white/20 animate-pulse">
                Loading 3D Scene...
            </div>
            <Suspense fallback={<div className="text-white">Loading...</div>}>
                <Spline scene={sceneUrl} />
            </Suspense>

            {/* Overlay to Prevent Hijacking Scroll if needed, or just decoration */}
            <div className="absolute bottom-4 right-4 bg-black/50 px-3 py-1 rounded-full text-xs text-white/50 pointer-events-none">
                Interactive 3D
            </div>
        </div>
    );
};
