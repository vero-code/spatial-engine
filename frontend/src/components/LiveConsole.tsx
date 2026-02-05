import React, { useState } from 'react';

const LiveConsole: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'audio' | 'video'>('audio');

  return (
    <div className="h-full flex flex-col animate-fade-in">
        <div className="glass-panel p-8 h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white font-display">
                    Gemini <span className="text-accent-primary">Live</span> Console
                </h2>
                <div className="flex gap-2 bg-black/20 p-1 rounded-lg">
                    <button
                        onClick={() => setActiveTab('audio')}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                            activeTab === 'audio' 
                            ? 'bg-accent-primary text-white shadow-lg' 
                            : 'text-gray-400 hover:text-white hover:bg-white/5'
                        }`}
                    >
                        🎤 Microphone
                    </button>
                    <button
                        onClick={() => setActiveTab('video')}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                            activeTab === 'video' 
                            ? 'bg-accent-primary text-white shadow-lg' 
                            : 'text-gray-400 hover:text-white hover:bg-white/5'
                        }`}
                    >
                        📸 Camera + Mic
                    </button>
                </div>
                <div className="flex gap-2">
                    <span className="px-3 py-1 bg-white/5 rounded-full text-xs font-mono text-gray-400 border border-white/10">
                        STATUS: READY
                    </span>
                </div>
            </div>
            
            <div className="flex-grow flex items-center justify-center border-2 border-dashed border-white/5 rounded-xl bg-white/5 relative overflow-hidden group">
                {activeTab === 'audio' ? (
                    <div className="text-center">
                        <div className="w-24 h-24 rounded-full bg-accent-primary/10 mx-auto mb-4 flex items-center justify-center border border-accent-primary/20 group-hover:border-accent-primary/40 transition-colors">
                            <span className="text-4xl">🎤</span>
                        </div>
                        <p className="text-gray-400 font-medium">Audio Stream Ready</p>
                        <p className="text-gray-600 text-sm mt-2">Waiting for connection...</p>
                    </div>
                ) : (
                    <div className="text-center">
                         <div className="w-24 h-24 rounded-full bg-accent-secondary/10 mx-auto mb-4 flex items-center justify-center border border-accent-secondary/20 group-hover:border-accent-secondary/40 transition-colors">
                            <span className="text-4xl">📸</span>
                        </div>
                        <p className="text-gray-400 font-medium">Multimodal Stream Ready</p>
                         <p className="text-gray-600 text-sm mt-2">Camera and Microphone access standby</p>
                    </div>
                )}
            </div>
        </div>
    </div>
  );
};

export default LiveConsole;
