'use client';
import {useState} from 'react';
const sessions = [
  {name:'Morning sketch club',category:'Creative',time:'Saturday / 10:00',note:'Bring a pencil. Leave with a new perspective.'},
  {name:'The neighborhood table',category:'Community',time:'Sunday / 12:30',note:'A shared lunch and a good conversation.'},
  {name:'Small ideas, big walks',category:'Outdoors',time:'Sunday / 16:00',note:'An easy walk along the river. Everyone welcome.'}
];
export default function Page() {
  const [query,setQuery]=useState('');
  const visible=sessions.filter(s=>(s.name+' '+s.category).toLowerCase().includes(query.toLowerCase()));
  return <main><header><a href="#sessions" className="brand">gather<span> / a little closer</span></a><span>LOCAL PEOPLE. SHARED TIME.</span></header>
    <section className="intro"><p className="eyebrow">THE WEEKEND EDIT</p><h1>Make room<br/>for good company.</h1><p>A few hours, a new face, a different kind of weekend.<br/>Find your next small adventure.</p></section>
    <section id="sessions" aria-labelledby="session-heading"><div className="toolbar"><h2 id="session-heading">Coming together</h2><div><label htmlFor="search">Find a session</label><input id="search" type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Try creative or outdoors"/></div></div>
      <p role="status">{visible.length} sessions found</p><div className="grid">{visible.map((s,i)=><article key={s.name}><span className="number">0{sessions.indexOf(s)+1}</span><p className="tag">{s.category}</p><h3>{s.name}</h3><p>{s.note}</p><p className="time">{s.time}</p></article>)}</div>
      {!visible.length&&<div className="empty"><h3>No sessions match that search.</h3><button onClick={()=>setQuery('')}>Show all sessions</button></div>}
    </section><footer>Good things happen nearby. <span>GATHER / COMMUNITY EDITION</span></footer></main>;
}
