import React from "react";
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { FileText, ArrowUpRight, Search, LoaderCircle } from 'lucide-react';
import api from '../services/api';
import Results from './Results';

export default function History(){
 const {id}=useParams();if(id)return <Results/>;
 const [items,setItems]=useState([]);const [query,setQuery]=useState('');const [loading,setLoading]=useState(true);const [error,setError]=useState('');
 useEffect(()=>{api.get('/analyses').then(r=>setItems(r.data)).catch(e=>setError(e.response?.data?.detail||'Could not load history.')).finally(()=>setLoading(false));},[]);
 const filtered=items.filter(x=>`analysis ${x.id} ${x.match_score}`.toLowerCase().includes(query.toLowerCase()));
 return <div className="stack-xl"><div className="page-intro"><span className="eyebrow">YOUR WORKSPACE</span><h2>Analysis history</h2><p className="muted">Revisit your previous resume comparisons and recommendations.</p></div><section className="panel"><div className="history-toolbar"><div className="searchbox"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search analyses…"/></div><span className="muted small-text">{filtered.length} {filtered.length===1?'record':'records'}</span></div>{error&&<div className="alert">{error}</div>}{loading?<div className="empty-state"><LoaderCircle className="spin"/> Loading history…</div>:filtered.length===0?<div className="empty-state"><div className="empty-icon"><FileText/></div><b>{items.length?'No matching records':'No analyses yet'}</b><p>{items.length?'Try another search.':'Your completed resume analyses will appear here.'}</p><Link className="btn secondary" to="/analyze">Start an analysis</Link></div>:<div className="table-wrap"><table className="history-table"><thead><tr><th>ANALYSIS</th><th>MATCH SCORE</th><th>DATE</th><th></th></tr></thead><tbody>{filtered.map(x=><tr key={x.id}><td><div className="table-file"><span className="table-file-icon"><FileText size={17}/></span><span><b>Resume analysis #{x.id}</b><small>Saved analysis report</small></span></div></td><td><span className="score-pill">{x.match_score}%</span></td><td className="date-cell">{new Date(x.created_at).toLocaleDateString()}</td><td><Link className="icon-link" to={`/history/${x.id}`} aria-label={`View analysis ${x.id}`}><ArrowUpRight size={17}/></Link></td></tr>)}</tbody></table></div>}</section></div>;
}
