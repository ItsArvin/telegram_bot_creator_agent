"use client";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, User } from "../lib/api";
import Link from "next/link";
type Bot = { id:string; name:string; description:string|null; status:string; current_version_id:string|null; created_at:string; updated_at:string };
type BotList = { items:Bot[]; total:number };
export default function DashboardPage(){
 const router=useRouter(); const [user,setUser]=useState<User|null>(null); const [bots,setBots]=useState<Bot[]>([]);
 const [name,setName]=useState(""); const [description,setDescription]=useState(""); const [error,setError]=useState(""); const [creating,setCreating]=useState(false);
 async function load(){ try { const me=await api<User>("/auth/me"); setUser(me); try { setBots((await api<BotList>("/bots")).items); } catch(err) { setError(err instanceof Error ? err.message : "Could not load bots"); } } catch(err) { if (err instanceof Error && err.message === "Authentication required") router.replace("/login"); else setError(err instanceof Error ? err.message : "Could not load dashboard"); } }
 useEffect(()=>{ void load(); },[router]);
 async function createBot(e:FormEvent){ e.preventDefault(); setError(""); if(!name.trim()) return; setCreating(true); try { const bot=await api<Bot>("/bots",{method:"POST",body:JSON.stringify({name:name.trim(),description:description.trim()||null})}); setBots(current=>[bot,...current]); setName(""); setDescription(""); } catch(err){ setError(err instanceof Error?err.message:"Could not create bot"); } finally { setCreating(false); } }
 async function deleteBot(id:string){ if(!window.confirm("Delete this bot workspace?")) return; try { await api<void>("/bots/"+id,{method:"DELETE"}); setBots(current=>current.filter(bot=>bot.id!==id)); } catch(err){ setError(err instanceof Error?err.message:"Could not delete bot"); } }
 async function logout(){ await api<void>("/auth/logout",{method:"POST"}); router.replace("/login"); }
 if(!user) return <main className="center-page">{error ? <div className="empty-card"><h2>Could not open dashboard</h2><p className="error">{error}</p><button className="secondary" onClick={()=>window.location.reload()}>Try again</button></div> : <p className="muted">Loading…</p>}</main>;
 return <main className="dashboard"><header className="dashboard-header"><div><p className="eyebrow">AGENTIC BOT BUILDER</p><h1>My Bots</h1><p className="muted">{user.email}</p></div><button className="secondary" onClick={logout}>Sign out</button></header>
 <section className="create-card"><div><span className="badge">NEW WORKSPACE</span><h2>Create a bot</h2><p className="muted">Start a separate workspace for each Telegram bot you want to build.</p></div>
 <form onSubmit={createBot} className="create-form"><label>Bot name<input value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Workshop Registration Bot" maxLength={160}/></label>
 <label>Description <span className="optional">(optional)</span><textarea value={description} onChange={e=>setDescription(e.target.value)} placeholder="What should this bot do?" maxLength={5000}/></label>
 {error && <p className="error">{error}</p>}<button disabled={creating||!name.trim()}>{creating?"Creating…":"Create bot"}</button></form></section>
 <section className="bot-section"><div className="section-heading"><h2>Your workspaces</h2><span className="muted">{bots.length} {bots.length===1?"bot":"bots"}</span></div>
 {bots.length===0 ? <div className="empty-card"><h3>No bots yet</h3><p className="muted">Create your first workspace above. Telegram connection and AI chat will be added in the next phases.</p></div> :
 <div className="bot-grid">{bots.map(bot=><article className="bot-card" key={bot.id}><div className="bot-card-top"><div><h3><Link href={"/dashboard/bots/" + bot.id}>{bot.name}</Link></h3><span className="status">● {bot.status}</span></div><button className="danger" onClick={()=>deleteBot(bot.id)}>Delete</button></div>{bot.description&&<p>{bot.description}</p>}<small>Updated {new Date(bot.updated_at).toLocaleString()}</small></article>)}</div>}</section></main>;
}