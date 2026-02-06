import { forwardRef } from 'react';

export const Star = forwardRef<SVGSVGElement, React.SVGProps<SVGSVGElement>>(
  (props, ref) => (
    <svg
      ref={ref}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  )
);
Star.displayName = 'Star';

export const Swirl = forwardRef<SVGSVGElement, React.SVGProps<SVGSVGElement>>(
  (props, ref) => (
    <svg
      ref={ref}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10S2 17.523 2 12" />
      <path d="M12 6c3.314 0 6 2.686 6 6s-2.686 6-6 6" />
      <path d="M12 10c1.105 0 2 .895 2 2s-.895 2-2 2" />
    </svg>
  )
);
Swirl.displayName = 'Swirl';

export const MusicWave = forwardRef<SVGSVGElement, React.SVGProps<SVGSVGElement>>(
  (props, ref) => (
    <svg
      ref={ref}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M2 10v4" />
      <path d="M6 6v12" />
      <path d="M10 4v16" />
      <path d="M14 8v8" />
      <path d="M18 6v12" />
      <path d="M22 10v4" />
    </svg>
  )
);
MusicWave.displayName = 'MusicWave';
