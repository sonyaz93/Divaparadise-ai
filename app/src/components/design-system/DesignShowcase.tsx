import { motion } from 'framer-motion';
import { MusicProductGrid } from './MusicProductGrid';
import { RadialMenu } from '../ui/RadialMenu';
import { InfinitySlider3D, SliderImageCard } from '../ui/InfinitySlider3D';
import { EndlessCarousel } from '../ui/EndlessCarousel';
import { Home, Settings, Heart, Share2, User, Music } from 'lucide-react';
import { BentoGrid } from './BentoGrid';
import { CustomCursor } from './CustomCursor';
import { TypographyShowcase } from './TypographyShowcase';
import { UtilitarianLayout } from './UtilitarianLayout';
import { SurrealCollage } from './SurrealCollage';
import { GrainyGradients } from './GrainyGradients';
import { EcoStyle } from './EcoStyle';
import { MinimalTypography } from './MinimalTypography';
import { ThreeDObject } from './ThreeDObject';
import { UserCard3D } from './UserCard3D';
import { AlbumCard3D } from './AlbumCard3D';
import { HolographicTilt } from '../ui/HolographicTilt';
import { SplineScene } from '../ui/SplineScene';
import { BloomEffects } from '../ui/BloomEffects';

export function DesignShowcase() {
    return (
        <div className="p-8 pb-32 min-h-screen bg-black text-white space-y-24 relative overflow-x-hidden">
            <CustomCursor />

            <div className="space-y-6 max-w-4xl relative z-10">
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-6xl md:text-8xl font-black bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 bg-clip-text text-transparent tracking-tight leading-tight"
                >
                    Design System
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.7 }}
                    transition={{ delay: 0.2 }}
                    className="text-2xl text-white font-light tracking-wide max-w-2xl px-1"
                >
                    Showcasing Micro-interactions, Bento UI & Modern Aesthetics
                </motion.p>
            </div>

            {/* Animated Radial Menu Section - Moved to top for visibility */}
            <section className="space-y-8 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-8 h-1 bg-orange-500 rounded-full" />
                    <h2 className="text-2xl font-bold tracking-tight">Animated Radial Menu</h2>
                </div>
                <div className="flex justify-center items-center py-32 bg-zinc-900/40 rounded-3xl border border-white/5 backdrop-blur-sm relative overflow-hidden">
                    {/* Interaction Area Hint */}
                    <div className="absolute inset-0 flex items-center justify-center opacity-10 pointer-events-none">
                        <div className="w-64 h-64 border border-dashed border-white rounded-full animate-spin-slow"></div>
                    </div>

                    <RadialMenu
                        radius={120}
                        items={[
                            { icon: <Home className="w-5 h-5" />, label: "Home", onClick: () => console.log('Home') },
                            { icon: <Settings className="w-5 h-5" />, label: "Settings", onClick: () => console.log('Settings') },
                            { icon: <Heart className="w-5 h-5" />, label: "Likes", onClick: () => console.log('Likes') },
                            { icon: <Share2 className="w-5 h-5" />, label: "Share", onClick: () => console.log('Share') },
                            { icon: <User className="w-5 h-5" />, label: "Profile", onClick: () => console.log('Profile') },
                            { icon: <Music className="w-5 h-5" />, label: "Library", onClick: () => console.log('Library') },
                        ]} />
                </div>
            </section>

            <section className="space-y-12 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-12 h-1 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">Music Store Experience</h2>
                </div>
                <MusicProductGrid />
            </section>

            {/* 3D Cards Grid */}
            <div className="grid md:grid-cols-2 gap-12 relative z-10">
                <section className="space-y-8">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-violet-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Holographic ID</h2>
                    </div>
                    <UserCard3D />
                </section>

                <section className="space-y-8">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-pink-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Vinyl Interaction</h2>
                    </div>
                    <AlbumCard3D />
                </section>
            </div>

            <section className="space-y-12 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-12 h-1 bg-purple-500 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">Bento Grid Layout</h2>
                </div>
                <BentoGrid />
            </section>

            <section className="space-y-12 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-12 h-1 bg-indigo-500 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">3D Objects & Motion</h2>
                </div>
                <ThreeDObject />
            </section>

            <section className="space-y-12 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-12 h-1 bg-pink-500 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">Expressive Typography & Brutalism</h2>
                </div>
                <TypographyShowcase />
            </section>

            <div className="grid md:grid-cols-2 gap-8">
                <section className="space-y-8 relative z-10">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-green-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Utilitarian Design</h2>
                    </div>
                    <UtilitarianLayout />
                </section>

                <section className="space-y-8 relative z-10">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-yellow-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Surrealism Collage</h2>
                    </div>
                    <SurrealCollage />
                </section>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
                <section className="space-y-8 relative z-10">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-cyan-500 rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Grainy Gradients</h2>
                    </div>
                    <GrainyGradients />
                </section>

                <section className="space-y-8 relative z-10">
                    <div className="flex items-center gap-4">
                        <span className="w-8 h-1 bg-[#8f9e83] rounded-full" />
                        <h2 className="text-2xl font-bold tracking-tight">Sustainable / Eco</h2>
                    </div>
                    <EcoStyle />
                </section>
            </div>

            {/* 3D Infinite Slider Section */}
            <section className="space-y-12 relative z-10 overflow-hidden py-10">
                <div className="flex items-center gap-4 mb-8">
                    <span className="w-12 h-1 bg-pink-500 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">Infinite 3D Gallery</h2>
                </div>

                <div className="space-y-8">
                    <InfinitySlider3D duration={30} className="h-[250px]">
                        <SliderImageCard src="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1619983081563-430f63602796?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1511379938547-c1f69419868d?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1000&auto=format&fit=crop" />
                    </InfinitySlider3D>

                    <InfinitySlider3D duration={35} reverse className="h-[250px]">
                        <SliderImageCard src="https://images.unsplash.com/photo-1514525253440-b393452e8d26?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1487180144351-b8472da7d491?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1506157786151-b8491531f063?q=80&w=1000&auto=format&fit=crop" />
                        <SliderImageCard src="https://images.unsplash.com/photo-1459749411177-0473ef7161eb?q=80&w=1000&auto=format&fit=crop" />
                    </InfinitySlider3D>
                </div>
            </section>

            {/* Endless Interactive Carousel Section */}
            <section className="space-y-12 relative z-10 py-10">
                <div className="flex items-center gap-4 mb-8">
                    <span className="w-12 h-1 bg-lime-400 rounded-full" />
                    <h2 className="text-4xl font-bold tracking-tight">Coverflow 3D Gallery</h2>
                </div>
                <div className="relative h-[500px] flex items-center justify-center -mx-8 sm:mx-0">
                    {/* -mx-8 to breakout on mobile if needed, or just normal container */}
                    <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-black to-transparent z-20 pointer-events-none" />
                    <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-black to-transparent z-20 pointer-events-none" />

                    <EndlessCarousel
                        className="h-full"
                        images={[
                            "https://images.unsplash.com/photo-1535905557558-afc4877a26fc?q=80&w=1000&auto=format&fit=crop",
                            "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop",
                            "https://images.unsplash.com/photo-1542202229-7d9b4b059372?q=80&w=1000&auto=format&fit=crop",
                            "https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?q=80&w=1000&auto=format&fit=crop",
                            "https://images.unsplash.com/photo-1525097487452-6278ff080c31?q=80&w=1000&auto=format&fit=crop",
                            "https://images.unsplash.com/photo-1535376472810-5d229c6bda0c?q=80&w=1000&auto=format&fit=crop"
                        ]}
                    />
                    <div className="absolute bottom-10 left-1/2 -translate-x-1/2">
                        <p className="text-center text-zinc-500 text-sm tracking-widest uppercase">Drag 3D Cards</p>
                    </div>
                </div>
            </section>

            <section className="space-y-8 relative z-10">
                <div className="flex items-center gap-4">
                    <span className="w-8 h-1 bg-white rounded-full" />
                    <h2 className="text-2xl font-bold tracking-tight">Minimal / Ink Trap Fonts</h2>
                </div>
                <MinimalTypography />
            </section>

            {/* Advanced 3D Section */}
            <section className="space-y-12 relative z-10 py-12 border-t border-white/10">
                <div className="flex items-center gap-4 mb-8">
                    <span className="w-12 h-1 bg-cyan-400 rounded-full box-shadow-glow" />
                    <h2 className="text-4xl font-bold tracking-tight">Advanced 3D & Interactions</h2>
                </div>

                <div className="grid lg:grid-cols-2 gap-8">
                    {/* Bloom Effect */}
                    <div className="space-y-4">
                        <h3 className="text-xl font-semibold text-zinc-400">Postprocessing Bloom</h3>
                        <BloomEffects />
                    </div>

                    {/* Holographic Tilt */}
                    <div className="space-y-4">
                        <h3 className="text-xl font-semibold text-zinc-400">Holographic Tilt</h3>
                        <div className="flex justify-center items-center h-[400px] bg-zinc-900/30 rounded-2xl border border-white/5">
                            <HolographicTilt className="w-[300px] h-[400px]">
                                <div className="w-full h-full bg-gradient-to-br from-violet-600 to-indigo-900 rounded-xl flex flex-col items-center justify-center p-6 border border-white/20 shadow-2xl">
                                    <div className="text-6xl mb-4">🛸</div>
                                    <h3 className="text-2xl font-bold text-white">Holo Card</h3>
                                    <p className="text-white/60 text-center mt-2">Hover over me to see the parallax tilt and glare effect.</p>
                                </div>
                            </HolographicTilt>
                        </div>
                    </div>
                </div>

                {/* Spline Scene */}
                <div className="space-y-4">
                    <h3 className="text-xl font-semibold text-zinc-400">Interactive Spline Scene</h3>
                    <SplineScene />
                </div>
            </section>

            {/* Decorative Elements */}
            <div className="fixed top-20 right-0 w-[500px] h-[500px] bg-purple-900/20 blur-[100px] rounded-full pointer-events-none -z-10" />
            <div className="fixed bottom-0 left-0 w-[600px] h-[600px] bg-blue-900/10 blur-[120px] rounded-full pointer-events-none -z-10" />
        </div>
    );
}
