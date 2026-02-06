import { motion } from "framer-motion";

export function UtilitarianLayout() {
    return (
        <div className="border border-white/20 font-mono text-xs uppercase grid grid-cols-4 gap-px bg-white/20">
            <motion.div
                className="bg-black p-4 col-span-4 border-b border-white/20 flex justify-between items-center"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
            >
                <span>SYSTEM_STATUS: ONLINE</span>
                <span className="animate-pulse flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full" />
                    LIVE
                </span>
            </motion.div>

            <div className="bg-black p-8 col-span-4 md:col-span-3 min-h-[200px] flex flex-col justify-between">
                <h3 className="text-4xl font-bold tracking-tighter">
                    FUNCTION<br />OVER<br />FORM.
                </h3>
                <div className="w-full h-px bg-white/20 mt-8 relative">
                    <motion.div
                        className="absolute top-0 left-0 h-full bg-white w-1/4"
                        animate={{ left: ["0%", "75%", "0%"] }}
                        transition={{ duration: 5, ease: "linear", repeat: Infinity }}
                    />
                </div>
            </div>

            <div className="bg-black col-span-4 md:col-span-1 grid grid-rows-4 gap-px">
                {["DATA_01", "DATA_02", "DATA_03", "DATA_04"].map((item, i) => (
                    <div key={i} className="p-4 hover:bg-white text-white hover:text-black transition-colors cursor-pointer flex items-center justify-between group">
                        {item}
                        <span className="opacity-0 group-hover:opacity-100 mb-1">↗</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
