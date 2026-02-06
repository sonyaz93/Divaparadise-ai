import { useState, useRef, useEffect, Suspense, lazy } from 'react';
import { Send, X, Sparkles, User, Settings2 } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';
import { cn } from '../../lib/utils';
import { SKILLS_CATALOG } from '../../config/skills';

const Diva3DCanvas = lazy(() => import('./Diva3DCanvas'));

export function ChatPanel() {
    const { messages, isOpen, setOpen, addMessage, isTyping, currentMode, setMode } = useChatStore();
    const [input, setInput] = useState('');
    const [showModes, setShowModes] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isTyping]);

    const handleSend = () => {
        if (!input.trim()) return;
        addMessage(input, 'user');
        setInput('');
    };

    return (
        <>
            {/* 3D Robot Mascot - Persistent & Animated */}
            <div
                className={cn(
                    "fixed z-50 pointer-events-auto transition-all duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)]", // Bouncy transition
                    isOpen
                        ? "top-24 right-[26rem] w-64 h-64" // Open: Left of panel
                        : "top-28 right-4 w-48 h-48"       // Closed: Under the trigger button (slightly smaller)
                )}
            >
                <div className="w-full h-full relative">
                    <Suspense fallback={<div className="w-16 h-16 bg-purple-900/20 animate-pulse rounded-full mx-auto mt-10" />}>
                        <Diva3DCanvas />
                    </Suspense>
                </div>
            </div>

            {/* Chat Panel Container */}
            {isOpen && (
                <div className="fixed top-24 right-8 w-96 h-[600px] z-50 flex flex-col bg-black/60 backdrop-blur-3xl border border-white/10 rounded-3xl shadow-2xl shadow-purple-900/40 overflow-visible animate-in fade-in zoom-in duration-300 slide-in-from-top-4">
                    {/* Header */}
                    <div className="relative p-5 border-b border-white/10 bg-gradient-to-r from-purple-900/40 to-transparent flex items-center justify-between overflow-visible">
                        <div className="flex items-center gap-3">
                            {/* 3D Pop-out Icon */}
                            <div className="absolute -top-10 -left-6 w-28 h-28 rounded-full border-[6px] border-purple-500 shadow-[0_10px_40px_rgba(168,85,247,0.6)] z-50 bg-black overflow-hidden transform hover:scale-105 transition-transform duration-300">
                                <img src="/images/AI/item/diva-profile-cyber.png" className="w-full h-full object-cover" alt="Diva Profile" />
                                {/* Gloss effect */}
                                <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent opacity-50" />
                            </div>

                            {/* Text Container (Pushed right) */}
                            <div className="ml-24 flex flex-col justify-center h-14">
                                <div className="flex items-center gap-1.5">
                                    <h3 className="text-lg font-black italic tracking-wider text-white drop-shadow-md">DIVA <span className="text-purple-400">AI</span></h3>
                                    <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" />
                                </div>
                                <p className="text-[10px] text-green-400 font-bold bg-green-400/10 px-2 py-0.5 rounded-full w-fit">● ONLINE</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-1">
                            <button
                                onClick={() => {
                                    setShowModes(!showModes);
                                }}
                                className={cn(
                                    "p-2 rounded-full transition-colors",
                                    showModes ? "bg-purple-500/20 text-purple-400" : "hover:bg-white/10 text-gray-400 hover:text-white"
                                )}
                                title="Change AI Mode"
                            >
                                <Settings2 className="w-5 h-5" />
                            </button>
                            <button
                                onClick={() => setOpen(false)}
                                className="p-2 rounded-full hover:bg-white/10 transition-colors text-gray-400 hover:text-white"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                    </div>

                    {/* Mode Selector Overlay */}
                    {showModes && (
                        <div className="absolute top-[80px] left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-md border-b border-white/10 p-4 animate-in slide-in-from-top-2 duration-200">
                            <p className="text-[10px] uppercase tracking-wider text-gray-500 font-bold mb-3">Select AI Specialist</p>
                            <div className="grid grid-cols-1 gap-2">
                                {Object.entries(SKILLS_CATALOG).map(([key, cat]) => (
                                    <button
                                        key={key}
                                        onClick={() => {
                                            setMode(key);
                                            setShowModes(false);
                                        }}
                                        className={cn(
                                            "text-left p-3 rounded-xl text-xs transition-all border",
                                            currentMode === key
                                                ? "bg-purple-600/20 border-purple-500/50 text-white font-bold"
                                                : "bg-white/5 border-transparent text-gray-400 hover:bg-white/10 hover:text-white"
                                        )}
                                    >
                                        {cat.name}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Chat Content */}
                    <div
                        ref={scrollRef}
                        className="flex-1 overflow-y-auto p-5 pb-20 space-y-4 scrollbar-hide"
                    >
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={cn(
                                    "flex items-end gap-2 max-w-[85%]",
                                    msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto"
                                )}
                            >
                                <div className={cn(
                                    "w-10 h-10 rounded-full flex items-center justify-center text-[10px] shadow-sm overflow-hidden",
                                    msg.role === 'user' ? "bg-white/10 text-white" : "border-2 border-purple-500/30"
                                )}>
                                    {msg.role === 'user' ? (
                                        <User className="w-3 h-3" />
                                    ) : (
                                        <img src="/images/AI/item/diva-profile-cyber.png" className="w-full h-full object-cover" alt="Diva" />
                                    )}
                                </div>
                                <div className={cn(
                                    "p-3 rounded-2xl text-xs leading-relaxed shadow-sm",
                                    msg.role === 'user'
                                        ? "bg-white text-black rounded-br-none"
                                        : "bg-white/5 border border-white/10 text-gray-200 rounded-bl-none"
                                )}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}

                        {isTyping && (
                            <div className="flex items-center gap-2 mr-auto">
                                <div className="w-10 h-10 rounded-full border border-purple-500/30 overflow-hidden">
                                    <img src="/images/AI/item/diva-profile-cyber.png" className="w-full h-full object-cover" alt="Diva" />
                                </div>
                                <div className="bg-white/5 border border-white/10 p-3 rounded-2xl rounded-bl-none">
                                    <div className="flex gap-1">
                                        <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" />
                                        <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                                        <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="p-5 border-t border-white/10 bg-black/20 z-10">
                        {/* Quick Reactions Bar - 2 Rows */}
                        <div className="grid grid-cols-6 gap-2 pb-3">
                            {[
                                { emoji: '👍', label: 'Like' },
                                { emoji: '👏', label: 'Clap' },
                                { emoji: '🙏', label: 'Thanks' },
                                { emoji: '😊', label: 'Smile' },
                                { emoji: '😆', label: 'Laugh' },
                                { emoji: '😂', label: 'Joy' },
                                { emoji: '😭', label: 'Cry' },
                                { emoji: '😍', label: 'Love' },
                                { emoji: '❤️', label: 'Heart' },
                                { emoji: '👋', label: 'Bye' },
                                { emoji: '😴', label: 'Good Night' }
                            ].map((reaction) => (
                                <button
                                    key={reaction.label}
                                    onClick={() => addMessage(reaction.emoji, 'user')}
                                    className="w-10 h-10 rounded-2xl bg-white/5 border border-white/10 hover:bg-purple-500/20 hover:border-purple-500/50 hover:scale-110 active:scale-95 transition-all flex items-center justify-center text-xl shadow-sm"
                                    title={reaction.label}
                                >
                                    {reaction.emoji}
                                </button>
                            ))}
                        </div>

                        <div className="relative group/input">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Talk to Diva AI..."
                                className="w-full bg-white/5 border border-white/10 rounded-2xl py-3 pl-4 pr-12 text-xs text-white placeholder:text-gray-500 focus:outline-none focus:border-purple-500/50 transition-all group-hover/input:border-white/20"
                            />
                            <button
                                onClick={handleSend}
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-xl bg-purple-600 text-white hover:bg-purple-500 transition-all shadow-lg shadow-purple-900/40"
                            >
                                <Send className="w-3.5 h-3.5" />
                            </button>
                        </div>
                        <p className="mt-3 text-[10px] text-center text-gray-500">
                            Diva is here to curate your paradise experience.
                        </p>
                    </div>
                </div>
            )}
        </>

    );
}
