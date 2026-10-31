import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  switchRoleTest: (role: 'admin' | 'investigator' | 'claimant') => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('claimsight_user');
    const savedToken = localStorage.getItem('claimsight_token');
    if (savedUser && savedToken) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('claimsight_user');
        localStorage.removeItem('claimsight_token');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const res = await api.login({ email, password });
    const { access_token, user } = res.data;
    localStorage.setItem('claimsight_token', access_token);
    localStorage.setItem('claimsight_user', JSON.stringify(user));
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem('claimsight_token');
    localStorage.removeItem('claimsight_user');
    setUser(null);
  };

  const switchRoleTest = async (role: 'admin' | 'investigator' | 'claimant') => {
    if (role === 'admin') {
      await login('admin@claimsight.ai', 'ClaimsightAdmin2026!');
    } else if (role === 'investigator') {
      await login('investigator@claimsight.ai', 'Investigator2026!');
    } else {
      await login('claimant@claimsight.ai', 'Claimant2026!');
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, switchRoleTest }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
