import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  ShieldAlert,
  Clock,
  FileCheck2,
  AlertTriangle,
  FolderOpen,
  ArrowRight,
  TrendingUp,
  Activity,
  CheckCircle2,
  FileText
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await api.getDashboardAnalytics();
      setMetrics(res.data);
    } catch (err) {
      console.error('Failed to load dashboard metrics', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-slate-500 font-medium">Aggregating live SIU investigation metrics...</p>
        </div>
      </div>
    );
  }

  const kpis = metrics?.kpis || {};
  const urgent = metrics?.urgent_claims || [];
  const recent = metrics?.recent_activity || [];
  const scenarios = metrics?.scenario_distribution || [];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Top Welcome & Summary */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Overview Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time status of motor claims, forensic contradictions, and Next-Best-Evidence actions.
          </p>
        </div>
        <div className="flex items-center gap-3">
          {user?.role === 'claimant' && (
            <Link
              to="/claims/new"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold shadow-sm transition flex items-center gap-2"
            >
              <span>+ Register New Claim</span>
            </Link>
          )}
          <Link
            to="/investigation"
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-semibold shadow-sm transition flex items-center gap-2"
          >
            <ShieldAlert className="w-4 h-4 text-blue-400" />
            <span>Open SIU Workspace</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Total Registered</span>
            <FolderOpen className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-3xl font-extrabold text-slate-900 mt-3">{kpis.total_claims ?? 10}</div>
          <div className="text-xs text-slate-500 mt-2 flex items-center gap-1">
            <span className="text-emerald-600 font-medium">+100% active DB</span> motor dossiers
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Active Investigation</span>
            <Activity className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-3xl font-extrabold text-indigo-600 mt-3">{kpis.under_investigation ?? 6}</div>
          <div className="text-xs text-slate-500 mt-2">Multimodal AI synthesis live</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Awaiting Evidence</span>
            <Clock className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-3xl font-extrabold text-amber-600 mt-3">{kpis.awaiting_evidence ?? 2}</div>
          <div className="text-xs text-slate-500 mt-2">Next-Best-Evidence dispatched</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Priority Review</span>
            <AlertTriangle className="w-4 h-4 text-red-500" />
          </div>
          <div className="text-3xl font-extrabold text-red-600 mt-3">{kpis.urgent_review_count ?? 3}</div>
          <div className="text-xs text-red-600 font-medium mt-2">Contradictions require investigator review</div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Closed / Approved</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-600 mt-3">{kpis.completed_investigations ?? 2}</div>
          <div className="text-xs text-slate-500 mt-2">Avg duration: {kpis.average_duration_days} days</div>
        </div>
      </div>

      {/* Main Grid: Urgent Attention Claims + Recent Audit Trail */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Urgent Claims Requiring Review (2 Cols) */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
                Claims Requiring Priority Forensic Review
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Claims with highest contradiction density and materiality scores.
              </p>
            </div>
            <Link to="/claims" className="text-xs text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1">
              View All Claims <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {urgent.map((c: any) => (
              <div
                key={c.claim_id}
                className="p-4 rounded-lg border border-slate-200 hover:border-blue-400 bg-slate-50/50 hover:bg-white transition flex items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold bg-slate-200 text-slate-700 px-2 py-0.5 rounded">
                      {c.claim_id}
                    </span>
                    <span className="text-sm font-semibold text-slate-800">{c.title}</span>
                  </div>
                  <div className="text-xs text-slate-500 flex items-center gap-3">
                    <span>Reg: <strong className="text-slate-700">{c.vehicle_reg}</strong></span>
                    <span>Status: <span className="capitalize font-medium text-slate-600">{c.status.replace('_', ' ')}</span></span>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <div className="text-right">
                    <div className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Priority Score</div>
                    <div className="text-base font-extrabold text-red-600">{c.priority_score.toFixed(1)} / 100</div>
                  </div>
                  <Link
                    to={`/investigation/${c.claim_id}`}
                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-xs font-semibold shadow-xs transition"
                  >
                    Investigate
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Forensic Audit Activity Stream (1 Col) */}
        <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-600" />
              Live Investigation Activity
            </h2>
            <span className="text-[11px] text-emerald-600 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Active SIU Node
            </span>
          </div>

          <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
            {recent.map((log: any, idx: number) => (
              <div key={idx} className="text-xs p-3 rounded-lg bg-slate-50 border border-slate-150 space-y-1">
                <div className="flex items-center justify-between text-slate-400 font-mono text-[10px]">
                  <span>{log.claim_id}</span>
                  <span>{new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                <div className="font-semibold text-slate-800 text-[11px]">{log.action.replace(/_/g, ' ')}</div>
                <p className="text-slate-500 text-[11px] leading-tight">{log.details}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Synthetic Scenario Breakdown Showcase */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900">Configured Investigation Scenarios in Dataset</h2>
        <p className="text-xs text-slate-500">
          Synthetic motor claim scenarios covering the full spectrum of multimodal inconsistencies and policy conditions.
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {scenarios.map((sc: any, idx: number) => (
            <div key={idx} className="p-3 rounded-lg bg-slate-50 border border-slate-200/60 text-center">
              <div className="text-lg font-bold text-blue-600">{sc.value}</div>
              <div className="text-xs font-medium text-slate-700 capitalize mt-0.5">{sc.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

