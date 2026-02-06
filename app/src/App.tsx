import { useState } from 'react';
import { Library } from './components/library/Library';
import { DesignShowcase } from './components/design-system/DesignShowcase';
import { AudioPlayer } from './components/player/AudioPlayer';
import { Sidebar } from './components/layout/Sidebar';
import { AIAssistant } from './components/ai/AIAssistant';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('library');

  return (
    <div className="flex h-screen bg-black text-white overflow-hidden font-sans">
      {/* Sidebar Layout */}
      <Sidebar onNavigate={(view) => setCurrentView(view)} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col relative overflow-y-auto overflow-x-hidden scrollbar-hide">
        {/* Grain overlay */}
        <div className="grain-overlay pointer-events-none" />

        {/* Floating AI Assistant */}
        <AIAssistant />

        {/* Content */}
        <main className="flex-1">
          {currentView === 'library' ? <Library /> : <DesignShowcase />}
        </main>
      </div>

      {/* Audio Player (fixed at bottom) */}
      <AudioPlayer />
    </div>
  );
}

export default App;
