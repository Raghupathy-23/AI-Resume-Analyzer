import React from "react";
import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import Analyze from './pages/Analyze';
import History from './pages/History';

export default function App(){
 const {loading,user}=useAuth();
 if(loading)return <div className="loading-screen">Preparing your workspace…</div>;
 return <Routes>
  <Route path="/login" element={user?<Navigate to="/" replace/>:<Auth mode="login"/>}/>
  <Route path="/register" element={user?<Navigate to="/" replace/>:<Auth mode="register"/>}/>
  <Route path="/" element={<ProtectedRoute><Layout/></ProtectedRoute>}>
   <Route index element={<Dashboard/>}/>
   <Route path="analyze" element={<Analyze/>}/>
   <Route path="history" element={<History/>}/>
   <Route path="history/:id" element={<History/>}/>
  </Route>
  <Route path="*" element={<Navigate to="/" replace/>}/>
 </Routes>;
}
