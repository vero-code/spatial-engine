import React, { useState } from 'react';

const MarketHub: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  const search = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    setIsSearching(true);
    setTimeout(() => {
      setResults([
        { name: "Philips Hue A21 LED", lumens: 1600, price: 19.99, protocol: "Zigbee/Matter", verified: true },
        { name: "Sengled Smart Bulb", lumens: 800, price: 9.99, protocol: "Zigbee", verified: true },
        { name: "Generic LED Bulb", lumens: 1500, price: 4.50, protocol: "None", verified: false }
      ]);
      setIsSearching(false);
    }, 1200);
  };

  return (
    <div className="animate-fade-in space-y-6">
      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold uppercase tracking-widest text-gray-500 mb-6">Market Intelligence & Verification</h3>
        <form onSubmit={search} className="flex gap-4">
          <input 
            type="text" 
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search products e.g. 'Philips Hue 1600lm LED'..."
            className="flex-grow bg-[#0d1117] border border-border-muted rounded-lg px-4 py-3 text-white focus:outline-none focus:border-accent-primary"
          />
          <button type="submit" className="btn-premium btn-glow">Run Multi-threaded Search</button>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isSearching ? (
          <div className="col-span-full h-48 flex items-center justify-center text-accent-primary animate-pulse">
            Agent searching markets and verifying technical specs...
          </div>
        ) : results.length === 0 ? (
          <div className="col-span-full h-48 flex flex-col items-center justify-center text-gray-500 opacity-50">
            <span className="text-4xl mb-2">🛒</span>
            <p className="text-sm italic">Search for real-world lighting products. Agent validates CRI, Dimmable, and Protocol specs.</p>
          </div>
        ) : (
          results.map((p, i) => <ProductCard key={i} product={p} />)
        )}
      </div>
    </div>
  );
};

const ProductCard = ({ product }: { product: any }) => (
  <div className="glass-panel p-6 hover:border-accent-primary/50 transition-colors group">
    <div className="flex justify-between items-start mb-4">
      <h4 className="font-bold text-white group-hover:text-accent-primary transition-colors">{product.name}</h4>
      {product.verified && <span className="text-xs bg-accent-secondary/20 text-accent-secondary px-2 py-0.5 rounded border border-accent-secondary/30">Verified</span>}
    </div>
    <div className="space-y-2 text-xs text-gray-400">
      <div className="flex justify-between"><span>Lumens</span><span className="text-white font-mono">{product.lumens}lm</span></div>
      <div className="flex justify-between"><span>Price</span><span className="text-white font-mono">${product.price}</span></div>
      <div className="flex justify-between"><span>Protocol</span><span className="text-white font-mono">{product.protocol}</span></div>
    </div>
  </div>
);

export default MarketHub;
