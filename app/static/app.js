const state = { tasks: [], notes: JSON.parse(localStorage.getItem('devdesk_notes') || '[]') };
const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, { headers: {'Content-Type':'application/json'}, ...options });
  if (!response.ok) throw new Error((await response.json()).detail || 'Request failed');
  return response.status === 204 ? null : response.json();
}

function renderTasks(targetId, items = state.tasks) {
  const target = $(targetId);
  if (!items.length) { target.innerHTML = '<div class="empty">No tasks yet. Create one to get started.</div>'; return; }
  target.innerHTML = items.map(t => `<div class="task"><input type="checkbox" ${t.completed ? 'checked':''} onchange="toggleTask(${t.id},this.checked)"><div class="task-main"><div class="task-title ${t.completed?'done':''}">${escapeHtml(t.title)}</div>${t.description?`<div class="task-desc">${escapeHtml(t.description)}</div>`:''}</div><div class="task-actions"><button class="icon" onclick="editTask(${t.id})">✎</button><button class="icon" onclick="removeTask(${t.id})">×</button></div></div>`).join('');
}

function escapeHtml(value){return String(value).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function updateStats(){ $('total-count').textContent=state.tasks.length; $('done-count').textContent=state.tasks.filter(t=>t.completed).length; $('todo-count').textContent=state.tasks.filter(t=>!t.completed).length; $('note-count').textContent=state.notes.length; }
async function loadTasks(){ state.tasks=await api('/tasks'); renderTasks('all-tasks'); renderTasks('recent-tasks',state.tasks.slice(0,5)); updateStats(); }
async function toggleTask(id, completed){await api(`/tasks/${id}`,{method:'PATCH',body:JSON.stringify({completed})});await loadTasks();}
async function removeTask(id){if(confirm('Delete this task?')){await api(`/tasks/${id}`,{method:'DELETE'});await loadTasks();}}
function openTask(id=null){$('task-id').value=id||'';$('dialog-title').textContent=id?'Edit task':'New task';if(id){const t=state.tasks.find(x=>x.id===id);$('task-title').value=t.title;$('task-description').value=t.description||'';}else{$('task-title').value='';$('task-description').value='';}$('task-dialog').showModal();}
function editTask(id){openTask(id)}
async function saveTask(e){e.preventDefault();const id=$('task-id').value;const body={title:$('task-title').value.trim(),description:$('task-description').value.trim()};if(!body.title)return;if(id)await api(`/tasks/${id}`,{method:'PATCH',body:JSON.stringify(body)});else await api('/tasks',{method:'POST',body:JSON.stringify(body)});$('task-dialog').close();await loadTasks();}
function renderNotes(){const target=$('notes-list');target.innerHTML=state.notes.length?state.notes.map((n,i)=>`<article class="note"><strong>${escapeHtml(n.title||'Note')}</strong><div>${escapeHtml(n.body)}</div><small>${new Date(n.createdAt).toLocaleString()} · <button class="icon" onclick="deleteNote(${i})">delete</button></small></article>`).join(''):'<div class="empty">No notes yet.</div>';updateStats();}
function saveNote(){const body=$('quick-note').value.trim();if(!body)return;state.notes.unshift({title:'Quick note',body,createdAt:Date.now()});localStorage.setItem('devdesk_notes',JSON.stringify(state.notes));$('quick-note').value='';renderNotes();}
function deleteNote(i){state.notes.splice(i,1);localStorage.setItem('devdesk_notes',JSON.stringify(state.notes));renderNotes();}
function showView(view){document.querySelectorAll('.view').forEach(v=>v.classList.add('hidden'));$(`${view}-view`).classList.remove('hidden');$('page-title').textContent=view[0].toUpperCase()+view.slice(1);document.querySelectorAll('.nav').forEach(n=>n.classList.toggle('active',n.dataset.view===view));}
document.querySelectorAll('[data-view]').forEach(el=>el.addEventListener('click',()=>showView(el.dataset.view)));
$('new-task').onclick=()=>openTask();$('quick-add').onclick=()=>openTask();$('cancel-task').onclick=()=>$('task-dialog').close();$('task-form').addEventListener('submit',saveTask);$('save-note').onclick=saveNote;$('new-note').onclick=()=>{showView('dashboard');$('quick-note').focus()};$('task-search').oninput=e=>renderTasks('all-tasks',state.tasks.filter(t=>(t.title+' '+t.description).toLowerCase().includes(e.target.value.toLowerCase())));$('theme-btn').onclick=()=>document.body.classList.toggle('light');
loadTasks();renderNotes();
