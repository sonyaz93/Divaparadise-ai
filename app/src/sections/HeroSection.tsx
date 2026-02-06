import { useEffect, useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';
import { Sparkles, Zap, Play } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const HeroSection = () => {
  const { t } = useTranslation();
  const sectionRef = useRef<HTMLElement>(null);
  const headlineRef = useRef<HTMLDivElement>(null);
  const subheadlineRef = useRef<HTMLDivElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);
  const sticker1Ref = useRef<HTMLDivElement>(null);
  const sticker2Ref = useRef<HTMLDivElement>(null);

  const heroImages = [
    { src: '/hero_img_a.jpg', alt: 'Pop artist performance' },
    { src: '/hero_img_b.jpg', alt: 'Rapper portrait' },
    { src: '/hero_img_c.jpg', alt: 'DJ at decks' },
    { src: '/hero_img_d.jpg', alt: 'Indie band performance' },
    { src: '/hero_img_e.jpg', alt: 'Featured vocalist' },
    { src: '/hero_img_f.jpg', alt: 'Electronic producer' },
  ];

  // Auto-play entrance animation on load
  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

      // Cards entrance
      tl.fromTo(
        cardsRef.current,
        { opacity: 0, scale: 0.92, y: 40, rotate: (i) => (i % 2 === 0 ? 6 : -6) },
        { opacity: 1, scale: 1, y: 0, rotate: 0, duration: 0.8, stagger: 0.08 },
        0
      );

      // Headline entrance
      tl.fromTo(
        headlineRef.current,
        { opacity: 0, y: 28, rotateX: 35 },
        { opacity: 1, y: 0, rotateX: 0, duration: 0.7 },
        0.4
      );

      // Subheadline entrance
      tl.fromTo(
        subheadlineRef.current,
        { opacity: 0, y: 28, rotateX: 35 },
        { opacity: 1, y: 0, rotateX: 0, duration: 0.7 },
        0.5
      );

      // CTA entrance
      tl.fromTo(
        ctaRef.current,
        { opacity: 0, y: 16, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.6 },
        0.7
      );

      // Stickers entrance
      tl.fromTo(
        [sticker1Ref.current, sticker2Ref.current],
        { opacity: 0, scale: 0, rotate: -120 },
        { opacity: 1, scale: 1, rotate: 0, duration: 0.6, stagger: 0.1 },
        0.6
      );
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  // Scroll-driven animation
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
          onLeaveBack: () => {
            // Reset all elements to visible when scrolling back to top
            gsap.set([headlineRef.current, subheadlineRef.current, ctaRef.current], {
              opacity: 1,
              y: 0,
              x: 0,
            });
            gsap.set(cardsRef.current, { opacity: 1, scale: 1, x: 0, y: 0, rotate: 0 });
            gsap.set([sticker1Ref.current, sticker2Ref.current], { opacity: 1, scale: 1 });
          },
        },
      });

      // EXIT phase (70% - 100%)
      // Headline exit
      scrollTl.fromTo(
        [headlineRef.current, subheadlineRef.current],
        { y: 0, opacity: 1 },
        { y: '-22vh', opacity: 0, ease: 'power2.in' },
        0.7
      );

      // Cards exit with stagger based on position
      cardsRef.current.forEach((card, i) => {
        const isLeft = i === 0 || i === 3;
        const isRight = i === 2 || i === 5;
        const xOffset = isLeft ? '-10vw' : isRight ? '10vw' : '0';
        const yOffset = i < 3 ? '-10vh' : '10vh';
        const rotate = i % 2 === 0 ? -10 : 10;

        scrollTl.fromTo(
          card,
          { x: 0, y: 0, rotate: 0, scale: 1, opacity: 1 },
          { x: xOffset, y: yOffset, rotate, scale: 0.92, opacity: 0, ease: 'power2.in' },
          0.7 + i * 0.02
        );
      });

      // CTA exit
      scrollTl.fromTo(
        ctaRef.current,
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
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="discover"
      className="relative w-full h-screen bg-charcoal overflow-hidden z-10"
    >
      {/* Background vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(11,12,16,0.8)_100%)]" />

      {/* Collage Grid */}
      <div className="absolute inset-0 grid grid-cols-3 grid-rows-2 gap-3 p-4 lg:p-6">
        {heroImages.map((img, index) => (
          <div
            key={index}
            ref={(el) => {
              if (el) cardsRef.current[index] = el;
            }}
            className={`relative overflow-hidden rounded-2xl lg:rounded-3xl ${
              index === 4 ? 'ring-2 ring-pink/50' : ''
            }`}
            style={{ zIndex: index === 4 ? 4 : 2 + (index % 2) }}
          >
            <img
              src={img.src}
              alt={img.alt}
              className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 hover:scale-105"
            />
            {index === 4 && (
              <div className="absolute inset-0 bg-gradient-to-t from-pink/20 to-transparent" />
            )}
          </div>
        ))}
      </div>

      {/* Headline Overlay */}
      <div className="absolute inset-0 flex flex-col items-center justify-center z-20 pointer-events-none">
        <div
          ref={headlineRef}
          className="text-center"
          style={{ perspective: '1000px' }}
        >
          <h1 className="font-display font-bold text-5xl sm:text-6xl md:text-7xl lg:text-8xl xl:text-9xl text-text-primary tracking-tighter drop-shadow-2xl">
            {t('hero.title')}
          </h1>
        </div>
        <div
          ref={subheadlineRef}
          className="text-center mt-2"
          style={{ perspective: '1000px' }}
        >
          <p className="font-display font-semibold text-xl sm:text-2xl md:text-3xl lg:text-4xl text-text-secondary tracking-wide">
            {t('hero.subtitle')}
          </p>
        </div>

        {/* CTA */}
        <div ref={ctaRef} className="mt-8 pointer-events-auto">
          <Button
            size="lg"
            className="bg-pink hover:bg-pink-light text-white font-semibold px-8 py-6 text-lg rounded-full shadow-neon hover:shadow-[0_0_30px_rgba(255,45,143,0.6)] transition-all duration-300 hover:scale-105"
          >
            <Play className="w-5 h-5 mr-2 fill-white" />
            {t('hero.cta')}
          </Button>
          <p className="text-text-secondary/70 text-sm mt-4 text-center">
            {t('hero.noCreditCard')}
          </p>
        </div>
      </div>

      {/* Decorative Stickers */}
      <div
        ref={sticker1Ref}
        className="absolute top-[18vh] left-[26vw] z-30 animate-float"
      >
        <div className="w-12 h-12 lg:w-16 lg:h-16 text-pink">
          <Sparkles className="w-full h-full" />
        </div>
      </div>
      <div
        ref={sticker2Ref}
        className="absolute bottom-[18vh] right-[12vw] z-30 animate-float"
        style={{ animationDelay: '1s' }}
      >
        <div className="w-14 h-14 lg:w-20 lg:h-20 text-pink">
          <Zap className="w-full h-full" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
