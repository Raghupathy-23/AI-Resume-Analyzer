import React from "react";
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { FileSearch, LayoutDashboard, History, LogOut, FileText, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  const signOut = () => { logout(); navigate('/login'); };
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Sparkles size={21}/></div><div><strong>ResumeIQ</strong><small>AI Career Companion</small></div></div>
      <div className="nav-label">WORKSPACE</div>
      <nav>
        <NavLink to="/" end><LayoutDashboard size={18}/>Dashboard</NavLink>
        <NavLink to="/analyze"><FileSearch size={18}/>Analyze Resume</NavLink>
        <NavLink to="/history"><History size={18}/>Analysis History</NavLink>
      </nav>
      <div className="sidebar-bottom"><div className="user-mini"><div className="avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div><div className="user-copy"><strong>{user?.name}</strong><small>{user?.email}</small></div></div><button className="logout" onClick={signOut}><LogOut size={17}/>Sign out</button></div>
    </aside>
    <main className="main-area"><header className="topbar"><div><span className="eyebrow">CAREER INTELLIGENCE</span><h1>AI Resume Analyzer</h1></div><div className="topbar-badge"><span className="online-dot"/>AI assistant ready</div></header><div className="page-content"><Outlet/></div></main>
  </div>;
}
