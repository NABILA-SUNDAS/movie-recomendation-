const API = "http://127.0.0.1:8000";
const results = document.getElementById("results");
const input = document.getElementById("query");
const btnSearch = document.getElementById("btnSearch");
const btnRandom = document.getElementById("btnRandom");

function card(movie){
  const initials = movie.title.slice(0,1).toUpperCase();
  const el = document.createElement("article");
  el.className = "card";
  el.innerHTML = `
    <div class="thumb">${initials}</div>
    <div class="meta">
      <div class="title">${movie.title}</div>
      <div class="genres">${movie.genres || ""} ${movie.year ? " • " + movie.year : ""}</div>
      <p class="overview">${movie.overview || ""}</p>
      <div><span class="badge">AI Suggests</span></div>
    </div>`;
  return el;
}

function render(list){
  results.innerHTML = "";
  if(!list || list.length === 0){
    results.innerHTML = "<p style='text-align:center'>No results. Try another title (e.g., <strong>Inception</strong>).</p>";
    return;
  }
  list.forEach(m => results.appendChild(card(m)));
}

async function doSearch(){
  const q = input.value.trim();
  if(!q) return;
  const searchRes = await fetch(`${API}/api/recommend?title=${encodeURIComponent(q)}&k=12`);
  if(searchRes.ok){
    const data = await searchRes.json();
    render(data.recommendations);
  }else{
    // fallback to search
    const res = await fetch(`${API}/api/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    render(data.results);
  }
}

async function doRandom(){
  const res = await fetch(`${API}/api/random?k=12`);
  const data = await res.json();
  render(data.results);
}

btnSearch.addEventListener("click", doSearch);
btnRandom.addEventListener("click", doRandom);
input.addEventListener("keydown", (e)=>{ if(e.key==="Enter") doSearch(); });

// Initial load
doRandom();