import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Play, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

gsap.registerPlugin(ScrollTrigger);

const NewReleases = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLDivElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);

  const releases = [
    { image: '/new_release_01.jpg', title: 'Celestial Pop', artist: 'Nova' },
    { image: '/new_release_02.jpg', title: 'Night Fall', artist: 'Echoes' },
    { image: '/new_release_03.jpg', title: 'Velocity Falls', artist: 'Breakers' },
    { image: '/new_release_04.jpg', title: 'Neo Circuit', artist: 'Synthesis' },
    { image: '/new_release_05.jpg', title: 'Driftwood Harmony', artist: 'Mist' },
    { image: '/new_release_06.jpg', title: 'Echoes in Blue', artist: 'Aether' },
    { image: '/new_release_07.jpg', title: 'Eternal Fire', artist: 'Soul' },
    { image: '/new_release_08.jpg', title: 'Fractured Reality', artist: 'Silence' },
  ];

  useLayoutEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      // Heading animation
      gsap.fromTo(
        headingRef.current,
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: section,
            start: 'top 80%',
            end: 'top 35%',
            scrub: true,
          },
        }
      );

      // Cards animation
      cardsRef.current.forEach((card) => {
        gsap.fromTo(
          card,
          { x: '10vw', opacity: 0, scale: 0.97 },
          {
            x: 0,
            opacity: 1,
            scale: 1,
            duration: 0.6,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: card,
              start: 'top 90%',
              end: 'top 60%',
              scrub: true,
            },
          }
        );
      });

      // Track parallax
      gsap.fromTo(
        trackRef.current,
        { x: 0 },
        {
          x: '-8vw',
          ease: 'none',
          scrollTrigger: {
            trigger: section,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
          },
        }
      );
    }, section);

    return () => ctx.revert();
  }, []);

  const scroll = (direction: 'left' | 'right') => {
    if (trackRef.current) {
      const scrollAmount = 400;
      trackRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth',
      });
    }
  };

  return (
    <section
      ref={sectionRef}
      className="relative w-full min-h-screen bg-charcoal py-20 lg:py-32 z-[60]"
    >
      <div className="w-full px-6 lg:px-12">
        {/* Heading */}
        <div ref={headingRef} className="flex items-end justify-between mb-12 lg:mb-16">
          <div>
            <h2 className="font-display font-bold text-4xl md:text-5xl lg:text-6xl text-text-primary mb-4">
              New Releases
            </h2>
            <p className="text-text-secondary text-lg lg:text-xl">
              This week's drops, curated.
            </p>
          </div>
          
          {/* Navigation buttons */}
          <div className="hidden md:flex items-center gap-3">
            <Button
              variant="outline"
              size="icon"
              className="rounded-full border-white/20 hover:border-pink hover:bg-pink/10"
              onClick={() => scroll('left')}
            >
              <ChevronLeft className="w-5 h-5" />
            </Button>
            <Button
              variant="outline"
              size="icon"
              className="rounded-full border-white/20 hover:border-pink hover:bg-pink/10"
              onClick={() => scroll('right')}
            >
              <ChevronRight className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* Carousel */}
      <div
        ref={trackRef}
        className="flex gap-4 lg:gap-6 overflow-x-auto scrollbar-hide px-6 lg:px-12 pb-4"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {releases.map((release, i) => (
          <div
            key={i}
            ref={(el) => {
              if (el) cardsRef.current[i] = el;
            }}
            className="group relative flex-shrink-0 w-[200px] sm:w-[240px] lg:w-[280px] cursor-pointer"
          >
            {/* Image */}
            <div className="relative aspect-[4/5] rounded-2xl lg:rounded-3xl overflow-hidden mb-4">
              <img
                src={release.image}
                alt={release.title}
                className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
              />
              
              {/* Overlay */}
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <button className="w-12 h-12 lg:w-14 lg:h-14 rounded-full bg-pink flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300 hover:scale-110">
                  <Play className="w-5 h-5 lg:w-6 lg:h-6 text-white fill-white ml-0.5" />
                </button>
              </div>
            </div>
            
            {/* Info */}
            <h3 className="font-display font-semibold text-text-primary text-base lg:text-lg group-hover:text-pink transition-colors truncate">
              {release.title}
            </h3>
            <p className="text-text-secondary text-sm truncate">{release.artist}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default NewReleases;
