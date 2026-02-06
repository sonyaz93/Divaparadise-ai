import { Canvas, useFrame } from "@react-three/fiber";
import { Float, ContactShadows, Environment } from "@react-three/drei";
import { useRef, useState } from "react";
import * as THREE from 'three';

function AnimatedShape(props: any) {
    const meshRef = useRef<THREE.Mesh>(null!);
    const [hovered, setHover] = useState(false);

    useFrame((_, delta) => {
        meshRef.current.rotation.x += delta * 0.5;
        meshRef.current.rotation.y += delta * 0.2;
        // meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.2;
    });

    return (
        <mesh
            {...props}
            ref={meshRef}
            onPointerOver={() => setHover(true)}
            onPointerOut={() => setHover(false)}
            scale={hovered ? 1.2 : 1}
        >
            <icosahedronGeometry args={[1, 1]} />
            <meshStandardMaterial
                color={hovered ? "#ec4899" : "#8b5cf6"}
                roughness={0.1}
                metalness={0.8}
                wireframe={!hovered}
            />
        </mesh>
    );
}

export function ThreeDObject() {
    return (
        <div className="w-full h-[400px] bg-gradient-to-b from-gray-900 to-black rounded-xl overflow-hidden border border-white/10 relative">
            <div className="absolute top-6 left-6 z-10 pointer-events-none">
                <h3 className="text-2xl font-bold text-white">3D Motion</h3>
                <p className="text-gray-400 text-sm">Interactive WebGL Objects</p>
            </div>

            <Canvas camera={{ position: [0, 0, 4], fov: 50 }}>
                <ambientLight intensity={0.5} />
                <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} />
                <pointLight position={[-10, -10, -10]} intensity={0.5} />

                <Float speed={2} rotationIntensity={1} floatIntensity={1}>
                    <AnimatedShape position={[0, 0, 0]} />
                </Float>

                <ContactShadows position={[0, -2, 0]} opacity={0.5} scale={10} blur={2.5} far={4} />
                <Environment preset="city" />
            </Canvas>
        </div>
    );
}
