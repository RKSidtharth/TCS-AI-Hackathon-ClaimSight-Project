import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderOpen,
  FilePlus2,
  FileSearch,
  Sparkles,
  BarChart3,
  Sliders,
  ShieldCheck,
  Camera,
  Scale
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const isClaimant = user?.role === 'claimant';

  const isAdmin = user?.role === 'admin';

  const navItems = isClaimant
    ? [
        { to: '/claims', label: 'My Registered Claims', icon: FolderOpen },
        { to: '/claims/new', label: 'Register New Claim', icon: FilePlus2 },
        { to: '/evidence', label: 'Upload Claim Evidence', icon: Camera },
      ]
    : [
        { to: '/', label: 'Overview Dashboard', icon: LayoutDashboard, exact: true },
        { to: '/claims', label: 'Claims Directory', icon: FolderOpen },
        { to: '/evidence', label: 'Evidence Centre', icon: Camera },
        { to: '/investigation', label: 'Investigation Workspace', icon: Sparkles, badge: 'AI Engine' },
        { to: '/reports', label: 'Reports & Dossiers', icon: FileSearch },
        { to: '/analytics', label: 'Analytics & Audit', icon: BarChart3 },
        { to: '/settings', label: 'Policy & Model Registry', icon: Sliders },
      ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 min-h-[calc(100vh-57px)]">
      <div className="py-5 px-3">
        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-3">
          Investigation Modules
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.exact}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-400 border border-blue-500/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <div className="flex items-center space-x-3">
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Core Principle Footer */}
      <div className="p-4 m-3 rounded-lg bg-slate-950/70 border border-slate-800 text-[11px] text-slate-400">
        <div className="flex items-center space-x-1.5 text-blue-400 font-semibold mb-1">
          <Scale className="w-3.5 h-3.5" />
          <span>Core SIU Principle</span>
        </div>
        <p className="leading-relaxed text-slate-400">
          Decision-support intelligence. Contradictions indicate areas requiring verification, never an automated verdict of fraud.
        </p>
      </div>
    </aside>
  );
};

