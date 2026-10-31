import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { DashboardPage } from './pages/DashboardPage';
import { ClaimsListPage } from './pages/ClaimsListPage';
import { NewClaimPage } from './pages/NewClaimPage';
import { InvestigationWorkspace } from './pages/InvestigationWorkspace';
import { EvidenceCentrePage } from './pages/EvidenceCentrePage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { LoginPage } from './pages/LoginPage';
import { ReportsPage } from './pages/ReportsPage';

const ProtectedLayout: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white text-sm">
        Initializing CLAIMSIGHT SIU Node...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const isClaimant = user?.role === 'claimant';

  return (
    <div className="min-h-screen bg-[#f8fafc] flex flex-col font-sans">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 overflow-x-hidden min-h-[calc(100vh-57px)]">
          <Routes>
            <Route path="/" element={isClaimant ? <ClaimsListPage /> : <DashboardPage />} />
            <Route path="/claims" element={<ClaimsListPage />} />
            <Route
              path="/claims/new"
              element={user?.role === 'claimant' ? <NewClaimPage /> : <Navigate to="/claims" replace />}
            />
            <Route path="/evidence" element={<EvidenceCentrePage />} />
            {!isClaimant && (
              <>
                <Route path="/investigation" element={<InvestigationWorkspace />} />
                <Route path="/investigation/:claimId" element={<InvestigationWorkspace />} />
                <Route path="/reports" element={<ReportsPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </>
            )}
            <Route path="*" element={<Navigate to={isClaimant ? "/claims" : "/"} replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/*" element={<ProtectedLayout />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
