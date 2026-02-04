import React from 'react';

interface DashboardProps {
  roomState: {
    area: number;
    reflection: number;
    lumens: number;
    lux: number;
  };
  logs: Array<{ id: string; msg: string; type: string; time: string }>;
}

const Dashboard: React.FC<DashboardProps> = ({ roomState, logs }) => {
  return (
    <div className="animate-fade-in space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500">Room State Summary</h3>
            <span className="px-2 py-1 bg-accent-primary/20 text-accent-primary text-[10px] font-bold rounded border border-accent-primary/30">LATEST_SCAN</span>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <Metric label="Total Area" value={`${roomState.area === 0 ? '--' : roomState.area} m²`} />
            <Metric label="Wall Albedo" value={roomState.reflection === 0 ? '--' : roomState.reflection.toString()} />
            <Metric label="Total Lumens" value={`${roomState.lumens === 0 ? '--' : roomState.lumens} lm`} />
            <Metric label="Avg. Lux" value={`${roomState.lux === 0 ? '--' : roomState.lux} lux`} highlight />
          </div>
        </div>

        <div className="glass-panel p-6">
          <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Compliance Status</h3>
          <div className="flex flex-col items-center justify-center min-h-[100px] text-center">
            {roomState.lux === 0 ? (
              <p className="text-gray-500 italic">Waiting for data...</p>
            ) : roomState.lux >= 500 ? (
              <div className="text-accent-secondary">
                <p className="text-4xl mb-2">✅</p>
                <p className="font-bold">ISO COMPLIANT</p>
                <p className="text-xs opacity-70">(Office Standard)</p>
              </div>
            ) : (
              <div className="text-accent-danger">
                <p className="text-4xl mb-2">⚠️</p>
                <p className="font-bold">NON-COMPLIANT</p>
                <p className="text-xs opacity-70">(Deficit Detected)</p>
              </div>
            )}
          </div>
        </div>

        <div className="lg:col-span-3 glass-panel p-6">
          <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-4">Physics Reasoning Log</h3>
          <div className="terminal-box h-48 flex flex-col gap-1">
            {logs.map(log => (
              <p key={log.id} className={`text-xs ${log.type === 'success' ? 'text-accent-secondary' : log.type === 'warn' ? 'text-accent-gold' : 'text-accent-primary'}`}>
                <span className="opacity-50 mr-2">[{log.time}]</span>
                {log.msg}
              </p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const Metric = ({ label, value, highlight = false }: { label: string; value: string; highlight?: boolean }) => (
  <div className="flex flex-col gap-1">
    <span className="text-xs text-gray-500">{label}</span>
    <span className={`text-2xl font-bold ${highlight ? 'text-accent-gold' : 'text-white'}`}>{value}</span>
  </div>
);

export default Dashboard;
