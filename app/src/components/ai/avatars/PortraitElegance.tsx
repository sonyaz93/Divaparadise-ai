import { useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useGLTF } from '@react-three/drei';

export function PortraitElegance() {
    const group = useRef<THREE.Group>(null);
    const gltf = useGLTF('/images/AI/item/diva_elegance.glb');
    const mixer = useRef<THREE.AnimationMixer | null>(null);

    useEffect(() => {
        if (gltf && gltf.scene) {
            const scene = gltf.scene;
            const animations = gltf.animations;

            if (animations && animations.length > 0) {
                mixer.current = new THREE.AnimationMixer(scene);
                const action = mixer.current.clipAction(animations[0]);
                action.play();
            }

            scene.position.y = -1.6;
            scene.scale.set(1.5, 1.5, 1.5);

            scene.traverse((child) => {
                if (child instanceof THREE.Mesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;

                    const materials = Array.isArray(child.material) ? child.material : [child.material];

                    materials.forEach((mat: any) => {
                        if (!mat) return;
                        const matName = mat.name.toLowerCase();
                        const meshName = child.name.toLowerCase();

                        // Portrait of Elegance: Transform Michelle -> Blonde/Jeans/White Shirt
                        if (matName.includes('skin') || matName.includes('body') || meshName.includes('body')) {
                            mat.color.set('#FFF0E0'); // Fair Skin
                            mat.emissive.set('#000000');
                            mat.emissiveIntensity = 0;
                        } else if (matName.includes('hair') || meshName.includes('hair')) {
                            mat.color.set('#E6C280'); // Blonde
                            mat.emissive.set('#000000');
                            mat.emissiveIntensity = 0;
                        } else if (matName.includes('pant') || matName.includes('bottom') || meshName.includes('bottom')) {
                            mat.color.set('#1a56db'); // Blue Jeans
                            mat.metalness = 0.1;
                            mat.roughness = 0.8;
                        } else if (matName.includes('top') || matName.includes('shirt') || meshName.includes('top')) {
                            mat.color.set('#FFFFFF'); // White Shirt
                            mat.metalness = 0;
                            mat.roughness = 0.9;
                        }
                    });
                }
            });
        }
    }, [gltf]);

    useFrame((state, delta) => {
        if (mixer.current) mixer.current.update(delta);
        if (group.current) {
            const targetX = (state.pointer.x * Math.PI) / 8;
            group.current.rotation.y = THREE.MathUtils.lerp(group.current.rotation.y, targetX, 0.1);
        }
    });

    return <primitive ref={group} object={gltf.scene} />;
}
