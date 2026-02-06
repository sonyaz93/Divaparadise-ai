use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct AudioEngine {
    gain: f32,
    peak_value: f32,
}

#[wasm_bindgen]
impl AudioEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            gain: 1.0,
            peak_value: 0.0,
        }
    }

    /// ปรับระดับ Gain (ระดับเสียง)
    pub fn set_gain(&mut self, value: f32) {
        self.gain = value.clamp(0.0, 2.0);
    }

    /// ประมวลผล Array ของเสียง (PCM Audio Data)
    /// ฟังก์ชันนี้จะรับข้อมูลเสียงดิบมาจัดการระดับความดังและส่งกลับคืน
    pub fn process_audio(&mut self, audio_data: &mut [f32]) {
        let mut local_max = 0.0;
        
        for sample in audio_data.iter_mut() {
            // 1. Apply Gain
            *sample *= self.gain;
            
            // 2. Simple Limiter (ป้องกันเสียงแตก)
            if *sample > 1.0 { *sample = 1.0; }
            if *sample < -1.0 { *sample = -1.0; }

            // 3. Track Peak for Visualizer
            let abs_sample = sample.abs();
            if abs_sample > local_max {
                local_max = abs_sample;
            }
        }

        // เก็บค่า Peak เพื่อให้นำไปแสดงผล Visualizer ได้
        self.peak_value = local_max;
    }

    /// คืนค่าระดับเสียงสูงสุดที่ประมวลผลไปล่าสุด (ใช้สำหรับ Visualizer)
    pub fn get_peak(&self) -> f32 {
        self.peak_value
    }

    /// คำนวณ Spectrum data (แบ่งย่านความถี่เบื้องต้น)
    /// รับข้อมูลความถี่ดิบจาก AnalyserNode (FFT) และสรุปความแรงของแต่ละย่าน
    pub fn calculate_spectrum(&self, freq_data: &[u8], num_bars: usize) -> Vec<f32> {
        let chunk_size = freq_data.len() / num_bars;
        let mut bars = Vec::with_capacity(num_bars);

        for i in 0..num_bars {
            let start = i * chunk_size;
            let end = (i + 1) * chunk_size;
            let chunk = &freq_data[start..end];
            
            // หาค่าเฉลี่ยความแรงในย่านนี้
            let sum: f32 = chunk.iter().map(|&x| x as f32).sum();
            let avg = sum / chunk_size as f32;
            
            // Normalize ให้เป็นค่า 0.0 - 1.0 (ปกติ u8 คือ 0-255)
            bars.push((avg / 255.0).powf(1.5)); // ยกกำลัง 1.5 เพื่อให้การเต้นชัดเจนขึ้น (Contrast)
        }
        
        bars
    }
}

/// Helper ฟังก์ชันสำหรับ Debug ในเบราว์เซอร์
#[wasm_bindgen]
pub fn init_engine() {
    #[cfg(feature = "console")]
    console_error_panic_hook::set_once();
    
    web_sys::console::log_1(&"Divaparadises Core Engine (Rust) Initialized".into());
}
