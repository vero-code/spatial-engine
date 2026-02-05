import React, { useState } from 'react';

interface EconomicEngineProps {
  baseUrl: string;
  onLog: (msg: string, type?: string) => void;
  onAnalysisComplete?: (data: any) => void;
}

const EconomicEngine: React.FC<EconomicEngineProps> = ({ baseUrl, onLog, onAnalysisComplete }) => {
  const [inputs, setInputs] = useState({ oldW: 60, newW: 9, price: 5.99, hours: 5, rate: 0.17, budget: 50 });
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Derived state: recalculate lamps based on budget and price
  const lampCount = Math.floor(inputs.budget / inputs.price) || 0;

  const analyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${baseUrl}/roi-analysis?old_watts=${inputs.oldW}&new_watts=${inputs.newW}&price=${inputs.price}&hours=${inputs.hours}&rate=${inputs.rate}&count=${lampCount}`, {
        method: 'POST'
      });
      const data = await response.json();
      setResults(data);
      if (onAnalysisComplete) onAnalysisComplete(data);
      onLog(`ROI Analysis complete. Replacing ${lampCount} lamps saves $${data.annual_savings_usd} annually.`, 'success');
    } catch (err) {
      onLog(`ROI Analysis failed. check backend connection.`, 'warn');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 glass-panel p-6 relative overflow-hidden">
        {/* Background glow for Generative UI feel */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-accent-primary/10 rounded-full blur-[100px] pointer-events-none" />
        
        <div className="flex justify-between items-start mb-6">
          <h3 className="text-sm font-bold uppercase tracking-widest text-gray-400">Energy ROI & Economic Core</h3>
          <div className="px-3 py-1 bg-accent-secondary/10 border border-accent-secondary/30 rounded-full">
            <span className="text-[10px] font-mono text-accent-secondary uppercase font-bold animate-pulse">System Online</span>
          </div>
        </div>

        <form onSubmit={analyze} className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-6">
             <Input label="Current Wattage (W)" value={inputs.oldW} onChange={v => setInputs({ ...inputs, oldW: Number(v) })} />
             <Input label="New Energy-Efficient (W)" value={inputs.newW} onChange={v => setInputs({ ...inputs, newW: Number(v) })} />
             <Input label="Unit Price (USD)" value={inputs.price} step={0.01} onChange={v => setInputs({ ...inputs, price: Number(v) })} />
          </div>

          <div className="space-y-6">
             <div className="flex flex-col gap-3">
                <div className="flex justify-between items-center">
                  <label className="text-[10px] text-gray-500 font-bold uppercase tracking-tighter">Investment Budget ($)</label>
                  <span className="text-sm font-mono text-white bg-white/5 px-2 py-0.5 rounded border border-white/10">${inputs.budget}</span>
                </div>
                <input 
                  type="range" 
                  min="5" 
                  max="500" 
                  step="5"
                  value={inputs.budget} 
                  onChange={e => setInputs({ ...inputs, budget: Number(e.target.value) })}
                  className="w-full accent-accent-primary bg-white/5 h-1.5 rounded-lg appearance-none cursor-pointer hover:bg-white/10 transition-all"
                />
             </div>

             <div className="p-4 bg-accent-primary/5 border border-accent-primary/20 rounded-xl flex flex-col items-center justify-center gap-1 group hover:border-accent-primary/40 transition-all duration-500">
                <span className="text-[10px] uppercase font-bold text-gray-500 group-hover:text-accent-primary transition-colors">Calculated Lamp Count</span>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-black text-white font-mono tracking-tighter drop-shadow-[0_0_10px_rgba(0,163,255,0.3)]">{lampCount}</span>
                  <span className="text-xs text-gray-400 font-bold uppercase tracking-widest">Units</span>
                </div>
             </div>

             <Input label="Daily Usage (Hrs)" value={inputs.hours} onChange={v => setInputs({ ...inputs, hours: Number(v) })} />
             <Input label="Rate ($/kWh)" value={inputs.rate} step={0.01} onChange={v => setInputs({ ...inputs, rate: Number(v) })} />
          </div>
          
          <div className="md:col-span-2 pt-4">
            <button type="submit" disabled={loading} className="w-full btn-premium btn-glow py-4 text-sm font-bold tracking-widest">
              {loading ? 'Synthesizing Economic Data...' : 'RECALCULATE GLOBAL SAVINGS'}
            </button>
          </div>
        </form>

        {results && (
          <div className="mt-8 grid grid-cols-3 gap-4 p-6 bg-white/[0.02] rounded-2xl border border-white/10 animate-fade-in divide-x divide-white/5">
            <ResultItem label="Annual Savings" value={`$${results.annual_savings_usd}`} />
            <ResultItem label="Payback Period" value={`${results.payback_period_months} mo`} />
            <ResultItem label="CO₂ Reduction" value={`${results.co2_reduction_kg} kg`} />
          </div>
        )}

        {results?.roi_chart_image && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
             <div className="p-4 bg-black/40 rounded-lg border border-white/10 overflow-hidden">
               <img src={`data:image/png;base64,${results.roi_chart_image}`} alt="ROI Payback Chart" className="w-full rounded scale-105 hover:scale-100 transition-transform duration-700" />
             </div>
             {results?.consumption_chart_image && (
               <div className="p-4 bg-black/40 rounded-lg border border-white/10 overflow-hidden">
                 <img src={`data:image/png;base64,${results.consumption_chart_image}`} alt="Consumption Chart" className="w-full rounded scale-105 hover:scale-100 transition-transform duration-700" />
               </div>
             )}
          </div>
        )}
      </div>

      <div className="glass-panel p-6 flex flex-col">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Utility Market Feed</h3>
        <div className="space-y-4 flex-grow">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Enter City/Region..." 
              className="flex-grow bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-accent-primary transition-all focus:ring-1 focus:ring-accent-primary/30"
            />
            <button className="px-4 py-2 bg-white/10 rounded-lg text-xs font-bold hover:bg-white/20 transition-colors">Fetch</button>
          </div>
          <div className="flex-grow flex flex-col justify-center items-center opacity-40 italic text-center p-8">
             <div className="w-8 h-8 border-2 border-accent-primary border-t-transparent rounded-full animate-spin mb-4" />
             <p className="text-xs text-gray-500 leading-relaxed">
               Economic agent synchronizing with real-time utility market data...
             </p>
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
      className="bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent-primary"
    />
  </div>
);

const ResultItem = ({ label, value }: { label: string; value: string }) => (
  <div className="flex flex-col items-center gap-1">
    <span className="text-[10px] uppercase font-bold text-gray-500">{label}</span>
    <span className="text-xl font-bold text-accent-secondary font-mono">{value}</span>
  </div>
);

export default EconomicEngine;
