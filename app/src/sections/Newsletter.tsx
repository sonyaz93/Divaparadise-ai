import { useRef, useLayoutEffect, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Music, Users, HelpCircle } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const Newsletter = () => {
  const { t } = useTranslation();
  const sectionRef = useRef<HTMLElement>(null);
  const headlineRef = useRef<HTMLDivElement>(null);
  const formRef = useRef<HTMLDivElement>(null);
  const footerRef = useRef<HTMLDivElement>(null);
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const footerLinks = [
    {
      title: 'Discover',
      links: ['New Releases', 'Trending', 'Genres', 'Moods'],
      icon: Music,
    },
    {
      title: 'Artists',
      links: ['Featured', 'Spotlight', 'Rising', 'Legends'],
      icon: Users,
    },
    {
      title: 'Support',
      links: ['Help Center', 'Contact Us', 'Terms', 'Privacy'],
      icon: HelpCircle,
    },
  ];

  useLayoutEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      // Headline animation
      gsap.fromTo(
        headlineRef.current,
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

      // Form animation
      gsap.fromTo(
        formRef.current,
        { x: '-6vw', opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: formRef.current,
            start: 'top 85%',
            end: 'top 50%',
            scrub: true,
          },
        }
      );

      // Footer animation
      gsap.fromTo(
        footerRef.current,
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: footerRef.current,
            start: 'top 90%',
            end: 'top 70%',
            scrub: true,
          },
        }
      );
    }, section);

    return () => ctx.revert();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setIsSubmitted(true);
      setEmail('');
      setTimeout(() => setIsSubmitted(false), 3000);
    }
  };

  return (
    <section
      ref={sectionRef}
      className="relative w-full min-h-screen bg-charcoal-light py-20 lg:py-32 z-[80]"
    >
      <div className="w-full px-6 lg:px-12">
        {/* Newsletter Content */}
        <div className="max-w-4xl mb-20 lg:mb-32">
          <div ref={headlineRef}>
            <h2 className="font-display font-bold text-4xl md:text-5xl lg:text-7xl text-text-primary mb-4">
              {t('newsletter.title')}
            </h2>
            <p className="text-text-secondary text-lg lg:text-xl max-w-lg">
              {t('newsletter.subtitle')}
            </p>
          </div>

          <div ref={formRef} className="mt-8 lg:mt-12">
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md">
              <Input
                type="email"
                placeholder={t('newsletter.emailPlaceholder')}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 bg-white/5 border-white/10 text-text-primary placeholder:text-text-secondary/50 rounded-full px-6 py-6 focus:border-pink focus:ring-pink"
              />
              <Button
                type="submit"
                size="lg"
                className="bg-pink hover:bg-pink-light text-white font-semibold px-8 rounded-full shadow-neon hover:shadow-[0_0_30px_rgba(255,45,143,0.6)] transition-all duration-300"
              >
                {isSubmitted ? (
                  'Subscribed!'
                ) : (
                  <>
                    {t('newsletter.subscribe')}
                    <Send className="w-4 h-4 ml-2" />
                  </>
                )}
              </Button>
            </form>
          </div>
        </div>

        {/* Footer */}
        <div ref={footerRef} className="border-t border-white/10 pt-12 lg:pt-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 lg:gap-12 mb-12">
            {/* Logo & Description */}
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-full bg-pink flex items-center justify-center">
                  <Music className="w-4 h-4 text-white" />
                </div>
                <span className="font-display font-bold text-xl text-text-primary">
                  Divaparadises
                </span>
              </div>
              <p className="text-text-secondary/70 text-sm">
                Discover your next obsession. Music for every mood, moment, and memory.
              </p>
            </div>

            {/* Links */}
            {footerLinks.map((column, i) => (
              <div key={i}>
                <div className="flex items-center gap-2 mb-4">
                  <column.icon className="w-4 h-4 text-pink" />
                  <h4 className="font-display font-semibold text-text-primary">
                    {column.title}
                  </h4>
                </div>
                <ul className="space-y-2">
                  {column.links.map((link, j) => (
                    <li key={j}>
                      <a
                        href="#"
                        className="text-text-secondary/70 hover:text-pink text-sm transition-colors"
                      >
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Legal */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-8 border-t border-white/5">
            <p className="text-text-secondary/50 text-sm">
              © Divaparadises. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <a href="#" className="text-text-secondary/50 hover:text-pink text-sm transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-text-secondary/50 hover:text-pink text-sm transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-text-secondary/50 hover:text-pink text-sm transition-colors">
                Cookies
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Newsletter;
