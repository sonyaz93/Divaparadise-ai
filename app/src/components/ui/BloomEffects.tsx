import React from 'react';
import { Canvas } from '@react-three/fiber';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import { OrbitControls, Text, Float } from '@react-three/drei';
import { cn } from '@/lib/utils';

interface BloomEffectsProps {
    className?: string;
}

export const BloomEffects: React.FC<BloomEffectsProps> = ({ className }) => {
    return (
        <div className={cn("w-full h-[400px] rounded-2xl overflow-hidden bg-black border border-white/10", className)}>
            <Canvas camera={{ position: [0, 0, 5] }}>
                <color attach="background" args={['#050505']} />

                <Float speed={2} rotationIntensity={1.5} floatIntensity={2}>
                    <Text
                        fontSize={1}
                        color="#fff" // Base color white
                        anchorX="center"
                        anchorY="middle"
                    >
                        NEON
                        <meshStandardMaterial
                            color="#ff00ff"
                            emissive="#ff00ff"
                            emissiveIntensity={2} // Key for Bloom
                            toneMapped={false}
                        />
                    </Text>
                </Float>

                <Float speed={1.5} rotationIntensity={2} floatIntensity={1} position={[2, -1, -2]}>
                    <mesh>
                        <icosahedronGeometry args={[0.8, 0]} />
                        <meshStandardMaterial
                            color="#00ffff"
                            emissive="#00ffff"
                            emissiveIntensity={3}
                            toneMapped={false}
                        />
                    </mesh>
                </Float>

                <Float speed={2.5} rotationIntensity={1} floatIntensity={3} position={[-2, 1, -1]}>
                    <mesh>
                        <torusKnotGeometry args={[0.6, 0.2, 128, 16]} />
                        <meshStandardMaterial
                            color="#ffaa00"
                            emissive="#ffaa00"
                            emissiveIntensity={2}
                            toneMapped={false}
                        />
                    </mesh>
                </Float>

                <OrbitControls enableZoom={false} />

                {/* Postprocessing Effects */}
                <EffectComposer>
                    <Bloom
                        luminanceThreshold={0.2}
                        mipmapBlur
                        intensity={1.5}
                        radius={0.6}
                    />
                </EffectComposer>
            </Canvas>
            <div className="absolute top-4 left-4 bg-black/50 px-3 py-1 rounded-full text-xs text-white/70 pointer-events-none">
                R3F + Postprocessing (Bloom)
            </div>
        </div>
    );
};
