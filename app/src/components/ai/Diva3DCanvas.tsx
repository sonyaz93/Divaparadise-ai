import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Sparkles, PerspectiveCamera, Environment, ContactShadows, Float, useGLTF } from '@react-three/drei';
import { PortraitElegance } from './avatars/PortraitElegance';

// Preload assets
useGLTF.preload('/images/AI/item/diva_elegance.glb');

const Diva3DCanvas = () => {
    // Determine Lighting Configuration for Elegance
    const lightingConfig = { point1: '#ffffff', point2: '#ffe4c4', ambient: 2.0 };

    return (
        <div className="w-full h-full min-h-[220px]">
            <Canvas
                shadows
                gl={{ antialias: true, alpha: true }}
            >
                <PerspectiveCamera makeDefault position={[0, 0, 4]} fov={35} />

                <ambientLight intensity={lightingConfig.ambient} />
                <spotLight position={[5, 10, 5]} angle={0.3} penumbra={1} intensity={6} castShadow color="#ffffff" />
                <pointLight position={[-5, 5, -5]} intensity={8} color={lightingConfig.point1} />
                <pointLight position={[5, 5, 5]} intensity={8} color={lightingConfig.point2} />
                <directionalLight position={[0, 10, 0]} intensity={2} />

                <Suspense fallback={null}>
                    <Environment preset="city" />
                    <ContactShadows position={[0, -2, 0]} opacity={0.5} scale={10} blur={2.5} far={4} />

                    {/* Floating Animation Wrapper */}
                    <Float
                        speed={2.2}
                        rotationIntensity={0.3}
                        floatIntensity={0.4}
                    >
                        <PortraitElegance />
                    </Float>

                    <Sparkles count={50} scale={5} size={2} speed={0.4} opacity={0.5} color={lightingConfig.point1} />
                </Suspense>
            </Canvas>
        </div>
    );
};

export default Diva3DCanvas;
