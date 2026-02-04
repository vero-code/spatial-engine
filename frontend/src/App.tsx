import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import PhysicsEngine from './components/PhysicsEngine';
import EconomicEngine from './components/EconomicEngine';
import VisionAudit from './components/VisionAudit';
import MarketHub from './components/MarketHub';
import ConfigGenerator from './components/ConfigGenerator';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [roomState, setRoomState] = useState({
    area: 0,
    reflection: 0.8,
    lumens: 0,
    lux: 0
  });
  const [logs, setLogs] = useState<any[]>([
    { id: '1', msg: 'Spatial Engine initialized...', type: 'system', time: '15:10:01' },
    { id: '2', msg: 'Multimodal Vision Ready (Gemini 3.0)', type: 'system', time: '15:10:02' },
    { id: '3', msg: 'Deterministic Engine Online.', type: 'system', time: '15:10:03' }
  ]);

  const addLog = (msg: string, type: string = 'system') => {
    const time = new Date().toLocaleTimeString([], { hour12: false });
    setLogs(prev => [...prev, { id: Date.now().toString(), msg, type, time }]);
  };

  const handleCalculateLux = (lux: number) => {
    setRoomState(prev => ({ ...prev, lux }));
    addLog(`Point Calculation: ${lux} lux at target.`, 'success');
  };

  const handleAuditComplete = (area: number, reflection: number) => {
    setRoomState(prev => ({ ...prev, area, reflection }));
    addLog(`Spatial Audit synced. Room Area: ${area}m²`, 'success');
  };

  return (
    <div className="flex bg-bg-dark min-h-screen text-[#c9d1d9] font-sans antialiased">
      <div className="bg-overlay"></div>
      <div className="noise-filter"></div>
      
      <Sidebar activeSection={activeSection} setActiveSection={setActiveSection} />

      <main className="ml-64 flex-grow p-12 max-w-7xl">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-4xl font-bold font-display tracking-tight text-white mb-1">
              Optical Engineer <span className="text-accent-primary">Console</span>
            </h1>
            <p className="text-gray-500 text-sm font-medium">Autonomous Physics Analysis & Energy Simulation</p>
          </div>
          <button className="btn-premium bg-white/5 border border-border-muted text-gray-300 hover:bg-white/10 transition-colors">
            Export Engineering Report
          </button>
        </header>

        <div className="content-container">
          {activeSection === 'dashboard' && <Dashboard roomState={roomState} logs={logs} />}
          {activeSection === 'physics' && <PhysicsEngine onCalculateLux={handleCalculateLux} onGenerateReport={(r) => addLog(`Optimization Report: ${r.deficit}lm deficit.`, r.deficit > 0 ? 'warn' : 'success')} />}
          {activeSection === 'economics' && <EconomicEngine />}
          {activeSection === 'vision' && <VisionAudit onAuditComplete={handleAuditComplete} log={addLog} />}
          {activeSection === 'market' && <MarketHub />}
          {activeSection === 'config' && <ConfigGenerator />}
          {activeSection === 'standards' && (
            <div className="glass-panel p-12 text-center animate-fade-in">
              <span className="text-6xl mb-6 block">📘</span>
              <h3 className="text-xl font-bold mb-2">Expert Knowledge Base (RAG)</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                Knowledge Base loaded with latest Zigbee 3.0, Matter 1.2, and ISO-8995:2026 standards.
                Search interface coming in next iteration.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
