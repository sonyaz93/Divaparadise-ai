import { useState, useEffect } from 'react';
import { Menu, X, Play, Languages } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';

const Navigation = () => {
  const { t, i18n } = useTranslation();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'th' : 'en';
    i18n.changeLanguage(newLang);
  };

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 100);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: t('nav.discover'), href: '#discover' },
    { name: t('nav.artists'), href: '#artists' },
    { name: t('nav.charts'), href: '#charts' },
    { name: t('nav.playlists'), href: '#playlists' },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled
          ? 'bg-charcoal/90 backdrop-blur-md border-b border-white/5'
          : 'bg-transparent'
      }`}
    >
      <div className="w-full px-6 lg:px-12">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-full bg-pink flex items-center justify-center group-hover:scale-110 transition-transform">
              <Play className="w-4 h-4 text-white fill-white ml-0.5" />
            </div>
            <span className="font-display font-bold text-xl text-text-primary tracking-tight">
              Divaparadises
            </span>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-8">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="text-text-secondary hover:text-text-primary text-sm font-medium transition-colors relative group"
              >
                {link.name}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-pink transition-all duration-300 group-hover:w-full" />
              </a>
            ))}
          </div>

          {/* CTA Button */}
          <div className="hidden lg:flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleLanguage}
              className="text-text-secondary hover:text-text-primary transition-colors"
              title={i18n.language === 'en' ? 'Switch to Thai' : 'สลับเป็นภาษาอังกฤษ'}
            >
              <Languages className="w-5 h-5" />
            </Button>
            <Button
              variant="outline"
              className="border-pink text-pink hover:bg-pink hover:text-white transition-all duration-300 rounded-full px-6"
            >
              {t('nav.startListening')}
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden p-2 text-text-primary"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
        className={`lg:hidden absolute top-full left-0 right-0 bg-charcoal/95 backdrop-blur-md border-b border-white/5 transition-all duration-300 ${
          isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
        }`}
      >
        <div className="px-6 py-6 space-y-4">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="block text-text-secondary hover:text-text-primary text-lg font-medium transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              {link.name}
            </a>
          ))}
          <div className="flex gap-2 mt-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleLanguage}
              className="text-text-secondary hover:text-text-primary transition-colors"
            >
              <Languages className="w-5 h-5" />
            </Button>
            <Button
              variant="outline"
              className="flex-1 border-pink text-pink hover:bg-pink hover:text-white transition-all duration-300 rounded-full"
            >
              {t('nav.startListening')}
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
