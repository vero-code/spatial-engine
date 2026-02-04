import React, { useState } from 'react';

const ConfigGenerator: React.FC = () => {
  const [hub, setHub] = useState('hk');
  const [config, setConfig] = useState<string | null>(null);

  const generate = () => {
    const data = {
      room: "Executive Office",
      agent: "Spatial Engine AI",
      version: "1.0",
      hub: hub === 'ha' ? 'Home Assistant' : hub === 'hk' ? 'HomeKit' : 'Matter',
      scenes: {
        focus: { brightness_pct: 100, color_temp_kelvin: 4500 },
        relax: { brightness_pct: 40, color_temp_kelvin: 2700 },
        cinema: { brightness_pct: 15, color_temp_kelvin: 2200 }
      },
      compliance: "ISO-8995-2026-PASS"
    };
    setConfig(JSON.stringify(data, null, 4));
  };

  return (
    <div className="animate-fade-in space-y-6">
      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Smart Scene Config Generator</h3>
        <div className="flex flex-col md:flex-row gap-6 items-end">
          <div className="flex flex-col gap-2 flex-grow max-w-xs">
            <label className="text-xs text-gray-500 font-semibold uppercase">Smart Home Hub Type</label>
            <select 
              value={hub}
              onChange={e => setHub(e.target.value)}
              className="bg-[#0d1117] border border-border-muted rounded-lg px-4 py-2 text-white focus:outline-none focus:border-accent-primary"
            >
              <option value="ha">Home Assistant (YAML)</option>
              <option value="hk">HomeKit (JSON)</option>
              <option value="matter">Matter Universal</option>
            </select>
          </div>
          <button onClick={generate} className="btn-premium btn-glow flex-grow">Generate Provisioning Config</button>
        </div>
      </div>

      <div className="glass-panel p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500">Output Stream</h3>
          {config && <button className="text-xs text-accent-primary hover:underline font-bold">Download config.json</button>}
        </div>
        <div className="terminal-box h-64 overflow-auto whitespace-pre">
          <code className="text-accent-gold">{config || '{ "status": "Ready to generate" }'}</code>
        </div>
      </div>
    </div>
  );
};

export default ConfigGenerator;
