<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<title>Snake — Mobile + Desktop (Profiles & High Scores)</title>
<style>
  :root{
    --bg:#121214; --panel:#212329; --panel2:#2b2e35; --border:#3d4148;
    --text:#e9e9ee; --dim:#b8bdc7; --accent:#42c784; --warn:#ea4b43;
  }
  html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial,"Noto Sans",sans-serif}
  .wrap{max-width:920px;margin:0 auto;padding:16px}
  header{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:12px}
  h1{font-size:22px;margin:0;letter-spacing:1px}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px}
  .row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .grow{flex:1}
  select,input,button{background:var(--panel2);color:var(--text);border:1px solid var(--border);border-radius:10px;padding:10px 12px;font-size:14px}
  button{cursor:pointer}
  button.primary{background:linear-gradient(180deg,#18c08b,#109e74);border:none}
  button.ghost{background:transparent;border:1px dashed var(--border)}
  .muted{color:var(--dim)}
  .grid{display:grid;grid-template-columns:repeat(3,minmax(160px,1fr));gap:12px}
  @media (max-width:720px){.grid{grid-template-columns:1fr}}
  canvas{display:block;background:#16181c;border:1px solid var(--border);border-radius:12px;width:100%;height:auto;touch-action:none}
  .bar{display:flex;justify-content:space-between;align-items:center;margin:10px 2px}
  .kbd{font:12px/1.4 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;background:#111;border:1px solid #333;padding:2px 6px;border-radius:6px;color:#ddd}
  .stats{display:flex;gap:14px;flex-wrap:wrap}
  .stat{background:#191b20;border:1px solid var(--border);border-radius:10px;padding:8px 10px}
  /* On-screen controls */
  .pad{position:fixed;inset:auto 10px 10px auto;display:grid;grid-template-columns:60px 60px 60px;grid-template-rows:60px 60px 60px;gap:6px;opacity:.9}
  .pad .btn{background:#1f2329;border:1px solid #3a3f47;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#dfe6ee;font-weight:700;user-select:none}
  .pad .btn:active{background:#262a30}
  .pad .empty{opacity:0}
  .pad.left{left:10px;right:auto}
  .toggle{display:flex;gap:8px;align-items:center}
  .pill{padding:6px 10px;border-radius:999px;background:#191b20;border:1px solid var(--border);font-size:12px}
  .link{color:#9ad9ff;text-decoration:none}
  .hidden{display:none}
  footer{margin:18px 0 8px;color:var(--dim);font-size:12px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>🐍 Snake — Mobile + Desktop</h1>
    <div class="row">
      <a class="link" href="#" id="showHigh">High Scores</a>
    </div>
  </header>

  <div class="card">
    <div class="row">
      <div class="grow">
        <div class="row" style="gap:8px;align-items:center">
          <label for="profileSelect" class="muted">Profile</label>
          <select id="profileSelect"></select>
          <button id="newProfileBtn" class="ghost">New</button>
          <button id="renameProfileBtn" class="ghost">Rename</button>
          <button id="deleteProfileBtn" class="ghost" title="Delete this profile">Delete</button>
        </div>
      </div>
      <div class="row">
        <button id="playBtn" class="primary">Play</button>
        <button id="pauseBtn">Pause</button>
        <button id="restartBtn">Restart</button>
      </div>
    </div>

    <div class="bar">
      <div class="stats">
        <div class="stat">Score: <b id="score">0</b></div>
        <div class="stat">Best: <b id="best">0</b></div>
        <div class="stat">Games: <b id="games">0</b></div>
        <div class="stat pill" id="wrapState">WRAP: OFF</div>
        <div class="stat pill" id="gridState">GRID: OFF</div>
      </div>
      <div class="muted">Keys: <span class="kbd">Arrows/WASD</span> <span class="kbd">P</span> <span class="kbd">R</span> <span class="kbd">W</span> <span class="kbd">G</span></div>
    </div>

    <canvas id="game" width="672" height="480"></canvas>

    <div class="row" style="margin-top:10px">
      <button id="toggleWrap" class="ghost">Toggle Wrap (W)</button>
      <button id="toggleGrid" class="ghost">Toggle Grid (G)</button>
      <button id="showHigh2" class="ghost">View High Scores</button>
    </div>
  </div>

  <footer>
    Mobile controls: on-screen D-Pad or swipe. Desktop: arrows/WASD. — Built clean & minimal.
  </footer>
</div>

<!-- On-screen D-Pad (appears on touch devices; always shown for demo—toggle below if desired) -->
<div class="pad left" id="padLeft">
  <div class="empty"></div>
  <div class="btn" data-dir="up">▲</div>
  <div class="empty"></div>
  <div class="btn" data-dir="left">◀</div>
  <div class="empty"></div>
  <div class="btn" data-dir="right">▶</div>
  <div class="empty"></div>
  <div class="btn" data-dir="down">▼</div>
  <div class="empty"></div>
</div>

<!-- Modals -->
<div id="highModal" class="hidden">
  <div class="wrap">
    <div class="card">
      <h2 style="margin:4px 0 12px">🏆 High Scores</h2>
      <div id="highList"></div>
      <div class="row" style="margin-top:12px">
        <button id="closeHigh" class="primary">Close</button>
        <button id="exportBtn">Export</button>
        <input id="importFile" type="file" accept="application/json" />
      </div>
    </div>
  </div>
</div>

<script>
/** ===============================
 *  Storage: profiles & scores
 *  ================================= */
const LS_KEY = "snake_profiles_v1";
const CUR_KEY = "snake_current_profile_v1";
function loadProfiles(){
  try{ return JSON.parse(localStorage.getItem(LS_KEY) || "[]"); }catch{ return [] }
}
function saveProfiles(p){ localStorage.setItem(LS_KEY, JSON.stringify(p)); }
function getCurrentId(){ return localStorage.getItem(CUR_KEY); }
function setCurrentId(id){ localStorage.setItem(CUR_KEY, id); }

function makeProfile(name){
  const id = "p_"+Math.random().toString(36).slice(2,10);
  const now = new Date().toISOString();
  return { id, name, best:0, games:0, lastScore:0, createdAt:now, updatedAt:now };
}
function upsertProfile(update){
  const arr = loadProfiles();
  const idx = arr.findIndex(p=>p.id===update.id);
  update.updatedAt = new Date().toISOString();
  if(idx>=0) arr[idx]=update; else arr.push(update);
  saveProfiles(arr);
}
function getProfile(id){ return loadProfiles().find(p=>p.id===id)||null; }
function deleteProfile(id){
  const arr = loadProfiles().filter(p=>p.id!==id);
  saveProfiles(arr);
  if(getCurrentId()===id){ const first = arr[0]; setCurrentId(first?first.id:""); }
}
function ensureInitialProfile(){
  let arr = loadProfiles();
  if(arr.length===0){
    const p = makeProfile("Player 1");
    arr=[p]; saveProfiles(arr); setCurrentId(p.id);
  }
  if(!getCurrentId()){ setCurrentId(arr[0].id); }
}
ensureInitialProfile();

/** ===============================
 *  UI elements
 *  ================================= */
const sel = document.getElementById("profileSelect");
const btnNew = document.getElementById("newProfileBtn");
const btnRename = document.getElementById("renameProfileBtn");
const btnDelete = document.getElementById("deleteProfileBtn");
const playBtn = document.getElementById("playBtn");
const pauseBtn = document.getElementById("pauseBtn");
const restartBtn = document.getElementById("restartBtn");
const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const gamesEl = document.getElementById("games");
const wrapState = document.getElementById("wrapState");
const gridState = document.getElementById("gridState");
const toggleWrapBtn = document.getElementById("toggleWrap");
const toggleGridBtn = document.getElementById("toggleGrid");
const showHigh = document.getElementById("showHigh");
const showHigh2 = document.getElementById("showHigh2");
const highModal = document.getElementById("highModal");
const closeHigh = document.getElementById("closeHigh");
const highList = document.getElementById("highList");
const exportBtn = document.getElementById("exportBtn");
const importFile = document.getElementById("importFile");

function refreshProfileSelect(){
  const arr = loadProfiles();
  const cur = getCurrentId();
  sel.innerHTML = "";
  arr.forEach(p=>{
    const o=document.createElement("option");
    o.value=p.id; o.textContent=`${p.name} (best: ${p.best})`;
    if(p.id===cur) o.selected=true;
    sel.appendChild(o);
  });
  updateStats();
}
function updateStats(){
  const p = getProfile(getCurrentId());
  if(!p) return;
  bestEl.textContent = p.best;
  gamesEl.textContent = p.games;
}
refreshProfileSelect();

/** ===============================
 *  Game core (Canvas)
 *  ================================= */
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const TILE = 24;
const GW = 28, GH = 20; // 672x480
const MOVE_MS = 110;

const COLORS = {
  bg: "#121214",
  grid: "#282c34",
  head: "#28c784",
  body: "#1e9e6b",
  food: "#ea4035",
  text: "#e9e9ee",
  overlay: "rgba(0,0,0,0.45)"
};

let state = "menu"; // "menu"|"playing"|"dead"|"paused"
let showGrid = false;
let wrap = false;

let snake = [];
let dir = {x:1,y:0};
let pendingDir = {x:1,y:0};
let food = null;
let score = 0;
let lastTick = 0;
let acc = 0;

function spawnFood(){
  const occ = new Set(snake.map(p=>p.x+","+p.y));
  const free=[];
  for(let x=0;x<GW;x++) for(let y=0;y<GH;y++){
    const k=x+","+y; if(!occ.has(k)) free.push({x,y});
  }
  food = free.length? free[Math.floor(Math.random()*free.length)] : null;
}
function resetGame(){
  snake = [];
  const cx=Math.floor(GW/2), cy=Math.floor(GH/2);
  for(let i=0;i<4;i++) snake.push({x:cx-i,y:cy});
  dir={x:1,y:0}; pendingDir={x:1,y:0}; score=0;
  spawnFood();
  state="playing"; acc=0; lastTick=performance.now();
  scoreEl.textContent = "0";
}
function setDir(nx,ny){
  if(nx===-dir.x && ny===-dir.y) return; // prevent reverse
  pendingDir = {x:nx,y:ny};
}
function step(dt){
  if(state!=="playing") return;
  acc+=dt;
  while(acc>=MOVE_MS){
    acc-=MOVE_MS;
    dir=pendingDir;
    let nx=snake[0].x+dir.x, ny=snake[0].y+dir.y;

    if(wrap){ nx=(nx+GW)%GW; ny=(ny+GH)%GH; }
    else{
      if(nx<0||nx>=GW||ny<0||ny>=GH){ onDead(); return; }
    }
    const head={x:nx,y:ny};
    // self collision
    if(snake.some(p=>p.x===head.x && p.y===head.y)){ onDead(); return; }
    snake.unshift(head);
    if(food && head.x===food.x && head.y===food.y){
      score++; scoreEl.textContent=score;
      spawnFood();
    }else{
      snake.pop();
    }
  }
}
function onDead(){
  state="dead";
  persistScore();
  draw(); // show overlay w/o waiting
}
function persistScore(){
  const id=getCurrentId(); if(!id) return;
  const p=getProfile(id); if(!p) return;
  p.lastScore = score;
  p.games = (p.games||0)+1;
  if(score > (p.best||0)) p.best = score;
  upsertProfile(p);
  updateStats();
}
function togglePause(){
  if(state==="playing"){ state="paused"; }
  else if(state==="paused"){ state="playing"; lastTick=performance.now(); }
}
function renderGrid(){
  ctx.strokeStyle = COLORS.grid;
  ctx.lineWidth = 1;
  for(let x=0;x<=GW;x++){ ctx.beginPath(); ctx.moveTo(x*TILE,0); ctx.lineTo(x*TILE,GH*TILE); ctx.stroke(); }
  for(let y=0;y<=GH;y++){ ctx.beginPath(); ctx.moveTo(0,y*TILE); ctx.lineTo(GW*TILE,y*TILE); ctx.stroke(); }
}
function draw(){
  // bg
  ctx.fillStyle = COLORS.bg; ctx.fillRect(0,0,canvas.width,canvas.height);
  if(showGrid) renderGrid();
  // food
  if(food){
    ctx.fillStyle = COLORS.food;
    roundRect(food.x*TILE+4, food.y*TILE+4, TILE-8, TILE-8, 8, true);
  }
  // snake
  snake.forEach((p,i)=>{
    const color = i===0? COLORS.head : COLORS.body;
    ctx.fillStyle = color;
    roundRect(p.x*TILE+2, p.y*TILE+2, TILE-4, TILE-4, 6, true);
  });

  if(state==="paused" || state==="dead"){
    ctx.fillStyle = COLORS.overlay;
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = COLORS.text;
    ctx.font="28px system-ui, sans-serif";
    ctx.textAlign="center";
    ctx.fillText(state==="paused"?"Paused":"Game Over", canvas.width/2, canvas.height/2-16);
    ctx.font="14px system-ui, sans-serif";
    ctx.fillText("Press R to Restart", canvas.width/2, canvas.height/2+14);
  }
}
function roundRect(x,y,w,h,r,fill){
  const rr = Math.min(r, w/2, h/2);
  ctx.beginPath();
  ctx.moveTo(x+rr,y);
  ctx.arcTo(x+w,y,x+w,y+h,rr);
  ctx.arcTo(x+w,y+h,x,y+h,rr);
  ctx.arcTo(x,y+h,x,y,rr);
  ctx.arcTo(x,y,x+w,y,rr);
  ctx.closePath();
  if(fill) ctx.fill(); else ctx.stroke();
}

function frame(t){
  const dt = t - lastTick; lastTick = t;
  step(dt);
  draw();
  requestAnimationFrame(frame);
}
requestAnimationFrame((t)=>{ lastTick=t; draw(); });

/** ===============================
 *  Input: keyboard, touch, d-pad, swipe
 *  ================================= */
document.addEventListener("keydown",(e)=>{
  if(e.key==="ArrowUp"||e.key==="w") setDir(0,-1);
  else if(e.key==="ArrowDown"||e.key==="s") setDir(0,1);
  else if(e.key==="ArrowLeft"||e.key==="a") setDir(-1,0);
  else if(e.key==="ArrowRight"||e.key==="d") setDir(1,0);
  else if(e.key==="p") togglePause();
  else if(e.key==="r"){ resetGame(); }
  else if(e.key==="g"){ showGrid=!showGrid; gridState.textContent = "GRID: "+(showGrid?"ON":"OFF"); }
  else if(e.key==="w"){ wrap=!wrap; wrapState.textContent = "WRAP: "+(wrap?"ON":"OFF"); }
});

const pad = document.getElementById("padLeft");
pad.addEventListener("touchstart",(e)=>{
  const t = e.target.closest(".btn");
  if(t){ const d=t.getAttribute("data-dir");
    if(d==="up") setDir(0,-1);
    if(d==="down") setDir(0,1);
    if(d==="left") setDir(-1,0);
    if(d==="right") setDir(1,0);
  }
},{passive:true});

// Swipe on canvas
let sx=0, sy=0, swiping=false;
canvas.addEventListener("touchstart",(e)=>{ const t=e.changedTouches[0]; sx=t.clientX; sy=t.clientY; swiping=true; },{passive:true});
canvas.addEventListener("touchmove",(e)=>{},{passive:true});
canvas.addEventListener("touchend",(e)=>{
  if(!swiping) return; swiping=false;
  const t=e.changedTouches[0];
  const dx=t.clientX-sx, dy=t.clientY-sy;
  if(Math.abs(dx)>Math.abs(dy)){
    if(dx>12) setDir(1,0); else if(dx<-12) setDir(-1,0);
  }else{
    if(dy>12) setDir(0,1); else if(dy<-12) setDir(0,-1);
  }
},{passive:true});

/** ===============================
 *  Buttons & UI actions
 *  ================================= */
playBtn.onclick = ()=>{ if(state!=="playing") resetGame(); };
pauseBtn.onclick = ()=> togglePause();
restartBtn.onclick = ()=> resetGame();
toggleWrapBtn.onclick = ()=>{ wrap=!wrap; wrapState.textContent = "WRAP: "+(wrap?"ON":"OFF"); };
toggleGridBtn.onclick = ()=>{ showGrid=!showGrid; gridState.textContent = "GRID: "+(showGrid?"ON":"OFF"); };

btnNew.onclick = ()=>{
  const name = prompt("New profile name?");
  if(!name) return;
  const p = makeProfile(name.trim());
  upsertProfile(p); setCurrentId(p.id); refreshProfileSelect();
};
btnRename.onclick = ()=>{
  const cur = getProfile(getCurrentId()); if(!cur) return;
  const name = prompt("Rename profile:", cur.name);
  if(!name) return;
  cur.name = name.trim(); upsertProfile(cur); refreshProfileSelect();
};
btnDelete.onclick = ()=>{
  const cur = getProfile(getCurrentId()); if(!cur) return;
  if(!confirm(`Delete profile "${cur.name}"? This cannot be undone.`)) return;
  deleteProfile(cur.id); refreshProfileSelect();
};
sel.onchange = ()=>{ setCurrentId(sel.value); refreshProfileSelect(); };

function buildHighList(){
  const arr = loadProfiles().slice().sort((a,b)=> (b.best||0)-(a.best||0));
  const cur = getCurrentId();
  const rows = arr.map((p,i)=>{
    const mark = p.id===cur ? " (current)" : "";
    return `<div class="row" style="justify-content:space-between;border-bottom:1px dashed var(--border);padding:6px 0">
      <div><b>#${i+1}</b> — ${escapeHtml(p.name)}${mark}</div>
      <div class="muted">Best: <b>${p.best||0}</b> · Games: ${p.games||0} · Last: ${p.lastScore||0}</div>
    </div>`;
  }).join("") || `<div class="muted">No profiles yet.</div>`;
  highList.innerHTML = rows;
}
function escapeHtml(s){ return s.replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m])); }

function openHigh(){ buildHighList(); highModal.classList.remove("hidden"); }
function closeHighModal(){ highModal.classList.add("hidden"); }

document.getElementById("showHigh").onclick=openHigh;
document.getElementById("showHigh2").onclick=openHigh;
closeHigh.onclick=closeHighModal;

// Export / Import
exportBtn.onclick = ()=>{
  const data = localStorage.getItem(LS_KEY) || "[]";
  const blob = new Blob([data],{type:"application/json"});
  const a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="snake-profiles.json";
  a.click();
};
importFile.onchange = (e)=>{
  const file=e.target.files[0]; if(!file) return;
  const reader=new FileReader();
  reader.onload=()=>{
    try{
      const arr=JSON.parse(reader.result);
      if(Array.isArray(arr)){ saveProfiles(arr); refreshProfileSelect(); alert("Imported profiles."); }
      else alert("Invalid file.");
    }catch{ alert("Invalid JSON."); }
  };
  reader.readAsText(file);
};

/** ===============================
 *  Initial UI state sync
 *  ================================= */
wrapState.textContent = "WRAP: OFF";
gridState.textContent = "GRID: OFF";
scoreEl.textContent = "0";
updateStats();

/** ===============================
 *  Resize handling (keep crisp pixels)
 *  ================================= */
function fitCanvas(){
  // Canvas has fixed internal resolution; CSS scales responsively via width:100%
  // Nothing needed here for now; kept for future DPR adjustments.
}
window.addEventListener("resize", fitCanvas);
fitCanvas();
</script>
</body>
</html>
