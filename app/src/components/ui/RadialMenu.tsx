import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RadialMenuItem {
    icon: React.ReactNode;
    label?: string;
    onClick: () => void;
}

interface RadialMenuProps {
    items: RadialMenuItem[];
    triggerIcon?: React.ReactNode;
    radius?: number;
    className?: string;
}

export const RadialMenu: React.FC<RadialMenuProps> = ({
    items,
    triggerIcon,
    radius = 100,
    className,
}) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => setIsOpen(!isOpen);

    // Animation variants
    const menuVariants = {
        closed: {
            transition: { staggerChildren: 0.05, staggerDirection: -1 }
        },
        open: {
            transition: { staggerChildren: 0.07, delayChildren: 0.1 }
        }
    };

    const itemVariants = {
        closed: { opacity: 0, scale: 0, x: 0, y: 0 },
        open: (i: number) => {
            const angle = (i * 360) / items.length;
            // Convert angle to radians for layout, adjust -90 deg to start from top
            const radian = (angle - 90) * (Math.PI / 180);
            return {
                opacity: 1,
                scale: 1,
                x: Math.cos(radian) * radius,
                y: Math.sin(radian) * radius,
                transition: { type: 'spring' as const, stiffness: 200, damping: 20 }
            };
        }
    };

    return (
        <div className={cn("relative flex items-center justify-center", className)}>
            {/* Menu Items Container */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="absolute inset-0 flex items-center justify-center top-0 left-0"
                        variants={menuVariants}
                        initial="closed"
                        animate="open"
                        exit="closed"
                    >
                        {items.map((item, index) => (
                            <motion.button
                                key={index}
                                custom={index}
                                variants={itemVariants}
                                onClick={() => {
                                    item.onClick();
                                    setIsOpen(false);
                                }}
                                className="absolute flex items-center justify-center w-12 h-12 rounded-full bg-white shadow-lg text-primary hover:bg-gray-100 hover:scale-110 active:scale-95 transition-colors z-10"
                                title={item.label}
                            >
                                {item.icon}
                            </motion.button>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Trigger Button */}
            <motion.button
                onClick={toggleMenu}
                className="relative z-20 flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 transition-all"
                whileTap={{ scale: 0.9 }}
            >
                <motion.div
                    initial={false}
                    animate={{ rotate: isOpen ? 45 : 0 }}
                    transition={{ type: "spring", stiffness: 200, damping: 20 }}
                >
                    {triggerIcon || <Plus className="w-8 h-8" />}
                </motion.div>
            </motion.button>
        </div>
    );
};
