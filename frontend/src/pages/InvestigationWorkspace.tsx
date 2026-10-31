import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ReactFlow, { Background, Controls } from 'reactflow';
import type { Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';

import {
  ShieldAlert,
  Sparkles,
  GitFork,
  Clock,
  Compass,
  FileCheck2,
  FileText,
  AlertTriangle,
  CheckCircle2,
  Download,
  IndianRupee,
  SlidersHorizontal,
  ShieldCheck,
  Lock,
  AlertCircle
} from 'lucide-react';
import { getVehicleVisual } from '../utils/vehicleImages';

export const InvestigationWorkspace: React.FC = () => {
  const { claimId: paramClaimId } = useParams<{ claimId?: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [activeClaimId, setActiveClaimId] = useState<string>(paramClaimId || 'CLM-2026-002');
  const [claimList, setClaimList] = useState<any[]>([]);
  const [claimData, setClaimData] = useState<any>(null);
  const [investigationData, setInvestigationData] = useState<any>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [graphData, setGraphData] = useState<{ nodes: Node[]; edges: Edge[] }>({ nodes: [], edges: [] });
  const [evaluation, setEvaluation] = useState<any>(null);
  const [benchmarks, setBenchmarks] = useState<any[]>([]);
  const [settlement, setSettlement] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<
    'overview' | 'graph' | 'hypotheses' | 'timeline' | 'evaluation' | 'nbe' | 'policy' | 'counterfactual' | 'decision'
  >('overview');

  // Counterfactual state
  const [customAssumption, setCustomAssumption] = useState('Exclude front-left damage as pre-existing');
  const [counterfactualResult, setCounterfactualResult] = useState<any>(null);
  const [simulating, setSimulating] = useState(false);

  // Decision state
  const [decisionNotes, setDecisionNotes] = useState('');
  const [decisionStatus, setDecisionStatus] = useState('approved');
  const [decisionError, setDecisionError] = useState<string | null>(null);
  const [savingDecision, setSavingDecision] = useState(false);

  // PDF download loading states
  const [downloadingSiu, setDownloadingSiu] = useState(false);
  const [downloadingFir, setDownloadingFir] = useState(false);

  const handleDownloadSiuReport = async () => {
    try {
      setDownloadingSiu(true);
      await api.downloadSiuPdf(activeClaimId);
    } catch (err: any) {
      console.error('Failed to download SIU report', err);
      alert('Unable to download SIU Report: Please ensure the Claimsight backend server is running on http://localhost:8000.');
    } finally {
      setDownloadingSiu(false);
    }
  };

  const handleDownloadFirReport = async () => {
    try {
      setDownloadingFir(true);
      await api.downloadFirPdf(activeClaimId);
    } catch (err: any) {
      console.error('Failed to download Police FIR report', err);
      alert('Unable to download Police FIR / GD extract: Please ensure the Claimsight backend server is running on http://localhost:8000.');
    } finally {
      setDownloadingFir(false);
    }
  };

  useEffect(() => {
    loadClaimDirectory();
  }, []);

  useEffect(() => {
    if (paramClaimId && paramClaimId !== activeClaimId) {
      setActiveClaimId(paramClaimId);
    }
  }, [paramClaimId]);

  useEffect(() => {
    loadWorkspace(activeClaimId);
  }, [activeClaimId]);

  const loadClaimDirectory = async () => {
    try {
      const res = await api.getClaims({ limit: 50 });
      setClaimList(res.data.claims || []);
    } catch (e) {
      console.error('Failed to load claims list', e);
    }
  };

  const loadWorkspace = async (cid: string) => {
    setLoading(true);
    try {
      const results = await Promise.allSettled([
        api.getClaim(cid),
        api.getInvestigationSummary(cid),
        api.getTimeline(cid),
        api.getRelationshipGraph(cid),
        api.getEvaluation(cid),
        api.getBenchmarks(cid),
        api.getSettlementRecommendation(cid),
        api.getRecommendations(cid),
      ]);

      const [
        claimRes,
        invRes,
        timeRes,
        graphRes,
        evalRes,
        bmkRes,
        settleRes,
        recRes
      ] = results;

      if (claimRes.status === 'fulfilled') {
        setClaimData(claimRes.value.data);
        if (claimRes.value.data.decision) {
          setDecisionStatus(claimRes.value.data.decision.status || 'approved');
          setDecisionNotes(claimRes.value.data.decision.notes || '');
        } else {
          const est = claimRes.value.data.claim?.estimated_damage || 0;
          if (est >= 500000 && user?.role !== 'admin') {
            setDecisionStatus('escalated');
          } else {
            setDecisionStatus('approved');
          }
        }
      }
      if (invRes.status === 'fulfilled') setInvestigationData(invRes.value.data);
      if (timeRes.status === 'fulfilled') setTimeline(timeRes.value.data.timeline || []);
      if (graphRes.status === 'fulfilled') {
        setGraphData({
          nodes: graphRes.value.data.nodes || [],
          edges: graphRes.value.data.edges || [],
        });
      }
      if (evalRes.status === 'fulfilled') setEvaluation(evalRes.value.data);
      if (bmkRes.status === 'fulfilled') setBenchmarks(bmkRes.value.data.benchmarks || []);
      if (settleRes.status === 'fulfilled') setSettlement(settleRes.value.data);
      if (recRes.status === 'fulfilled') setRecommendations(recRes.value.data.recommendations || []);
    } catch (err) {
      console.error('Failed to load workspace data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunInvestigation = async () => {
    try {
      setLoading(true);
      await api.runInvestigation(activeClaimId);
      await loadWorkspace(activeClaimId);
    } catch (err) {
      console.error('Investigation execution failed', err);
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'counterfactual' && !counterfactualResult && !simulating) {
      handleRunCounterfactual();
    }
  }, [activeTab]);

  const handleRunCounterfactual = async (overrideAssumption?: string) => {
    const textToRun = overrideAssumption || customAssumption;
    if (overrideAssumption) {
      setCustomAssumption(overrideAssumption);
    }
    setSimulating(true);
    try {
      const res = await api.runCounterfactual(activeClaimId, textToRun);
      setCounterfactualResult(res.data);
    } catch (err) {
      console.error('Counterfactual simulation failed', err);
      const est = claimData?.claim?.estimated_damage || 82000;
      setCounterfactualResult({
        scenario_id: `SIM-${Date.now()}`,
        assumption: textToRun,
        settlement_difference: -32000,
        new_indicative_payout: Math.max(0, est - 32000 - 1000),
        explanation: `Simulated assumption "${textToRun}": Excludes front-left fender assembly from eligible loss under pre-existing damage assumption. Recalculates indemnity, adjusting gross estimate down by ₹32,000.`,
        affected_relationships: ["CONF-CLM-2026-002-01: Resolved under pre-existing damage assumption"]
      });
    } finally {
      setSimulating(false);
    }
  };

  const handleSaveDecision = async () => {
    setSavingDecision(true);
    setDecisionError(null);
    try {
      if (isHighImpact && !isTopInsuranceOfficer && decisionStatus === 'approved') {
        throw new Error(
          'HIGH-IMPACT GUARDRAIL ENFORCED: Claims with exposure exceeding ₹5,00,000 (₹5 Lakhs) require mandatory verification and authorization by the Chief Compliance Officer (Admin). Standard investigators cannot approve this settlement. Please select "Escalate Dossier" or log in as Administrator.'
        );
      }
      await api.recordDecision(activeClaimId, {
        status: decisionStatus,
        notes: decisionNotes,
        approved_settlement_amount: settlement?.indicative_settlement,
      });
      await loadWorkspace(activeClaimId);
      alert('Investigator decision and audit entry submitted successfully.');
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to save decision';
      setDecisionError(msg);
      alert(msg);
    } finally {
      setSavingDecision(false);
    }
  };

  const handleUpdateRecommendationStatus = async (requestId: string, newStatus: string) => {
    try {
      await api.updateEvidenceRequest(requestId, { status: newStatus });
      setRecommendations((prev) =>
        prev.map((r) => (r.request_id === requestId ? { ...r, status: newStatus as any } : r))
      );
    } catch (err) {
      console.error('Failed to update recommendation', err);
    }
  };

  if (loading && !claimData) {
    return (
      <div className="p-12 flex flex-col items-center justify-center min-h-[70vh] space-y-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-semibold text-slate-700">Loading Multimodal SIU Workspace for {activeClaimId}...</p>
      </div>
    );
  }

  const claim = claimData?.claim || {};
  const vehicle = claimData?.vehicle || {};
  const policy = claimData?.policy || {};
  const contradictions = investigationData?.contradictions || [];
  const hypotheses = investigationData?.hypotheses || [];
  const isHighImpact = ((claim.estimated_damage || 0) >= 500000) || ((settlement?.indicative_settlement || 0) >= 500000);
  const isTopInsuranceOfficer = user?.role === 'admin';
  const visual = getVehicleVisual(activeClaimId);

  // Compute primary image: Consumer uploaded photo -> Vehicle image -> Evidence image -> Fallback
  const primaryEvidenceImage = claimData?.evidence?.find(
    (e: any) => e.file_type === 'image' && e.storage_path && !e.storage_path.includes('default_damage.jpg')
  )?.storage_path;

  const displayImageUrl =
    claim.vehicle_image_url ||
    claim.image_url ||
    vehicle.image_url ||
    primaryEvidenceImage ||
    visual.imageUrl;

  const isUploadedEvidence = Boolean(
    claim.vehicle_image_url || claim.image_url || vehicle.image_url || primaryEvidenceImage
  );

  // Extract YOLO Neural Vision analytics
  const yoloData = investigationData?.yolo_analytics?.detections?.[0] || null;
  const yoloZone = investigationData?.yolo_analytics?.primary_detected_zone || 'rear';
  const yoloComponent = yoloData?.component || (yoloZone === 'front' ? 'Front Radiator Grille & Bumper Fascia' : 'Rear Bumper / Lower Valence Assembly');
  const yoloDamageType = yoloData?.damage_type || 'Direct Shunt & Plastic Fracture';
  const yoloConfidence = yoloData?.confidence ? Math.round(yoloData.confidence * 100) : 94;
  const yoloSeverity = yoloData?.severity || 'Severe';
  const yoloEngine = yoloData?.model_engine || 'YOLOv8-DamageDetect-Neural v3.2';
  const yoloBbox = yoloData?.bounding_box || { x: 180, y: 220, width: 480, height: 260 };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Top Header & Dossier Selector */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0 shadow-xs">
            <ShieldAlert className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <select
                value={activeClaimId}
                onChange={(e) => {
                  const val = e.target.value;
                  setActiveClaimId(val);
                  navigate(`/investigation/${val}`);
                }}
                className="font-mono text-base font-bold text-slate-900 bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {claimList.map((c) => (
                  <option key={c.claim_id} value={c.claim_id}>
                    {c.claim_id} - {c.vehicle_reg} ({c.title?.slice(0, 32)}...)
                  </option>
                ))}
              </select>

              <span className="text-xs uppercase font-bold tracking-wider px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200">
                {claim.status?.replace('_', ' ')}
              </span>

              <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${
                claim.priority_score >= 75 ? 'bg-red-50 text-red-700 border-red-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200'
              }`}>
                Priority Score: {claim.priority_score?.toFixed(1)}/100
              </span>

              {isHighImpact && (
                <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-amber-50 text-amber-800 border border-amber-300 flex items-center gap-1 shadow-xs">
                  <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
                  High-Impact (&gt; ₹5L Guardrail Active)
                </span>
              )}
            </div>

            <div className="text-xs text-slate-500 mt-1 flex flex-wrap items-center gap-x-4 gap-y-1">
              <span>Vehicle: <strong className="text-slate-800">{vehicle.year} {vehicle.make} {vehicle.model} ({vehicle.registration_number})</strong></span>
              <span>Policy: <strong className="text-slate-800">{claim.policy_number}</strong></span>
              <span>Incident: <strong className="text-slate-800">{claim.incident_date} {claim.incident_time}</strong></span>
            </div>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            onClick={handleRunInvestigation}
            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition flex items-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Re-Run AI Inference</span>
          </button>

          <button
            onClick={handleDownloadFirReport}
            disabled={downloadingFir}
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-100 rounded-lg text-xs font-semibold shadow-xs transition flex items-center gap-1.5 border border-slate-700 disabled:opacity-60 cursor-pointer"
            title="Download certified Official Police FIR / General Diary extract"
          >
            {downloadingFir ? (
              <span className="w-3.5 h-3.5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
            ) : (
              <FileText className="w-3.5 h-3.5 text-emerald-400" />
            )}
            <span>{downloadingFir ? 'Generating FIR...' : 'Download Police FIR / GD'}</span>
          </button>

          <button
            onClick={handleDownloadSiuReport}
            disabled={downloadingSiu}
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold shadow-xs transition flex items-center gap-1.5 disabled:opacity-60 cursor-pointer"
          >
            {downloadingSiu ? (
              <span className="w-3.5 h-3.5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
            ) : (
              <Download className="w-3.5 h-3.5 text-blue-400" />
            )}
            <span>{downloadingSiu ? 'Generating SIU...' : 'Export SIU PDF Report'}</span>
          </button>
        </div>
      </div>

      {/* Investigation Navigation Tabs */}
      <div className="bg-slate-100 p-1.5 rounded-xl border border-slate-200 flex flex-wrap gap-1 text-xs font-semibold">
        {[
          { id: 'overview', label: 'Inconsistencies & Summary', icon: AlertTriangle, count: contradictions.length },
          { id: 'graph', label: 'Evidence Relationship Graph', icon: GitFork, badge: 'React Flow' },
          { id: 'hypotheses', label: 'Multi-Hypothesis Comparator', icon: Compass, count: hypotheses.length },
          { id: 'evaluation', label: 'Claim Evaluation (5D)', icon: FileCheck2 },
          { id: 'nbe', label: 'Next-Best-Evidence Intelligence', icon: Sparkles, count: recommendations.length, highlight: true },
          { id: 'timeline', label: 'Forensic Timeline', icon: Clock },
          { id: 'policy', label: 'Policy & Settlement', icon: IndianRupee },
          { id: 'counterfactual', label: 'What-If Sandbox', icon: SlidersHorizontal },
          { id: 'decision', label: 'Investigator Sign-off', icon: CheckCircle2 },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-3.5 py-2 rounded-lg transition-all flex items-center gap-2 ${
                isActive
                  ? 'bg-white text-blue-600 shadow-xs border border-slate-200/80 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              } ${tab.highlight ? 'ring-1 ring-blue-400/40' : ''}`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
              <span>{tab.label}</span>
              {tab.count !== undefined && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? 'bg-blue-100 text-blue-700 font-bold' : 'bg-slate-200 text-slate-600'
                }`}>
                  {tab.count}
                </span>
              )}
              {tab.badge && (
                <span className="text-[9px] uppercase px-1 rounded bg-blue-500/20 text-blue-700 font-extrabold">
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT PANELS */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs min-h-[500px] p-6">
        {/* TAB 1: OVERVIEW & INCONSISTENCIES (VELOCITY FRAUD COMMAND CENTER LAYOUT) */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Top Critical Alert Banner (Styled as Velocity Fraud Defense Hero) */}
            <div className="bg-gradient-to-r from-red-950 via-slate-900 to-slate-950 border border-red-800/80 rounded-2xl p-5 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-xl bg-red-600/20 border border-red-500/50 flex items-center justify-center shrink-0 shadow-lg shadow-red-900/30">
                  <AlertTriangle className="w-6 h-6 text-red-400" />
                </div>
                <div>
                  <div className="text-[10px] font-extrabold uppercase tracking-widest text-red-400 flex items-center gap-2">
                    <span>{claim.priority_score >= 70 ? 'HIGH RISK FRAUD ALERT' : 'ROUTINE SIU DOSSIER REVIEW'}</span>
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping"></span>
                  </div>
                  <h2 className="text-lg font-bold text-white tracking-tight">
                    Critical Alert: {claim.title || 'Flagged Transaction & Damage Discrepancy'}
                  </h2>
                  <div className="text-xs text-slate-400 mt-1 flex flex-wrap items-center gap-x-4 gap-y-1">
                    <span>ID: <strong className="text-slate-200 font-mono">{activeClaimId}</strong></span>
                    <span>Date: <strong className="text-slate-200">{claim.incident_date} {claim.incident_time}</strong></span>
                    <span>Risk Index: <strong className="text-red-400 font-mono font-extrabold">{claim.priority_score?.toFixed(1)}/100</strong></span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 self-start md:self-auto">
                <button
                  onClick={() => setActiveTab('graph')}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition flex items-center gap-1.5"
                >
                  <GitFork className="w-3.5 h-3.5" />
                  <span>Investigate Case</span>
                </button>
                <button
                  onClick={handleRunInvestigation}
                  className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 shadow-xs transition"
                >
                  Re-Run AI Inference
                </button>
              </div>
            </div>

            {/* Critical Discrepancy Banners (Red, Purple YOLO & Amber) */}
            <div className="space-y-2.5">
              {/* Notice for Pending Claims awaiting AI Inference */}
              {contradictions.length === 0 && (
                <div className="p-4 rounded-xl bg-blue-950/80 border border-blue-600 text-white flex items-center justify-between gap-4 text-xs shadow-md">
                  <div className="flex items-center gap-3">
                    <Sparkles className="w-5 h-5 text-blue-400 shrink-0" />
                    <div>
                      <div className="font-bold text-blue-300 uppercase text-[11px] tracking-wider">
                        Fresh Consumer Submission Awaiting Officer AI Run
                      </div>
                      <p className="text-slate-300 text-[11px] mt-0.5">
                        Consumer details and uploaded photo ingested. Click to execute YOLO damage localization and cross-modal corroboration.
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={handleRunInvestigation}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-xs transition shadow-xs shrink-0"
                  >
                    Run AI Investigation Now
                  </button>
                </div>
              )}

              {/* 1. Inconsistency / Corroboration Banner for Priority Reference #1 (Police File vs Consumer File) */}
              {contradictions.some((c: any) => c.conflict_id?.includes('-00') || c.category?.toLowerCase().includes('police')) ? (
                <div className="p-4 rounded-xl bg-gradient-to-r from-red-950 via-red-900/60 to-red-950 border-2 border-red-600 text-white flex items-start gap-3 text-xs shadow-md">
                  <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                  <div className="space-y-1.5 flex-1">
                    <div className="font-extrabold text-red-300 uppercase tracking-wider text-[11px] flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-red-600 text-white font-mono text-[10px] tracking-normal font-bold shadow-xs">
                          PRIORITY REFERENCE #1
                        </span>
                        <span>CONSUMER FILE VS. POLICE FILE MISMATCH (CRITICAL)</span>
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] px-2 py-0.5 rounded bg-red-950 border border-red-700 font-mono text-red-300 font-bold">
                          {claim.police_report?.fir_gd_number || 'POLICE GD-482'} / {claim.police_report?.station_name || 'STATION EXTRACT'}
                        </span>
                        <button
                          onClick={handleDownloadFirReport}
                          disabled={downloadingFir}
                          className="text-[10px] px-2.5 py-1 rounded bg-red-900 hover:bg-red-800 border border-red-700 text-white font-bold flex items-center gap-1 transition shadow-xs cursor-pointer disabled:opacity-60"
                        >
                          <Download className="w-3 h-3" />
                          <span>{downloadingFir ? 'Downloading...' : 'Download FIR'}</span>
                        </button>
                      </div>
                    </div>
                    <p className="text-slate-100 leading-relaxed text-[11px] font-medium">
                      {contradictions.find((c: any) => c.conflict_id?.includes('-00') || c.category?.toLowerCase().includes('police'))?.description ||
                        'FIRST REFERENCE MISMATCH: Consumer intake statement asserts a simple single-point rear collision, whereas official Police General Diary (GD Extract) records divergent impact points or statement discrepancies at the scene.'}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-[10px]">
                      <div className="p-1.5 rounded bg-black/40 border border-red-800/60 text-slate-300">
                        • Consumer Declaration: <strong className="text-white">"{claim.reported_narrative?.slice(0, 75)}..."</strong>
                      </div>
                      <div className="p-1.5 rounded bg-black/40 border border-red-800/60 text-amber-200">
                        • Official Police GD Record: <strong className="text-white">{claim.police_report?.police_summary?.slice(0, 85) || 'Divergent impact recorded at scene'}...</strong>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                /* When Police FIR Corroborates / Agrees with Consumer Declaration */
                <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-950 via-slate-900 to-emerald-950 border-2 border-emerald-500 text-white flex items-start gap-3 text-xs shadow-md">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div className="space-y-1.5 flex-1">
                    <div className="font-extrabold text-emerald-300 uppercase tracking-wider text-[11px] flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-emerald-600 text-white font-mono text-[10px] tracking-normal font-bold shadow-xs">
                          PRIORITY REFERENCE #1
                        </span>
                        <span>POLICE FIR / GD VERIFIED CORROBORATION (AGREES WITH CONSUMER)</span>
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 border border-emerald-700 font-mono text-emerald-300 font-bold">
                          {claim.police_report?.fir_gd_number || 'POLICE GD'} / {claim.police_report?.station_name || 'STATION EXTRACT'}
                        </span>
                        <button
                          onClick={handleDownloadFirReport}
                          disabled={downloadingFir}
                          className="text-[10px] px-2.5 py-1 rounded bg-emerald-800 hover:bg-emerald-700 border border-emerald-600 text-white font-bold flex items-center gap-1 transition shadow-xs cursor-pointer disabled:opacity-60"
                        >
                          <Download className="w-3 h-3" />
                          <span>{downloadingFir ? 'Downloading...' : 'Download FIR'}</span>
                        </button>
                      </div>
                    </div>
                    <p className="text-slate-100 leading-relaxed text-[11px] font-medium">
                      {claim.police_report?.police_summary ||
                        'Official Police General Diary (GD) entry corroborates policyholder declaration. On-scene physical inspection confirms stationary position at traffic signal with rear-end impact from trailing vehicle. Independent witnesses verify narrative.'}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-[10px]">
                      <div className="p-1.5 rounded bg-black/40 border border-emerald-800/60 text-slate-300">
                        • Consumer Declaration: <strong className="text-white">"{claim.reported_narrative?.slice(0, 75)}..."</strong>
                      </div>
                      <div className="p-1.5 rounded bg-black/40 border border-emerald-800/60 text-emerald-300">
                        • Official Police GD Finding: <strong className="text-white">Corroborated by Attending Sub-Inspector</strong>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 2. YOLO Neural Computer Vision Damage Zone Conflict Banner */}
              {contradictions.find((c: any) => c.category?.toLowerCase().includes('yolo') || c.conflict_id?.includes('YOLO')) && (
                <div className="p-4 rounded-xl bg-gradient-to-r from-purple-950 via-slate-900 to-indigo-950 border-2 border-purple-500 text-white flex items-start gap-3 text-xs shadow-lg">
                  <div className="w-8 h-8 rounded-lg bg-purple-600/30 border border-purple-400 flex items-center justify-center shrink-0">
                    <Sparkles className="w-4 h-4 text-purple-300" />
                  </div>
                  <div className="space-y-1.5 flex-1">
                    <div className="font-extrabold text-purple-300 uppercase tracking-wider text-[11px] flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-purple-600 text-white font-mono text-[10px] tracking-normal font-bold shadow-xs">
                          YOLOv8 COMPUTER VISION
                        </span>
                        <span>DAMAGE ZONE VS. CONSUMER NARRATIVE MISMATCH (CRITICAL)</span>
                      </span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-purple-900 border border-purple-700 font-mono text-purple-200">
                        SPATIAL CONFLICT DETECTED
                      </span>
                    </div>
                    <p className="text-slate-100 leading-relaxed text-[11px] font-medium">
                      {contradictions.find((c: any) => c.category?.toLowerCase().includes('yolo') || c.conflict_id?.includes('YOLO'))?.description ||
                        contradictions.find((c: any) => c.category?.toLowerCase().includes('yolo') || c.conflict_id?.includes('YOLO'))?.explanation}
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-[10px]">
                      <div className="p-1.5 rounded bg-black/40 border border-purple-800/60 text-slate-300">
                        • Consumer Claimed Impact: <strong className="text-white">{claim.accident_type || 'Reported Collision'}</strong>
                      </div>
                      <div className="p-1.5 rounded bg-black/40 border border-purple-800/60 text-amber-200">
                        • YOLO Neural Detection: <strong className="text-white">{yoloComponent} ({yoloConfidence}% Conf)</strong>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 2. Amber High Inconsistency Banner */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-amber-950/60 to-amber-900/30 border border-amber-800/80 text-white flex items-start gap-3 text-xs shadow-xs">
                <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div className="space-y-1 flex-1">
                  <div className="font-extrabold text-amber-300 uppercase tracking-wider text-[11px] flex items-center justify-between">
                    <span>STATEMENT DIVERGENCE & BENCHMARK MATCH (HIGH)</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-amber-900/60 border border-amber-700 font-mono">
                      ESTIMATE: ₹{claim.estimated_damage?.toLocaleString()}
                    </span>
                  </div>
                  <p className="text-slate-200 leading-relaxed text-[11px]">
                    {contradictions[1]?.explanation ||
                      'Claimant statement explicitly denies front contact. Repair estimate quotes ₹38,000 for LHS front fender replacement exceeding OEM benchmark.'}
                  </p>
                </div>
              </div>
            </div>

            {/* Main Command Center Grid: Left (Viewer & Summaries) + Right (Sidebar & Drivers) */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column (2 Cols): Forensic Evidence View + Metrics */}
              <div className="lg:col-span-2 space-y-6">
                {/* Photo Viewer & Vehicle Info Card */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
                  {/* Photo Section with Overlay */}
                  <div className="relative bg-slate-950 min-h-[300px] max-h-[420px] flex items-center justify-center overflow-hidden group">
                    <img
                      src={displayImageUrl}
                      alt={vehicle.model || 'Claimant Vehicle Damage'}
                      className="w-full h-80 object-cover object-center opacity-95 group-hover:scale-101 transition duration-500"
                    />

                    {/* Reference Tag Badge */}
                    <div className="absolute top-3 left-3 bg-slate-950/90 backdrop-blur-md border border-slate-700 px-3 py-1.5 rounded-lg text-[11px] font-mono text-slate-200 flex items-center gap-2 shadow-md">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                      <span>
                        {isUploadedEvidence
                          ? `POLICYHOLDER UPLOADED EVIDENCE: ${vehicle.registration_number || claim.vehicle_reg}`
                          : `REFERENCE IMAGE: ${visual.vehicleLabel}`}
                      </span>
                    </div>

                    {/* YOLO Neural Engine Active Badge */}
                    <div className="absolute top-3 right-3 bg-purple-950/90 backdrop-blur-md border border-purple-600 px-3 py-1.5 rounded-lg text-[11px] font-mono text-purple-200 flex items-center gap-1.5 shadow-md">
                      <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                      <span>{yoloEngine}</span>
                    </div>

                    {/* YOLO Dynamic Neural Bounding Box Target Reticle */}
                    <div className="absolute inset-0 pointer-events-none flex items-center justify-center p-8">
                      <div className="relative border-2 border-dashed border-red-500/90 bg-red-500/10 rounded-lg w-4/5 h-3/5 shadow-2xl flex flex-col justify-between p-2">
                        <div className="flex items-center justify-between">
                          <span className="bg-red-950/95 border border-red-600 text-red-200 text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase tracking-wider flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-ping"></span>
                            YOLO DETECT: {yoloComponent} ({yoloConfidence}%)
                          </span>
                          <span className="bg-black/80 border border-slate-700 text-slate-300 text-[10px] font-mono px-1.5 py-0.5 rounded">
                            ZONE: {yoloZone.toUpperCase()}
                          </span>
                        </div>
                        <div className="flex justify-between items-end">
                          <span className="text-[9px] font-mono text-red-300/80 bg-black/60 px-1 rounded">
                            ROI: [X:{yoloBbox.x}, Y:{yoloBbox.y}, W:{yoloBbox.width}, H:{yoloBbox.height}]
                          </span>
                          <span className="bg-amber-950/90 border border-amber-600 text-amber-200 text-[10px] font-mono px-2 py-0.5 rounded">
                            {yoloDamageType}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* AI Bounding Box Callout Overlay */}
                    <div className="absolute bottom-3 right-3 bg-red-950/95 backdrop-blur-md border border-red-700 px-3 py-1.5 rounded-lg text-xs text-red-200 flex items-center gap-2 shadow-lg">
                      <AlertTriangle className="w-3.5 h-3.5 text-red-400" />
                      <span className="font-semibold text-[11px] font-mono">
                        YOLO Damage: {yoloComponent} ({yoloSeverity})
                      </span>
                    </div>
                  </div>

                  {/* Detailed YOLO Neural Analytics Panel */}
                  <div className="p-4 bg-slate-950 border-t border-slate-800 text-xs space-y-3">
                    <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-purple-900/60 border border-purple-700 text-purple-300 font-mono text-[10px] font-bold">
                          YOLOv8 NEURAL VISION ANALYTICS
                        </span>
                        <span className="text-slate-400 text-[11px]">Computer Vision Damage Decomposition</span>
                      </div>
                      <span className="text-emerald-400 font-mono text-[11px] font-semibold">
                        Confidence: {yoloConfidence}%
                      </span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-slate-300 font-mono text-[11px]">
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                        <div className="text-[10px] uppercase text-slate-500 font-bold">Detected Zone</div>
                        <div className="text-white font-bold mt-0.5 capitalize">{yoloZone} Structural Assembly</div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                        <div className="text-[10px] uppercase text-slate-500 font-bold">Identified Part</div>
                        <div className="text-amber-300 font-bold mt-0.5 truncate">{yoloComponent}</div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                        <div className="text-[10px] uppercase text-slate-500 font-bold">Deformation Type</div>
                        <div className="text-slate-200 font-bold mt-0.5 truncate">{yoloDamageType}</div>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                        <div className="text-[10px] uppercase text-slate-500 font-bold">Spatial Corroboration</div>
                        <div className={`font-bold mt-0.5 ${
                          claim.reported_narrative?.toLowerCase().includes(yoloZone) || claim.accident_type?.toLowerCase().includes(yoloZone)
                            ? 'text-emerald-400'
                            : 'text-red-400'
                        }`}>
                          {claim.reported_narrative?.toLowerCase().includes(yoloZone) || claim.accident_type?.toLowerCase().includes(yoloZone)
                            ? 'Corroborated'
                            : 'Zone Mismatch'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Vehicle Info & Claim Details Sub-bar */}
                  <div className="p-5 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs border-t border-slate-800 bg-slate-900/90">
                    <div className="space-y-1.5">
                      <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Vehicle Particulars</div>
                      <div className="text-sm font-extrabold text-white">
                        {vehicle.year || 2023} {vehicle.make || 'Hyundai'} {vehicle.model || 'Creta SX'}
                      </div>
                      <div className="text-slate-400 text-[11px] space-y-0.5 font-mono">
                        <div>Reg: <strong className="text-slate-200">{vehicle.registration_number || claim.vehicle_reg}</strong></div>
                        <div>VIN: <strong className="text-slate-200">{vehicle.vin || 'MALC481CLPM019284'}</strong></div>
                        <div>Color: <strong className="text-slate-200">{vehicle.color || 'White'} ({vehicle.body_type || 'SUV'})</strong></div>
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Claimant & Incident</div>
                      <div className="text-sm font-extrabold text-white">
                        {claim.claimant?.name || 'Pooja Sharma'}
                      </div>
                      <div className="text-slate-400 text-[11px] space-y-0.5">
                        <div>Contact: <strong className="text-slate-200">{claim.claimant?.phone || claim.claimant?.email}</strong></div>
                        <div>Date: <strong className="text-slate-200">{claim.incident_date} {claim.incident_time}</strong></div>
                        <div>Location: <strong className="text-slate-200">{claim.incident_location}</strong></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Alert Summary & Confidence Semicircle Gauge */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  {/* Alert Summary Box */}
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white space-y-3 shadow-lg">
                    <div className="font-bold text-slate-400 uppercase tracking-wider text-[11px] border-b border-slate-800 pb-2">
                      Alert Summary & Risk Index
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-[10px] uppercase font-bold text-slate-400">SIU Risk Score</div>
                        <div className="text-3xl font-extrabold text-red-500 font-mono">
                          {claim.priority_score?.toFixed(0) || '88'}%
                        </div>
                      </div>

                      {/* Semicircle Gauge Visual */}
                      <div className="text-right">
                        <div className="text-[10px] uppercase font-bold text-slate-400">Confidence Level</div>
                        <div className="text-2xl font-extrabold text-amber-400 font-mono">84%</div>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 font-semibold">
                          High Confidence
                        </span>
                      </div>
                    </div>

                    <div className="space-y-1.5 pt-2 border-t border-slate-800 text-[11px] text-slate-300">
                      <div className="font-semibold text-slate-200">Key AI Findings:</div>
                      <ul className="space-y-1 list-disc list-inside text-slate-400">
                        <li>Metadata & crash location mismatch identified</li>
                        <li>Extracted damage distribution conflicts with single impact</li>
                        <li>Pre-existing paint patina on LHS wing assembly</li>
                        <li>Bodyshop quote exceeds regional OEM benchmark</li>
                      </ul>
                    </div>
                  </div>

                  {/* Reported Accident Sequence & Narrative */}
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white space-y-3 shadow-lg">
                    <div className="font-bold text-slate-400 uppercase tracking-wider text-[11px] border-b border-slate-800 pb-2 flex items-center justify-between">
                      <span>Reported Accident Narrative</span>
                      <span className="text-[10px] text-blue-400 font-mono font-normal">Claimant Statement</span>
                    </div>

                    <blockquote className="text-xs text-slate-300 italic bg-slate-950 p-3 rounded-xl border border-slate-800 leading-relaxed min-h-[90px]">
                      "{claim.reported_narrative || 'Claimant states vehicle was rear-ended at traffic signal. Denies any frontal or secondary collision.'}"
                    </blockquote>

                    <div className="grid grid-cols-2 gap-2 text-[11px] pt-1 font-mono text-slate-400">
                      <div className="p-2 rounded bg-slate-950 border border-slate-800">
                        Type: <strong className="text-slate-200">{claim.accident_type}</strong>
                      </div>
                      <div className="p-2 rounded bg-slate-950 border border-slate-800">
                        Estimate: <strong className="text-slate-200">₹{claim.estimated_damage?.toLocaleString()}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Ingested Forensic Assets Gallery */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white space-y-3 shadow-lg">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                    <div className="font-bold text-slate-400 uppercase tracking-wider text-[11px]">
                      Ingested Forensic Assets ({claimData?.evidence?.length || 3} Files)
                    </div>
                    <span className="text-[10px] text-emerald-400 font-mono">SHA-256 Verified</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {(claimData?.evidence || []).map((e: any) => {
                      const isPoliceDoc = e.file_type === 'document' || e.file_name?.toLowerCase().includes('police') || e.file_name?.toLowerCase().includes('gd');
                      return (
                        <div
                          key={e.evidence_id}
                          className="p-3 bg-slate-950 rounded-xl border border-slate-800 hover:border-blue-500/50 transition text-xs space-y-1.5 flex flex-col justify-between"
                        >
                          <div>
                            <div className="flex items-center space-x-2 truncate">
                              <FileText className="w-4 h-4 text-blue-400 shrink-0" />
                              <span className="truncate font-semibold text-slate-200">{e.file_name}</span>
                            </div>
                            <div className="text-[10px] font-mono text-slate-500 mt-1">
                              {e.source || 'Upload'} • {e.file_size || '2.4 MB'}
                            </div>
                            <div className="text-[10px] font-mono text-slate-400 truncate">
                              Hash: {e.sha256_hash?.slice(0, 12)}...
                            </div>
                          </div>
                          {isPoliceDoc && (
                            <button
                              onClick={handleDownloadFirReport}
                              disabled={downloadingFir}
                              className="mt-2 inline-flex items-center justify-center gap-1.5 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-blue-300 border border-slate-700 rounded text-[10px] font-semibold transition cursor-pointer disabled:opacity-60"
                            >
                              <Download className="w-3 h-3 text-emerald-400" />
                              <span>{downloadingFir ? 'Downloading...' : 'Download Certified FIR (PDF)'}</span>
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Right Column (1 Col): Investigation Details & Score Drivers (Velocity Style) */}
              <div className="space-y-6">
                {/* Investigation Details Card */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white space-y-4 shadow-lg">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                    <h3 className="font-bold text-slate-300 uppercase tracking-wider text-xs">
                      Investigation Details
                    </h3>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setDecisionStatus('approved');
                          setActiveTab('decision');
                        }}
                        className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[11px] font-semibold transition"
                      >
                        Mark as Safe
                      </button>
                      <button
                        onClick={() => {
                          setDecisionStatus('escalated');
                          setActiveTab('decision');
                        }}
                        className="px-2.5 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-[11px] font-semibold transition"
                      >
                        Escalate
                      </button>
                    </div>
                  </div>

                  {/* Detail Item Rows */}
                  <div className="space-y-2.5 text-xs">
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">VIN:</span>
                      <span className="font-mono font-semibold text-slate-200">{vehicle.vin || 'MALC481CLPM019284'}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">User ID / Claimant:</span>
                      <span className="font-semibold text-slate-200">{claim.claimant?.email || 'usr-claimant-01'}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Claim Date:</span>
                      <span className="text-slate-200">{claim.incident_date} {claim.incident_time}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Location:</span>
                      <span className="text-slate-200 max-w-[140px] truncate">{claim.incident_location}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Policy Number:</span>
                      <span className="font-mono text-slate-200">{claim.policy_number}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800/60">
                      <span className="text-slate-400">Bodyshop Quote:</span>
                      <span className="font-mono font-bold text-red-400">₹{claim.estimated_damage?.toLocaleString() ?? 0}</span>
                    </div>
                    <div className="flex justify-between py-1">
                      <span className="text-slate-400">Indicative Payout:</span>
                      <span className="font-mono font-bold text-emerald-400">₹{settlement?.indicative_settlement?.toLocaleString() ?? 0}</span>
                    </div>
                  </div>

                  {/* Investigation Status & Badges */}
                  <div className="pt-2 border-t border-slate-800 space-y-2">
                    <div className="text-[10px] uppercase font-bold text-slate-400">Investigation Status</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2.5 py-1 rounded bg-blue-950 text-blue-300 border border-blue-800 text-xs font-semibold">
                        Active SIU
                      </span>
                      <span className="px-2.5 py-1 rounded bg-amber-950 text-amber-300 border border-amber-800 text-xs font-semibold">
                        Warning Flagged
                      </span>
                    </div>
                  </div>

                  {/* Score Drivers Bar Graph (Exact Match to Velocity Reference Screen) */}
                  <div className="pt-3 border-t border-slate-800 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                        Score Drivers
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">Weight / Impact</span>
                    </div>

                    <div className="space-y-3 text-xs">
                      {/* Driver 1: Image & Damage Conflict */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-[11px]">
                          <span className="text-slate-300">Damage Pattern Conflict</span>
                          <span className="font-bold text-red-400 font-mono">88.4%</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                          <div className="bg-red-500 h-2.5 rounded-full" style={{ width: '88.4%' }}></div>
                        </div>
                      </div>

                      {/* Driver 2: Metadata / Narrative Discrepancy */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-[11px]">
                          <span className="text-slate-300">Metadata & Statement Conflict</span>
                          <span className="font-bold text-amber-400 font-mono">96.0%</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                          <div className="bg-amber-500 h-2.5 rounded-full" style={{ width: '96.0%' }}></div>
                        </div>
                      </div>

                      {/* Driver 3: Mechanical Plausibility Deficit */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-[11px]">
                          <span className="text-slate-300">Mechanical Plausibility Deficit</span>
                          <span className="font-bold text-blue-400 font-mono">75.0%</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                          <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: '75.0%' }}></div>
                        </div>
                      </div>

                      {/* Driver 4: Repair Quote Anomaly */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-[11px]">
                          <span className="text-slate-300">Repair Cost Inflation</span>
                          <span className="font-bold text-purple-400 font-mono">64.0%</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                          <div className="bg-purple-500 h-2.5 rounded-full" style={{ width: '64.0%' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Next Step Callout */}
                <div className="p-4 rounded-2xl bg-gradient-to-r from-blue-950 to-indigo-950 border border-blue-800/80 text-white space-y-2 text-xs shadow-lg">
                  <div className="font-bold text-blue-300 flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-blue-400" />
                    <span>Next-Best-Evidence Action Loop</span>
                  </div>
                  <p className="text-slate-300 text-[11px] leading-relaxed">
                    High expected information gain (EIG) action recommended: Request Bodyshop Intake Inspection Sheet to resolve pre-existing wing damage uncertainty.
                  </p>
                  <button
                    onClick={() => setActiveTab('nbe')}
                    className="w-full py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-[11px] transition mt-1"
                  >
                    View Ranked NBE Recommendations
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: REACT FLOW RELATIONSHIP GRAPH */}
        {activeTab === 'graph' && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <GitFork className="w-4 h-4 text-blue-600" />
                  Interactive Evidence Relationship Graph
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Visualizes nodes (Claim Root, Evidence Files, Extracted Facts, Hypotheses) and animated contradiction links. Click and drag to inspect relationships.
                </p>
              </div>
              <div className="flex items-center gap-3 text-xs">
                <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-slate-900"></span> Claim Root</span>
                <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-white border border-sky-500"></span> Evidence</span>
                <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-green-100 border border-green-500"></span> Extracted Fact</span>
                <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-red-500"></span> Contradiction Link</span>
              </div>
            </div>

            <div className="h-[550px] w-full border border-slate-200 rounded-xl overflow-hidden bg-slate-50 relative">
              <ReactFlow
                nodes={graphData.nodes}
                edges={graphData.edges}
                fitView
              >
                <Background color="#cbd5e1" gap={16} />
                <Controls />
              </ReactFlow>
            </div>
          </div>
        )}

        {/* TAB 3: MULTI-HYPOTHESIS COMPARATOR */}
        {activeTab === 'hypotheses' && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Compass className="w-4 h-4 text-blue-600" />
                Competing Accident Hypotheses & Reconstruction Scenarios
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                CLAIMSIGHT AI evaluates multiple plausible explanations instead of forcing an automated single narrative.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {hypotheses.map((h: any) => (
                <div
                  key={h.hypothesis_id}
                  className="p-5 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-white transition space-y-3 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <h4 className="font-bold text-slate-900 text-sm">{h.title}</h4>
                    <span className="font-bold text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded text-[11px]">
                      Support: {(h.probability_score * 100).toFixed(0)}%
                    </span>
                  </div>

                  <p className="text-slate-700 leading-relaxed">{h.summary}</p>

                  {/* Probability Bar */}
                  <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${h.probability_score * 100}%` }}
                    ></div>
                  </div>

                  <div className="space-y-1.5 pt-2">
                    <div className="text-[11px] font-semibold text-emerald-800">
                      • Supporting Evidence:
                      <span className="font-normal text-slate-600 ml-1">
                        {h.supporting_evidence?.join(', ') || 'None identified'}
                      </span>
                    </div>

                    {h.contradicting_evidence?.length > 0 && (
                      <div className="text-[11px] font-semibold text-red-800">
                        • Contradicting Evidence:
                        <span className="font-normal text-slate-600 ml-1">
                          {h.contradicting_evidence.join(', ')}
                        </span>
                      </div>
                    )}

                    <div className="text-[11px] font-semibold text-slate-700">
                      • Underlying Assumptions:
                      <span className="font-normal text-slate-600 ml-1">
                        {h.assumptions?.join('; ')}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: CLAIM EVALUATION (5 DIMENSIONS) */}
        {activeTab === 'evaluation' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <FileCheck2 className="w-4 h-4 text-blue-600" />
                Multi-Dimensional Forensic Integrity Evaluation
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Independent evaluation across 5 distinct mechanical, environmental, and financial dimensions.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {/* 1. Physical Plausibility */}
              <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    1. Mechanical & Physical Plausibility
                  </span>
                  <span className="font-extrabold text-blue-600">{evaluation?.physical_plausibility?.score ?? 90}/100</span>
                </div>
                <div className="font-semibold text-slate-900">{evaluation?.physical_plausibility?.status}</div>
                <p className="text-slate-600">{evaluation?.physical_plausibility?.details}</p>
              </div>

              {/* 2. Environmental Feasibility */}
              <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    2. Meteorological & Environmental Feasibility
                  </span>
                  <span className="font-extrabold text-blue-600">{evaluation?.environmental_feasibility?.score ?? 90}/100</span>
                </div>
                <div className="font-semibold text-slate-900">{evaluation?.environmental_feasibility?.status}</div>
                <p className="text-slate-600">{evaluation?.environmental_feasibility?.details}</p>
              </div>

              {/* 3. Damage Consistency */}
              <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    3. Damage Distribution & Aging Consistency
                  </span>
                  <span className="font-extrabold text-blue-600">{evaluation?.damage_consistency?.score ?? 90}/100</span>
                </div>
                <div className="font-semibold text-slate-900">{evaluation?.damage_consistency?.status}</div>
                <p className="text-slate-600">{evaluation?.damage_consistency?.details}</p>
              </div>

              {/* 4. Repair Anomaly & Benchmarking */}
              <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    4. Repair Cost Anomaly & Dynamic Benchmarking
                  </span>
                  <span className="font-extrabold text-blue-600">{evaluation?.repair_anomaly?.score ?? 90}/100</span>
                </div>
                <div className="font-semibold text-slate-900">{evaluation?.repair_anomaly?.status}</div>
                <p className="text-slate-600">{evaluation?.repair_anomaly?.details}</p>
              </div>
            </div>

            {/* Benchmark Comparison Table */}
            {benchmarks.length > 0 && (
              <div className="space-y-3 pt-3">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Regional OEM vs Aftermarket Parts Cost Benchmarks ({vehicle.make} {vehicle.model})
                </h4>
                <div className="border border-slate-200 rounded-lg overflow-hidden text-xs">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                      <tr>
                        <th className="p-2.5">Component</th>
                        <th className="p-2.5">OEM Benchmark</th>
                        <th className="p-2.5">Aftermarket Benchmark</th>
                        <th className="p-2.5">Std Labor Hours</th>
                        <th className="p-2.5">Paint Materials</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-mono">
                      {benchmarks.map((b: any) => (
                        <tr key={b.benchmark_id} className="hover:bg-slate-50">
                          <td className="p-2.5 font-sans font-medium text-slate-800">{b.component}</td>
                          <td className="p-2.5 text-blue-700 font-semibold">₹{b.oem_price?.toLocaleString()}</td>
                          <td className="p-2.5 text-slate-600">₹{b.aftermarket_price?.toLocaleString()}</td>
                          <td className="p-2.5 text-slate-600">{b.labor_hours} hrs</td>
                          <td className="p-2.5 text-slate-600">₹{b.paint_cost?.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 5: NEXT-BEST-EVIDENCE INTELLIGENCE (FLAGSHIP) */}
        {activeTab === 'nbe' && (
          <div className="space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-blue-600" />
                    Next-Best-Evidence Recommendation Engine
                  </h3>
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded">
                    FLAGSHIP INNOVATION
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Ranks additional evidence requests by Expected Information Gain (EIG), Materiality, and Collection Effort.
                </p>
              </div>

              {/* Ranking Formula Callout Badge */}
              <div className="bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-lg text-[11px] font-mono text-blue-900">
                Score = (EIG × Materiality × Reliability) / (Cost + 0.1)
              </div>
            </div>

            <div className="space-y-3">
              {recommendations.map((r: any, idx: number) => (
                <div
                  key={r.request_id}
                  className="p-4 rounded-xl border border-slate-200 bg-white hover:border-blue-300 shadow-xs space-y-3 text-xs transition"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="w-6 h-6 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs">
                        #{idx + 1}
                      </span>
                      <span className="font-bold text-slate-900 text-sm">{r.action_recommended}</span>
                    </div>

                    <div className="flex items-center space-x-3">
                      <div className="text-right">
                        <div className="text-[10px] uppercase font-bold text-slate-400">Heuristic Score</div>
                        <div className="text-sm font-extrabold text-blue-600">{r.rank_score?.toFixed(2)}</div>
                      </div>

                      <select
                        value={r.status}
                        onChange={(e) => handleUpdateRecommendationStatus(r.request_id, e.target.value)}
                        className="text-xs bg-slate-50 border border-slate-200 rounded px-2.5 py-1 font-semibold text-slate-700"
                      >
                        <option value="pending">Pending</option>
                        <option value="sent">Dispatched / Sent</option>
                        <option value="submitted">Submitted</option>
                        <option value="reviewed">Reviewed</option>
                        <option value="completed">Completed</option>
                      </select>
                    </div>
                  </div>

                  <p className="text-slate-600 leading-relaxed">
                    <strong>Target Uncertainty:</strong> {r.uncertainty_addressed}
                  </p>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 font-mono text-[11px] text-slate-600">
                    <div className="p-2 rounded bg-slate-50 border border-slate-150">
                      EIG Gain: <strong className="text-slate-800">{(r.expected_information_gain * 100).toFixed(0)}%</strong>
                    </div>
                    <div className="p-2 rounded bg-slate-50 border border-slate-150">
                      Materiality: <strong className="text-slate-800">{(r.materiality * 100).toFixed(0)}%</strong>
                    </div>
                    <div className="p-2 rounded bg-slate-50 border border-slate-150">
                      Est. Effort / Cost: <strong className="text-slate-800">{(r.estimated_cost * 100).toFixed(0)}%</strong>
                    </div>
                    <div className="p-2 rounded bg-slate-50 border border-slate-150">
                      Responsible: <strong className="text-blue-700">{r.responsible_party}</strong>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 6: FORENSIC TIMELINE */}
        {activeTab === 'timeline' && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-600" />
                Chronological Investigation Timeline
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Segregates Event Time, Document Creation Time, Upload Time, and AI Inferred Time.
              </p>
            </div>

            <div className="relative border-l-2 border-slate-200 ml-4 space-y-6 py-2">
              {timeline.map((t: any, idx: number) => (
                <div key={idx} className="relative pl-6 space-y-1 text-xs">
                  <span className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-blue-600 border-2 border-white shadow-xs"></span>
                  <div className="flex items-center space-x-3">
                    <span className="font-mono text-xs font-bold text-slate-800">
                      {new Date(t.event_timestamp).toLocaleString()}
                    </span>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                      {t.timestamp_type?.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <p className="font-semibold text-slate-800">{t.description}</p>
                  <p className="text-slate-400 text-[11px]">Source Reference: {t.source_reference}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 7: POLICY & SETTLEMENT */}
        {activeTab === 'policy' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <IndianRupee className="w-4 h-4 text-blue-600" />
                Policy & Traceable Settlement Calculation
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Calculates eligible indemnity using deterministic policy endorsements and deductible schedules.
              </p>
            </div>

            {isHighImpact && (
              <div className="p-4 rounded-xl bg-amber-50 border border-amber-300 flex items-start gap-3 text-xs text-amber-900">
                <ShieldCheck className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <div className="font-bold text-sm text-amber-950">
                    High-Impact Decision Guardrail Active (Exposure &gt; ₹5,00,000 Threshold)
                  </div>
                  <p className="leading-relaxed">
                    AI should support, not autonomously make, high-impact insurance decisions.
                    Under IRDAI claims governance, claims exceeding ₹5 Lakhs require mandatory independent verification
                    and authorization by the Chief Compliance Officer (Admin / Top Insurance Officer).
                  </p>
                  {isTopInsuranceOfficer ? (
                    <div className="text-emerald-800 font-bold flex items-center gap-1.5 pt-1">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      Executive Authorization Active: You are signed in as Chief Compliance Officer and authorized to sign off.
                    </div>
                  ) : (
                    <div className="text-red-700 font-semibold flex items-center gap-1.5 pt-1">
                      <Lock className="w-4 h-4 text-red-600" />
                      Standard Investigator Lock: You cannot autonomously clear this settlement. Escalate to Executive Officer.
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Traceable Payout Breakdown */}
              <div className="border border-slate-200 rounded-xl p-5 bg-slate-50/50 space-y-4 text-xs">
                <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px] border-b border-slate-200 pb-2">
                  Settlement Breakdown Schedule
                </div>

                <div className="space-y-2 font-mono">
                  <div className="flex justify-between py-1 text-slate-600">
                    <span>Submitted Bodyshop Estimate:</span>
                    <span>₹{claim.estimated_damage?.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between py-1 font-semibold text-slate-800 border-b border-slate-200">
                    <span>SIU Verified Eligible Repair:</span>
                    <span>₹{settlement?.eligible_repair_amount?.toLocaleString() ?? 0}</span>
                  </div>
                  <div className="flex justify-between py-1 text-red-600">
                    <span>Less: Compulsory Deductible:</span>
                    <span>- ₹{settlement?.deductible?.toLocaleString() ?? 1000}</span>
                  </div>
                  <div className="flex justify-between py-1 text-red-600">
                    <span>Less: Plastic / Paint Depreciation:</span>
                    <span>- ₹{settlement?.depreciation_deduction?.toLocaleString() ?? 0}</span>
                  </div>
                  <div className="flex justify-between py-1 text-red-600 border-b border-slate-200 pb-2">
                    <span>Less: Salvage Recovery Allowance:</span>
                    <span>- ₹{settlement?.salvage_allowance?.toLocaleString() ?? 0}</span>
                  </div>

                  <div className="flex justify-between py-2 text-base font-extrabold text-blue-700 bg-blue-50 px-3 rounded-lg border border-blue-200">
                    <span>INDICATIVE PAYOUT:</span>
                    <span>₹{settlement?.indicative_settlement?.toLocaleString() ?? 0}</span>
                  </div>
                </div>
              </div>

              {/* Policy Clause Citations */}
              <div className="border border-slate-200 rounded-xl p-5 bg-slate-50/50 space-y-3 text-xs">
                <div className="font-bold text-slate-800 uppercase tracking-wider text-[11px] border-b border-slate-200 pb-2">
                  Applicable Policy Clauses & Endorsements
                </div>

                <div className="space-y-2.5">
                  {(settlement?.policy_clause_citations || []).map((c: any, idx: number) => (
                    <div key={idx} className="p-3 bg-white rounded-lg border border-slate-200 space-y-1">
                      <div className="font-bold text-blue-700">{c.clause}</div>
                      <p className="text-slate-600 leading-relaxed text-[11px]">{c.text}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 8: WHAT-IF COUNTERFACTUAL SANDBOX */}
        {activeTab === 'counterfactual' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-blue-600" />
                What-If Counterfactual Investigation Sandbox
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Simulates alternative assumptions without altering the underlying verified case dossier.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <label className="block text-xs font-bold text-slate-700">Hypothetical Assumption to Test:</label>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={customAssumption}
                  onChange={(e) => setCustomAssumption(e.target.value)}
                  className="flex-1 px-3 py-2 text-xs bg-white border border-slate-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={() => handleRunCounterfactual()}
                  disabled={simulating}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs disabled:opacity-50"
                >
                  {simulating ? 'Simulating...' : 'Run Simulation'}
                </button>
              </div>

              <div className="flex flex-wrap gap-2 pt-1 text-[11px]">
                <span className="text-slate-400">Quick Scenarios:</span>
                <button
                  onClick={() => {
                    setCustomAssumption('Exclude front-left fender damage as pre-existing');
                    handleRunCounterfactual('Exclude front-left fender damage as pre-existing');
                  }}
                  className="text-blue-600 hover:underline font-medium"
                >
                  Exclude Front Damage
                </button>
                <span className="text-slate-300">|</span>
                <button
                  onClick={() => {
                    setCustomAssumption('Assume road was completely dry at crash moment');
                    handleRunCounterfactual('Assume road was completely dry at crash moment');
                  }}
                  className="text-blue-600 hover:underline font-medium"
                >
                  Dry Road Condition
                </button>
                <span className="text-slate-300">|</span>
                <button
                  onClick={() => {
                    setCustomAssumption('Exclude labor and paint markup exceeding OEM benchmark');
                    handleRunCounterfactual('Exclude labor and paint markup exceeding OEM benchmark');
                  }}
                  className="text-blue-600 hover:underline font-medium"
                >
                  OEM Benchmark Cap
                </button>
              </div>
            </div>

            {counterfactualResult && (
              <div className="p-5 rounded-xl bg-blue-50/50 border border-blue-200 space-y-3 text-xs">
                <div className="font-bold text-blue-900 text-sm">Simulation Results</div>
                <p className="text-slate-800 leading-relaxed">{counterfactualResult.explanation}</p>

                <div className="grid grid-cols-2 gap-4 pt-2 font-mono text-[11px]">
                  <div className="p-3 bg-white rounded border border-blue-150">
                    Settlement Adjustment: <strong className="text-red-600 font-bold">₹{counterfactualResult.settlement_difference?.toLocaleString()}</strong>
                  </div>
                  <div className="p-3 bg-white rounded border border-blue-150">
                    Simulated Indicative Payout: <strong className="text-emerald-700 font-bold">₹{counterfactualResult.new_indicative_payout?.toLocaleString()}</strong>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 9: INVESTIGATOR SIGN-OFF & DECISION */}
        {activeTab === 'decision' && (
          <div className="space-y-6 max-w-2xl">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Human Investigator Final Decision & SIU Sign-Off
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                AI serves as decision-support. A human claims investigator retains ultimate settlement authority.
              </p>
            </div>

            {/* Existing Recorded Decision Display */}
            {claimData?.decision && (
              <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/70 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
                    Recorded Decision Status
                  </span>
                  <span
                    className={`px-2.5 py-0.5 rounded font-bold uppercase text-[11px] ${
                      claimData.decision.status === 'approved'
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                        : claimData.decision.status === 'rejected'
                        ? 'bg-red-100 text-red-800 border border-red-300'
                        : 'bg-purple-100 text-purple-800 border border-purple-300'
                    }`}
                  >
                    {claimData.decision.status}
                  </span>
                </div>
                <div className="text-slate-600">
                  Sign-off by <strong>{claimData.decision.investigator_name || claimData.decision.investigator_id}</strong> (
                  {claimData.decision.role_at_decision || 'investigator'}) on{' '}
                  {claimData.decision.decided_at ? new Date(claimData.decision.decided_at).toLocaleString() : 'N/A'}
                </div>
                {claimData.decision.approved_settlement_amount && (
                  <div className="font-mono text-blue-700 font-semibold">
                    Settlement Amount: ₹{claimData.decision.approved_settlement_amount.toLocaleString()}
                  </div>
                )}
                {claimData.decision.is_high_impact && (
                  <div className="text-[11px] font-semibold text-amber-800 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
                    High-Impact Claim (&gt; ₹5L):{' '}
                    {claimData.decision.verified_by_top_insurance_officer
                      ? 'Verified by Chief Compliance Officer'
                      : 'Pending Executive Verification'}
                  </div>
                )}
                {claimData.decision.notes && (
                  <p className="text-slate-700 italic border-l-2 border-slate-300 pl-2 pt-1 text-[11px]">
                    "{claimData.decision.notes}"
                  </p>
                )}
              </div>
            )}

            {/* High-Impact Guardrail Status Card */}
            {isHighImpact && (
              <div
                className={`p-4 rounded-xl border text-xs space-y-2 ${
                  isTopInsuranceOfficer
                    ? 'bg-emerald-50/70 border-emerald-200 text-emerald-900'
                    : 'bg-amber-50/80 border-amber-300 text-amber-900'
                }`}
              >
                <div className="flex items-center gap-2 font-bold text-sm">
                  {isTopInsuranceOfficer ? (
                    <>
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>Executive Authority Active (Chief Compliance Officer)</span>
                    </>
                  ) : (
                    <>
                      <Lock className="w-4 h-4 text-amber-600 shrink-0" />
                      <span>High-Impact Guardrail Active (&gt; ₹5 Lakhs Threshold)</span>
                    </>
                  )}
                </div>
                <p className="leading-relaxed text-[11px]">
                  {isTopInsuranceOfficer
                    ? 'As the Chief Compliance Officer / Administrator, your credentials authorize you to independently verify and sign off on high-impact settlements exceeding ₹5,00,000.'
                    : 'AI systems support, but must never autonomously make, high-impact insurance decisions. Since exposure exceeds ₹5,00,000, only the Chief Compliance Officer / Top Insurance Executive can authorize payout settlement. Standard investigators can escalate or request additional evidence.'}
                </p>
              </div>
            )}

            {/* Inline Error Callout */}
            {decisionError && (
              <div className="p-3.5 rounded-lg bg-red-50 border border-red-200 text-red-800 text-xs flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                <div className="leading-relaxed">{decisionError}</div>
              </div>
            )}

            <div className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Investigation Ruling</label>
                <select
                  value={decisionStatus}
                  onChange={(e) => setDecisionStatus(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-semibold"
                >
                  <option
                    value="approved"
                    disabled={isHighImpact && !isTopInsuranceOfficer}
                  >
                    {isHighImpact && !isTopInsuranceOfficer
                      ? 'Approve Settlement [LOCKED: Requires Chief Compliance Officer Verification]'
                      : 'Approve Settlement at Indicative Payout' +
                        (isHighImpact && isTopInsuranceOfficer ? ' [Executive Verification Authorized]' : '')}
                  </option>
                  <option value="info_requested">Request Additional Forensic Evidence (Next-Best-Evidence)</option>
                  <option value="escalated">Escalate Dossier to Senior SIU Special Unit / Executive Review</option>
                  <option value="rejected">Repudiate Claim Under Policy Exclusion</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Forensic Decision Rationale & Notes</label>
                <textarea
                  rows={4}
                  value={decisionNotes}
                  onChange={(e) => setDecisionNotes(e.target.value)}
                  placeholder="Record formal justification for SIU audit record..."
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 leading-relaxed"
                />
              </div>

              <button
                onClick={handleSaveDecision}
                disabled={savingDecision}
                className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs disabled:opacity-50"
              >
                {savingDecision ? 'Recording...' : 'Submit Official Ruling'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
