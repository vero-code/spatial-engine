import React from 'react';

interface VisualizerProps {
  isActive: boolean;
  isModelTalking: boolean;
}

const Visualizer: React.FC<VisualizerProps> = ({ isActive, isModelTalking }) => {
  return (
    <div className="relative flex items-center justify-center w-64 h-64">
      {/* Rings */}
      <div className={`absolute inset-0 rounded-full border-2 border-cyan-500/20 ${isActive ? 'pulse-ring' : ''}`} />
      <div className={`absolute inset-4 rounded-full border-2 border-blue-500/20 ${isActive ? 'pulse-ring' : ''}`} style={{ animationDelay: '0.5s' }} />
      <div className={`absolute inset-8 rounded-full border-2 border-indigo-500/20 ${isActive ? 'pulse-ring' : ''}`} style={{ animationDelay: '1s' }} />
      
      {/* Central Core */}
      <div className={`relative z-10 w-32 h-32 rounded-full flex items-center justify-center transition-all duration-500 ${
        isModelTalking 
          ? 'bg-gradient-to-tr from-cyan-400 to-blue-600 scale-110 shadow-[0_0_50px_rgba(34,211,238,0.5)]' 
          : isActive 
            ? 'bg-slate-800 border-2 border-slate-700' 
            : 'bg-slate-900 border-2 border-slate-800 opacity-50'
      }`}>
        <svg 
          className={`w-12 h-12 transition-colors duration-500 ${isModelTalking ? 'text-white' : 'text-slate-500'}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
          />
        </svg>
      </div>
      <style>{`
        @keyframes pulse-ring {
            0% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 0.3; }
            100% { transform: scale(0.8); opacity: 0.5; }
        }
        .pulse-ring {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
      `}</style>
    </div>
  );
};

export default Visualizer;
