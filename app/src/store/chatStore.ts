import { create } from 'zustand';

export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

interface ChatStore {
    messages: Message[];
    isOpen: boolean;
    isTyping: boolean;
    currentMode: string;
    avatarId: string;
    toggleChat: () => void;
    setOpen: (open: boolean) => void;
    setMode: (mode: string) => void;
    setAvatar: (avatarId: string) => void;
    addMessage: (content: string, role: 'user' | 'assistant') => void;
    clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
    messages: [
        {
            id: '1',
            role: 'assistant',
            content: 'สวัสดีค่ะพี่ ยินดีต้อนรับสู่ Divaparadises นะคะ! วันนี้อยากให้ Diva ช่วยหาเพลงแนวไหน หรือมีอะไรให้ Diva ช่วยแนะนำไหมคะ? 🎵✨',
            timestamp: new Date(),
        }
    ],
    isOpen: false,
    isTyping: false,
    currentMode: 'diva_receptionist',
    avatarId: 'diva_elegance',
    toggleChat: () => set((state) => ({ isOpen: !state.isOpen })),
    setOpen: (open) => set({ isOpen: open }),
    setMode: (mode) => set({ currentMode: mode }),
    setAvatar: (avatarId) => set({ avatarId }),
    addMessage: (content, role) => {
        const newMessage: Message = {
            id: Math.random().toString(36).substring(7),
            role,
            content,
            timestamp: new Date(),
        };
        set((state) => ({
            messages: [...state.messages, newMessage],
            isTyping: role === 'user'
        }));

        // Get AI Response from real AI Service
        if (role === 'user') {
            setTimeout(async () => {
                const currentState = useChatStore.getState();
                try {
                    // Import AI Service dynamically
                    const { aiService } = await import('../services/aiService');
                    const { getSkillsSystemPrompt } = await import('../config/skills');

                    let aiResponseText: string;

                    // Use AI Specialist system prompt if mode is not default
                    const systemPrompt = currentState.currentMode === 'diva_receptionist'
                        ? undefined // Use default (which we updated to Diva)
                        : getSkillsSystemPrompt(currentState.currentMode as any);

                    console.log(`🤖 Using AI Mode: ${currentState.currentMode}`);

                    const response = await aiService.sendMessage(
                        content,
                        systemPrompt,
                        currentState.messages.slice(0, -1) // Send conversation history
                    );

                    if (response.success && response.text) {
                        aiResponseText = response.text;
                    } else {
                        console.error('❌ AI Response failed:', response.error);
                        aiResponseText = `ขออภัยค่ะ พี่คะ ดูเหมือนระบบเชื่อมต่อ AI จะขัดข้องเล็กน้อย (${response.error || 'Unknown Error'}) Diva แนะนำให้พี่ตรวจสอบ VITE_GEMINI_API_KEY ในไฟล์ .env.local หรือลองใหม่อีกครั้งนะคะ 😊`;
                    }

                    const aiResponse: Message = {
                        id: Math.random().toString(36).substring(7),
                        role: 'assistant',
                        content: aiResponseText,
                        timestamp: new Date(),
                    };

                    set((state) => ({
                        messages: [...state.messages, aiResponse],
                        isTyping: false
                    }));
                } catch (error) {
                    console.error('AI Response Error:', error);
                    // Fallback to mock on error
                    const aiResponse: Message = {
                        id: Math.random().toString(36).substring(7),
                        role: 'assistant',
                        content: getMockResponse(content),
                        timestamp: new Date(),
                    };
                    set((state) => ({
                        messages: [...state.messages, aiResponse],
                        isTyping: false
                    }));
                }
            }, 1500);
        }
    },
    clearMessages: () => set({
        messages: [{
            id: '1',
            role: 'assistant',
            content: 'สวัสดีค่ะพี่ ยินดีต้อนรับสู่ Divaparadises นะคะ! ✨',
            timestamp: new Date(),
        }]
    }),
}));

function getMockResponse(input: string): string {
    const text = input.toLowerCase();
    if (text.includes('เพลง') || text.includes('music')) return 'ตอนนี้ Diva แนะนำแนว Jazz หรือ Acoustic นุ่มๆ ให้พี่นะคะ ลองกดฟังที่หน้าหลักได้เลยค่ะ! 🎺';
    if (text.includes('สวัสดี') || text.includes('hello')) return 'สวัสดีค่ะ! วันนี้ Diva พร้อมเป็นเพื่อนฟังเพลงพรีเมียมให้พี่แล้วค่ะ 😊';
    if (text.includes('ชอบ') || text.includes('vibe')) return 'ดีใจที่พี่ชอบนะคะ! Diva ตั้งใจเลือกสิ่งที่ดีที่สุดให้พี่เสมอค่ะ ❤️';
    return 'Diva รับทราบค่ะ! พี่อยากให้ Diva ช่วยทำอะไรเพิ่มเติมเกี่ยวกับเพลงในพาราไดซ์แห่งนี้ไหมคะ? ✨';
}
