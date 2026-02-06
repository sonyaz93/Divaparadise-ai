# Web Design Tools & Trends 2026 🎨
> **Diva Paradox Design System**

This documentation covers the modern web design trends and tools implementing for Divaparadises. These components are located in `src/components/design-system/`.

---

## 1. Bento Grid Layout 🍱
**File**: `BentoGrid.tsx`
**Concept**: Inspired by Japanese bento boxes, this layout organizes content into strictly aligned, rectangular compartments.
**Features**:
- Responsive CSS Grid.
- Hover animations revealing hidden details.
- "Smart Video" placeholders.
- **Use Case**: Landing pages, Feature showcases.

## 2. Custom Cursor (Micro-interactions) 🖱️
**File**: `CustomCursor.tsx`
**Concept**: Replacing the default cursor with a dynamic element that reacts to the environment.
**Features**:
- Follows mouse movement with spring physics (Framer Motion).
- Expands when hovering over clickable elements (buttons, links).
- Blend modes for high contrast.

## 3. Expressive Typography & Brutalism 🅰️
**File**: `TypographyShowcase.tsx`
**Concept**: Rules are meant to be broken. Large sizes, overlapping text, and raw aesthetics.
**Features**:
- **Negative Space**: Using emptiness to draw focus.
- **Outline/Stroke Fonts**: Using `-webkit-text-stroke`.
- **Marquee Animation**: Infinite scrolling text.

## 4. Utilitarian Style (Function over Form) 🛠️
**File**: `UtilitarianLayout.tsx`
**Concept**: Exposing the structure. Design that focuses on raw functionality and grids.
**Features**:
- Visible 1px borders.
- Monospaced fonts (Code style).
- "System Status" indicators.
- High contrast black/white.

## 5. Surrealism Collage (Digital Scrapbooking) 🖼️
**File**: `SurrealCollage.tsx`
**Concept**: Mixing digital and analog worlds. Combining realistic photos with abstract shapes.
**Features**:
- Paper textures (Masking/Overlays).
- Rotated elements breaking the grid.
- Mixed media (Photos + Vector Shapes).
- **Technique**: Using CSS `mix-blend-mode` (multiply, screen) to blend layers.

## 6. Grainy Gradients 🌫️
**File**: `GrainyGradients.tsx`
**Concept**: Adding tactile texture to smooth digital gradients to avoid "plastic" feelings.
**Features**:
- **SVG Noise Filter**: A robust way to generate noise without heavy images.
- **Blurry Blobs**: Moving colored shapes behind the noise.
- **Glassmorphism**: Soft background blurs.

## 7. Rugged & Sustainable (Eco Style) 🌿
**File**: `EcoStyle.tsx`
**Concept**: Bringing nature to the web. Earth tones and organic imperfections.
**Features**:
- Earthy color palette (#2c3325, #8f9e83).
- Dashed lines and rounded corners.
- Organic motion (rotating circles).

## 8. Minimal / Ink Trap Fonts ✒️
**File**: `MinimalTypography.tsx`
**Concept**: Fonts originally designed for small printing (where ink would bleed into corners) now used large for aesthetic effect.
**Features**:
- Extreme contrast.
- Tight tracking (letter-spacing).
- Minimal layout with high readability.

## 9. 3D Objects & Motion 🧊
**File**: `ThreeDObject.tsx`
**Concept**: True 3D elements running natively in the browser using WebGL.
**Features**:
- Powered by **React Three Fiber**.
- Real-time lighting and shadows.
- Interactive mesh that responds to mouse hover.


## 10. 3D User Card (Holographic Tilt) 🪪
**File**: `UserCard3D.tsx`
**Concept**: A premium profile card that mimics a physical holographic card.
**Features**:
- **3D Tilt**: Card follows mouse movement with spring physics.
- **Holographic Glare**: An overlay shine that moves opposite to the rotation.
- **Parallax Depth**: Elements inside the card (Avatar, Badges) float at different Z-depths.


## 11. 3D Album Product Card 🎵
**File**: `AlbumCard3D.tsx`
**Concept**: A digital collectible vinyl record interaction.
**Features**:
- **Vinyl Slide**: Hovering over the cover triggers the record to spin and slide out.
- **Micro-interactions**: Play/Like buttons appear on hover with backdrop blur.
- **Physical Tilt**: The entire assembly responds to mouse tilt physics.


## 12. 3D Flip Product Card 👟
**File**: `FlipCard3D.tsx`
**Concept**: E-commerce product card inspired by modern sneaker drops.
**Features**:
- **180° Flip**: Rotates completely on hover to reveal secondary information.
- **Floating Element**: Product image floats subtly to create depth.
- **Glassmorphism**: Badge and overlays use backdrop blur.


## 13. Music Flip & Motion Cards 🎧
**File**: `SongCard3D.tsx`, `MusicProductGrid.tsx`
**Concept**: Responsive eCommerce grid for digital music products.
**Features**:
- **Double-Sided Info**: Front shows art/title, back shows full details and purchase options.
- **Floating 3D Notes**: Decorative elements float with depth.
- **Waveform Animation**: Simulated audio visualization on the back.
- **Responsive Layout**: Auto-adapts from 1 to 4 columns.

---
**How to use:**
All components are unified in `DesignShowcase.tsx`. To add them to other parts of the app, simply import the component and drop it in. Most are self-contained.
