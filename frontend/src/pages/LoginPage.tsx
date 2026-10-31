import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Lock, Mail, ArrowRight, UserCheck } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('investigator@claimsight.ai');
  const [password, setPassword] = useState('Investigator2026!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (e: string, p: string) => {
    setEmail(e);
    setPassword(p);
    setLoading(true);
    setError(null);
    try {
      await login(e, p);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-blue-600 mx-auto flex items-center justify-center shadow-lg shadow-blue-500/20">
            <ShieldAlert className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-wider">CLAIMSIGHT AI</h1>
          <p className="text-xs text-slate-400">Multimodal Autonomous Insurance Claims Investigator</p>
        </div>

        {/* Login Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div className="border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200">SIU Portal Authentication</h2>
            <p className="text-xs text-slate-400 mt-0.5">Enter authorized investigator credentials.</p>
          </div>

          {error && (
            <div className="p-3 rounded-lg bg-red-950/60 border border-red-800/80 text-red-300 text-xs">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-300 font-semibold mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-xs transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <span>{loading ? 'Authenticating...' : 'Sign In to Investigation Workspace'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick-Test Buttons for Judges */}
          <div className="border-t border-slate-800 pt-4 space-y-2">
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider text-center">
              Quick Test Personas
            </div>
            <div className="grid grid-cols-1 gap-2">
              <button
                type="button"
                onClick={() => handleQuickLogin('investigator@claimsight.ai', 'Investigator2026!')}
                className="w-full py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-slate-200 text-xs font-medium text-left flex items-center justify-between border border-slate-700/60"
              >
                <div>
                  <div className="font-bold text-blue-400">Senior Investigator (Sarah Chen)</div>
                  <div className="text-[10px] text-slate-400">Full SIU workspace, graph, & decisions</div>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('admin@claimsight.ai', 'ClaimsightAdmin2026!')}
                className="w-full py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-slate-200 text-xs font-medium text-left flex items-center justify-between border border-slate-700/60"
              >
                <div>
                  <div className="font-bold text-purple-400">Administrator (Chief Compliance Officer)</div>
                  <div className="text-[10px] text-slate-400">Executive metrics, model registry & deletes</div>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('claimant@claimsight.ai', 'Claimant2026!')}
                className="w-full py-2 px-3 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-slate-200 text-xs font-medium text-left flex items-center justify-between border border-slate-700/60"
              >
                <div>
                  <div className="font-bold text-emerald-400">Policyholder (Rajesh Kumar)</div>
                  <div className="text-[10px] text-slate-400">Evidence submission & notifications</div>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

