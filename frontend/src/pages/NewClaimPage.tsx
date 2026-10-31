import React, { useState, useRef, useEffect } from 'react';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  FilePlus2,
  Car,
  User,
  Calendar,
  IndianRupee,
  ArrowLeft,
  UploadCloud,
  Image as ImageIcon,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Trash2,
  Clock,
  MapPin
} from 'lucide-react';

export const NewClaimPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Clean empty state — user fills in their own details
  const [formData, setFormData] = useState({
    policy_number: '',
    claimant: {
      name: user?.name || '',
      phone: '',
      email: user?.email || '',
    },
    vehicle: {
      registration: '',
      make: '',
      model: '',
      year: new Date().getFullYear(),
      vin: '',
      color: '',
      body_type: 'Sedan',
    },
    incident_date: new Date().toISOString().split('T')[0],
    incident_time: '12:00',
    incident_location: '',
    accident_type: 'Rear-End Collision',
    reported_narrative: '',
    estimated_damage: '',
    third_party: '',
  });

  // No image preloaded — user uploads their own image
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string>('');
  const [uploadedFileSize, setUploadedFileSize] = useState<string>('');

  useEffect(() => {
    if (user) {
      setFormData((prev) => ({
        ...prev,
        claimant: {
          name: user.name || prev.claimant.name,
          email: user.email || prev.claimant.email,
          phone: prev.claimant.phone,
        },
      }));
    }
  }, [user]);

  const handleChange = (field: string, val: any) => {
    setFormData((prev) => ({ ...prev, [field]: val }));
  };

  const handleNestedChange = (parent: 'claimant' | 'vehicle', field: string, val: any) => {
    setFormData((prev) => ({
      ...prev,
      [parent]: { ...prev[parent], [field]: val },
    }));
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const rawDataUrl = event.target?.result as string;
        // Optimize resolution to ensure reliable transport and pristine UI display
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let width = img.width;
          let height = img.height;
          const maxDim = 1280;
          if (width > maxDim || height > maxDim) {
            if (width > height) {
              height = Math.round((height * maxDim) / width);
              width = maxDim;
            } else {
              width = Math.round((width * maxDim) / height);
              height = maxDim;
            }
          }
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.drawImage(img, 0, 0, width, height);
            const optimizedDataUrl = canvas.toDataURL('image/jpeg', 0.85);
            setUploadedImage(optimizedDataUrl);
          } else {
            setUploadedImage(rawDataUrl);
          }
        };
        img.onerror = () => {
          setUploadedImage(rawDataUrl);
        };
        img.src = rawDataUrl;

        setUploadedFileName(file.name);
        setUploadedFileSize(`${(file.size / (1024 * 1024)).toFixed(2)} MB`);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSelectSample = (sampleUrl: string, sampleName: string) => {
    setUploadedImage(sampleUrl);
    setUploadedFileName(sampleName);
    setUploadedFileSize('3.20 MB');
  };

  const handleRemoveImage = () => {
    setUploadedImage(null);
    setUploadedFileName('');
    setUploadedFileSize('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.policy_number.trim()) {
      setError('Please provide your insurance policy number.');
      return;
    }
    if (!formData.vehicle.registration.trim()) {
      setError('Please provide your vehicle registration number.');
      return;
    }
    if (!formData.reported_narrative.trim()) {
      setError('Please describe what happened in the accident narrative.');
      return;
    }
    if (!uploadedImage) {
      setError('Please upload at least one photograph of the vehicle damage.');
      return;
    }

    setSubmitting(true);

    try {
      const payload = {
        ...formData,
        estimated_damage: parseFloat(formData.estimated_damage as any) || 25000,
        vehicle_image_url: uploadedImage,
        photo_attachments: [uploadedFileName || 'vehicle_damage_upload.jpg'],
      };

      const res = await api.createClaim(payload);
      const newClaimId = res.data.claim_id;

      // Navigate to claims list so claimant sees their newly submitted claim
      navigate('/claims', {
        state: {
          justCreatedClaimId: newClaimId,
          message: 'Your claim has been submitted to the Executive SIU Officer for investigation.',
        },
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit claim. Please check the fields.');
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <FilePlus2 className="w-6 h-6 text-blue-600" />
            File a Motor Insurance Claim
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Submit your policy number, vehicle details, damage photograph, and accident description.
          </p>
        </div>
        <button
          onClick={() => navigate('/claims')}
          className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 font-semibold"
        >
          <ArrowLeft className="w-4 h-4" /> Back to My Claims
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 1. Policy Number & Claimant */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
            <User className="w-4 h-4 text-blue-600" />
            1. Insurance Policy & Claimant Information
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Insurance Policy Number <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. POL-HND-2025-8812"
                value={formData.policy_number}
                onChange={(e) => handleChange('policy_number', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono font-bold text-slate-900"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Claimant Full Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="Your full name"
                value={formData.claimant.name}
                onChange={(e) => handleNestedChange('claimant', 'name', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">Phone Number</label>
              <input
                type="text"
                placeholder="+91 98765 43210"
                value={formData.claimant.phone}
                onChange={(e) => handleNestedChange('claimant', 'phone', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">Registered Email</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={formData.claimant.email}
                onChange={(e) => handleNestedChange('claimant', 'email', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* 2. Vehicle Details */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
            <Car className="w-4 h-4 text-blue-600" />
            2. Insured Vehicle Details
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Vehicle Registration Number <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. KA-05-NB-9812"
                value={formData.vehicle.registration}
                onChange={(e) => handleNestedChange('vehicle', 'registration', e.target.value.toUpperCase())}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono font-bold text-slate-900 uppercase"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Make <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Hyundai, Honda, Tata"
                value={formData.vehicle.make}
                onChange={(e) => handleNestedChange('vehicle', 'make', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Model & Variant <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Creta SX, City ZX, Nexon"
                value={formData.vehicle.model}
                onChange={(e) => handleNestedChange('vehicle', 'model', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">Manufacturing Year</label>
              <input
                type="number"
                placeholder="2023"
                value={formData.vehicle.year}
                onChange={(e) => handleNestedChange('vehicle', 'year', parseInt(e.target.value) || 2023)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">Body Type & Color</label>
              <div className="flex gap-2">
                <select
                  value={formData.vehicle.body_type}
                  onChange={(e) => handleNestedChange('vehicle', 'body_type', e.target.value)}
                  className="w-1/2 px-2 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  <option value="Sedan">Sedan</option>
                  <option value="SUV">SUV</option>
                  <option value="Hatchback">Hatchback</option>
                  <option value="MPV">MPV</option>
                </select>
                <input
                  type="text"
                  placeholder="Color (e.g. White)"
                  value={formData.vehicle.color}
                  onChange={(e) => handleNestedChange('vehicle', 'color', e.target.value)}
                  className="w-1/2 px-2 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">VIN / Chassis Number</label>
              <input
                type="text"
                placeholder="Optional"
                value={formData.vehicle.vin}
                onChange={(e) => handleNestedChange('vehicle', 'vin', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>
          </div>
        </div>

        {/* 3. Upload Vehicle Damage Photograph */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <ImageIcon className="w-4 h-4 text-blue-600" />
              3. Vehicle Damage Photograph <span className="text-red-500">*</span>
            </h2>
            <span className="text-[10px] text-slate-500 font-medium">
              YOLO Computer Vision & Component Detection Active
            </span>
          </div>

          <p className="text-xs text-slate-500">
            Upload a clear photo of the damaged area. When received at the office, the Executive Officer will run YOLO neural analysis to verify damage location against your description.
          </p>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileSelect}
          />

          {!uploadedImage ? (
            /* Upload Dropzone */
            <div
              onClick={() => fileInputRef.current?.click()}
              className="p-8 border-2 border-dashed border-slate-300 hover:border-blue-500 rounded-xl bg-slate-50 hover:bg-blue-50/40 transition cursor-pointer flex flex-col items-center justify-center text-center space-y-3"
            >
              <div className="w-12 h-12 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center shadow-xs">
                <UploadCloud className="w-6 h-6" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-800">
                  Click to select or drag and drop your accident photo
                </p>
                <p className="text-[11px] text-slate-500 mt-1">
                  Supports JPG, PNG, HEIC up to 25MB from phone or computer
                </p>
              </div>
              <button
                type="button"
                className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs transition"
              >
                Browse Image File
              </button>
            </div>
          ) : (
            /* Uploaded Image Preview */
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-white space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  Photograph Uploaded Successfully
                </span>
                <button
                  type="button"
                  onClick={handleRemoveImage}
                  className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1 transition"
                >
                  <Trash2 className="w-3.5 h-3.5" /> Remove / Replace
                </button>
              </div>

              <div className="relative rounded-lg overflow-hidden border border-slate-800 bg-black flex items-center justify-center max-h-64">
                <img
                  src={uploadedImage}
                  alt="Vehicle damage preview"
                  className="w-full max-h-64 object-contain object-center"
                />
              </div>

              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 border-t border-slate-800 pt-2">
                <span className="truncate max-w-xs text-slate-200 font-semibold">{uploadedFileName}</span>
                <span>{uploadedFileSize}</span>
              </div>
            </div>
          )}

          {/* Quick Sample Selector */}
          <div className="pt-2 flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-400 text-[11px] font-medium flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-blue-500" />
              Or try a sample damage image:
            </span>
            <button
              type="button"
              onClick={() =>
                handleSelectSample(
                  'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80',
                  'rear_bumper_valence_shunt.jpg'
                )
              }
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium"
            >
              Rear Bumper Shunt
            </button>
            <button
              type="button"
              onClick={() =>
                handleSelectSample(
                  'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80',
                  'front_grille_fender_dent.jpg'
                )
              }
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium"
            >
              Front Grille & Wing
            </button>
            <button
              type="button"
              onClick={() =>
                handleSelectSample(
                  'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80',
                  'side_door_tbone_impact.jpg'
                )
              }
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-[11px] font-medium"
            >
              Side Door T-Bone
            </button>
          </div>
        </div>

        {/* 4. What Happened / Incident Details */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2 border-b border-slate-100 pb-3">
            <Calendar className="w-4 h-4 text-blue-600" />
            4. Accident Details & Narrative (Consumer Side of Story)
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Date of Incident <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                required
                value={formData.incident_date}
                onChange={(e) => handleChange('incident_date', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Approximate Time <span className="text-red-500">*</span>
              </label>
              <input
                type="time"
                required
                value={formData.incident_time}
                onChange={(e) => handleChange('incident_time', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Accident Impact Category</label>
              <select
                value={formData.accident_type}
                onChange={(e) => handleChange('accident_type', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-medium"
              >
                <option value="Rear-End Collision">Rear-End Collision</option>
                <option value="Front-End Collision">Front-End Collision</option>
                <option value="Intersection T-Bone">Intersection T-Bone</option>
                <option value="Side Swipe While Parked">Side Swipe While Parked</option>
                <option value="Front Grille & Sensor Impact">Front Grille & Sensor Impact</option>
                <option value="Single Vehicle Ditch Departure">Single Vehicle Ditch Departure</option>
              </select>
            </div>
          </div>

          <div className="text-xs">
            <label className="block text-slate-700 font-semibold mb-1">
              Accident Location / Street Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Indiranagar 100ft Road, Bengaluru"
              value={formData.incident_location}
              onChange={(e) => handleChange('incident_location', e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="text-xs">
            <label className="block text-slate-700 font-semibold mb-1">
              What Happened? (Your Statement & Damage Description) <span className="text-red-500">*</span>
            </label>
            <textarea
              rows={4}
              required
              placeholder="Describe what occurred, impact direction, and what parts of your car were damaged (e.g. 'I was slowing down at the signal when a trailing vehicle hit my rear bumper...')"
              value={formData.reported_narrative}
              onChange={(e) => handleChange('reported_narrative', e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 leading-relaxed font-mono text-[11px]"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">
                Estimated Repair Amount (INR ₹) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                required
                placeholder="e.g. 35000"
                value={formData.estimated_damage}
                onChange={(e) => handleChange('estimated_damage', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 font-mono font-bold text-slate-900"
              />
            </div>

            <div>
              <label className="block text-slate-600 font-medium mb-1">Other Vehicles Involved (if any)</label>
              <input
                type="text"
                placeholder="e.g. White Swift (KA-04-XX-1234) or None"
                value={formData.third_party}
                onChange={(e) => handleChange('third_party', e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Submit Actions */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/claims')}
            className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-semibold rounded-lg transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg shadow-sm transition disabled:opacity-50 flex items-center gap-2"
          >
            {submitting ? (
              <span>Submitting Claim & Uploading...</span>
            ) : (
              <span>Submit Claim to Insurance Office</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
