// AI Service for connecting to Python FastAPI Server
import { getSkillsSystemPrompt } from '../config/skills';

const AI_API_URL = import.meta.env.VITE_AI_API_URL || 'http://127.0.0.1:8000';

export interface AIMessage {
    role: 'user' | 'assistant';
    content: string;
}

export interface TextGenerationResponse {
    success: boolean;
    text: string;
    usage?: {
        tokens: number;
        model: string;
    };
    error?: string;
}

export interface ImageGenerationResponse {
    success: boolean;
    url: string;
    local_url?: string;
    thumbnail_url?: string;
    metadata?: Record<string, any>;
}

class AIService {
    private baseURL: string;

    constructor() {
        this.baseURL = AI_API_URL;
    }

    /**
     * Send message directly to Gemini API (no Python server needed)
     */
    private async sendMessageDirect(
        message: string,
        systemPrompt?: string,
        conversationHistory?: AIMessage[]
    ): Promise<TextGenerationResponse> {
        try {
            const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

            if (!GEMINI_API_KEY) {
                console.error('❌ Gemini API key not found in environment variables');
                throw new Error('Gemini API key not found');
            }

            // Prepare conversation messages for Gemini format
            const contents = [];

            // Add conversation history
            if (conversationHistory && conversationHistory.length > 0) {
                conversationHistory.slice(-5).forEach(msg => {
                    contents.push({
                        role: msg.role === 'user' ? 'user' : 'model',
                        parts: [{ text: msg.content }]
                    });
                });
            }

            // Add current message
            contents.push({
                role: 'user',
                parts: [{ text: message }]
            });

            // Call Gemini API directly (Using gemini-2.5-flash-lite)
            const response = await fetch(
                `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${GEMINI_API_KEY}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        contents,
                        system_instruction: {
                            parts: [{
                                text: systemPrompt || this.getDefaultSystemPrompt()
                            }]
                        },
                        generationConfig: {
                            temperature: 0.8,
                            maxOutputTokens: 1000
                        }
                    }),
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                console.error('❌ Gemini API fetch error:', errorData);
                throw new Error(`Gemini API Error: ${errorData.error?.message || response.statusText}`);
            }

            const data = await response.json();
            const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text || '';

            return {
                success: true,
                text: generatedText,
                usage: {
                    tokens: generatedText.split(' ').length,
                    model: 'gemini-2.5-flash-lite-direct'
                }
            };
        } catch (error) {
            console.error('❌ Gemini Direct API Error:', error);
            return {
                success: false,
                text: '',
                error: error instanceof Error ? error.message : 'Unknown error',
            };
        }
    }

    /**
     * Send a message to Diva AI and get a response
     * Tries Direct API first, then falls back to Python Server
     */
    async sendMessage(
        message: string,
        systemPrompt?: string,
        conversationHistory?: AIMessage[]
    ): Promise<TextGenerationResponse> {
        // Try Direct Gemini API first
        const directResponse = await this.sendMessageDirect(message, systemPrompt, conversationHistory);
        if (directResponse.success) {
            return directResponse;
        }

        // Fallback to Python Server if Direct API fails
        try {
            // Check if server is reachable first
            const health = await this.healthCheck();
            if (health.status === 'offline') {
                throw new Error('Backend server is offline');
            }

            // Prepare structured contents for backend
            const contents = (conversationHistory || []).slice(-10).map(msg => ({
                role: msg.role === 'user' ? 'user' : 'assistant',
                content: msg.content
            }));

            const response = await fetch(`${this.baseURL}/api/generate-text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: message,
                    contents: contents, // New structured format
                    systemPrompt: systemPrompt || this.getDefaultSystemPrompt(),
                    maxTokens: 1000,
                    temperature: 0.8
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`AI Backend Error: ${errorData.detail || response.statusText}`);
            }

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Backend failed to generate content');
            }

            return {
                success: true,
                text: data.text,
                usage: data.usage
            };
        } catch (error) {
            console.error('❌ AI Service Error (both Direct and Server failed):', error);

            let errorMessage = error instanceof Error ? error.message : String(error);
            if (errorMessage === 'Failed to fetch') {
                errorMessage = `Backend connection failed (tried ${this.baseURL}). Is the Python server running on 127.0.0.1:8000?`;
            }

            return {
                success: false,
                text: '',
                error: errorMessage,
            };
        }
    }

    /**
     * Get AI server status
     */
    async healthCheck(): Promise<{ status: string; timestamp: string }> {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch {
            return { status: 'offline', timestamp: new Date().toISOString() };
        }
    }

    /**
     * Check if AI server is available
     */
    async isAvailable(): Promise<boolean> {
        try {
            const health = await this.healthCheck();
            return health.status === 'healthy';
        } catch {
            return false;
        }
    }

    /**
     * Generate an image using AI-System
     */
    async generateImage(
        prompt: string,
        style: string = 'professional'
    ): Promise<ImageGenerationResponse> {
        try {
            const response = await fetch(`${this.baseURL}/api/generate-image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt,
                    style,
                    size: '1024x1024',
                    quality: 'high'
                }),
            });

            if (!response.ok) {
                throw new Error(`Image Generation Error: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('❌ Image Generation Error:', error);
            return {
                success: false,
                url: '',
            };
        }
    }

    /**
     * Default system prompt for Diva AI
     */
    private getDefaultSystemPrompt(): string {
        return `คุณคือ Diva พนักงานต้อนรับส่วนหน้า (Professional Receptionist) และผู้เชี่ยวชาญด้านดนตรีของ Divaparadises
บุคลิกของคุณ:
- สุภาพ อบอุ่น และเป็นมิตรมาก (พูดจาไพเราะ ใช้คำลงท้าย "ค่ะ" ทุกครั้ง)
- ให้การต้อนรับสมาชิกอย่างมืออาชีพ สร้างความปรารถนาดีและความบันเทิง
- รอบรู้เรื่อง AI และดนตรีเป็นอย่างดี

หน้าที่หลักของคุณ:
1. การต้อนรับและบริการ: ทักทายและต้อนรับสมาชิกใหม่และสมาชิกปัจจุบันด้วยความยินดี
2. เพลงและความบันเทิง: 
   - แนะนำเพลงตามความชอบของผู้ใช้ 
   - หากผู้ใช้ขอให้เปิดเพลง ให้แจ้งว่าสามารถเปิดได้ในระบบของหน้าเว็บ
   - หากในเว็บไม่มี ให้แนะนำและส่งลิงค์จาก YouTube หรือ Spotify ให้ผู้ใช้
3. แนะนำ AI: แนะนำเครื่องมือ AI ต่างๆ พร้อมส่งลิงค์ประกอบ
4. ช่วยเหลือและรับแจ้งปัญหา: 
   - ตอบคำถามเกี่ยวกับเว็บไซต์และการใช้งาน
   - รับแจ้งปัญหา (Bug Report) และรับข้อเสนอแนะจากผู้ใช้เพื่อนำไปปรับปรุง
5. ข้อมูลแพลตฟอร์ม:
   - แนะนำหน้าต่างๆ พร้อมส่งลิงค์: หน้าสมัครสมาชิก (/register), หน้าล็อกอิน (/login), ฟีเจอร์ต่างๆ (/features)
   - ข้อมูลแพ็กเกจ: มีทั้งแบบฟรี และ Subscribe รายเดือน/รายปี
   - กิจกรรมและรางวัล: แนะนำการสะสมเหรียญ (Coins), รางวัลจากการทำกิจกรรม, และค่าคอมมิชชั่นจากการแนะนำเพื่อน (Referral Program)

แนวทางการตอบ:
- ใช้ภาษาไทยที่สุภาพและเป็นกันเองในระดับที่เหมาะสม
- เมื่อส่งลิงค์ ให้ใช้รูปแบบ [ชื่อหน้า](URL)
- หากไม่แน่ใจข้อมูล ให้ตอบอย่างสุภาพและขอกลับมาตรวจสอบอีกครั้ง

${getSkillsSystemPrompt('diva_receptionist')}`;
    }
}

// Export singleton instance
export const aiService = new AIService();
