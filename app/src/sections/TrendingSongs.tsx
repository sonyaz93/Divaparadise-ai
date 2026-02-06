import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useTranslation } from 'react-i18next';
import { Play, Heart, MoreHorizontal } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const TrendingSongs = () => {
  const { t } = useTranslation();
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);

  const songs = [
    { image: '/trending_song_01.jpg', title: 'Neon Dreams', artist: 'Luna Voss', duration: '3:42' },
    { image: '/trending_song_02.jpg', title: 'Echoes of Light', artist: 'The Wanderers', duration: '4:15' },
    { image: '/trending_song_03.jpg', title: 'City Pulse', artist: 'Night Runners', duration: '3:28' },
    { image: '/trending_song_04.jpg', title: 'Velocity Falls', artist: 'Sky Breakers', duration: '3:55' },
    { image: '/trending_song_05.jpg', title: 'Night Wave', artist: 'Deep Echo', duration: '4:02' },
    { image: '/trending_song_06.jpg', title: 'Celestial Drifts', artist: 'Star Chasers', duration: '3:33' },
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
          { y: 80, opacity: 0, scale: 0.98, rotate: -2 },
          {
            y: 0,
            opacity: 1,
            scale: 1,
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
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="charts"
      className="relative w-full min-h-screen bg-charcoal py-20 lg:py-32 z-30"
    >
      <div className="w-full px-6 lg:px-12">
        {/* Heading */}
        <div ref={headingRef} className="mb-12 lg:mb-16">
          <h2 className="font-display font-bold text-4xl md:text-5xl lg:text-6xl text-text-primary mb-4">
            {t('trendingSongs.title')}
          </h2>
          <p className="text-text-secondary text-lg lg:text-xl max-w-xl">
            {t('trendingSongs.subtitle')}
          </p>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
          {songs.map((song, i) => (
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
                  src={song.image}
                  alt={song.title}
                  className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
                />
                
                {/* Overlay */}
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                  <button className="w-14 h-14 rounded-full bg-pink flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300 hover:scale-110">
                    <Play className="w-6 h-6 text-white fill-white ml-1" />
                  </button>
                </div>
              </div>

              {/* Info */}
              <div className="p-4 lg:p-5">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-display font-semibold text-text-primary text-lg group-hover:text-pink transition-colors">
                      {song.title}
                    </h3>
                    <p className="text-text-secondary text-sm mt-1">{song.artist}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="p-2 rounded-full hover:bg-white/10 transition-colors opacity-0 group-hover:opacity-100">
                      <Heart className="w-4 h-4 text-text-secondary" />
                    </button>
                    <button className="p-2 rounded-full hover:bg-white/10 transition-colors opacity-0 group-hover:opacity-100">
                      <MoreHorizontal className="w-4 h-4 text-text-secondary" />
                    </button>
                  </div>
                </div>
                <p className="text-text-secondary/60 text-xs mt-3">{song.duration}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrendingSongs;
