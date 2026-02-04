import React, { useState } from 'react';

interface VisionAuditProps {
  onAuditComplete: (file: File) => Promise<any>;
}

const VisionAudit: React.FC<VisionAuditProps> = ({ onAuditComplete }) => {
  const [image, setImage] = useState<string | null>(null);
  const [isAuditing, setIsAuditing] = useState(false);
  const [checks, setChecks] = useState([
    { id: 1, label: '3x3 Grid Analysis', status: 'pending' },
    { id: 2, label: 'Material Identification', status: 'pending' },
    { id: 3, label: 'Shadow Mapping', status: 'pending' },
    { id: 4, label: 'Reference Object Inference', status: 'pending' },
  ]);
  const [heatmapOverlay, setHeatmapOverlay] = useState<string | null>(null);
  const [showHeatmap, setShowHeatmap] = useState(false);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const reader = new FileReader();
      const file = e.target.files[0];
      reader.onload = (re) => setImage(re.target!.result as string);
      reader.readAsDataURL(file);
      // We'll store the file on the input element's data attribute or just handle it in runAudit
    }
  };

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    setImage(null);
    setHeatmapOverlay(null);
    setShowHeatmap(false);
    const fileInput = document.getElementById('vision-upload') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  };

  const runAudit = async () => {
    const fileInput = document.getElementById('vision-upload') as HTMLInputElement;
    if (!fileInput.files?.[0]) return;

    setIsAuditing(true);
    setChecks(prev => prev.map(c => ({ ...c, status: 'pending' })));

    // Trigger components UI sequence before/during API call
    let step = 0;
    const interval = setInterval(() => {
      if (step < checks.length) {
        setChecks(prev => prev.map((c, i) => i === step ? { ...c, status: 'done' } : c));
        step++;
      } else {
        clearInterval(interval);
      }
    }, 500);

    const result = await onAuditComplete(fileInput.files[0]);
    setIsAuditing(false);
    
    if (result && result.vision_data && result.vision_data.heatmap_overlay) {
       setHeatmapOverlay(result.vision_data.heatmap_overlay);
       setShowHeatmap(true);
    }
    
    if (!result) {
       setChecks(prev => prev.map(c => ({ ...c, status: 'pending' })));
    }
  };

  return (
    <div className="animate-fade-in grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 glass-panel p-6 flex flex-col items-center">
        <h3 className="w-full text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Vision Audit Console</h3>
        
        <div 
          className="w-full h-[500px] border-2 border-dashed border-border-muted rounded-2xl flex flex-col items-center justify-center cursor-pointer hover:border-accent-primary transition-colors group relative overflow-hidden"
          onClick={() => document.getElementById('vision-upload')?.click()}
        >
          {heatmapOverlay && showHeatmap ? (
             <img src={`data:image/png;base64,${heatmapOverlay}`} alt="Heatmap Overlay" className="h-full w-full object-contain" />
          ) : image ? (
            <img src={image} alt="Upload" className="h-full w-full object-cover opacity-60" />
          ) : (
            <div className="text-center">
              <span className="text-5xl mb-4 block group-hover:scale-110 transition-transform">📸</span>
              <p className="text-gray-400">Drag room photo here or <span className="text-accent-primary font-bold">browse</span></p>
            </div>
          )}
          <input type="file" id="vision-upload" hidden onChange={handleUpload} />
          
          {image && (
             <div className="absolute top-2 right-2 flex gap-2" onClick={e => e.stopPropagation()}>
                {heatmapOverlay && (
                    <button 
                      onClick={() => setShowHeatmap(!showHeatmap)}
                      className="bg-black/80 hover:bg-black text-white text-xs px-2 py-1 rounded border border-white/20"
                    >
                      {showHeatmap ? 'Show Original' : 'Show Heatmap'}
                    </button>
                )}
                <button 
                  onClick={handleRemove}
                  className="bg-red-600/80 hover:bg-red-600 text-white text-xs px-2 py-1 rounded border border-white/20"
                >
                  ✕
                </button>
             </div>
          )}
        </div>

        <button 
          onClick={runAudit}
          disabled={!image || isAuditing}
          className="w-full btn-premium btn-glow mt-6"
        >
          {isAuditing ? 'Analyzing Multimodal Stream...' : 'Run Spatial Audit'}
        </button>
      </div>

      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Extraction Pipeline</h3>
        <div className="space-y-4">
          {checks.map(check => (
            <div key={check.id} className={`flex items-center gap-3 p-3 rounded-lg border border-border-muted transition-opacity ${check.status === 'pending' ? 'opacity-40' : 'opacity-100'}`}>
              <span className="text-lg">{check.status === 'done' ? '✅' : '⭕'}</span>
              <span className="text-xs font-semibold">{check.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default VisionAudit;
