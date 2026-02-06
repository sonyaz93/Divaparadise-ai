import { MessageSquare } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';
import { ChatPanel } from './ChatPanel';

export function AIAssistant() {
    const { toggleChat, isOpen } = useChatStore();

    return (
        <>
            <div
                onClick={toggleChat}
                className="fixed top-6 right-8 z-50 group cursor-pointer"
            >
                {!isOpen && (
                    <div className="relative">
                        {/* 3D Pop-out Icon */}
                        <div className="w-20 h-20 rounded-full border-[5px] border-purple-500 shadow-[0_10px_30px_rgba(168,85,247,0.6)] bg-black overflow-hidden transform group-hover:scale-105 transition-transform duration-300">
                            <img src="/images/AI/item/diva-profile-cyber.png" className="w-full h-full object-cover" alt="Diva" />
                            <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent opacity-50" />
                        </div>

                        {/* Label Badge */}
                        <div className="absolute -bottom-2 -right-2 bg-black/80 backdrop-blur border border-purple-500/50 px-2 py-0.5 rounded-full flex items-center gap-1.5 shadow-lg">
                            <span className="text-[10px] font-bold text-white tracking-wide">DIVA AI</span>
                            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                        </div>
                    </div>
                )}
            </div>

            <ChatPanel />
        </>
    );
}
