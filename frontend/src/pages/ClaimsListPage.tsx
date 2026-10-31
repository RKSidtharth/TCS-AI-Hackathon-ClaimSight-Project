import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Link } from 'react-router-dom';
import type { Claim } from '../types';
import { useAuth } from '../context/AuthContext';
import { Search, Filter, ShieldAlert, Download, ShieldCheck, Camera } from 'lucide-react';

export const ClaimsListPage: React.FC = () => {
  const { user } = useAuth();
  const isClaimant = user?.role === 'claimant';
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [highImpactOnly, setHighImpactOnly] = useState(false);

  useEffect(() => {
    fetchClaims();
  }, [search, statusFilter, priorityFilter]);

  const fetchClaims = async () => {
    try {
      setLoading(true);
      const res = await api.getClaims({
        search: search || undefined,
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
      });
      setClaims(res.data.claims || []);
    } catch (err) {
      console.error('Error fetching claims', err);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityBadge = (priority: string, score: number) => {
    if (score >= 80) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800 border border-red-200">
          <span className="w-1.5 h-1.5 rounded-full bg-red-600"></span>
          Urgent ({score.toFixed(0)})
        </span>
      );
    } else if (score >= 60) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
          Medium ({score.toFixed(0)})
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        Low ({score.toFixed(0)})
      </span>
    );
  };

  const getStatusBadge = (status: string) => {
    const map: Record<string, { label: string; bg: string; text: string }> = {
      investigation_active: { label: 'Active Investigation', bg: 'bg-blue-50 border-blue-200', text: 'text-blue-700' },
      awaiting_evidence: { label: 'Awaiting Evidence', bg: 'bg-amber-50 border-amber-200', text: 'text-amber-700' },
      investigation_completed: { label: 'Settlement Cleared', bg: 'bg-emerald-50 border-emerald-200', text: 'text-emerald-700' },
      escalated_to_siu: { label: 'Escalated to SIU', bg: 'bg-purple-50 border-purple-200', text: 'text-purple-700' },
      intake_pending: { label: 'Intake In Progress', bg: 'bg-slate-50 border-slate-200', text: 'text-slate-700' },
    };
    const s = map[status] || { label: status.replace('_', ' '), bg: 'bg-slate-50 border-slate-200', text: 'text-slate-700' };
    return (
      <span className={`inline-block px-2.5 py-1 rounded-md text-xs font-medium border ${s.bg} ${s.text}`}>
        {s.label}
      </span>
    );
  };

  const handleDownloadReport = async (cid: string) => {
    try {
      await api.downloadSiuPdf(cid);
    } catch (err) {
      alert('Failed to download report: Backend server is not running on http://localhost:8000.');
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Motor Claims Directory</h1>
          <p className="text-sm text-slate-500 mt-1">
            Access active dossiers, forensic contradiction indicators, and Next-Best-Evidence action loops.
          </p>
        </div>
        {user?.role === 'claimant' && (
          <Link
            to="/claims/new"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold shadow-xs transition flex items-center gap-2 self-start sm:self-auto"
          >
            <span>+ Register New Claim</span>
          </Link>
        )}
      </div>

      {/* Filters & Search Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="relative w-full md:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search by Claim ID, Vehicle Reg, or Claimant Name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
          />
        </div>

        <div className="flex items-center space-x-3 w-full md:w-auto">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:outline-none focus:border-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="investigation_active">Active Investigation</option>
              <option value="awaiting_evidence">Awaiting Evidence</option>
              <option value="investigation_completed">Settlement Cleared</option>
              <option value="intake_pending">Intake In Progress</option>
            </select>
          </div>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:outline-none focus:border-blue-500"
          >
            <option value="">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <button
            onClick={() => setHighImpactOnly(!highImpactOnly)}
            className={`px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition border ${
              highImpactOnly
                ? 'bg-amber-100 border-amber-300 text-amber-900 shadow-xs'
                : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
            <span>&gt; ₹5L Guardrail Only</span>
          </button>
        </div>
      </div>

      {/* Claims Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-500 text-sm">Loading motor claims dossiers...</div>
        ) : claims.filter((c) => !highImpactOnly || (c.estimated_damage || 0) >= 500000).length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">No claims found matching the criteria.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                  <th className="py-3.5 px-4">Claim ID</th>
                  <th className="py-3.5 px-4">Vehicle & Claimant</th>
                  <th className="py-3.5 px-4">Incident Details</th>
                  <th className="py-3.5 px-4 text-right">Estimate & Guardrail</th>
                  <th className="py-3.5 px-4 text-center">Status</th>
                  <th className="py-3.5 px-4 text-center">Priority</th>
                  <th className="py-3.5 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {claims
                  .filter((c) => !highImpactOnly || (c.estimated_damage || 0) >= 500000)
                  .map((claim) => (
                    <tr key={claim.claim_id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-slate-900">
                        {isClaimant ? (
                          <span>{claim.claim_id}</span>
                        ) : (
                          <Link
                            to={`/investigation/${claim.claim_id}`}
                            className="text-blue-600 hover:text-blue-800 hover:underline"
                          >
                            {claim.claim_id}
                          </Link>
                        )}
                      </td>

                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2.5">
                          {(claim.vehicle_image_url || claim.image_url) && (
                            <img
                              src={claim.vehicle_image_url || claim.image_url}
                              alt="Damage thumbnail"
                              className="w-10 h-10 rounded-lg object-cover border border-slate-200 shadow-2xs shrink-0"
                            />
                          )}
                          <div>
                            <div className="font-semibold text-slate-800">{claim.vehicle_reg}</div>
                            <div className="text-slate-500">{claim.claimant?.name}</div>
                          </div>
                        </div>
                      </td>

                      <td className="py-3.5 px-4 max-w-xs truncate">
                        <div className="font-medium text-slate-800">{claim.accident_type}</div>
                        <div className="text-slate-400 truncate">{claim.incident_location}</div>
                      </td>

                      <td className="py-3.5 px-4 text-right font-mono">
                        <div className="font-bold text-slate-900">
                          ₹{claim.estimated_damage?.toLocaleString() ?? 0}
                        </div>
                        {(claim.estimated_damage || 0) >= 500000 && (
                          <div className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-300 mt-1">
                            <ShieldCheck className="w-3 h-3 text-amber-600" />
                            &gt; ₹5L CCO Sign-off
                          </div>
                        )}
                      </td>

                      <td className="py-3.5 px-4 text-center">{getStatusBadge(claim.status)}</td>

                      <td className="py-3.5 px-4 text-center">
                        {getPriorityBadge(claim.priority, claim.priority_score)}
                      </td>

                      <td className="py-3.5 px-4 text-center">
                        <div className="flex items-center justify-center space-x-2">
                          {isClaimant ? (
                            <Link
                              to="/evidence"
                              className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-medium transition flex items-center gap-1 shadow-xs"
                            >
                              <Camera className="w-3.5 h-3.5" />
                              <span>Evidence</span>
                            </Link>
                          ) : (
                            <Link
                              to={`/investigation/${claim.claim_id}`}
                              className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-white rounded text-xs font-medium transition flex items-center gap-1 shadow-xs"
                            >
                              <ShieldAlert className="w-3.5 h-3.5 text-blue-400" />
                              <span>Investigate</span>
                            </Link>
                          )}
                          <button
                            onClick={() => handleDownloadReport(claim.claim_id)}
                            title="Download SIU PDF Report"
                            className="p-1 text-slate-500 hover:text-blue-600 hover:bg-slate-100 rounded transition cursor-pointer"
                          >
                            <Download className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
