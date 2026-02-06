import { Home, Search, Library as LibraryIcon, SquarePlus, Heart, Music2, Palette } from 'lucide-react';
import { cn } from '../../lib/utils';

interface SidebarItemProps {
    icon: any;
    label: string;
    active?: boolean;
    onClick?: () => void;
}

function SidebarItem({ icon: Icon, label, active, onClick }: SidebarItemProps) {
    return (
        <div
            onClick={onClick}
            className={cn(
                "flex items-center gap-4 px-4 py-3 cursor-pointer transition-all rounded-lg group",
                active ? "bg-purple-900/40 text-white" : "text-gray-400 hover:text-white hover:bg-white/5"
            )}>
            <Icon className={cn("w-6 h-6", active ? "text-purple-400" : "group-hover:text-purple-400")} />
            <span className="font-medium">{label}</span>
        </div>
    );
}

export function Sidebar({ onNavigate }: { onNavigate?: (view: string) => void }) {
    return (
        <div className="w-64 h-full bg-black border-r border-white/5 flex flex-col p-4">
            {/* Branding */}
            <div className="flex items-center gap-3 px-2 mb-10 mt-2">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-purple-900/20 overflow-hidden">
                    <img src="/images/Icon/logo.png" alt="Diva Logo" className="w-full h-full object-cover scale-150" />
                </div>
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400 tracking-tight">
                    Divaparadises
                </span>
            </div>

            {/* Main Nav */}
            <div className="space-y-1 mb-8">
                <SidebarItem icon={Home} label="Home" active />
                <SidebarItem icon={Search} label="Search" />
                <SidebarItem icon={LibraryIcon} label="Your Library" />
            </div>

            {/* Playlists Section */}
            <div className="space-y-1 mb-8">
                <div className="px-4 mb-4">
                    <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Your Playlists</span>
                </div>
                <SidebarItem icon={SquarePlus} label="Create Playlist" />
                <SidebarItem icon={Heart} label="Liked Songs" />
                <div className="pt-4 border-t border-white/10 mt-4">
                    <SidebarItem
                        icon={Palette}
                        label="Design System"
                        onClick={() => onNavigate?.('design-showcase')}
                    />
                </div>
            </div>

            <div className="mt-auto p-4 rounded-2xl bg-gradient-to-br from-purple-900/20 to-indigo-900/10 border border-purple-500/20">
                <div className="flex items-center gap-3 mb-3">
                    <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">
                        <Music2 className="w-4 h-4 text-purple-400" />
                    </div>
                    <span className="text-xs font-semibold text-purple-300">Suno AI Integration</span>
                </div>
                <p className="text-[10px] text-gray-400 leading-relaxed">
                    Unlock premium features with AI-generated tracks from Suno.
                </p>
            </div>
        </div>
    );
}
