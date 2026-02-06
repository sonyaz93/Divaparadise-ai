import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Badge } from '@/components/ui/badge';
import { ArrowRight } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const GenreExplorer = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const headingRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);

  const genres = [
    {
      image: '/genre_pop.jpg',
      name: 'Pop',
      tags: ['Hits', 'Fresh', 'Global'],
      description: 'Catchy melodies that dominate the charts',
    },
    {
      image: '/genre_indie.jpg',
      name: 'Indie',
      tags: ['Underground', 'Rising', 'Raw'],
      description: 'Authentic sounds from emerging artists',
    },
    {
      image: '/genre_electronic.jpg',
      name: 'Electronic',
      tags: ['Night', 'Dance', 'Bass'],
      description: 'Pulsating beats for the dance floor',
    },
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
          { y: 100, opacity: 0, scale: 0.98 },
          {
            y: 0,
            opacity: 1,
            scale: 1,
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
      className="relative w-full min-h-screen bg-charcoal py-20 lg:py-32 z-50"
    >
      <div className="w-full px-6 lg:px-12">
        {/* Heading */}
        <div ref={headingRef} className="mb-12 lg:mb-16">
          <h2 className="font-display font-bold text-4xl md:text-5xl lg:text-6xl text-text-primary mb-4">
            Explore by Genre
          </h2>
          <p className="text-text-secondary text-lg lg:text-xl max-w-xl">
            Pick a mood. We'll build the queue.
          </p>
        </div>

        {/* Genre Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {genres.map((genre, i) => (
            <div
              key={i}
              ref={(el) => {
                if (el) cardsRef.current[i] = el;
              }}
              className="group relative rounded-2xl lg:rounded-3xl overflow-hidden cursor-pointer card-glass hover:border-pink/30 transition-all duration-500 hover:-translate-y-2"
            >
              {/* Image */}
              <div className="relative aspect-[3/4] overflow-hidden">
                <img
                  src={genre.image}
                  alt={genre.name}
                  className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700 group-hover:scale-105"
                />
                
                {/* Gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-charcoal via-charcoal/50 to-transparent" />
                
                {/* Content */}
                <div className="absolute bottom-0 left-0 right-0 p-6 lg:p-8">
                  <h3 className="font-display font-bold text-3xl lg:text-4xl text-text-primary mb-2 group-hover:text-pink transition-colors">
                    {genre.name}
                  </h3>
                  <p className="text-text-secondary text-sm mb-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    {genre.description}
                  </p>
                  
                  {/* Tags */}
                  <div className="flex flex-wrap gap-2">
                    {genre.tags.map((tag, j) => (
                      <Badge
                        key={j}
                        variant="secondary"
                        className="bg-white/10 text-text-primary hover:bg-pink hover:text-white transition-colors border-0"
                      >
                        {tag}
                      </Badge>
                    ))}
                  </div>
                  
                  {/* Explore link */}
                  <div className="mt-4 flex items-center gap-2 text-pink opacity-0 group-hover:opacity-100 transition-opacity duration-300 transform translate-y-2 group-hover:translate-y-0">
                    <span className="text-sm font-medium">Explore</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default GenreExplorer;
