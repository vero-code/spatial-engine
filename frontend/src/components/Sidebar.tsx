import React from 'react';

interface SidebarProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, setActiveSection }) => {
  const navItems = [
    { id: 'dashboard', icon: '📊', label: 'Dashboard' },
    { id: 'physics', icon: '⚛️', label: 'Physics Core' },
    { id: 'economics', icon: '💰', label: 'Economic Engine' },
    { id: 'market', icon: '🛒', label: 'Market Hub' },
    { id: 'vision', icon: '👁️', label: 'Vision Audit' },
    { id: 'standards', icon: '📘', label: 'Standards KB' },
    { id: 'config', icon: '⚙️', label: 'Config Gen' },
  ];

  return (
    <nav className="w-64 bg-[#0d1117]/95 border-r border-border-muted flex flex-col fixed h-screen z-50">
      <div className="p-8 flex items-center gap-3">
        <span className="text-2xl">💡</span>
        <span className="font-bold text-xl tracking-tight text-white">
          Spatial<span className="text-accent-primary">Engine</span>
        </span>
      </div>

      <ul className="flex-grow space-y-1">
        {navItems.map((item) => (
          <li
            key={item.id}
            onClick={() => setActiveSection(item.id)}
            className={`px-6 py-3 flex items-center gap-4 cursor-pointer transition-all border-l-4 ${
              activeSection === item.id
                ? 'bg-accent-primary/10 text-accent-primary border-accent-primary'
                : 'text-gray-400 border-transparent hover:bg-white/5 hover:text-white'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </li>
        ))}
      </ul>

      <div className="p-6 border-t border-border-muted">
        <div className="flex items-center gap-2 text-xs font-semibold mb-2">
          <span className="w-2 h-2 bg-accent-secondary rounded-full shadow-[0_0_8px_var(--color-accent-secondary)]"></span>
          <span className="text-accent-secondary uppercase tracking-widest">Core Active</span>
        </div>
        <p className="text-[10px] text-gray-500 font-mono">v1.0.4 - Gemini 3 Pro</p>
      </div>
    </nav>
  );
};

export default Sidebar;
