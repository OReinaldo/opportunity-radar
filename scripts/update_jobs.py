import os,json,hashlib,requests
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).resolve().parents[1]/"docs/data.json"; key=os.environ["SERPAPI_KEY"]; d=json.loads(p.read_text()); jobs={j["id"]:j for j in d["jobs"]}
queries=[("Empresarial","operations manager director Vigo Galicia"),("Empresarial","business operations strategy innovation Galicia"),("Empresarial","operations manager Porto Braga Portugal"),("Empresarial","project manager PMO remote Spain"),("Fútbol","football operations club management Galicia"),("Fútbol","futebol operations sports management Porto Braga"),("Fútbol","football business development Portugal")]
terms=["operations","strategy","innovation","transformation","continuous improvement","kpi","cost","project management","pmo","sports management","football operations","club management","sports business","business development"]
for sector,q in queries:
 r=requests.get("https://serpapi.com/search.json",params={"engine":"google_jobs","q":q,"api_key":key,"hl":"es","gl":"es"},timeout=30).json()
 for x in r.get("jobs_results",[]):
  t=x.get("title","");c=x.get("company_name","");u=x.get("share_link","")
  txt=(t+" "+c+" "+x.get("description","")).lower()
  if not(t and c and u) or any(z in txt for z in ["junior","trainee","intern","becario"]): continue
  score=min(99,45+sum(4 for z in terms if z in txt)+(12 if any(z in txt for z in ["director","head","manager","responsable","gerente","gestor"]) else 0))
  if score<58: continue
  jid=hashlib.sha1((t+c+u.split("?")[0]).encode()).hexdigest()[:16]
  jobs[jid]={"id":jid,"title":t,"company":c,"location":x.get("location","No indicada"),"mode":"100% remoto" if "remote" in txt or "remoto" in txt else "Presencial","sector":sector,"salary":"No indicado","published":(x.get("detected_extensions") or {}).get("posted_at",""),"url":u,"score":score,"reason":"Coincidencia automática con el perfil objetivo.","keywords":[z.title() for z in terms if z in txt][:12]}
p.write_text(json.dumps({"updated_at":datetime.now(timezone.utc).isoformat(),"jobs":sorted(jobs.values(),key=lambda x:x["score"],reverse=True)[:500]},ensure_ascii=False,indent=2))
