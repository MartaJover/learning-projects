# generate_resume.py
# Interactive, cross-filtered resume with colors and hard/soft skill split.

import json
from pathlib import Path
from typing import Optional

# ---------------------------
# 1) Source data
# ---------------------------
def create_data() -> dict:
    projects = [
        {
            "project_name": "Data Migration & Scaling",
            "company": "E&C Consultants",
            "period": "Feb 2020 - May 2021",
            "description": (
                "System migration from legacy to modern data stores. Built Python and SQL ETLs, "
                "automated reporting with VBA and designed scalable architectures."
            ),
            "skills": {"Python": 4, "SQL": 4, "VBA": 3, "ETL": 4, "Data Engineering": 4, "Communication": 4},
            "start_year": 2020,
            "end_year": 2021,
        },
        {
            "project_name": "E-commerce AI Plugins",
            "company": "CleverPy",
            "period": "Apr 2017 - Dec 2017",
            "description": "WordPress plugins for recommenders, churn detectors and customer segmentation.",
            "skills": {"Python": 4, "Machine Learning": 4, "Recommender Systems": 3, "Customer Segmentation": 3},
            "start_year": 2017,
            "end_year": 2017,
        },
        {
            "project_name": "Bus Predictive Engine",
            "company": "Synergica",
            "period": "Jun 2021 - Mar 2022",
            "description": (
                "Predictive engine for Asturias public buses. Scaled to 820 buses, anomaly detection and "
                "algorithm orchestrator for multimodal transport."
            ),
            "skills": {"Python": 5, "Time Series Analysis": 4, "LSTM": 4, "Monitoring": 3, "Algorithm Orchestration": 3},
            "start_year": 2021,
            "end_year": 2022,
        },
        {
            "project_name": "Energy Consumption Forecasting",
            "company": "Synergica",
            "period": "Jun 2021 - Mar 2022",
            "description": "LSTM energy forecasting with MAPE below 2 percent.",
            "skills": {"Python": 5, "LSTM": 4, "Machine Learning": 4, "Forecasting": 4},
            "start_year": 2021,
            "end_year": 2022,
        },
        {
            "project_name": "INTEGRACLOUD Suite",
            "company": "MySphera",
            "period": "Mar 2022 - Present",
            "description": (
                "Suite for real time national indicators and model management. Architected 50 plus data warehouses "
                "and scalable ETL workflows."
            ),
            "skills": {"Data Warehousing": 5, "Real-time Systems": 4, "Python": 4, "ETL": 4, "Database Design": 4, "Strategy": 4},
            "start_year": 2022,
            "end_year": None,  # Present
        },
        {
            "project_name": "LLM Banking System",
            "company": "Agile Impacts",
            "period": "Mar 2023 - Jul 2023",
            "description": "Collaborative LLM system for banking. Reduced memo generation time from months to weeks.",
            "skills": {"Large Language Models": 5, "Python": 4, "Machine Learning": 4, "Banking Analytics": 3, "Leadership": 4},
            "start_year": 2023,
            "end_year": 2023,
        },
        {
            "project_name": "FAITH & vitana.io",
            "company": "Health R&D",
            "period": "Various",
            "description": "Product owner for vitana.io and contributor to FAITH. High trust AI models and cross functional teams.",
            "skills": {"AI Model Development": 5, "Project Management": 4, "Data Strategy": 4, "High trust AI": 5},
            "start_year": 2022,
            "end_year": 2023,
        },
        {
            "project_name": "GATEKEEPER & Frailty Prediction",
            "company": "Activage Ageing Association",
            "period": "Mar 2022 - Jul 2025",
            "description": (
                "Data strategy and governance for Spanish pilots. Semi supervised frailty prediction and FHIR synthetic data generator."
            ),
            "skills": {"Data Strategy": 4, "Governance": 4, "Frailty Prediction": 4, "Semi supervised Learning": 4, "Synthetic Data Generation": 3},
            "start_year": 2022,
            "end_year": 2025,
        },
        {
            "project_name": "AI & Data Consulting",
            "company": "Self employed",
            "period": "Jun 2023 - Present",
            "description": "Mentorships, PoCs and guidance for SMEs on their data journey.",
            "skills": {"Consulting": 5, "Data Strategy": 4, "Mentorship": 4, "Proof of Concept": 4, "Communication": 4},
            "start_year": 2023,
            "end_year": None,  # Present
        },
    ]

    company_skills = {}
    for p in projects:
        comp = p["company"]
        company_skills.setdefault(comp, {})
        for s, v in p["skills"].items():
            company_skills[comp][s] = company_skills[comp].get(s, 0) + int(v)

    companies = [{"company_name": c, "skills": sk} for c, sk in company_skills.items()]
    return {"projects": projects, "companies": companies}


# ---------------------------
# 2) Writers
# ---------------------------
def write_json(data: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_html(out_path: str = "hector_resume.html",
               data: Optional[dict] = None,
               json_filename: str = "hector_resume_skills.json",
               embed_data: bool = True,
               description: str = (
                   "(Data/MLOps) (Scientist/Engineer) with strong math background and end to end delivery focus."
                   "\nCurious, results oriented and a clear communicator."
               )) -> None:
    safe_desc = (description or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    if embed_data and data is not None:
        inline_json_block = (
            '<script id="resume-data" type="application/json">'
            + json.dumps(data, ensure_ascii=False)
            + "</script>"
        )
        loader_js = (
            "function loadData(){"
            "  const el=document.getElementById('resume-data');"
            "  return JSON.parse(el.textContent);"
            "}"
        )
    else:
        inline_json_block = ""
        loader_js = (
            "async function loadData(){"
            "  const res=await fetch('__JSON_FILENAME__',{cache:'no-store'});"
            "  return await res.json();"
            "}"
        )

    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Héctor Chuliá - Interactive Resume</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
<style>
  /* Dark UI with high contrast cards */
  body { background:#0b1220; color:#e5e7eb; }
  a.link { color:#93c5fd; }
  .card { background:#0f172a; border:1px solid #1f2937; border-radius:0.75rem; box-shadow:0 1px 2px rgba(0,0,0,0.35); padding:1rem; }
  .chart-card { min-height:360px; }
  .timeline-card { min-height:260px; }
  .projects-panel { max-height:calc(100vh - 8rem); overflow-y:auto; }
  .muted { color:#94a3b8; }
  .title { font-weight:700; }
  .kpi { font-weight:600; }
  .toolbar button { border:1px solid #334155; padding:0.3rem 0.6rem; border-radius:0.375rem; background:#0b1220; }
</style>
</head>
<body class="text-slate-100">
  <header class="max-w-7xl mx-auto px-4 pt-6 pb-4 text-center">
    <h1 class="text-3xl md:text-4xl font-extrabold">Héctor Chuliá</h1>
    <p class="mt-2 max-w-3xl mx-auto text-sm md:text-base muted">__DESC__</p>
    <div class="mt-3 text-sm space-x-3">
      <a href="https://hchg.xyz" class="link">hchg.xyz</a>
      <span>·</span><a href="mailto:hector.chg.data@gmail.com" class="link">hector.chg.data@gmail.com</a>
      <span>·</span><a href="tel:+34692226668" class="link">(+34)692226668</a>
      <span>·</span><a href="https://gitlab.com/hector.chg" class="link">GitLab</a>
      <span>·</span><a href="https://www.linkedin.com/in/hector-data/" class="link">LinkedIn</a>
    </div>
    <div class="toolbar mt-3">
      <button id="clear-filters">Clear filters</button>
      <span id="filter-pill" class="text-sm muted ml-2"></span>
    </div>
  </header>

  <!-- Two columns: visuals left, text right. Stacks on small screens -->
  <main class="max-w-8xl mx-auto px-4 pb-10">
    <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
      <!-- LEFT -->
      <section class="md:col-span-6 space-y-4 order-1">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="card chart-card"><div id="company-chart" class="w-full h-full"></div></div>
          <div class="card chart-card"><div id="skills-hard-chart" class="w-full h-full"></div></div>
          <div class="card chart-card"><div id="skills-soft-chart" class="w-full h-full"></div></div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div class="card timeline-card lg:col-span-2"><div id="timeline-chart" class="w-full h-full"></div></div>
          <div class="card">
            <h2 class="title text-lg mb-3">Quick Stats</h2>
            <div id="quick-stats" class="text-sm space-y-1"></div>
          </div>
        </div>
      </section>

      <!-- RIGHT -->
      <aside class="md:col-span-6 order-2">
        <div class="card projects-panel md:sticky md:top-4">
          <h2 class="title text-xl mb-3">Projects</h2>
          <div id="projects-list"></div>
        </div>
      </aside>
    </div>
  </main>

  <footer id="contact" class="text-center text-sm muted py-6">
    © 2025 Héctor Chuliá. All rights reserved.
  </footer>

__INLINE_JSON__

<script>
  __LOADER_JS__

  // Strong palettes for contrast on dark cards
  const PALETTE_COMP = ['#3b82f6','#10b981','#f59e0b','#ef4444','#06b6d4','#8b5cf6','#f472b6','#9ca3af','#22c55e','#60a5fa'];
  const PALETTE_HARD = ['#f59e0b'];
  const PALETTE_SOFT = ['#8b5cf6'];
  const PALETTE_TIME = ['#38bdf8'];

  // Plotly dark layout primitives
  const PLOT_FONT = {family:'Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial', color:'#e5e7eb'};
  const AXIS = {tickcolor:'#94a3b8', gridcolor:'#334155', zerolinecolor:'#475569', linecolor:'#475569'};

  const state = { companies:new Set(), skills:new Set(), years:new Set() };

  const SOFT_OVERRIDES = new Set([
    'Communication','Leadership','Strategy','Data Strategy','Project Management','Mentorship',
    'Consulting','Governance','High trust AI','Data Warehousing'
  ]);
  const SOFT_KEYWORDS = ['communication','leadership','strategy','management','mentorship','governance','consult','warehousing'];
  function isSoftSkill(name){
    if (!name) return false;
    if (SOFT_OVERRIDES.has(name)) return true;
    const n = name.toLowerCase();
    return SOFT_KEYWORDS.some(k=>n.includes(k));
  }

  function pill(){
    const c = state.companies.size ? `Companies: ${[...state.companies].join(', ')}` : '';
    const s = state.skills.size ? `Skills: ${[...state.skills].join(', ')}` : '';
    const y = state.years.size ? `Years: ${[...state.years].join(', ')}` : '';
    const parts = [c,s,y].filter(Boolean);
    document.getElementById('filter-pill').textContent = parts.length ? parts.join('  |  ') : 'No filters';
  }

  function applyFilters(projects){
    return projects.filter(p=>{
      if (state.companies.size && !state.companies.has(p.company)) return false;
      if (state.years.size && !state.years.has(parseInt(p.start_year||0))) return false;
      if (state.skills.size){
        const keys = Object.keys(p.skills||{});
        const has = keys.some(k=>state.skills.has(k));
        if (!has) return false;
      }
      return true;
    });
  }

    function aggs(projects){
  const comp = {}, hard = {}, soft = {}, years = {};
  const nowY = new Date().getFullYear();

  function yearRange(p){
    // Prefer explicit fields
    let s = Number(p.start_year);
    let e = p.end_year == null ? nowY : Number(p.end_year);

    // Fallback parse
    if (!Number.isFinite(s) || !Number.isFinite(e)) {
      const period = String(p.period || '');
      const m = period.match(/(19|20)[0-9]{2}/g) || [];
      if (!Number.isFinite(s) && m[0]) s = Number(m[0]);
      if (!Number.isFinite(e) && m[m.length-1]) e = Number(m[m.length-1]);
      if (period.toLowerCase().includes('present')) e = nowY;
    }
    if (!Number.isFinite(s) && Number.isFinite(e)) s = e;
    if (Number.isFinite(s) && !Number.isFinite(e)) e = s;
    if (!Number.isFinite(s) && !Number.isFinite(e)) return [];
    if (e < s) e = s;

    const out = [];
    for (let y = s; y <= e; y++) out.push(y);
    return out;
  }

  projects.forEach(p=>{
    comp[p.company] = (comp[p.company]||0) + 1;
    Object.entries(p.skills||{}).forEach(([k,v])=>{
      const bucket = isSoftSkill(k) ? soft : hard;
      bucket[k] = (bucket[k]||0) + Number(v||0);
    });
    yearRange(p).forEach(y => { years[y] = (years[y]||0) + 1; });
  });
  return {comp, hard, soft, years};
}

  function sortedDesc(obj){ return Object.entries(obj).sort((a,b)=>b[1]-a[1]); }

  function renderProjects(list){
    const container = document.getElementById('projects-list');
    container.innerHTML = list.map(p=>`
      <div class="mb-6">
        <div class="font-semibold text-slate-100">${p.project_name}</div>
        <div class="text-sm muted">${p.company} · ${p.period}</div>
        <div class="mt-1 text-sm text-slate-200">${p.description||''}</div>
      </div>`).join('');
  }

    function renderQuickStats(list){
        const uniqueCompanies = new Set(list.map(p=>p.company));
        const totalSkills = list.reduce((acc,p)=>acc+Object.keys(p.skills||{}).length,0);
        document.getElementById('quick-stats').innerHTML = `
        <div><span class="kpi">${list.length}</span> projects</div>
        <div><span class="kpi">${uniqueCompanies.size}</span> companies</div>
        <div><span class="kpi">${totalSkills}</span> skills (for the)</div>`;
    }

    function barH(names, vals, color, selectedSet){
        const selIdx = names.map((n,i)=>selectedSet.has(n)?i:-1).filter(i=>i>=0);
        const colors = Array(names.length).fill(color);
        return {
            type: 'bar',
            orientation: 'h',
            y: names,
            x: vals.map(v => Number(v) || 0),
            marker: { color: colors, line: { color: 'rgba(255,255,255,0.25)', width: 1 } },
            opacity: 0.95,
            text: vals.map(v => String(v)),
            textposition: 'inside',          // was 'outside'
            insidetextanchor: 'end',
            textfont: { color: '#0f172a' },  // dark text on colored bar
            cliponaxis: false,
            hoverlabel: { bgcolor: '#0f172a', font: { color: '#e5e7eb' } },
            hovertemplate: '%{y}: %{x}<extra></extra>'
        };
    }

    function barV(names, vals, color, selectedSet){
        const selIdx = names.map((n,i)=>selectedSet.has(n)?i:-1).filter(i=>i>=0);
        const colors = Array(names.length).fill(color);
        return {
            type:'bar',x:names,y:vals,
            marker:{ color:colors, line:{ color:'rgba(255,255,255,0.12)', width:1 } },
            selectedpoints:selIdx,
            hoverlabel:{ bgcolor:'#0f172a', font:{color:'#e5e7eb'} },
            hovertemplate:'%{x}: %{y}<extra></extra>'
        };
    }

    function leftMarginFor(names){
        const longest = names.reduce((m,s)=>Math.max(m, (s||'').length), 0);
        // 6 px per char, between 80 and 220 px
        return Math.max(120, Math.min(220, longest * 3));
    }
        
function layouts(){
  const base = {
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)',
    font:{ family:'Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial', color:'#e5e7eb' }
  };
  const AXIS = { tickcolor:'#94a3b8', gridcolor:'#334155', zerolinecolor:'#475569', linecolor:'#475569' };

  return {
    company: Object.assign({}, base, {
      title:'Projects by Company', autosize:true, margin:{t:40,r:20,b:40,l:220}, showlegend:false,
      yaxis:Object.assign({ type:'category', automargin:true }, AXIS),
      xaxis:Object.assign({ type:'linear', rangemode:'tozero', automargin:true }, AXIS)
    }),
    hard: Object.assign({}, base, {
      title:'Hard Skills', autosize:true, margin:{t:40,r:20,b:40,l:220}, showlegend:false,
      yaxis:Object.assign({ type:'category', automargin:true }, AXIS),
      xaxis:Object.assign({ type:'linear', rangemode:'tozero', automargin:true }, AXIS)
    }),
    soft: Object.assign({}, base, {
      title:'Soft Skills', autosize:true, margin:{t:40,r:20,b:40,l:220}, showlegend:false,
      yaxis:Object.assign({ type:'category', automargin:true }, AXIS),
      xaxis:Object.assign({ type:'linear', rangemode:'tozero', automargin:true }, AXIS)
    }),
    time: Object.assign({}, base, {
      title:'Projects Timeline', autosize:true, margin:{t:40,r:20,b:40,l:60}, showlegend:false,
      xaxis:Object.assign({ type:'category' }, AXIS), yaxis:AXIS, bargap:0.25
    })
  };
}

  function heightOf(id,minH){ const el=document.getElementById(id); return Math.max(el.clientHeight||0,minH); }
  function relayoutHeights(){
    Plotly.relayout('company-chart',     {height:heightOf('company-chart',360)});
    Plotly.relayout('skills-hard-chart', {height:heightOf('skills-hard-chart',360)});
    Plotly.relayout('skills-soft-chart', {height:heightOf('skills-soft-chart',360)});
    Plotly.relayout('timeline-chart',    {height:heightOf('timeline-chart',260)});
  }

    function redraw(data, first=false){
        const filtered = applyFilters(data.projects);
        const A = aggs(filtered);

        const comp = sortedDesc(A.comp);
        const compNames = comp.map(d=>d[0]);
        const compVals  = comp.map(d=>d[1]);

        const hard = sortedDesc(A.hard).slice(0,15);
        const hardNames = hard.map(d=>d[0]);
        const hardVals  = hard.map(d=>d[1]);

        const soft = sortedDesc(A.soft).slice(0,15);
        const softNames = soft.map(d=>d[0]);
        const softVals  = soft.map(d=>d[1]);

        const years = Object.keys(A.years).map(y=>parseInt(y,10)).sort((a,b)=>a-b);
        const yearsStr = years.map(String);
        const yearVals = years.map(y=>A.years[y]);

        const L = layouts();

        // dynamic left margins so bars get room
        const mlComp = leftMarginFor(compNames);
        const mlHard = leftMarginFor(hardNames);
        const mlSoft = leftMarginFor(softNames);

        // force linear x range and lock y to your sorted arrays
        const compLayout = Object.assign({}, L.company, {
            margin: Object.assign({}, L.company.margin, { l: mlComp }),
            yaxis: Object.assign({}, L.company.yaxis, { categoryorder:'array', categoryarray: compNames }),
            xaxis: Object.assign({}, L.company.xaxis, { type:'linear', range:[0, Math.max(1, ...compVals)*1.35] }),
            height: heightOf('company-chart', 360)
        });
        const hardLayout = Object.assign({}, L.hard, {
            margin: Object.assign({}, L.hard.margin, { l: mlHard }),
            yaxis: Object.assign({}, L.hard.yaxis, { categoryorder:'array', categoryarray: hardNames }),
            xaxis: Object.assign({}, L.hard.xaxis, { type:'linear', range:[0, Math.max(1, ...hardVals)*1.35] }),
            height: heightOf('skills-hard-chart', 360)
        });
        const softLayout = Object.assign({}, L.soft, {
            margin: Object.assign({}, L.soft.margin, { l: mlSoft }),
            yaxis: Object.assign({}, L.soft.yaxis, { categoryorder:'array', categoryarray: softNames }),
            xaxis: Object.assign({}, L.soft.xaxis, { type:'linear', range:[0, Math.max(1, ...softVals)*1.35] }),
            height: heightOf('skills-soft-chart', 360)
        });
        const timeLayout = Object.assign({}, L.time, { height: heightOf('timeline-chart', 260) });

        const compTrace = barH(compNames, compVals, PALETTE_COMP[0], state.companies);
        const hardTrace = barH(hardNames, hardVals, PALETTE_HARD[0], state.skills);
        const softTrace = barH(softNames, softVals, PALETTE_SOFT[0], state.skills);
        const timeTrace = barV(yearsStr, yearVals, PALETTE_TIME[0], state.years);

        const cfg = { responsive:true, displayModeBar:false };
        if (first){
            Plotly.newPlot('company-chart',     [compTrace], compLayout, cfg);
            Plotly.newPlot('skills-hard-chart', [hardTrace], hardLayout, cfg);
            Plotly.newPlot('skills-soft-chart', [softTrace], softLayout, cfg);
            Plotly.newPlot('timeline-chart',    [timeTrace], timeLayout, cfg);
        } else {
            Plotly.react('company-chart',     [compTrace], compLayout);
            Plotly.react('skills-hard-chart', [hardTrace], hardLayout);
            Plotly.react('skills-soft-chart', [softTrace], softLayout);
            Plotly.react('timeline-chart',    [timeTrace], timeLayout);
        }

        renderProjects(filtered);
        renderQuickStats(filtered);
        pill();
        setTimeout(relayoutHeights, 60);
  }

  function toggle(setObj,key){ if (setObj.has(key)) setObj.delete(key); else setObj.add(key); }

  function attachCrossfilterHandlers(data){
    document.getElementById('clear-filters').addEventListener('click',()=>{
      state.companies.clear(); state.skills.clear(); state.years.clear();
      redraw(data);
    });
    document.getElementById('company-chart').on('plotly_click',ev=>{ toggle(state.companies, ev.points[0].y); redraw(data); });
    document.getElementById('skills-hard-chart').on('plotly_click',ev=>{ toggle(state.skills, ev.points[0].y); redraw(data); });
    document.getElementById('skills-soft-chart').on('plotly_click',ev=>{ toggle(state.skills, ev.points[0].y); redraw(data); });
    document.getElementById('timeline-chart').on('plotly_click',ev=>{ toggle(state.years, parseInt(ev.points[0].x,10)); redraw(data); });
    window.addEventListener('resize', relayoutHeights);
  }

  document.addEventListener('DOMContentLoaded', async ()=>{
    const data = await loadData();
    redraw(data, true);
    attachCrossfilterHandlers(data);
  });
</script>
</body>
</html>
"""

    html = (
        html.replace("__DESC__", safe_desc)
            .replace("__INLINE_JSON__", inline_json_block)
            .replace("__LOADER_JS__", loader_js)
            .replace("__JSON_FILENAME__", json_filename)
    )
    Path(out_path).write_text(html, encoding="utf-8")

# ---------------------------
# 3) Main
# ---------------------------
def main():
    data = create_data()
    json_path = Path("hector_resume_skills_v2.json")
    html_path = Path("hector_resume_v2.html")
    write_json(data, json_path)
    write_html(out_path=str(html_path), data=data, json_filename=json_path.name, embed_data=True)
    print(f"Wrote {json_path} and {html_path}")

if __name__ == "__main__":
    main()
