import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { ShieldAlert, LogOut, ShieldCheck, User } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRoleBadge = (role?: string) => {
    switch (role) {
      case 'admin':
        return {
          label: 'Executive / Chief Compliance Officer',
          bg: 'bg-purple-950/80 border-purple-500/40 text-purple-300',
          dot: 'bg-purple-400',
        };
      case 'investigator':
        return {
          label: 'Senior SIU Investigator',
          bg: 'bg-blue-950/80 border-blue-500/40 text-blue-300',
          dot: 'bg-blue-400',
        };
      default:
        return {
          label: 'Verified Policyholder (Claimant)',
          bg: 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300',
          dot: 'bg-emerald-400',
        };
    }
  };

  const badge = getRoleBadge(user?.role);

  return (
    <header className="bg-slate-950 text-white border-b border-slate-800 px-6 py-3 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center space-x-4">
        <Link to="/" className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <ShieldAlert className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-wider bg-gradient-to-r from-blue-400 via-indigo-200 to-white bg-clip-text text-transparent">
                CLAIMSIGHT AI
              </span>
              <span className="text-[10px] font-semibold uppercase tracking-widest bg-blue-900/60 border border-blue-500/30 text-blue-300 px-1.5 py-0.5 rounded">
                SIU Core v3.1
              </span>
            </div>
            <p className="text-[11px] text-slate-400 leading-none">Multimodal Autonomous Insurance Claims Investigator</p>
          </div>
        </Link>
      </div>

      <div className="flex items-center space-x-5">
        {/* Active Guardrail Indicator */}
        <div className="hidden lg:flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-slate-900 border border-amber-500/30 text-amber-300 text-xs font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400 shrink-0" />
          <span>IRDAI Guardrail: ₹5,00,000+ Requires Top Insurance Guy Sign-Off</span>
        </div>

        {/* User Session Profile (No free switching once authenticated) */}
        {user && (
          <div className="flex items-center space-x-4">
            <div className="text-right hidden sm:block">
              <div className="text-sm font-semibold text-slate-200">{user.name}</div>
              <div className="mt-0.5 flex items-center justify-end">
                <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold border ${badge.bg}`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                  {badge.label}
                </span>
              </div>
            </div>

            <button
              onClick={handleLogout}
              className="px-3 py-1.5 bg-slate-900 hover:bg-red-950/60 text-slate-300 hover:text-red-300 border border-slate-800 hover:border-red-800/80 rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
              title="Sign out of active session"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Sign Out</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
