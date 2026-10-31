import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Camera, Upload, FileText, CheckCircle2, AlertCircle, Eye, Trash2, ShieldCheck, Download } from 'lucide-react';

export const EvidenceCentrePage: React.FC = () => {
  const [claims, setClaims] = useState<any[]>([]);
  const [selectedClaimId, setSelectedClaimId] = useState<string>('CLM-2026-002');
  const [evidenceList, setEvidenceList] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [fileToUpload, setFileToUpload] = useState<File | null>(null);
  const [notes, setNotes] = useState('');
  const [selectedPreview, setSelectedPreview] = useState<any | null>(null);

  useEffect(() => {
    loadClaims();
  }, []);

  useEffect(() => {
    if (selectedClaimId) {
      loadEvidence(selectedClaimId);
    }
  }, [selectedClaimId]);

  const loadClaims = async () => {
    try {
      const res = await api.getClaims({ limit: 50 });
      setClaims(res.data.claims || []);
    } catch (e) {
      console.error(e);
    }
  };

  const loadEvidence = async (cid: string) => {
    setLoading(true);
    try {
      const res = await api.getEvidence(cid);
      setEvidenceList(res.data.evidence || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fileToUpload) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', fileToUpload);
    if (notes) formData.append('notes', notes);

    try {
      await api.uploadEvidence(selectedClaimId, formData);
      setFileToUpload(null);
      setNotes('');
      await loadEvidence(selectedClaimId);
      alert('Forensic asset uploaded and indexed successfully.');
    } catch (err) {
      console.error('Upload failed', err);
      alert('Failed to upload evidence.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Camera className="w-6 h-6 text-blue-600" />
            Evidence Centre & Chain-of-Custody
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Forensic intake, cryptographic SHA-256 fingerprinting, EXIF examination, and perceptual duplicate detection.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <label className="text-xs font-semibold text-slate-600">Active Dossier:</label>
          <select
            value={selectedClaimId}
            onChange={(e) => setSelectedClaimId(e.target.value)}
            className="text-xs bg-white border border-slate-300 rounded-lg px-3 py-1.5 font-mono font-bold text-slate-800"
          >
            {claims.map((c) => (
              <option key={c.claim_id} value={c.claim_id}>
                {c.claim_id} - {c.vehicle_reg}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Upload Box */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
          <Upload className="w-4 h-4 text-blue-600" />
          Upload Forensic Evidence Asset to {selectedClaimId}
        </h2>

        <form onSubmit={handleUpload} className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div>
            <label className="block text-slate-600 font-semibold mb-1">Select File (Photo, PDF, Invoice)</label>
            <input
              type="file"
              required
              onChange={(e) => setFileToUpload(e.target.files ? e.target.files[0] : null)}
              className="w-full text-slate-600 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>

          <div>
            <label className="block text-slate-600 font-semibold mb-1">Forensic Annotations / Intake Notes</label>
            <input
              type="text"
              placeholder="e.g. Front crumple zone, workshop estimate"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={uploading || !fileToUpload}
              className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>{uploading ? 'Fingerprinting & Ingesting...' : 'Upload & Compute SHA-256'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Evidence Grid & Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900">
            Chain-of-Custody Inventory for {selectedClaimId} ({evidenceList.length} items)
          </h3>
          <span className="text-xs text-slate-500">Immutable Cryptographic Log</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-500 text-sm">Loading chain of custody...</div>
        ) : evidenceList.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">No evidence assets indexed for this claim.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">Evidence ID</th>
                  <th className="py-3 px-4">Asset Name</th>
                  <th className="py-3 px-4">Type</th>
                  <th className="py-3 px-4">SHA-256 Digest</th>
                  <th className="py-3 px-4">Source / Uploader</th>
                  <th className="py-3 px-4 text-center">Status</th>
                  <th className="py-3 px-4 text-center">Inspect</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {evidenceList.map((ev) => (
                  <tr key={ev.evidence_id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-slate-800">{ev.evidence_id}</td>
                    <td className="py-3 px-4 font-medium text-slate-800 flex items-center gap-2">
                      <FileText className="w-3.5 h-3.5 text-blue-600" />
                      <span>{ev.file_name}</span>
                    </td>
                    <td className="py-3 px-4 uppercase text-[10px] font-bold tracking-wider text-slate-500">
                      {ev.file_type}
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-500" title={ev.sha256_hash}>
                      {ev.sha256_hash?.slice(0, 16)}...
                    </td>
                    <td className="py-3 px-4 text-slate-600">{ev.source}</td>
                    <td className="py-3 px-4 text-center">
                      <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Verified
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => setSelectedPreview(ev)}
                        className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded font-semibold text-xs transition inline-flex items-center gap-1"
                      >
                        <Eye className="w-3 h-3 text-blue-600" /> Preview
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal Preview Dialog */}
      {selectedPreview && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h4 className="font-bold text-slate-900 text-sm">{selectedPreview.file_name}</h4>
                <p className="text-xs text-slate-400 font-mono mt-0.5">{selectedPreview.evidence_id}</p>
              </div>
              <button
                onClick={() => setSelectedPreview(null)}
                className="text-slate-400 hover:text-slate-700 font-bold text-lg"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="max-h-64 overflow-hidden rounded-lg bg-slate-100 flex items-center justify-center border border-slate-200">
                <img
                  src={`/api/evidence/${selectedPreview.evidence_id}/file`}
                  alt={selectedPreview.file_name}
                  className="max-h-64 object-contain"
                  onError={(e: any) => {
                    e.target.style.display = 'none';
                  }}
                />
              </div>

              <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1 font-mono text-[11px]">
                <div><strong>SHA-256 Digest:</strong> {selectedPreview.sha256_hash}</div>
                <div><strong>Source Provenance:</strong> {selectedPreview.source}</div>
                <div><strong>Notes:</strong> {selectedPreview.notes?.join('; ') || 'Standard intake'}</div>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedPreview(null)}
                className="px-4 py-1.5 bg-slate-900 text-white rounded text-xs font-semibold"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

