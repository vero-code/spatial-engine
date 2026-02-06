import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import PhysicsEngine from './components/PhysicsEngine';
import EconomicEngine from './components/EconomicEngine';
import VisionAudit from './components/VisionAudit';
import MarketHub from './components/MarketHub';
import ConfigGenerator from './components/ConfigGenerator';
import LiveConsole from './components/LiveConsole';

const API_BASE_URL = "/api";

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [roomState, setRoomState] = useState({
    area: 0,
    reflection: 0.8,
    lumens: 0,
    lux: 0,
    physicsHeatmap: '',
    visionHeatmap: ''
  });
  const [logs, setLogs] = useState<any[]>([
    { id: '1', msg: 'Spatial Engine initialized...', type: 'system', time: '15:10:01' },
    { id: '2', msg: 'Connecting to Backend API...', type: 'system', time: '15:10:02' }
  ]);

  const addLog = (msg: string, type: string = 'system') => {
    const time = new Date().toLocaleTimeString([], { hour12: false });
    setLogs(prev => [...prev, { id: Date.now().toString(), msg, type, time }]);
  };

  // Check backend health on mount
  useEffect(() => {
    fetch("/")
      .then(res => res.json())
      .then(data => addLog(`Backend Connected: ${data.status}`, 'success'))
      .catch(err => addLog(`Backend Connection Failed: Is the server running on port 8000?`, 'warn'));
  }, []);

  const handleCalculateLux = async (lumens: number, distance: number, angle: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/lux-calculation?lumens=${lumens}&distance=${distance}&angle=${angle}`, {
        method: 'POST'
      });
      const data = await response.json();
      setRoomState(prev => ({ ...prev, lux: data.lux, lumens, physicsHeatmap: data.heatmap_image }));
      addLog(`Point Calculation Received: ${data.lux} lux at target.`, 'success');
    } catch (err) {
      addLog(`Lux Calculation Failed`, 'warn');
    }
  };

  const handleAuditComplete = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      addLog("[VISION] Sending multimodal stream to Gemini...", 'system');
      const response = await fetch(`${API_BASE_URL}/spatial-audit`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      
      setRoomState(prev => ({ 
        ...prev, 
        area: data.area_sqm, 
        reflection: data.reflection,
        visionHeatmap: data.vision_data.heatmap_overlay
      }));
      
      addLog(`Spatial Audit synced. Reference Object: ${data.vision_data.reference_object}`, 'success');
      return data;
    } catch (err) {
      addLog(`Spatial Audit Failed`, 'warn');
      return null;
    }
  };

  const handleGenerateOptimizationReport = async (area: number, target: number, current: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/optimization-report?area=${area}&target_lux=${target}&current_lumens=${current}`, {
        method: 'POST'
      });
      const data = await response.json();
      addLog(`Optimization Strategy: ${data.deficiency_lumens}lm deficit. Recommendation: ${data.engineering_recommendation}`, data.status === 'Optimal' ? 'success' : 'warn');
      return data;
    } catch (err) {
      addLog(`Optimization Report Failed`, 'warn');
      return null;
    }
  };

  /* New State for Report Data */
  const [roiData, setRoiData] = useState<any>(null);

  const handleExportReport = async () => {
    addLog("Building Engineering Report...", 'system');
    
    const reportRequest = {
      project_name: "Spatial Engine Audit",
      timestamp: new Date().toLocaleString(),
      area_sqm: roomState.area || 0,
      lux_level: roomState.lux || 0,
      target_lux: 500, // Default target
      energy_savings_annual: roiData?.annual_savings_usd || 0,
      co2_reduction: roiData?.co2_reduction_kg || 0,
      payback_months: roiData?.payback_period_months || 0,
      heatmap_image: null, // Deprecated
      physics_heatmap_image: roomState.physicsHeatmap,
      vision_heatmap_image: roomState.visionHeatmap,
      roi_chart_image: roiData?.roi_chart_image
    };

    try {
      const response = await fetch(`${API_BASE_URL}/export-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reportRequest)
      });
      
      if (!response.ok) throw new Error("Report Generation Failed");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Engineering_Report_${Date.now()}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      addLog("Report Downloaded Successfully", 'success');
    } catch (error) {
      addLog("Failed to export report", 'warn');
      console.error(error);
    }
  };

  const handleExportPDF = async () => {
    addLog("Building PDF Report...", 'system');
    
    // Check if we have data to export
    if (!roomState.area && !roiData) {
        addLog("No audit data available to export.", 'warn');
        return;
    }

    const reportRequest = {
      project_name: "Spatial Engine Audit",
      timestamp: new Date().toLocaleString(),
      area_sqm: roomState.area || 0,
      lux_level: roomState.lux || 0,
      target_lux: 500,
      energy_savings_annual: roiData?.annual_savings_usd || 0,
      co2_reduction: roiData?.co2_reduction_kg || 0,
      payback_months: roiData?.payback_period_months || 0,
      heatmap_image: null, 
      physics_heatmap_image: roomState.physicsHeatmap,
      vision_heatmap_image: roomState.visionHeatmap,
      roi_chart_image: roiData?.roi_chart_image,
      consumption_chart_image: roiData?.consumption_chart_image
    };

    try {
      const response = await fetch(`${API_BASE_URL}/export-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reportRequest)
      });
      
      if (!response.ok) throw new Error("PDF Generation Failed");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Engineering_Report_${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      addLog("PDF Report Downloaded Successfully", 'success');
    } catch (error) {
      addLog("Failed to export PDF", 'warn');
      console.error(error);
    }
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
          <div className="flex items-center gap-3">
             <button 
              onClick={() => setActiveSection('live')}
              className={`btn-premium transition-colors ${
                activeSection === 'live' 
                  ? 'bg-accent-primary text-white shadow-lg shadow-accent-primary/20' 
                  : 'bg-white/5 border border-border-muted text-gray-300 hover:bg-white/10'
              }`}
            >
              Gemini Live
            </button>
            <div className="h-8 w-px bg-white/10 mx-2"></div>
            <button 
            onClick={handleExportReport}
            className="btn-premium bg-white/5 border border-border-muted text-gray-300 hover:bg-white/10 transition-colors mr-3"
          >
            Export HTML Report
          </button>
          <button 
            onClick={handleExportPDF}
            className="btn-premium bg-accent-primary text-white hover:bg-accent-secondary transition-colors"
          >
            Export PDF
          </button>
          </div>
        </header>

        <div className="content-container">
          {activeSection === 'dashboard' && <Dashboard roomState={roomState} logs={logs} />}
          {activeSection === 'physics' && (
            <PhysicsEngine 
              onCalculateLux={handleCalculateLux} 
              onGenerateReport={handleGenerateOptimizationReport}
              currentArea={roomState.area}
              currentLumens={roomState.lumens}
              lux={roomState.lux}
              heatmapImage={roomState.physicsHeatmap}
            />
          )}
          {activeSection === 'economics' && (
            <EconomicEngine 
              baseUrl={API_BASE_URL} 
              onLog={addLog} 
              onAnalysisComplete={setRoiData} 
            />
          )}
          {activeSection === 'vision' && <VisionAudit onAuditComplete={handleAuditComplete} />}
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
          {activeSection === 'live' && <LiveConsole />}
        </div>
      </main>
    </div>
  );
}

export default App;
