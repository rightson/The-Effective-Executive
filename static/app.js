'use strict';

// ─── Utilities ───────────────────────────────────────────────────────────────

function esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function fmt(dt) {
  if (!dt) return '—';
  const d = new Date(dt);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function fmtMins(m) {
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60), rem = m % 60;
  return rem ? `${h}h ${rem}m` : `${h}h`;
}

// ─── API ─────────────────────────────────────────────────────────────────────

function getCookie(name) {
  const m = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/[.$?*|{}()[\]\\\/+^]/g, '\\$&') + '=([^;]*)'));
  return m ? decodeURIComponent(m[1]) : '';
}

async function apiFetch(path, opts = {}) {
  const headers = Object.assign({}, opts.headers || {});
  if (opts.body !== undefined) headers['Content-Type'] = 'application/json';
  const csrf = getCookie('ee_csrf');
  if (csrf && opts.method && opts.method !== 'GET') headers['X-CSRF-Token'] = csrf;
  const r = await fetch(path, Object.assign({ credentials: 'same-origin' }, opts, { headers }));
  if (r.status === 401 && !path.startsWith('/api/auth/')) {
    auth.requireLogin();
    throw new Error('Not authenticated');
  }
  if (!r.ok) {
    let msg = await r.text();
    try { msg = JSON.parse(msg).detail || msg; } catch (_) {}
    throw new Error(msg);
  }
  if (r.status === 204) return null;
  return r.json();
}

const api = {
  get:  (p)    => apiFetch(p),
  post: (p, b) => apiFetch(p, { method: 'POST',   body: JSON.stringify(b) }),
  put:  (p, b) => apiFetch(p, { method: 'PUT',    body: JSON.stringify(b) }),
  del:  (p)    => apiFetch(p, { method: 'DELETE' }),
};

// ─── Modal ───────────────────────────────────────────────────────────────────

const modal = {
  show(title, html) {
    document.getElementById('modal-content').innerHTML =
      `<div class="modal-title">${esc(title)}</div>${html}`;
    document.getElementById('modal-overlay').classList.remove('hidden');
  },
  hide() { document.getElementById('modal-overlay').classList.add('hidden'); },
};

document.getElementById('modal-close').onclick = () => modal.hide();
document.getElementById('modal-overlay').addEventListener('click', e => {
  if (e.target === document.getElementById('modal-overlay')) modal.hide();
});

// ─── Auth ────────────────────────────────────────────────────────────────────

const auth = {
  user: null,
  members: [],

  async loadMe() {
    try {
      this.user = await api.get('/api/auth/me');
      try { this.members = await api.get('/api/org/members'); } catch (_) { this.members = []; }
      return this.user;
    } catch (_) {
      this.user = null;
      return null;
    }
  },

  requireLogin() {
    this.user = null;
    this.renderLogin();
  },

  renderNav() {
    const el = document.getElementById('nav-user');
    if (!el) return;
    if (!this.user) { el.innerHTML = ''; return; }
    el.innerHTML = `
      <span class="nav-user-name">${esc(this.user.display_name || this.user.email)}</span>
      <button class="btn btn-ghost btn-xs" id="nav-logout">Log out</button>`;
    document.getElementById('nav-logout').onclick = async () => {
      try { await api.post('/api/auth/logout', {}); } catch (_) {}
      auth.user = null;
      auth.renderLogin();
    };
  },

  renderLogin(mode = 'login') {
    document.getElementById('main').innerHTML = `
      <div class="auth-wrap">
        <div class="auth-card">
          <div class="section-title">${mode === 'signup' ? 'Create account' : 'Log in'}</div>
          <div class="section-subtitle">${mode === 'signup' ? 'Start your Drucker journal.' : 'Welcome back.'}</div>
          <form id="auth-form">
            <div class="form-grid cols-1">
              ${mode === 'signup' ? `
                <div class="form-group"><label>Display name</label>
                  <input type="text" name="display_name" placeholder="optional" /></div>` : ''}
              <div class="form-group"><label>Email</label>
                <input type="email" name="email" required autocomplete="email" /></div>
              <div class="form-group"><label>Password</label>
                <input type="password" name="password" required minlength="8" autocomplete="${mode === 'signup' ? 'new-password' : 'current-password'}" /></div>
            </div>
            <div id="auth-error" class="callout callout-warning hidden"></div>
            <div id="google-wrap" class="form-actions" style="justify-content:flex-start">
              <button type="button" class="btn btn-ghost" id="google-login">Continue with Google</button>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-ghost" id="auth-toggle">${mode === 'signup' ? 'Have an account? Log in' : 'New here? Sign up'}</button>
              <button type="submit" class="btn btn-primary">${mode === 'signup' ? 'Sign up' : 'Log in'}</button>
            </div>
          </form>
        </div>
      </div>`;
    this.renderNav();
    document.getElementById('auth-toggle').onclick = () => this.renderLogin(mode === 'signup' ? 'login' : 'signup');
        const googleBtn = document.getElementById('google-login');
    if (googleBtn) googleBtn.onclick = async () => {
      const token = prompt('Paste Google ID token');
      if (!token) return;
      const errBox = document.getElementById('auth-error');
      errBox.classList.add('hidden');
      try {
        await api.post('/api/auth/google', { id_token: token.trim() });
        await auth.loadMe();
        auth.renderNav();
        app.activate('dashboard');
      } catch (err) {
        errBox.textContent = err.message || 'Google login failed';
        errBox.classList.remove('hidden');
      }
    };
document.getElementById('auth-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const body = { email: fd.get('email'), password: fd.get('password') };
      if (mode === 'signup') body.display_name = fd.get('display_name') || '';
      const errBox = document.getElementById('auth-error');
      errBox.classList.add('hidden');
      try {
        await api.post(mode === 'signup' ? '/api/auth/signup' : '/api/auth/login', body);
        await auth.loadMe();
        auth.renderNav();
        app.activate('dashboard');
      } catch (err) {
        errBox.textContent = err.message || 'Failed';
        errBox.classList.remove('hidden');
      }
    };
  },
};

// ─── Dashboard ───────────────────────────────────────────────────────────────

let chartInstance = null;

const dashboard = {
  viewingUserId: null,

  async load() {
    const qs = this.viewingUserId && this.viewingUserId !== auth.user.id
      ? `?user_id=${this.viewingUserId}` : '';
    const d = await api.get('/api/dashboard' + qs);
    this.render(d);
  },

  render(d) {
    const warnClass = (n) => n > 0 ? '' : 'ok';

    const picker = (auth.members && auth.members.length) ? `
      <div class="dashboard-picker">
        <label>Viewing</label>
        <select id="dashboard-user">
          <option value="">My dashboard</option>
          ${auth.members.map(m => `<option value="${m.user_id}" ${this.viewingUserId === m.user_id ? 'selected' : ''}>${esc(m.display_name || m.email)} — ${esc(m.org_name)}</option>`).join('')}
        </select>
      </div>` : '';

    const heading = d.is_self ? 'Dashboard' : `Dashboard — ${esc(d.user.display_name || d.user.email)}`;
    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">${heading}</div>
          <div class="section-subtitle">Drucker's five habits at a glance${d.is_self ? '' : ' (read-only)'}</div>
        </div>
        ${picker}
      </div>

      <div class="stats-grid">
        <div class="stat-card accent-time">
          <div class="card-title">I. Time</div>
          <div class="stat-value">${d.time.total_hours}</div>
          <div class="stat-label">hours logged</div>
          ${d.time.undiagnosed > 0 ? `<div class="stat-sub">${d.time.undiagnosed} entries undiagnosed</div>` : `<div class="stat-sub ok">All entries diagnosed</div>`}
        </div>
        <div class="stat-card accent-contrib">
          <div class="card-title">II. Contributions</div>
          <div class="stat-value">${d.contributions.active}</div>
          <div class="stat-label">active contributions</div>
          <div class="stat-sub ok">${d.contributions.completed} completed</div>
        </div>
        <div class="stat-card accent-priority">
          <div class="card-title">IV. Priorities</div>
          <div class="stat-value">${d.priorities.active}</div>
          <div class="stat-label">active priorities</div>
          ${d.priorities.to_abandon > 0 ? `<div class="stat-sub">${d.priorities.to_abandon} candidates for abandonment</div>` : `<div class="stat-sub ok">No abandonment candidates</div>`}
        </div>
        <div class="stat-card accent-decision">
          <div class="card-title">V. Decisions</div>
          <div class="stat-value">${d.decisions.open}</div>
          <div class="stat-label">open decisions</div>
          <div class="stat-sub ok">${d.decisions.implemented} implemented</div>
        </div>
      </div>

      <div class="dashboard-grid">
        <div class="card">
          <div class="card-title" style="padding:20px 20px 0">Time by Category</div>
          <div class="chart-wrap">
            <canvas id="time-chart"></canvas>
          </div>
        </div>
        <div class="card card-body">
          <div class="card-title">Action Items</div>
          <div id="action-items"></div>
        </div>
      </div>
    `;

    this.renderChart(d.time.by_category);
    this.renderActions(d);
    const sel = document.getElementById('dashboard-user');
    if (sel) sel.onchange = () => {
      dashboard.viewingUserId = sel.value ? parseInt(sel.value) : null;
      dashboard.load();
    };
  },

  renderChart(by_cat) {
    if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
    const canvas = document.getElementById('time-chart');
    if (!canvas || !Object.keys(by_cat).length) {
      if (canvas) canvas.parentElement.innerHTML += '<div class="empty"><div class="empty-sub">No time data yet</div></div>';
      return;
    }

    const colorMap = {
      deep_work: '#4f46e5', meeting: '#2563eb', admin: '#64748b',
      communication: '#0891b2', waste: '#dc2626', uncategorized: '#94a3b8',
    };
    const labels = Object.keys(by_cat);
    const data   = labels.map(k => by_cat[k]);
    const colors = labels.map(k => colorMap[k] || '#94a3b8');

    chartInstance = new Chart(canvas, {
      type: 'doughnut',
      data: { labels: labels.map(l => l.replace(/_/g,' ')), datasets: [{ data, backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 12 } },
          tooltip: { callbacks: { label: (ctx) => ` ${fmtMins(ctx.raw)}` } },
        },
      },
    });
  },

  renderActions(d) {
    const items = [];
    if (d.time.undiagnosed > 0) items.push(`<div class="callout callout-warning">⚠ ${d.time.undiagnosed} time entries awaiting Drucker's three diagnostic questions — <a href="#time" onclick="app.navigate('time')">diagnose now</a></div>`);
    if (d.priorities.to_abandon > 0) items.push(`<div class="callout callout-warning">⚠ ${d.priorities.to_abandon} active priorities flagged for systematic abandonment — <a href="#priorities" onclick="app.navigate('priorities')">review</a></div>`);
    if (d.decisions.open > 0) items.push(`<div class="callout callout-info">ℹ ${d.decisions.open} decisions pending implementation — <a href="#decisions" onclick="app.navigate('decisions')">view decisions</a></div>`);
    if (!items.length) items.push('<div class="callout callout-info">✓ No urgent actions — keep building habits.</div>');
    document.getElementById('action-items').innerHTML = items.join('');
  },
};

// ─── Time Management ─────────────────────────────────────────────────────────

const time = {
  async load() {
    const [entries, analysis] = await Promise.all([
      api.get('/api/time-entries'),
      api.get('/api/time-entries/analysis'),
    ]);
    this.render(entries, analysis);
  },

  render(entries, analysis) {
    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">I. Know Thy Time</div>
          <div class="section-subtitle">Record time immediately — memory deceives. Then diagnose each entry with Drucker's three questions.</div>
        </div>
      </div>

      ${this.renderAnalysis(analysis)}
      ${this.renderAddForm()}
      ${this.renderTable(entries)}
    `;
    document.getElementById('time-add-form').onsubmit = (e) => this.handleAdd(e);
    document.getElementById('time-toggle').onclick = () => {
      const body = document.getElementById('time-form-body');
      const isHidden = body.style.display === 'none';
      body.style.display = isHidden ? '' : 'none';
      document.getElementById('time-toggle').textContent = isHidden ? '−' : '+';
    };
  },

  renderAnalysis(a) {
    if (!a.total_minutes) return '';
    const d = a.diagnosis;
    const totalD = d.total_diagnosed || 1;
    return `
      <div class="analysis-bar">
        <div class="analysis-item"><span class="analysis-value">${fmtMins(a.total_minutes)}</span><span class="analysis-label">total logged</span></div>
        <div class="analysis-item"><span class="analysis-value">${fmtMins(a.consolidated_minutes)}</span><span class="analysis-label">in 90+ min blocks</span></div>
        <div class="analysis-item"><span class="analysis-value">${d.total_diagnosed}</span><span class="analysis-label">entries diagnosed</span></div>
        <div class="analysis-item"><span class="analysis-value">${Math.round(d.worth_doing/totalD*100)}%</span><span class="analysis-label">worth doing</span></div>
        <div class="analysis-item"><span class="analysis-value">${Math.round(d.can_delegate/totalD*100)}%</span><span class="analysis-label">delegatable</span></div>
        <div class="analysis-item"><span class="analysis-value">${Math.round(d.wastes_others/totalD*100)}%</span><span class="analysis-label">waste others' time</span></div>
      </div>`;
  },

  renderAddForm() {
    return `
      <div class="add-panel" id="time-add-panel">
        <div class="add-panel-header">
          <span class="add-panel-title">Log Time Entry</span>
          <button class="add-panel-toggle" id="time-toggle">−</button>
        </div>
        <div id="time-form-body">
          <form id="time-add-form">
            <div class="form-grid cols-3">
              <div class="form-group span-2">
                <label>Activity</label>
                <input type="text" name="activity" required placeholder="What were you doing?" />
              </div>
              <div class="form-group">
                <label>Duration (minutes)</label>
                <input type="number" name="duration_minutes" required min="1" placeholder="e.g. 60" />
              </div>
              <div class="form-group span-3">
                <label>Category</label>
                <select name="category">
                  <option value="deep_work">Deep Work — focused intellectual work</option>
                  <option value="meeting">Meeting — discussions, calls</option>
                  <option value="admin">Admin — operational tasks</option>
                  <option value="communication">Communication — email, messages</option>
                  <option value="waste">Waste — identified as non-value</option>
                  <option value="uncategorized" selected>Uncategorized</option>
                </select>
              </div>
              <div class="form-group span-3">
                <label>Notes</label>
                <input type="text" name="notes" placeholder="Optional context" />
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Log Entry</button>
            </div>
          </form>
        </div>
      </div>`;
  },

  renderTable(entries) {
    if (!entries.length) return `<div class="empty"><div class="empty-icon">⏱</div><div class="empty-text">No time entries yet</div><div class="empty-sub">Log your first entry above. Record immediately — not from memory.</div></div>`;

    const rows = entries.map(e => {
      const diagBadge = e.worth_doing === null
        ? `<span class="badge badge-undiagnosed">Undiagnosed</span>`
        : `<span class="badge badge-diagnosed">Diagnosed</span>`;
      const diagDetail = e.worth_doing !== null ? `
        <div class="diag-cell" style="margin-top:4px">
          <span class="diag-item ${e.worth_doing ? 'diag-yes':'diag-no'}">${e.worth_doing?'✓':'✗'} Worth doing</span>
          <span class="diag-item ${e.can_delegate ? 'diag-yes':'diag-no'}">${e.can_delegate?'✓':'✗'} Can delegate</span>
          <span class="diag-item ${e.wastes_others ? 'diag-yes':'diag-no'}">${e.wastes_others?'△':'✓'} Wastes others</span>
        </div>` : '';
      return `
        <tr>
          <td class="td-muted">${fmt(e.timestamp)}</td>
          <td class="td-wrap">${esc(e.activity)}${e.notes ? `<div class="td-muted">${esc(e.notes)}</div>` : ''}</td>
          <td>${fmtMins(e.duration_minutes)}</td>
          <td><span class="badge badge-${esc(e.category)}">${esc(e.category.replace(/_/g,' '))}</span></td>
          <td>${diagBadge}${diagDetail}</td>
          <td>
            <div class="td-actions">
              ${e.worth_doing === null ? `<button class="btn btn-warning btn-xs" onclick="time.diagnose(${e.id})">Diagnose</button>` : `<button class="btn btn-ghost btn-xs" onclick="time.diagnose(${e.id})">Re-diagnose</button>`}
              <button class="btn btn-ghost btn-xs" onclick="time.delete(${e.id})">Delete</button>
            </div>
          </td>
        </tr>`;
    }).join('');

    return `
      <div class="table-wrap">
        <table>
          <thead><tr><th>Date</th><th>Activity</th><th>Duration</th><th>Category</th><th>Diagnosis</th><th>Actions</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  },

  async handleAdd(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    await api.post('/api/time-entries', {
      activity: fd.get('activity'),
      duration_minutes: parseInt(fd.get('duration_minutes')),
      category: fd.get('category'),
      notes: fd.get('notes'),
    });
    e.target.reset();
    await this.load();
  },

  diagnose(id) {
    modal.show("Drucker's Three Diagnostic Questions", `
      <div class="modal-desc">Answer honestly. These questions eliminate waste faster than any optimisation tool.</div>
      <form id="diag-form">
        <div class="form-grid cols-1" style="gap:16px">
          <div class="form-group">
            <label>1. What happens if this is not done at all?</label>
            <select name="worth_doing" required>
              <option value="">Select…</option>
              <option value="true">Nothing — this activity can be eliminated</option>
              <option value="false">Something important — keep it</option>
            </select>
          </div>
          <div class="form-group">
            <label>2. Could someone else do this equally well or better?</label>
            <select name="can_delegate" required>
              <option value="">Select…</option>
              <option value="true">Yes — delegate this</option>
              <option value="false">No — only I can do this</option>
            </select>
          </div>
          <div class="form-group">
            <label>3. Does this activity waste other people's time?</label>
            <select name="wastes_others" required>
              <option value="">Select…</option>
              <option value="true">Yes — redesign or eliminate</option>
              <option value="false">No — it respects others' time</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Diagnosis</button>
        </div>
      </form>
    `);
    document.getElementById('diag-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.put(`/api/time-entries/${id}`, {
        worth_doing: fd.get('worth_doing') === 'true',
        can_delegate: fd.get('can_delegate') === 'true',
        wastes_others: fd.get('wastes_others') === 'true',
      });
      modal.hide();
      await time.load();
    };
  },

  async delete(id) {
    if (!confirm('Delete this time entry?')) return;
    await api.del(`/api/time-entries/${id}`);
    await this.load();
  },
};

// ─── Contributions ────────────────────────────────────────────────────────────

const contributions = {
  async load() {
    const items = await api.get('/api/contributions');
    this.render(items);
  },

  render(items) {
    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">II. What Can I Contribute?</div>
          <div class="section-subtitle">Before any activity, ask: what observable difference will this make for the organisation? Write it down — if you can't, don't do it.</div>
        </div>
      </div>
      ${this.renderAddForm()}
      ${this.renderTable(items)}
    `;
    document.getElementById('contrib-add-form').onsubmit = (e) => this.handleAdd(e);
    document.getElementById('contrib-toggle').onclick = () => {
      const body = document.getElementById('contrib-form-body');
      const isHidden = body.style.display === 'none';
      body.style.display = isHidden ? '' : 'none';
      document.getElementById('contrib-toggle').textContent = isHidden ? '−' : '+';
    };
  },

  renderAddForm() {
    return `
      <div class="add-panel">
        <div class="add-panel-header">
          <span class="add-panel-title">Log Contribution</span>
          <button class="add-panel-toggle" id="contrib-toggle">−</button>
        </div>
        <div id="contrib-form-body">
          <form id="contrib-add-form">
            <div class="form-grid">
              <div class="form-group span-2">
                <label>Activity / Project</label>
                <input type="text" name="activity" required placeholder="e.g. Quarterly business review presentation" />
              </div>
              <div class="form-group span-2">
                <label>Expected Contribution — what observable external difference will this make?</label>
                <textarea name="expected_outcome" placeholder="e.g. Leadership team aligns on Q3 priorities; decision made by end of meeting"></textarea>
              </div>
              <div class="form-group">
                <label>Contribution Layer</label>
                <select name="layer">
                  <option value="direct_results">Direct Results — revenue, product, output</option>
                  <option value="values">Values — culture, standards, principles</option>
                  <option value="talent">Talent Development — growing people</option>
                </select>
              </div>
              <div class="form-group">
                <label>Status</label>
                <select name="status">
                  <option value="planned">Planned</option>
                  <option value="active">Active</option>
                </select>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Add Contribution</button>
            </div>
          </form>
        </div>
      </div>`;
  },

  renderTable(items) {
    if (!items.length) return `<div class="empty"><div class="empty-icon">🎯</div><div class="empty-text">No contributions logged yet</div><div class="empty-sub">What external result are you here to produce?</div></div>`;

    const rows = items.map(c => `
      <tr>
        <td class="td-wrap"><strong>${esc(c.activity)}</strong>${c.expected_outcome ? `<div class="td-muted" style="margin-top:3px">${esc(c.expected_outcome)}</div>` : ''}</td>
        <td><span class="badge badge-${esc(c.layer)}">${esc(c.layer.replace(/_/g,' '))}</span></td>
        <td><span class="badge badge-${esc(c.status)}">${esc(c.status)}</span></td>
        <td class="td-muted">${fmt(c.created_at)}</td>
        <td>
          <div class="td-actions">
            <button class="btn btn-ghost btn-xs" onclick="contributions.editStatus(${c.id}, '${esc(c.status)}')">Update</button>
            ${c.status !== 'completed' ? `<button class="btn btn-success btn-xs" onclick="contributions.complete(${c.id})">Complete</button>` : ''}
            <button class="btn btn-ghost btn-xs" onclick="contributions.delete(${c.id})">Delete</button>
          </div>
        </td>
      </tr>`).join('');

    return `
      <div class="table-wrap">
        <table>
          <thead><tr><th>Activity & Expected Outcome</th><th>Layer</th><th>Status</th><th>Created</th><th>Actions</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  },

  async handleAdd(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    await api.post('/api/contributions', {
      activity: fd.get('activity'),
      expected_outcome: fd.get('expected_outcome'),
      layer: fd.get('layer'),
      status: fd.get('status'),
    });
    e.target.reset();
    await this.load();
  },

  complete(id) {
    modal.show('Mark Contribution Complete', `
      <div class="modal-desc">What actually happened? Record the real outcome for future reference.</div>
      <form id="complete-form">
        <div class="form-grid cols-1">
          <div class="form-group">
            <label>Actual Outcome</label>
            <textarea name="actual_outcome" placeholder="Describe what external result was produced…" style="min-height:100px"></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-success">Mark Complete</button>
        </div>
      </form>
    `);
    document.getElementById('complete-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.put(`/api/contributions/${id}`, { status: 'completed', actual_outcome: fd.get('actual_outcome') });
      modal.hide();
      await contributions.load();
    };
  },

  editStatus(id, currentStatus) {
    modal.show('Update Contribution', `
      <form id="status-form">
        <div class="form-grid cols-1">
          <div class="form-group">
            <label>Status</label>
            <select name="status">
              <option value="planned" ${currentStatus==='planned'?'selected':''}>Planned</option>
              <option value="active" ${currentStatus==='active'?'selected':''}>Active</option>
              <option value="completed" ${currentStatus==='completed'?'selected':''}>Completed</option>
              <option value="cancelled" ${currentStatus==='cancelled'?'selected':''}>Cancelled</option>
            </select>
          </div>
          <div class="form-group">
            <label>Actual Outcome (optional)</label>
            <textarea name="actual_outcome" placeholder="What was the real result?"></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>
      </form>
    `);
    document.getElementById('status-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const body = { status: fd.get('status') };
      if (fd.get('actual_outcome')) body.actual_outcome = fd.get('actual_outcome');
      await api.put(`/api/contributions/${id}`, body);
      modal.hide();
      await contributions.load();
    };
  },

  async delete(id) {
    if (!confirm('Delete this contribution?')) return;
    await api.del(`/api/contributions/${id}`);
    await this.load();
  },
};

// ─── Strengths ────────────────────────────────────────────────────────────────

const strengths = {
  async load() {
    const items = await api.get('/api/strengths');
    this.render(items);
  },

  render(items) {
    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">III. Build on Strengths</div>
          <div class="section-subtitle">Only ask "what can they do?" — never start with limitations. Make strength productive, weakness irrelevant.</div>
        </div>
        <button class="btn btn-primary" onclick="strengths.showAddModal()">+ Add Strength</button>
      </div>
      ${this.renderGrid(items)}
    `;
  },

  renderGrid(items) {
    if (!items.length) return `<div class="empty"><div class="empty-icon">💪</div><div class="empty-text">No strengths mapped yet</div><div class="empty-sub">Document what you and your team do exceptionally well — with evidence.</div></div>`;

    // Group by owner
    const byOwner = {};
    items.forEach(s => { (byOwner[s.owner] = byOwner[s.owner] || []).push(s); });

    return Object.entries(byOwner).map(([owner, group]) => `
      <div style="margin-bottom:24px">
        <div style="font-size:13px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px">${esc(owner === 'self' ? 'My Strengths' : owner)}</div>
        <div class="strength-grid">
          ${group.map(s => this.renderCard(s)).join('')}
        </div>
      </div>`).join('');
  },

  renderCard(s) {
    return `
      <div class="strength-card">
        <div class="strength-card-header">
          <div class="strength-name">${esc(s.name)}</div>
          <span class="strength-owner">${esc(s.owner)}</span>
        </div>
        ${s.description ? `<div class="strength-desc">${esc(s.description)}</div>` : ''}
        ${s.evidence ? `<div class="strength-evidence"><div class="strength-evidence-label">Evidence</div>${esc(s.evidence)}</div>` : ''}
        <div class="td-actions">
          <button class="btn btn-ghost btn-xs" onclick="strengths.showEditModal(${s.id}, ${esc(JSON.stringify(s))})">Edit</button>
          <button class="btn btn-ghost btn-xs" onclick="strengths.delete(${s.id})">Delete</button>
        </div>
      </div>`;
  },

  showAddModal() {
    modal.show('Add Strength', this.formHtml());
    document.getElementById('strength-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.post('/api/strengths', { name: fd.get('name'), description: fd.get('description'), owner: fd.get('owner'), evidence: fd.get('evidence') });
      modal.hide();
      await strengths.load();
    };
  },

  showEditModal(id, s) {
    modal.show('Edit Strength', this.formHtml(s));
    document.getElementById('strength-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.put(`/api/strengths/${id}`, { name: fd.get('name'), description: fd.get('description'), owner: fd.get('owner'), evidence: fd.get('evidence') });
      modal.hide();
      await strengths.load();
    };
  },

  formHtml(s = {}) {
    return `
      <form id="strength-form">
        <div class="form-grid cols-1">
          <div class="form-group">
            <label>Strength / Capability</label>
            <input type="text" name="name" value="${esc(s.name||'')}" required placeholder="e.g. Structured problem decomposition" />
          </div>
          <div class="form-group">
            <label>Owner (self or team member name)</label>
            <input type="text" name="owner" value="${esc(s.owner||'self')}" placeholder="self" />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea name="description" placeholder="What does this strength enable?">${esc(s.description||'')}</textarea>
          </div>
          <div class="form-group">
            <label>Evidence — concrete examples that confirm this strength</label>
            <textarea name="evidence" placeholder="e.g. Reduced project scope ambiguity by 60% in last engagement">${esc(s.evidence||'')}</textarea>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>
      </form>`;
  },

  async delete(id) {
    if (!confirm('Delete this strength?')) return;
    await api.del(`/api/strengths/${id}`);
    await this.load();
  },
};

// ─── Priorities ───────────────────────────────────────────────────────────────

const priorities = {
  async load() {
    const items = await api.get('/api/priorities');
    this.render(items);
  },

  render(items) {
    const active    = items.filter(p => p.status === 'active');
    const abandoned = items.filter(p => p.status === 'abandoned');
    const done      = items.filter(p => p.status === 'done');
    const reviewNeeded = active.filter(p => p.would_start_today === false);

    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">IV. First Things First</div>
          <div class="section-subtitle">One task at a time. Courage to abandon the past. The question is never what to prioritise — it's what to stop.</div>
        </div>
        <div style="display:flex;gap:8px">
          ${reviewNeeded.length ? `<button class="btn btn-warning" onclick="priorities.abandonmentReview(${JSON.stringify(reviewNeeded.map(p=>p.id))})">⚠ Review ${reviewNeeded.length} Abandonment Candidate${reviewNeeded.length>1?'s':''}</button>` : ''}
          <button class="btn btn-primary" onclick="priorities.showAddModal()">+ Add Priority</button>
        </div>
      </div>
      ${this.renderAddPanel()}
      ${active.length ? this.renderTable(active, 'Active Priorities') : ''}
      ${abandoned.length ? this.renderTable(abandoned, 'Abandoned') : ''}
      ${done.length ? this.renderTable(done, 'Done') : ''}
      ${!items.length ? `<div class="empty"><div class="empty-icon">🎯</div><div class="empty-text">No priorities yet</div><div class="empty-sub">What is the single most important thing you should be doing right now?</div></div>` : ''}
    `;
  },

  renderAddPanel() {
    return `
      <div class="add-panel">
        <div class="add-panel-header">
          <span class="add-panel-title">Add Priority</span>
          <button class="add-panel-toggle" id="priority-toggle">+</button>
        </div>
        <div id="priority-form-body" style="display:none">
          <form id="priority-add-form">
            <div class="form-grid cols-1">
              <div class="form-group">
                <label>Priority</label>
                <input type="text" name="title" required placeholder="What is the one thing you must do?" />
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea name="description" placeholder="Why does this matter now?"></textarea>
              </div>
              <div class="form-group">
                <label>Drucker's Four Criteria — check all that apply</label>
                <div class="checkbox-group">
                  <label class="checkbox-row"><input type="checkbox" name="future_oriented" /> Future-oriented, not rooted in the past</label>
                  <label class="checkbox-row"><input type="checkbox" name="opportunity_not_problem" /> Capitalises on an opportunity, not just fixes a problem</label>
                  <label class="checkbox-row"><input type="checkbox" name="own_direction" /> Sets own direction, doesn't just follow the crowd</label>
                  <label class="checkbox-row"><input type="checkbox" name="high_meaning" /> Aims for something meaningful and significant, not merely safe</label>
                </div>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">Add Priority</button>
            </div>
          </form>
        </div>
      </div>`;
  },

  renderTable(items, title) {
    const rows = items.map(p => {
      const score = [p.future_oriented, p.opportunity_not_problem, p.own_direction, p.high_meaning].filter(Boolean).length;
      const criteria = [
        { key: 'future_oriented', label: 'Future' },
        { key: 'opportunity_not_problem', label: 'Opportunity' },
        { key: 'own_direction', label: 'Own direction' },
        { key: 'high_meaning', label: 'High meaning' },
      ].map(c => `<span class="badge badge-criteria ${p[c.key] ? '' : 'inactive'}">${esc(c.label)}</span>`).join('');

      const todayBadge = p.would_start_today === null ? ''
        : p.would_start_today ? '<span class="badge badge-completed" style="margin-top:4px;display:inline-block">Would start today ✓</span>'
        : '<span class="badge badge-danger" style="margin-top:4px;display:inline-block;background:#fee2e2;color:#b91c1c">Would NOT start today</span>';

      return `
        <tr>
          <td class="td-wrap"><strong>${esc(p.title)}</strong>${p.description ? `<div class="td-muted">${esc(p.description)}</div>` : ''}${todayBadge}</td>
          <td><div class="criteria-badges">${criteria}</div><div style="font-size:11px;color:var(--muted);margin-top:4px">${score}/4 criteria</div></td>
          <td><span class="badge badge-${esc(p.status)}">${esc(p.status)}</span></td>
          <td class="td-muted">${fmt(p.created_at)}</td>
          <td>
            <div class="td-actions">
              <button class="btn btn-ghost btn-xs" onclick="priorities.reviewOne(${p.id})">Review</button>
              ${p.status==='active' ? `<button class="btn btn-success btn-xs" onclick="priorities.setStatus(${p.id},'done')">Done</button>` : ''}
              ${p.status==='active' ? `<button class="btn btn-warning btn-xs" onclick="priorities.setStatus(${p.id},'abandoned')">Abandon</button>` : ''}
              <button class="btn btn-ghost btn-xs" onclick="priorities.delete(${p.id})">Delete</button>
            </div>
          </td>
        </tr>`;
    }).join('');

    return `
      <div style="margin-bottom:20px">
        <div style="font-size:13px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px">${esc(title)}</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Priority</th><th>Drucker Criteria</th><th>Status</th><th>Created</th><th>Actions</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  },

  showAddModal() { /* uses inline panel instead */ },

  reviewOne(id) {
    modal.show("Systematic Abandonment Review", `
      <div class="modal-desc">"If we did not already do this, would we — knowing what we know now — go into it?" — Drucker</div>
      <form id="review-form">
        <div class="form-grid cols-1">
          <div class="form-group">
            <label>Would you start this today, knowing what you know now?</label>
            <select name="answer" required>
              <option value="">Select…</option>
              <option value="true">Yes — continue</option>
              <option value="false">No — candidate for abandonment</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>
      </form>
    `);
    document.getElementById('review-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.put(`/api/priorities/${id}`, { would_start_today: fd.get('answer') === 'true' });
      modal.hide();
      await priorities.load();
    };
  },

  abandonmentReview(ids) {
    // Step through each candidate
    let idx = 0;
    const next = async () => {
      if (idx >= ids.length) { modal.hide(); await priorities.load(); return; }
      const id = ids[idx++];
      const p = await api.get('/api/priorities').then(all => all.find(x => x.id === id));
      modal.show(`Abandonment Review (${idx}/${ids.length})`, `
        <div class="callout callout-warning">⚠ This priority was flagged: "Would NOT start today"</div>
        <div style="font-size:16px;font-weight:700;margin-bottom:16px">${esc(p.title)}</div>
        ${p.description ? `<div class="td-muted" style="margin-bottom:16px">${esc(p.description)}</div>` : ''}
        <div class="modal-desc">Drucker: abandon the past to free up resources for the future. Deciding not to do something is harder than deciding to do it — but more important.</div>
        <div class="form-actions">
          <button class="btn btn-ghost" onclick="priorities.setStatus(${id},'active').then(next)">Keep — it's still worth doing</button>
          <button class="btn btn-warning" onclick="priorities.setStatus(${id},'abandoned').then(next)">Abandon — free this capacity</button>
        </div>
      `);
    };
    next();
  },

  async setStatus(id, status) {
    await api.put(`/api/priorities/${id}`, { status });
    await priorities.load();
  },

  async delete(id) {
    if (!confirm('Delete this priority?')) return;
    await api.del(`/api/priorities/${id}`);
    await this.load();
  },
};

// Wire up priority inline form toggle after render
document.addEventListener('click', (e) => {
  if (e.target.id === 'priority-toggle') {
    const body = document.getElementById('priority-form-body');
    if (!body) return;
    const isHidden = body.style.display === 'none';
    body.style.display = isHidden ? '' : 'none';
    e.target.textContent = isHidden ? '−' : '+';
    if (isHidden) document.getElementById('priority-add-form').onsubmit = (ev) => priorities.handleAdd(ev);
  }
});

priorities.handleAdd = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  await api.post('/api/priorities', {
    title: fd.get('title'),
    description: fd.get('description'),
    future_oriented: fd.get('future_oriented') === 'on',
    opportunity_not_problem: fd.get('opportunity_not_problem') === 'on',
    own_direction: fd.get('own_direction') === 'on',
    high_meaning: fd.get('high_meaning') === 'on',
  });
  e.target.reset();
  await priorities.load();
};

// ─── Decisions ────────────────────────────────────────────────────────────────

const decisions = {
  async load() {
    const items = await api.get('/api/decisions');
    this.render(items);
  },

  render(items) {
    document.getElementById('main').innerHTML = `
      <div class="section-header">
        <div>
          <div class="section-title">V. Effective Decisions</div>
          <div class="section-subtitle">Decisions require dissent, not consensus. Start with what's right — then compromise. Generic problems need rules; unique events need judgement.</div>
        </div>
        <button class="btn btn-primary" onclick="decisions.showAddModal()">+ New Decision</button>
      </div>
      ${this.renderTable(items)}
    `;
  },

  renderTable(items) {
    if (!items.length) return `<div class="empty"><div class="empty-icon">⚖️</div><div class="empty-text">No decisions logged yet</div><div class="empty-sub">Record important decisions using Drucker's five-step framework.</div></div>`;

    const rows = items.map(d => `
      <tr>
        <td class="td-wrap">
          <strong>${esc(d.title)}</strong>
          ${d.assignee ? `<div class="td-muted">Assigned to: ${esc(d.assignee)}</div>` : ''}
          ${d.has_dissent ? '<span class="dissent-badge" style="margin-top:4px;display:inline-flex">♟ Dissent generated</span>' : ''}
        </td>
        <td><span class="badge badge-${esc(d.problem_type)}">${esc(d.problem_type)}</span></td>
        <td><span class="badge badge-${esc(d.status)}">${esc(d.status)}</span></td>
        <td class="td-muted">${fmt(d.created_at)}</td>
        <td>
          <div class="td-actions">
            <button class="btn btn-ghost btn-xs" onclick="decisions.showDetail(${d.id})">View</button>
            <button class="btn btn-ghost btn-xs" onclick="decisions.showUpdateModal(${d.id}, '${esc(d.status)}')">Update</button>
            <button class="btn btn-ghost btn-xs" onclick="decisions.delete(${d.id})">Delete</button>
          </div>
        </td>
      </tr>`).join('');

    return `
      <div class="table-wrap">
        <table>
          <thead><tr><th>Decision</th><th>Type</th><th>Status</th><th>Date</th><th>Actions</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  },

  showAddModal() {
    modal.show('New Decision — Drucker\'s 5-Step Framework', `
      <form id="decision-form">
        <div class="decision-steps">

          <div class="decision-step">
            <div class="step-num">1</div>
            <div class="step-body">
              <div class="step-label">Classify the Problem</div>
              <div class="form-group">
                <label>Is this a generic (recurring) or unique (one-off) problem?</label>
                <select name="problem_type">
                  <option value="generic">Generic — build a rule or principle to handle this class of event</option>
                  <option value="unique">Unique — requires individual judgement; no template fits</option>
                </select>
              </div>
              <div class="form-group" style="margin-top:10px">
                <label>Decision Title</label>
                <input type="text" name="title" required placeholder="e.g. Hiring a VP of Engineering" />
              </div>
            </div>
          </div>

          <div class="decision-step">
            <div class="step-num">2</div>
            <div class="step-body">
              <div class="step-label">Define Boundary Conditions</div>
              <div class="form-group">
                <label>What minimum conditions must the solution satisfy to be valid?</label>
                <textarea name="boundary_conditions" placeholder="e.g. Must not increase headcount beyond 10; must ship within Q2; must be technically reversible"></textarea>
              </div>
            </div>
          </div>

          <div class="decision-step">
            <div class="step-num">3</div>
            <div class="step-body">
              <div class="step-label">What's Right (Before Compromise)</div>
              <div class="form-group">
                <label>What would the fully correct solution look like — ignoring constraints?</label>
                <textarea name="right_answer" placeholder="State the ideal answer first. Compromise comes later."></textarea>
              </div>
              <div class="form-group" style="margin-top:10px">
                <label>Compromise / Adaptation</label>
                <textarea name="compromise" placeholder="What concessions are acceptable? What would make this solution unacceptable?"></textarea>
              </div>
            </div>
          </div>

          <div class="decision-step">
            <div class="step-num">4</div>
            <div class="step-body">
              <div class="step-label">Build in Action</div>
              <div class="form-group">
                <label>Who is responsible for executing this decision?</label>
                <input type="text" name="assignee" placeholder="Name / role" />
              </div>
            </div>
          </div>

          <div class="decision-step">
            <div class="step-num">5</div>
            <div class="step-body">
              <div class="step-label">Build in Feedback</div>
              <div class="form-group">
                <label>How will you verify the decision is producing the expected results?</label>
                <textarea name="feedback_mechanism" placeholder="e.g. Review hire performance at 90 days; measure conversion rate at end of quarter"></textarea>
              </div>
              <div class="form-group" style="margin-top:10px">
                <label class="checkbox-row" style="cursor:pointer">
                  <input type="checkbox" name="has_dissent" />
                  <span>Dissent was deliberately generated — alternatives were seriously considered before reaching this decision</span>
                </label>
              </div>
            </div>
          </div>

        </div>
        <div class="callout callout-info">Drucker: "The first rule of decision making is that one does not make a decision unless there is disagreement."</div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Record Decision</button>
        </div>
      </form>
    `);
    document.getElementById('decision-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      await api.post('/api/decisions', {
        title: fd.get('title'),
        problem_type: fd.get('problem_type'),
        boundary_conditions: fd.get('boundary_conditions'),
        right_answer: fd.get('right_answer'),
        compromise: fd.get('compromise'),
        assignee: fd.get('assignee'),
        feedback_mechanism: fd.get('feedback_mechanism'),
        has_dissent: fd.get('has_dissent') === 'on',
      });
      modal.hide();
      await decisions.load();
    };
  },

  async showDetail(id) {
    const d = await api.get('/api/decisions').then(all => all.find(x => x.id === id));
    modal.show(d.title, `
      <div style="margin-bottom:8px">
        <span class="badge badge-${esc(d.problem_type)}">${esc(d.problem_type)}</span>
        <span class="badge badge-${esc(d.status)}" style="margin-left:6px">${esc(d.status)}</span>
        ${d.has_dissent ? '<span class="dissent-badge" style="margin-left:6px">♟ Dissent generated</span>' : ''}
      </div>
      <div class="decision-detail">
        ${d.boundary_conditions ? `<div class="detail-row"><div class="detail-label">Boundary Conditions</div><div class="detail-value">${esc(d.boundary_conditions)}</div></div>` : ''}
        ${d.right_answer ? `<div class="detail-row"><div class="detail-label">Right Answer (before compromise)</div><div class="detail-value">${esc(d.right_answer)}</div></div>` : ''}
        ${d.compromise ? `<div class="detail-row"><div class="detail-label">Compromise</div><div class="detail-value">${esc(d.compromise)}</div></div>` : ''}
        ${d.assignee ? `<div class="detail-row"><div class="detail-label">Assignee</div><div class="detail-value">${esc(d.assignee)}</div></div>` : ''}
        ${d.feedback_mechanism ? `<div class="detail-row"><div class="detail-label">Feedback Mechanism</div><div class="detail-value">${esc(d.feedback_mechanism)}</div></div>` : ''}
        ${d.outcome ? `<div class="detail-row"><div class="detail-label">Outcome</div><div class="detail-value">${esc(d.outcome)}</div></div>` : ''}
      </div>
      <div class="form-actions">
        <button class="btn btn-ghost" onclick="modal.hide()">Close</button>
        <button class="btn btn-primary" onclick="modal.hide();decisions.showUpdateModal(${d.id},'${esc(d.status)}')">Update Status</button>
      </div>
    `);
  },

  showUpdateModal(id, currentStatus) {
    modal.show('Update Decision', `
      <form id="decision-update-form">
        <div class="form-grid cols-1">
          <div class="form-group">
            <label>Status</label>
            <select name="status">
              <option value="open" ${currentStatus==='open'?'selected':''}>Open</option>
              <option value="implemented" ${currentStatus==='implemented'?'selected':''}>Implemented</option>
              <option value="reviewed" ${currentStatus==='reviewed'?'selected':''}>Reviewed</option>
            </select>
          </div>
          <div class="form-group">
            <label>Outcome (record what actually happened)</label>
            <textarea name="outcome" placeholder="What was the result of this decision?"></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" onclick="modal.hide()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>
      </form>
    `);
    document.getElementById('decision-update-form').onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const body = { status: fd.get('status') };
      if (fd.get('outcome')) body.outcome = fd.get('outcome');
      await api.put(`/api/decisions/${id}`, body);
      modal.hide();
      await decisions.load();
    };
  },

  async delete(id) {
    if (!confirm('Delete this decision?')) return;
    await api.del(`/api/decisions/${id}`);
    await this.load();
  },
};

// ─── Router ───────────────────────────────────────────────────────────────────

const sections = { dashboard, time, contributions, strengths, priorities, decisions };

const app = {
  current: null,

  navigate(section) {
    if (!sections[section]) section = 'dashboard';
    window.location.hash = section;
    this.activate(section);
  },

  async activate(section) {
    if (!sections[section]) section = 'dashboard';
    this.current = section;

    document.querySelectorAll('.nav-link').forEach(a => {
      a.classList.toggle('active', a.dataset.section === section);
    });

    document.getElementById('main').innerHTML = '<div style="padding:48px;text-align:center;color:var(--muted)">Loading…</div>';
    try {
      await sections[section].load();
    } catch (err) {
      document.getElementById('main').innerHTML = `<div class="empty"><div class="empty-icon">⚠</div><div class="empty-text">Failed to load</div><div class="empty-sub">${esc(err.message)}</div></div>`;
    }
  },

  async init() {
    document.querySelectorAll('.nav-link').forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        this.navigate(a.dataset.section);
      });
    });

    const user = await auth.loadMe();
    auth.renderNav();
    if (!user) { auth.renderLogin(); return; }

    const hash = (window.location.hash || '#dashboard').replace('#', '');
    this.activate(hash);

    window.addEventListener('hashchange', () => {
      const s = window.location.hash.replace('#', '');
      if (s !== this.current) this.activate(s);
    });
  },
};

document.addEventListener('DOMContentLoaded', () => app.init());
