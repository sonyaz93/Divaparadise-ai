import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Play, Users, Upload } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const CommunityPlaylists = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);
  const ctaRef = useRef<HTMLDivElement>(null);

  const playlists = [
    { image: '/community_01.jpg', title: 'Cozy Nights', curator: 'Sarah M.', followers: '12.5K' },
    { image: '/community_02.jpg', title: 'Rooftop Vibes', curator: 'The Collective', followers: '8.2K' },
    { image: '/community_03.jpg', title: 'Night Drive', curator: 'Alex R.', followers: '24.1K' },
    { image: '/community_04.jpg', title: 'Gym Pump', curator: 'FitFlow', followers: '15.8K' },
    { image: '/community_05.jpg', title: 'Focus Flow', curator: 'StudyBeats', followers: '31.4K' },
    { image: '/community_06.jpg', title: 'Beach Sunset', curator: 'Summer Crew', followers: '9.7K' },
  ];

  useLayoutEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      // Heading animation
      gsap.fromTo(
        headingRef.current,
        { y: 40, opacity: 0 },
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
          { y: 70, opacity: 0, rotate: -2 },
          {
            y: 0,
            opacity: 1,
            rotate: 0,
            duration: 0.6,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: card,
              start: 'top 85%',
              end: 'top 50%',
              scrub: true,
            },
          }
        );
      });

      // CTA animation
      gsap.fromTo(
        ctaRef.current,
        { scale: 0.95, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: ctaRef.current,
            start: 'top 90%',
            end: 'top 70%',
            scrub: true,
          },
        }
      );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="playlists"
      className="relative w-full min-h-screen bg-charcoal py-20 lg:py-32 z-[70]"
    >
      <div className="w-full px-6 lg:px-12">
        {/* Heading */}
        <div ref={headingRef} className="mb-12 lg:mb-16">
          <h2 className="font-display font-bold text-4xl md:text-5xl lg:text-6xl text-text-primary mb-4">
            Community Playlists
          </h2>
          <p className="text-text-secondary text-lg lg:text-xl max-w-xl">
            Made by fans. Updated daily.
          </p>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
          {playlists.map((playlist, i) => (
            <div
              key={i}
              ref={(el) => {
                if (el) cardsRef.current[i] = el;
              }}
              className="group relative rounded-2xl lg:rounded-3xl overflow-hidden cursor-pointer card-glass hover:border-pink/30 transition-all duration-300"
            >
              {/* Image */}
              <div className="relative aspect-video overflow-hidden">
                <img
                  src={playlist.image}
                  alt={playlist.title}
                  className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
                />
                
                {/* Overlay */}
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                  <button className="w-14 h-14 rounded-full bg-pink flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300 hover:scale-110">
                    <Play className="w-6 h-6 text-white fill-white ml-0.5" />
                  </button>
                </div>
              </div>

              {/* Info */}
              <div className="p-4 lg:p-5">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-display font-semibold text-text-primary text-lg group-hover:text-pink transition-colors">
                      {playlist.title}
                    </h3>
                    <p className="text-text-secondary text-sm mt-1">
                      by {playlist.curator}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-1 mt-3 text-text-secondary/60 text-xs">
                  <Users className="w-3 h-3" />
                  <span>{playlist.followers} followers</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div ref={ctaRef} className="mt-12 lg:mt-16 text-center">
          <Button
            variant="outline"
            size="lg"
            className="border-pink text-pink hover:bg-pink hover:text-white transition-all duration-300 rounded-full px-8"
          >
            <Upload className="w-5 h-5 mr-2" />
            Submit Your Playlist
          </Button>
        </div>
      </div>
    </section>
  );
};

export default CommunityPlaylists;
