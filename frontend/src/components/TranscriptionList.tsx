import React, { useEffect, useRef } from 'react';
import type { TranscriptionEntry } from '../types/live';

interface TranscriptionListProps {
  entries: TranscriptionEntry[];
}

const TranscriptionList: React.FC<TranscriptionListProps> = ({ entries }) => {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [entries]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 max-h-[400px] scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
      {entries.length === 0 && (
        <div className="text-center text-slate-500 italic py-10">
          Waiting for the conversation to start...
        </div>
      )}
      {entries.map((entry) => (
        <div 
          key={entry.id}
          className={`flex flex-col ${entry.role === 'user' ? 'items-end' : 'items-start'}`}
        >
          <div className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm shadow-sm transition-all animate-in fade-in slide-in-from-bottom-2 ${
            entry.role === 'user' 
              ? 'bg-indigo-600 text-white rounded-tr-none' 
              : 'bg-slate-800 text-slate-100 rounded-tl-none border border-slate-700'
          }`}>
            {entry.text}
          </div>
          <span className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider px-1">
            {entry.role === 'user' ? 'You' : 'Gemini'}
          </span>
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
};

export default TranscriptionList;
