import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow, Pagination, Autoplay } from 'swiper/modules';
import { cn } from '@/lib/utils';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import 'swiper/css/pagination';

interface EndlessCarouselProps {
  images: string[];
  className?: string;
  autoplaySpeed?: number;
}

export const EndlessCarousel: React.FC<EndlessCarouselProps> = ({
  images,
  className,
  autoplaySpeed = 2500
}) => {
  return (
    <div className={cn("w-full", className)}>
      <Swiper
        effect={'coverflow'}
        grabCursor={true}
        centeredSlides={true}
        slidesPerView={'auto'}
        initialSlide={Math.floor(images.length / 2)}
        loop={true}
        autoplay={{
          delay: autoplaySpeed,
          disableOnInteraction: false,
          pauseOnMouseEnter: true
        }}
        coverflowEffect={{
          rotate: 35,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true,
        }}
        pagination={{ clickable: true, dynamicBullets: true }}
        modules={[EffectCoverflow, Pagination, Autoplay]}
        className="w-full h-[500px] z-30"
      >
        {images.map((src, idx) => (
          <SwiperSlide
            key={idx}
            className="swiper-slide-custom"
            style={{ width: '300px', height: '400px' }}
          >
            {/* Note: SwiperSlide needs specific width for 'auto' slidesPerView */}
            {({ isActive }) => (
              <div
                className={cn(
                  "w-full h-full rounded-2xl overflow-hidden transition-all duration-500 border border-white/10 relative shadow-2xl bg-black",
                  isActive ? "ring-2 ring-white/50 brightness-110" : "brightness-50"
                )}
              >
                <img
                  src={src}
                  alt={`Slide ${idx}`}
                  className="w-full h-full object-cover"
                />
                {/* Reflection/Shine effect */}
                <div className="absolute inset-0 bg-gradient-to-tr from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
              </div>
            )}
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Custom Styles override for Swiper Pagination */}
      <style>{`
        .swiper-pagination-bullet {
            background: rgba(255,255,255,0.5);
        }
        .swiper-pagination-bullet-active {
            background: #ffffff;
        }
      `}</style>
    </div>
  );
};
