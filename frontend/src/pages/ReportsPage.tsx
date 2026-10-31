import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import {
  FileText,
  Download,
  ShieldAlert,
  ShieldCheck,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  AlertTriangle,
  FolderOpen
} from 'lucide-react';

interface ReportSummary {
  claim_id: string;
  title: string;
  vehicle_reg: string;
  accident_type: string;
  estimated_damage: number;
  status: string;
  is_investigated: boolean;
  is_high_impact: boolean;
  requires_executive_verification: boolean;
  investigation_status: 'COMPLETED' | 'IN_PROGRESS' | 'UNINVESTIGATED_PENDING';
  decision: string;
  report_id: string;
  generated_at: string;
  download_url: string;
}

export const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [stats, setStats] = useState({
    total_claims: 0,
    total_investigated: 0,
    total_uninvestigated: 0,
    total_high_impact_over_5l: 0,
  });
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'investigated' | 'uninvestigated' | 'high_impact'>('all');

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const res = await api.getAllReports();
      setReports(res.data.reports || []);
      setStats({
        total_claims: res.data.total_claims || 0,
        total_investigated: res.data.total_investigated || 0,
        total_uninvestigated: res.data.total_uninvestigated || 0,
        total_high_impact_over_5l: res.data.total_high_impact_over_5l || 0,
      });
    } catch (err) {
      console.error('Failed to load reports repository', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredReports = reports.filter((r) => {
    const matchesSearch =
      r.claim_id.toLowerCase().includes(search.toLowerCase()) ||
      r.vehicle_reg.toLowerCase().includes(search.toLowerCase()) ||
      (r.title && r.title.toLowerCase().includes(search.toLowerCase())) ||
      (r.accident_type && r.accident_type.toLowerCase().includes(search.toLowerCase()));

    if (!matchesSearch) return false;

    if (filterType === 'investigated') return r.is_investigated;
    if (filterType === 'uninvestigated') return !r.is_investigated;
    if (filterType === 'high_impact') return r.is_high_impact;
    return true;
  });

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <FileText className="w-6 h-6 text-blue-600" />
            Synthetic Investigation Reports & Dossier Registry
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Complete enterprise archive of all insurance claims: investigated, in-progress, repudiated, and fresh intake.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Link
            to="/investigation"
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-semibold transition flex items-center gap-2 shadow-xs"
          >
            <ShieldAlert className="w-4 h-4 text-blue-400" />
            <span>Open SIU Workspace</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Claims / Dossiers</div>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">{stats.total_claims}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Comprehensive DB population</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
            <FolderOpen className="w-5 h-5" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Investigated & Cleared</div>
            <div className="text-2xl font-extrabold text-emerald-600 mt-1">{stats.total_investigated}</div>
            <div className="text-[11px] text-emerald-700 mt-0.5">SIU completed / in-flight</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <CheckCircle2 className="w-5 h-5" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Uninvestigated / Intake</div>
            <div className="text-2xl font-extrabold text-slate-700 mt-1">{stats.total_uninvestigated}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Awaiting initial SIU run</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center">
            <Clock className="w-5 h-5" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-amber-200 bg-amber-50/20 shadow-xs flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-amber-800 uppercase tracking-wider">High-Impact (&gt; ₹5L)</div>
            <div className="text-2xl font-extrabold text-amber-900 mt-1">{stats.total_high_impact_over_5l}</div>
            <div className="text-[11px] text-amber-700 font-medium mt-0.5">Mandatory CCO Sign-off</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Filter Tabs & Search */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-1.5 p-1 bg-slate-100 rounded-lg text-xs font-semibold w-full md:w-auto overflow-x-auto">
          <button
            onClick={() => setFilterType('all')}
            className={`px-3 py-1.5 rounded-md transition ${
              filterType === 'all' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All Reports ({stats.total_claims})
          </button>
          <button
            onClick={() => setFilterType('investigated')}
            className={`px-3 py-1.5 rounded-md transition ${
              filterType === 'investigated' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Investigated ({stats.total_investigated})
          </button>
          <button
            onClick={() => setFilterType('uninvestigated')}
            className={`px-3 py-1.5 rounded-md transition ${
              filterType === 'uninvestigated' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Uninvestigated ({stats.total_uninvestigated})
          </button>
          <button
            onClick={() => setFilterType('high_impact')}
            className={`px-3 py-1.5 rounded-md transition ${
              filterType === 'high_impact' ? 'bg-amber-100 text-amber-900 font-bold shadow-xs' : 'text-amber-800 hover:text-amber-950'
            }`}
          >
            &gt; ₹5L Guardrail ({stats.total_high_impact_over_5l})
          </button>
        </div>

        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search claim, registration, or type..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
          />
        </div>
      </div>

      {/* Reports Listing Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-500 text-xs">Loading complete dossier repository...</div>
        ) : filteredReports.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs">No dossiers match the selected criteria.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                  <th className="py-3 px-4">Claim ID & Report Ref</th>
                  <th className="py-3 px-4">Vehicle & Incident Type</th>
                  <th className="py-3 px-4 text-right">Exposure / Claimed</th>
                  <th className="py-3 px-4 text-center">Investigation State</th>
                  <th className="py-3 px-4 text-center">₹5L Guardrail Status</th>
                  <th className="py-3 px-4 text-center">Ruling / Decision</th>
                  <th className="py-3 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredReports.map((report) => (
                  <tr key={report.claim_id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 font-mono">
                      <Link
                        to={`/investigation/${report.claim_id}`}
                        className="font-bold text-blue-600 hover:text-blue-800 hover:underline block"
                      >
                        {report.claim_id}
                      </Link>
                      <span className="text-[10px] text-slate-400">{report.report_id}</span>
                    </td>

                    <td className="py-3 px-4">
                      <div className="font-semibold text-slate-800">{report.vehicle_reg}</div>
                      <div className="text-slate-500 text-[11px] truncate max-w-xs">{report.title || report.accident_type}</div>
                    </td>

                    <td className="py-3 px-4 text-right font-mono font-bold text-slate-900">
                      ₹{report.estimated_damage?.toLocaleString() ?? 0}
                    </td>

                    <td className="py-3 px-4 text-center">
                      {report.investigation_status === 'COMPLETED' ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                          Investigated
                        </span>
                      ) : report.investigation_status === 'IN_PROGRESS' ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-blue-100 text-blue-800 border border-blue-200">
                          <Clock className="w-3 h-3 text-blue-600" />
                          In Progress
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
                          Uninvestigated (Fresh)
                        </span>
                      )}
                    </td>

                    <td className="py-3 px-4 text-center">
                      {report.is_high_impact ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                          <ShieldCheck className="w-3 h-3 text-amber-600" />
                          &gt; ₹5L CCO Required
                        </span>
                      ) : (
                        <span className="inline-block px-2.5 py-0.5 rounded-full text-[11px] text-slate-500 bg-slate-50 border border-slate-200">
                          Standard Clearable
                        </span>
                      )}
                    </td>

                    <td className="py-3 px-4 text-center uppercase font-bold text-[10px]">
                      <span
                        className={`px-2 py-0.5 rounded ${
                          report.decision === 'approved'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : report.decision === 'rejected'
                            ? 'bg-red-50 text-red-700 border border-red-200'
                            : report.decision === 'escalated'
                            ? 'bg-purple-50 text-purple-700 border border-purple-200'
                            : 'bg-slate-50 text-slate-500 border border-slate-200'
                        }`}
                      >
                        {report.decision || 'Pending'}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-center">
                      <div className="flex items-center justify-center space-x-2">
                        <Link
                          to={`/investigation/${report.claim_id}`}
                          className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-white rounded text-xs font-medium transition flex items-center gap-1 shadow-xs"
                        >
                          <ShieldAlert className="w-3 h-3 text-blue-400" />
                          <span>Investigate</span>
                        </Link>
                        <a
                          href={report.download_url}
                          download
                          title="Download SIU Investigation PDF"
                          className="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-slate-100 rounded transition border border-slate-200"
                        >
                          <Download className="w-3.5 h-3.5" />
                        </a>
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

