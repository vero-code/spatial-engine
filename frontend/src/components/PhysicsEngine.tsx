import React, { useState } from 'react';

interface PhysicsEngineProps {
  onCalculateLux: (lux: number) => void;
  onGenerateReport: (report: any) => void;
}

const PhysicsEngine: React.FC<PhysicsEngineProps> = ({ onCalculateLux, onGenerateReport }) => {
  const [luxInputs, setLuxInputs] = useState({ lumens: 800, dist: 2.5, angle: 120 });
  const [optiInputs, setOptiInputs] = useState({ area: 20, target: 150, current: 800 });
  const [report, setReport] = useState<any>(null);

  const calculateLux = (e: React.FormEvent) => {
    e.preventDefault();
    const rad = (luxInputs.angle * Math.PI) / 180;
    const solidAngle = 2 * Math.PI * (1 - Math.cos(rad / 2));
    const candela = luxInputs.lumens / solidAngle;
    const res = Math.round(candela / (luxInputs.dist * luxInputs.dist));
    onCalculateLux(res);
  };

  const generateReport = (e: React.FormEvent) => {
    e.preventDefault();
    const required = optiInputs.area * optiInputs.target;
    const deficit = Math.max(0, required - optiInputs.current);
    const bulbs = Math.ceil(deficit / 800);
    const newReport = { deficit, bulbs, target: optiInputs.target, avg: Math.round(optiInputs.current / optiInputs.area) };
    setReport(newReport);
    onGenerateReport(newReport);
  };

  return (
    <div className="animate-fade-in grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Lux Calculator</h3>
        <form onSubmit={calculateLux} className="space-y-4">
          <Input label="Lumens (lm)" value={luxInputs.lumens} onChange={v => setLuxInputs({ ...luxInputs, lumens: Number(v) })} />
          <Input label="Distance (m)" value={luxInputs.dist} step={0.1} onChange={v => setLuxInputs({ ...luxInputs, dist: Number(v) })} />
          <Input label="Beam Angle (°)" value={luxInputs.angle} onChange={v => setLuxInputs({ ...luxInputs, angle: Number(v) })} />
          <button type="submit" className="w-full btn-premium btn-glow mt-4">Calculate Lux</button>
        </form>
      </div>

      <div className="lg:col-span-2 glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Optimization Engine</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <form onSubmit={generateReport} className="space-y-4">
            <Input label="Room Area (m²)" value={optiInputs.area} onChange={v => setOptiInputs({ ...optiInputs, area: Number(v) })} />
            <div className="flex flex-col gap-2">
              <label className="text-xs text-gray-500 font-semibold uppercase">Target Standard</label>
              <select 
                className="bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent-primary"
                value={optiInputs.target}
                onChange={e => setOptiInputs({ ...optiInputs, target: Number(e.target.value) })}
              >
                <option value={500}>Office (500 Lux)</option>
                <option value={300}>Kitchen (300 Lux)</option>
                <option value={150}>Living Room (150 Lux)</option>
                <option value={100}>Corridor (100 Lux)</option>
              </select>
            </div>
            <Input label="Current Lumens (lm)" value={optiInputs.current} onChange={v => setOptiInputs({ ...optiInputs, current: Number(v) })} />
            <button type="submit" className="w-full btn-premium btn-glow mt-2">Generate Report</button>
          </form>

          <div className="bg-black/20 rounded-xl p-6 border-l-4 border-accent-primary">
            {!report ? (
              <p className="text-gray-500 italic text-sm">Enter parameters to visualize optimization strategy.</p>
            ) : (
              <div className="space-y-4 animate-fade-in">
                <div>
                  <p className="text-xs uppercase font-bold text-gray-500 mb-1">Status</p>
                  <p className={`font-bold ${report.deficit > 0 ? 'text-accent-danger' : 'text-accent-secondary'}`}>
                    {report.deficit > 0 ? 'CRITICAL DEFICIT ⚠️' : 'OPTIMAL COMPLIANCE ✅'}
                  </p>
                </div>
                <div className="text-sm space-y-2">
                  <p>Current average: <span className="text-white font-mono">{report.avg} lux</span></p>
                  <p>Target standard: <span className="text-white font-mono">{report.target} lux</span></p>
                  {report.deficit > 0 && (
                    <p className="text-gray-300 mt-4 leading-relaxed">
                      Engineering Recommendation: Add <span className="text-accent-primary font-bold">{report.bulbs}</span> more sources 
                      (approx 800lm each) to reach safe levels.
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const Input = ({ label, value, onChange, step = 1 }: { label: string; value: number; onChange: (v: string) => void; step?: number }) => (
  <div className="flex flex-col gap-2">
    <label className="text-xs text-gray-500 font-semibold uppercase">{label}</label>
    <input 
      type="number" 
      step={step}
      value={value}
      onChange={e => onChange(e.target.value)}
      className="bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent-primary transition-colors"
    />
  </div>
);

export default PhysicsEngine;
