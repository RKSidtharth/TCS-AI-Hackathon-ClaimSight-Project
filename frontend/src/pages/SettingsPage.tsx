import React from 'react';
import { Sliders, Cpu, Database, HardDrive, Globe, Shield, CheckCircle2 } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <Sliders className="w-6 h-6 text-blue-600" />
          System Configuration & AI Model Registry
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Active neural model versions, connected databases, external providers, and RBAC governance.
        </p>
      </div>

      {/* Model Registry Cards */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-blue-600" />
          Active AI/ML Model Registry
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900">YOLOv8-DamageDetect</span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                ACTIVE v2.4.1
              </span>
            </div>
            <p className="text-slate-600">
              Vehicle component segmentation and surface damage classification (dents, scratches, creases).
            </p>
            <div className="text-[11px] text-slate-400 font-mono">Confidence Threshold: 0.65</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900">PaddleOCR-DocumentIntel</span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                ACTIVE v3.1.0
              </span>
            </div>
            <p className="text-slate-600">
              Multi-page PDF policy, police GD entry, and repair estimate line item fact extractor.
            </p>
            <div className="text-[11px] text-slate-400 font-mono">Confidence Threshold: 0.80</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900">CrossModal-Consistency</span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                ACTIVE v4.0.2
              </span>
            </div>
            <p className="text-slate-600">
              Witness divergence analyzer, temporal/spatial EXIF validator, and contradiction engine.
            </p>
            <div className="text-[11px] text-slate-400 font-mono">Confidence Threshold: 0.75</div>
          </div>
        </div>
      </div>

      {/* Infrastructure & External Providers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-600" />
            Database & Object Storage
          </h2>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div className="font-bold text-slate-800">MongoDB Community Cluster</div>
                <div className="text-slate-500 font-mono text-[11px]">mongodb://localhost:27017/claimsight_ai</div>
              </div>
              <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600">
                <CheckCircle2 className="w-3.5 h-3.5" /> 22 Collections Live
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div className="font-bold text-slate-800">Forensic Object Storage Engine</div>
                <div className="text-slate-500 font-mono text-[11px]">Local Driver (backend/storage/uploads)</div>
              </div>
              <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600">
                <CheckCircle2 className="w-3.5 h-3.5" /> SHA-256 Indexed
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-600" />
            External Telemetry & Service Integrations
          </h2>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div className="font-bold text-slate-800">Historical Meteorological Reanalysis</div>
                <div className="text-slate-500 text-[11px]">IMD / OpenWeather verified historical precipitation</div>
              </div>
              <span className="text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                Configured
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <div>
                <div className="font-bold text-slate-800">Automotive EDR / Airbag Telematics Adapter</div>
                <div className="text-slate-500 text-[11px]">Bosch Crash Data Retrieval (CDR) interface</div>
              </div>
              <span className="text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                Ready
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Role-Based Access Control (RBAC) Policy */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Shield className="w-5 h-5 text-emerald-600" />
          Role-Based Access Governance (IRDAI & SIU Standards)
        </h2>

        <div className="border border-slate-200 rounded-lg overflow-hidden text-xs">
          <table className="w-full text-left">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 font-semibold">
              <tr>
                <th className="p-3">User Role</th>
                <th className="p-3">Claim Ingestion</th>
                <th className="p-3">Forensic Inconsistencies</th>
                <th className="p-3">Next-Best-Evidence</th>
                <th className="p-3">Settlement Sign-off</th>
                <th className="p-3">Audit Log Access</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="hover:bg-slate-50">
                <td className="p-3 font-bold text-purple-700">Administrator</td>
                <td className="p-3 text-emerald-600">Full Access</td>
                <td className="p-3 text-emerald-600">Full Access</td>
                <td className="p-3 text-emerald-600">Full Access</td>
                <td className="p-3 text-emerald-600">Executive Approval</td>
                <td className="p-3 text-emerald-600 font-bold">Unrestricted</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="p-3 font-bold text-blue-700">Senior Investigator</td>
                <td className="p-3 text-emerald-600">Assigned Dossiers</td>
                <td className="p-3 text-emerald-600">Full Access</td>
                <td className="p-3 text-emerald-600">Dispatch Requests</td>
                <td className="p-3 text-emerald-600">Recommendation Sign-off</td>
                <td className="p-3 text-slate-600">Read-Only Trail</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="p-3 font-bold text-slate-700">Policyholder (Claimant)</td>
                <td className="p-3 text-blue-600">Own Claim Only</td>
                <td className="p-3 text-slate-400">Restricted (SIU confidential)</td>
                <td className="p-3 text-blue-600">Respond to Requests</td>
                <td className="p-3 text-slate-400">View Approved Settlement</td>
                <td className="p-3 text-slate-400">No Access</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

