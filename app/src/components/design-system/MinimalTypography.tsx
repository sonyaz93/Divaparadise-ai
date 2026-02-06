export function MinimalTypography() {
    return (
        <div className="bg-white text-black p-12 min-h-[400px] flex flex-col justify-between">
            <div className="flex justify-between items-start border-b border-black pb-4">
                <span>VOL. 24</span>
                <span className="font-bold">INK TRAP STUDIO</span>
                <span>2026</span>
            </div>

            <div className="flex-1 flex flex-col justify-center py-12">
                <h1 className="text-9xl font-black tracking-tighter leading-[0.8]">
                    INK<br />
                    <span className="text-transparent stroke-text-black hover:text-black transition-colors duration-500 cursor-none">TRAP</span>
                </h1>
            </div>

            <div className="grid grid-cols-3 gap-8">
                <p className="text-sm font-medium max-w-xs">
                    Typography that acts as the primary visual element. High contrast, negative space, and deliberate readability.
                </p>
                <div className="col-span-2 border-t border-black pt-2 flex justify-between text-xs">
                    <span>( FIG. 1 )</span>
                    <span>READABILITY OPTIMIZED</span>
                </div>
            </div>

            <style>{`
        .stroke-text-black {
            -webkit-text-stroke: 2px black;
        }
      `}</style>
        </div>
    );
}
