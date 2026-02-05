import React, { useState } from 'react';

interface EconomicEngineProps {
  baseUrl: string;
  onLog: (msg: string, type?: string) => void;
  onAnalysisComplete?: (data: any) => void;
}

const EconomicEngine: React.FC<EconomicEngineProps> = ({ baseUrl, onLog, onAnalysisComplete }) => {
  const [inputs, setInputs] = useState({ oldW: 60, newW: 9, price: 5.99, hours: 5, rate: 0.17 });
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${baseUrl}/roi-analysis?old_watts=${inputs.oldW}&new_watts=${inputs.newW}&price=${inputs.price}&hours=${inputs.hours}&rate=${inputs.rate}`, {
        method: 'POST'
      });
      const data = await response.json();
      setResults(data);
      if (onAnalysisComplete) onAnalysisComplete(data);
      onLog(`ROI Analysis complete. Annual savings: $${data.annual_savings_usd}.`, 'success');
    } catch (err) {
      onLog(`ROI Analysis failed. check backend connection.`, 'warn');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Energy ROI & CO₂ Reducer</h3>
        <form onSubmit={analyze} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input label="Current Wattage (W)" value={inputs.oldW} onChange={v => setInputs({ ...inputs, oldW: Number(v) })} />
          <Input label="New Energy-Efficient (W)" value={inputs.newW} onChange={v => setInputs({ ...inputs, newW: Number(v) })} />
          <Input label="Unit Price (USD)" value={inputs.price} step={0.01} onChange={v => setInputs({ ...inputs, price: Number(v) })} />
          <Input label="Daily Usage (Hrs)" value={inputs.hours} onChange={v => setInputs({ ...inputs, hours: Number(v) })} />
          <Input label="Rate ($/kWh)" value={inputs.rate} step={0.01} onChange={v => setInputs({ ...inputs, rate: Number(v) })} />
          
          <div className="md:col-span-2 pt-4">
            <button type="submit" disabled={loading} className="w-full btn-premium btn-glow">
              {loading ? 'Performing Economic Simulation...' : 'Analyze Financial Impact'}
            </button>
          </div>
        </form>

        {results && (
          <div className="mt-8 flex justify-around p-6 bg-accent-secondary/5 rounded-xl border border-accent-secondary/20 animate-fade-in">
            <ResultItem label="Annual Savings" value={`$${results.annual_savings_usd}`} />
            <ResultItem label="Payback Period" value={`${results.payback_period_months} months`} />
            <ResultItem label="CO₂ Reduction" value={`${results.co2_reduction_kg} kg`} />
          </div>
        )}

        {results?.roi_chart_image && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
             <div className="p-4 bg-black/40 rounded-lg border border-white/10 animate-fade-in">
               <img src={`data:image/png;base64,${results.roi_chart_image}`} alt="ROI Payback Chart" className="w-full rounded" />
             </div>
             {results?.consumption_chart_image && (
               <div className="p-4 bg-black/40 rounded-lg border border-white/10 animate-fade-in">
                 <img src={`data:image/png;base64,${results.consumption_chart_image}`} alt="Consumption Chart" className="w-full rounded" />
               </div>
             )}
          </div>
        )}
      </div>

      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Rate Lookup</h3>
        <div className="space-y-4">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Enter City/Region..." 
              className="flex-grow bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-accent-primary"
            />
            <button className="px-4 py-2 bg-white/10 rounded-lg text-xs font-bold hover:bg-white/20 transition-colors">Fetch</button>
          </div>
          <div className="text-xs text-gray-500 leading-relaxed italic border-t border-border-muted pt-4">
            Market agent fetching real-time data from local utility providers...
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
