import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Play, Users, MapPin, Disc, Star, Sparkles } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const ArtistSpotlight = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const portraitRef = useRef<HTMLDivElement>(null);
  const infoCardRef = useRef<HTMLDivElement>(null);
  const headlineRef = useRef<HTMLHeadingElement>(null);
  const statsRef = useRef<HTMLDivElement[]>([]);
  const ctaRef = useRef<HTMLDivElement>(null);
  const sticker1Ref = useRef<HTMLDivElement>(null);
  const sticker2Ref = useRef<HTMLDivElement>(null);

  const stats = [
    { icon: Users, label: 'Monthly Listeners', value: '2.4M' },
    { icon: MapPin, label: 'Top City', value: 'Bangkok' },
    { icon: Disc, label: 'Latest Single', value: 'Neon Ghost' },
  ];

  useLayoutEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      const scrollTl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: 'top top',
          end: '+=130%',
          pin: true,
          scrub: 0.6,
        },
      });

      // ENTRANCE (0% - 30%)
      // Left portrait
      scrollTl.fromTo(
        portraitRef.current,
        { x: '-60vw', opacity: 0, scale: 0.92 },
        { x: 0, opacity: 1, scale: 1, ease: 'none' },
        0
      );

      // Right info card
      scrollTl.fromTo(
        infoCardRef.current,
        { x: '60vw', opacity: 0 },
        { x: 0, opacity: 1, ease: 'none' },
        0.05
      );

      // Headline
      scrollTl.fromTo(
        headlineRef.current,
        { y: '30vh', opacity: 0, rotate: -2 },
        { y: 0, opacity: 1, rotate: 0, ease: 'none' },
        0.1
      );

      // Stats
      statsRef.current.forEach((stat, i) => {
        scrollTl.fromTo(
          stat,
          { y: 40, opacity: 0 },
          { y: 0, opacity: 1, ease: 'none' },
          0.15 + i * 0.03
        );
      });

      // CTA
      scrollTl.fromTo(
        ctaRef.current,
        { scale: 0.9, opacity: 0 },
        { scale: 1, opacity: 1, ease: 'none' },
        0.2
      );

      // Stickers
      scrollTl.fromTo(
        [sticker1Ref.current, sticker2Ref.current],
        { scale: 0, rotate: -140, opacity: 0 },
        { scale: 1, rotate: 0, opacity: 1, ease: 'none' },
        0.15
      );

      // EXIT (70% - 100%)
      // Headline exit
      scrollTl.fromTo(
        headlineRef.current,
        { x: 0, opacity: 1 },
        { x: '-10vw', opacity: 0, ease: 'power2.in' },
        0.7
      );

      // Left portrait exit
      scrollTl.fromTo(
        portraitRef.current,
        { x: 0, opacity: 1 },
        { x: '-18vw', opacity: 0, ease: 'power2.in' },
        0.7
      );

      // Right card exit
      scrollTl.fromTo(
        infoCardRef.current,
        { x: 0, opacity: 1 },
        { x: '18vw', opacity: 0, ease: 'power2.in' },
        0.7
      );

      // Stickers drift opposite
      scrollTl.fromTo(
        sticker1Ref.current,
        { x: 0, opacity: 1 },
        { x: '6vw', opacity: 0, ease: 'power2.in' },
        0.75
      );
      scrollTl.fromTo(
        sticker2Ref.current,
        { x: 0, opacity: 1 },
        { x: '-6vw', opacity: 0, ease: 'power2.in' },
        0.75
      );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative w-full h-screen bg-charcoal overflow-hidden z-40"
    >
      {/* Left Big Portrait */}
      <div
        ref={portraitRef}
        className="absolute left-[4vw] lg:left-[6vw] top-[8vh] lg:top-[10vh] w-[42vw] lg:w-[46vw] h-[84vh] rounded-2xl lg:rounded-3xl overflow-hidden z-10 group"
      >
        <img
          src="/spotlight_portrait.jpg"
          alt="Luna Voss"
          className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-transparent to-charcoal/50" />
      </div>

      {/* Right Info Card */}
      <div
        ref={infoCardRef}
        className="absolute right-[4vw] lg:right-[6vw] top-[8vh] lg:top-[10vh] w-[46vw] lg:w-[40vw] h-[84vh] rounded-2xl lg:rounded-3xl card-glass z-0 flex flex-col justify-center px-6 lg:px-10"
      >
        {/* Artist Name */}
        <h3 className="font-display font-bold text-3xl md:text-4xl lg:text-5xl text-text-primary mb-2">
          Luna Voss
        </h3>
        
        {/* Bio */}
        <p className="text-text-secondary text-base lg:text-lg mb-8">
          Synth-pop architect. Night-drive anthems. 2B+ streams.
        </p>

        {/* Stats */}
        <div className="space-y-4 mb-8">
          {stats.map((stat, i) => (
            <div
              key={i}
              ref={(el) => {
                if (el) statsRef.current[i] = el;
              }}
              className="flex items-center gap-4"
            >
              <div className="w-10 h-10 lg:w-12 lg:h-12 rounded-xl bg-pink/10 flex items-center justify-center">
                <stat.icon className="w-5 h-5 lg:w-6 lg:h-6 text-pink" />
              </div>
              <div>
                <p className="text-text-secondary text-xs lg:text-sm uppercase tracking-wider">
                  {stat.label}
                </p>
                <p className="text-text-primary font-display font-semibold text-lg lg:text-xl">
                  {stat.value}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div ref={ctaRef}>
          <Button
            size="lg"
            className="bg-pink hover:bg-pink-light text-white font-semibold px-8 rounded-full shadow-neon hover:shadow-[0_0_30px_rgba(255,45,143,0.6)] transition-all duration-300 hover:scale-105"
          >
            <Play className="w-5 h-5 mr-2 fill-white" />
            Follow
          </Button>
        </div>
      </div>

      {/* Headline (overlaps the seam) */}
      <h2
        ref={headlineRef}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 font-display font-bold text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-text-primary text-center whitespace-nowrap drop-shadow-2xl z-20 pointer-events-none"
        style={{ textShadow: '0 4px 30px rgba(0,0,0,0.8)' }}
      >
        ARTIST
        <br />
        SPOTLIGHT
      </h2>

      {/* Decorative Stickers */}
      <div
        ref={sticker1Ref}
        className="absolute top-[16vh] right-[8vw] z-50 animate-float"
      >
        <div className="w-12 h-12 lg:w-16 lg:h-16 text-pink">
          <Star className="w-full h-full" />
        </div>
      </div>
      <div
        ref={sticker2Ref}
        className="absolute bottom-[12vh] left-[8vw] z-50 animate-float"
        style={{ animationDelay: '2s' }}
      >
        <div className="w-14 h-14 lg:w-20 lg:h-20 text-pink">
          <Sparkles className="w-full h-full" />
        </div>
      </div>
    </section>
  );
};

export default ArtistSpotlight;
