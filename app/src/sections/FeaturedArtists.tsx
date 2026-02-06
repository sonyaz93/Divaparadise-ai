import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';
import { Star, Swirl } from '@/components/ui/icons';

gsap.registerPlugin(ScrollTrigger);

const FeaturedArtists = () => {
  const { t } = useTranslation();
  const sectionRef = useRef<HTMLElement>(null);
  const leftCardsRef = useRef<HTMLDivElement[]>([]);
  const centerCardRef = useRef<HTMLDivElement>(null);
  const rightCardsRef = useRef<HTMLDivElement[]>([]);
  const headlineRef = useRef<HTMLHeadingElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);
  const sticker1Ref = useRef<HTMLDivElement>(null);
  const sticker2Ref = useRef<HTMLDivElement>(null);

  const leftArtists = [
    { src: '/featured_artist_01.jpg', name: 'Aurora Wave' },
    { src: '/featured_artist_02.jpg', name: 'Midnight Rider' },
    { src: '/featured_artist_03.jpg', name: 'Neon Pulse' },
  ];

  const rightArtists = [
    { src: '/featured_artist_04.jpg', name: 'Soul Searcher' },
    { src: '/featured_artist_05.jpg', name: 'Echo Dreams' },
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
      // Left column cards
      leftCardsRef.current.forEach((card, i) => {
        scrollTl.fromTo(
          card,
          { x: '-50vw', opacity: 0, rotate: -6, scale: 0.96 },
          { x: 0, opacity: 1, rotate: 0, scale: 1, ease: 'none' },
          i * 0.03
        );
      });

      // Center featured card
      scrollTl.fromTo(
        centerCardRef.current,
        { y: '100vh', opacity: 0, scale: 0.9 },
        { y: 0, opacity: 1, scale: 1, ease: 'none' },
        0.05
      );

      // Right column cards
      rightCardsRef.current.forEach((card, i) => {
        scrollTl.fromTo(
          card,
          { x: '50vw', opacity: 0, rotate: 6, scale: 0.96 },
          { x: 0, opacity: 1, rotate: 0, scale: 1, ease: 'none' },
          0.1 + i * 0.035
        );
      });

      // Headline
      scrollTl.fromTo(
        headlineRef.current,
        { x: '-18vw', opacity: 0 },
        { x: 0, opacity: 1, ease: 'none' },
        0.1
      );

      // Stickers
      scrollTl.fromTo(
        [sticker1Ref.current, sticker2Ref.current],
        { scale: 0, rotate: -120, opacity: 0 },
        { scale: 1, rotate: 0, opacity: 1, ease: 'none' },
        0.15
      );

      // CTA
      scrollTl.fromTo(
        ctaRef.current,
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, ease: 'none' },
        0.2
      );

      // EXIT (70% - 100%)
      // Center card stays longest
      scrollTl.fromTo(
        centerCardRef.current,
        { scale: 1, opacity: 1 },
        { scale: 0.96, opacity: 0, ease: 'power2.in' },
        0.7
      );

      // Side cards drift outward
      leftCardsRef.current.forEach((card, i) => {
        scrollTl.fromTo(
          card,
          { x: 0, opacity: 1 },
          { x: '-18vw', opacity: 0, ease: 'power2.in' },
          0.7 + i * 0.02
        );
      });

      rightCardsRef.current.forEach((card, i) => {
        scrollTl.fromTo(
          card,
          { x: 0, opacity: 1 },
          { x: '18vw', opacity: 0, ease: 'power2.in' },
          0.7 + i * 0.02
        );
      });

      // Headline exit
      scrollTl.fromTo(
        headlineRef.current,
        { y: 0, opacity: 1 },
        { y: '-10vh', opacity: 0, ease: 'power2.in' },
        0.75
      );

      // Stickers exit
      scrollTl.fromTo(
        [sticker1Ref.current, sticker2Ref.current],
        { opacity: 1, scale: 1 },
        { opacity: 0, scale: 0.5, ease: 'power2.in' },
        0.8
      );

      // CTA exit
      scrollTl.fromTo(
        ctaRef.current,
        { y: 0, opacity: 1 },
        { y: 20, opacity: 0, ease: 'power2.in' },
        0.8
      );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="artists"
      className="relative w-full h-screen bg-charcoal overflow-hidden z-20"
    >
      {/* Left Column - 3 stacked cards */}
      <div className="absolute left-[4vw] lg:left-[6vw] top-[8vh] lg:top-[10vh] w-[26vw] lg:w-[28vw] h-[84vh] flex flex-col gap-3 lg:gap-4">
        {leftArtists.map((artist, i) => (
          <div
            key={i}
            ref={(el) => {
              if (el) leftCardsRef.current[i] = el;
            }}
            className="relative flex-1 rounded-2xl lg:rounded-3xl overflow-hidden group cursor-pointer"
          >
            <img
              src={artist.src}
              alt={artist.name}
              className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
            <div className="absolute bottom-3 left-3 lg:bottom-4 lg:left-4">
              <p className="text-text-primary font-display font-semibold text-sm lg:text-base">
                {artist.name}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Center Featured Card */}
      <div
        ref={centerCardRef}
        className="absolute left-[32vw] lg:left-[36vw] top-[8vh] lg:top-[10vh] w-[34vw] lg:w-[34vw] h-[84vh] rounded-2xl lg:rounded-3xl overflow-hidden ring-2 ring-pink/50 shadow-neon z-10 group cursor-pointer"
      >
        <img
          src="/hero_img_e.jpg"
          alt="Featured Artist"
          className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-pink/30 via-transparent to-transparent" />
        
        {/* Headline over center card */}
        <h2
          ref={headlineRef}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 font-display font-bold text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-text-primary text-center whitespace-nowrap drop-shadow-2xl z-20"
        >
          {t('featuredArtists.title').split(' ').map((word, i) => (
            <span key={i}>
              {word}
              {i === 0 && <br />}
            </span>
          ))}
        </h2>
      </div>

      {/* Right Column - 2 cards */}
      <div className="absolute right-[4vw] lg:right-[6vw] top-[8vh] lg:top-[10vh] w-[26vw] lg:w-[22vw] h-[84vh] flex flex-col gap-3 lg:gap-4">
        {rightArtists.map((artist, i) => (
          <div
            key={i}
            ref={(el) => {
              if (el) rightCardsRef.current[i] = el;
            }}
            className="relative flex-1 rounded-2xl lg:rounded-3xl overflow-hidden group cursor-pointer"
          >
            <img
              src={artist.src}
              alt={artist.name}
              className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
            <div className="absolute bottom-3 left-3 lg:bottom-4 lg:left-4">
              <p className="text-text-primary font-display font-semibold text-sm lg:text-base">
                {artist.name}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* CTA */}
      <div
        ref={ctaRef}
        className="absolute bottom-[6vh] lg:bottom-[8vh] left-1/2 -translate-x-1/2 z-30"
      >
        <Button
          variant="outline"
          size="lg"
          className="border-pink text-pink hover:bg-pink hover:text-white transition-all duration-300 rounded-full px-6 lg:px-8"
        >
          {t('featuredArtists.subtitle')}
        </Button>
      </div>

      {/* Decorative Stickers */}
      <div
        ref={sticker1Ref}
        className="absolute top-[30vh] left-[30vw] z-40 animate-float"
      >
        <div className="w-10 h-10 lg:w-14 lg:h-14 text-pink">
          <Star className="w-full h-full" />
        </div>
      </div>
      <div
        ref={sticker2Ref}
        className="absolute bottom-[20vh] right-[28vw] z-40 animate-float"
        style={{ animationDelay: '1.5s' }}
      >
        <div className="w-12 h-12 lg:w-16 lg:h-16 text-pink">
          <Swirl className="w-full h-full" />
        </div>
      </div>
    </section>
  );
};

export default FeaturedArtists;
