
        const app = {
            pyodide: null,
            editor: null,
            algorithms: [],
            currentAlgo: null,
            mode: null, // 'blitz' or 'pb'
            
            timerInterval: null,
            startTime: null,
            elapsedMs: 0,
            blitzTimeLimitMs: 0,
            blitzQueue: [],
            blitzResults: [],
            customPlaylists: [],
            currentPlaylistId: null,
            activePoolOverride: null,
            
            attempts: [],
            personalBests: {},
            customAlgos: [],

            async api(path, options) {
                const res = await fetch(path, options ? {
                    headers: { 'Content-Type': 'application/json' },
                    ...options
                } : undefined);
                if (!res.ok) {
                    const detail = await res.text().catch(() => '');
                    throw new Error(`API ${path} failed (${res.status}): ${detail}`);
                }
                if (res.status === 204) return null;
                return res.json();
            },

            async migrateLegacyDataIfPresent() {
                const legacyAttempts = localStorage.getItem('algorep_attempts');
                const legacyBests = localStorage.getItem('algorep_personal_bests');
                const legacyCustom = localStorage.getItem('algorep_custom_algorithms');
                const legacyPlaylists = localStorage.getItem('algo_playlists');
                const hasLegacyData = legacyAttempts || legacyBests || legacyCustom || legacyPlaylists;
                if (!hasLegacyData) return;

                try {
                    await this.api('/api/migrate/import-legacy', {
                        method: 'POST',
                        body: JSON.stringify({
                            attempts: JSON.parse(legacyAttempts || '[]'),
                            personal_bests: JSON.parse(legacyBests || '{}'),
                            custom_algorithms: JSON.parse(legacyCustom || '[]'),
                            playlists: JSON.parse(legacyPlaylists || '[]')
                        })
                    });
                    localStorage.removeItem('algorep_attempts');
                    localStorage.removeItem('algorep_personal_bests');
                    localStorage.removeItem('algorep_custom_algorithms');
                    localStorage.removeItem('algo_playlists');
                } catch (e) {
                    // 409 = already migrated previously; anything else, leave localStorage
                    // untouched so we can retry next load.
                    console.warn('Legacy data migration skipped/failed:', e);
                }
            },

            initPyodideWorker() {
                return new Promise((resolve, reject) => {
                    if (this.pyodideWorker) {
                        this.pyodideWorker.terminate();
                    }
                    this.pyodideWorker = new Worker('./worker.js?v=' + Date.now());
                    
                    this.pyodideWorker.onmessage = (e) => {
                        if (e.data.type === 'ready') {
                            resolve();
                        } else if (e.data.type === 'error') {
                            reject(new Error(e.data.error));
                        } else if (e.data.type === 'run_success' || e.data.type === 'run_error') {
                            if (this.pendingRunCallback && this.pendingRunId === e.data.id) {
                                this.pendingRunCallback(e.data);
                                this.pendingRunCallback = null;
                            }
                        }
                    };
                    
                    this.pyodideWorker.onerror = (err) => {
                        console.error('Worker error:', err);
                        if (this.pendingRunCallback) {
                            this.pendingRunCallback({ type: 'run_error', error: 'Worker crashed (possibly Memory Limit Exceeded). Restarting worker...' });
                            this.pendingRunCallback = null;
                        }
                        this.initPyodideWorker();
                    };
                });
            },


            async init() {
                await this.migrateLegacyDataIfPresent();

                const [attempts, personalBests, customAlgos, playlists] = await Promise.all([
                    this.api('/api/attempts'),
                    this.api('/api/personal-bests'),
                    this.api('/api/custom-algorithms'),
                    this.api('/api/playlists')
                ]);
                this.attempts = attempts;
                this.personalBests = personalBests;
                this.customAlgos = customAlgos;
                this.customPlaylists = playlists;

                this.editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
                    mode: "python",
                    theme: "monokai",
                    lineNumbers: true,
                    indentUnit: 4,
                    matchBrackets: true,
                    autoCloseBrackets: true,
                    styleActiveLine: true,
                    viewportMargin: Infinity,
                    extraKeys: {
                        Tab: function(cm) {
                            if (cm.somethingSelected()) cm.indentSelection("add");
                            else cm.replaceSelection("    ", "end");
                        },
                        Backspace: function(cm) {
                            if (cm.somethingSelected()) return CodeMirror.Pass;
                            const cur = cm.getCursor();
                            const line = cm.getLine(cur.line);
                            const before = line.slice(0, cur.ch);
                            if (before.length > 0 && before.trim() === "") {
                                const remove = (before.length % 4 === 0) ? 4 : (before.length % 4);
                                cm.replaceRange("", {line: cur.line, ch: cur.ch - remove}, cur);
                            } else {
                                return CodeMirror.Pass;
                            }
                        }
                    }
                });
                
                document.fonts.ready.then(() => {
                    if (this.editor) this.editor.refresh();
                });

                try {
                    const data = await this.api('/api/algorithms');
                    this.algorithms = [...data, ...this.customAlgos];
                } catch(e) {
                    console.error("Failed to load algorithms from the server.", e);
                    document.getElementById('loading-message').innerText = "Failed to load algorithm bank from the server. Is server.py running?";
                    document.getElementById('loading-message').style.color = "var(--error)";
                    document.getElementById('loading-spinner').style.display = 'none';
                    return;
                }

                const pbSelect = document.getElementById('pb-select');
                pbSelect.innerHTML = this.algorithms.map(a => `<option value="${a.id}">${a.title} (${a.difficulty.toUpperCase()})</option>`).join('');

                try {
                    await this.initPyodideWorker();
                    document.getElementById('loading-overlay').style.display = 'none';
                } catch (err) {
                    console.error(err);
                    document.getElementById('loading-message').innerText = "Failed to load Python. Please check your internet connection and refresh.";
                    document.getElementById('loading-message').style.color = "var(--error)";
                    document.getElementById('loading-spinner').style.display = 'none';
                    return; 
                }
                
                this.updateHomeStats();
                this.showHome();
            },

            hideAllViews() { document.querySelectorAll('.view').forEach(v => v.classList.remove('active')); },
            showView(id) { 
                this.hideAllViews(); 
                document.getElementById(id).classList.add('active'); 
            },
            showHome() {
                this.cleanupPractice();
                this.activePoolOverride = null;
                this.updateHomeStats();
                this.showView('view-home');
                if (this.renderPacingBanner) this.renderPacingBanner();
            },
            
            

            // Playlists System
            getSmartPlaylists() {
                const solvedIds = Object.keys(this.personalBests);
                const unsolved = this.algorithms.filter(a => !solvedIds.includes(a.id));
                const solved = this.algorithms.filter(a => solvedIds.includes(a.id));
                
                // Ordered (category, keyword-list) pairs - first category whose keyword
                // set intersects the algorithm id's underscore-split tokens wins. Order
                // matters: more specific/unique keywords are placed earlier so generic
                // words (e.g. "path", "fast") don't steal entries that belong elsewhere.
                // Verified against all 84 current entries with zero misclassifications
                // and zero unmatched entries - see the topic-map design script used to
                // build this list before porting it here.
                const TOPIC_CATEGORIES = [
                    ['Binary Search', ['bs']],
                    ['BFS & DFS', ['bfs', 'dfs', 'multi', 'source', 'bipartite', 'connected', 'components', 'flood', 'fill']],
                    ['Graphs (Weighted/MST)', ['graph', 'dijkstra', 'bellman', 'warshall', 'kruskal', 'prim', 'topo', 'union', 'tarjan', 'bridges']],
                    ['Trees & Tries', ['tree', 'trie', 'preorder', 'inorder', 'postorder', 'lca', 'bst', 'diameter', 'serialize', 'deserialize']],
                    ['Advanced Data Structures', ['fenwick', 'segtree', 'sparse', 'table']],
                    ['String Algorithms', ['kmp', 'zfunction', 'manacher', 'pattern', 'rabin']],
                    ['Math & Number Theory', ['sieve', 'matrix', 'exponentiation', 'combinatorics', 'modular']],
                    ['Advanced Techniques', ['lifting', 'meet']],
                    ['Linked Lists', ['linked', 'node', 'lists', 'tortoise', 'middle']],
                    ['Stacks, Queues & Monotonic Structures', ['stack', 'deque', 'monotonic', 'rpn', 'parentheses', 'bracket']],
                    ['Intervals', ['interval', 'intervals']],
                    ['Heaps & Top-K', ['heap', 'largest', 'frequent']],
                    ['Sliding Window & Two Pointers', ['window', 'pointers', 'duplicate', 'dutch', 'fast', 'slow']],
                    ['Prefix Sum & Greedy Scans', ['prefix', 'kadane', 'difference']],
                    ['Dynamic Programming', ['dp', 'knapsack', 'lis', 'lcs', 'distance', 'balloons', 'robber', 'stairs', 'path', 'unique']],
                    ['Backtracking', ['backtracking', 'subsets', 'permutations', 'combination', 'queens']]
                ];

                const classifyTopic = (algoId) => {
                    const tokens = new Set(algoId.split('_').slice(2));
                    for (const [category, keywords] of TOPIC_CATEGORIES) {
                        if (keywords.some(k => tokens.has(k))) return category;
                    }
                    return null;
                };

                const topics = {};
                this.algorithms.forEach(a => {
                    const t = classifyTopic(a.id);
                    if (t) {
                        if (!topics[t]) topics[t] = [];
                        topics[t].push(a);
                    }
                });

                const topicPlaylists = Object.keys(topics).map(t => ({
                    id: 'topic_' + t.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase(),
                    name: t,
                    isDynamic: true,
                    algorithms: topics[t].map(a => a.id)
                }));

                return [
                    { id: 'dyn_unsolved', name: 'Unsolved Problems', isDynamic: true, algorithms: unsolved.map(a => a.id) },
                    { id: 'dyn_solved', name: 'Mastered Problems', isDynamic: true, algorithms: solved.map(a => a.id) },
                    ...topicPlaylists
                ];
            },
            
            showPlaylists() {
                this.renderPlaylists();
                this.showView('view-playlists');
            },

            renderPlaylists() {
                const container = document.getElementById('playlists-container');
                const smart = this.getSmartPlaylists();
                const custom = this.customPlaylists;
                
                let html = '<h3 style="color: var(--text-secondary); margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Smart Playlists</h3>';
                html += '<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 2rem;">';
                smart.forEach(p => {
                    html += `<div class="card" style="cursor: pointer; padding: 15px 25px; border: 1px solid var(--border-color); border-radius: 8px; flex: 1; min-width: 250px;" onclick="app.showPlaylistDetail('${p.id}')">
                        <h3 style="margin: 0 0 10px 0;">${p.name}</h3>
                        <span class="badge" style="background: var(--bg-layer-2); color: var(--text-secondary);">${p.algorithms.length} Problems</span>
                    </div>`;
                });
                html += '</div>';

                html += '<h3 style="color: var(--text-secondary); margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Custom Playlists</h3>';
                if(custom.length === 0) {
                    html += `<p style="color: var(--text-secondary);">You haven't created any custom playlists yet.</p>`;
                } else {
                    html += '<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 2rem;">';
                    custom.forEach(p => {
                        html += `<div class="card" style="cursor: pointer; padding: 15px 25px; border: 1px solid var(--border-color); border-radius: 8px; flex: 1; min-width: 250px;" onclick="app.showPlaylistDetail('${p.id}')">
                            <h3 style="margin: 0 0 10px 0;">${p.name}</h3>
                            <span class="badge" style="background: var(--bg-layer-2); color: var(--text-secondary);">${p.algorithms.length} Problems</span>
                        </div>`;
                    });
                    html += '</div>';
                }
                
                container.innerHTML = html;
            },

            showCreatePlaylistModal() {
                const name = prompt("Enter a name for the new playlist:");
                if(!name || !name.trim()) return;
                const newPlaylist = {
                    id: 'custom_' + Date.now(),
                    name: name.trim(),
                    isDynamic: false,
                    algorithms: []
                };
                this.customPlaylists.push(newPlaylist);
                this.saveCustomPlaylists();
                this.renderPlaylists();
                this.showPlaylistDetail(newPlaylist.id);
            },

            saveCustomPlaylists() {
                this.api('/api/playlists', {
                    method: 'PUT',
                    body: JSON.stringify(this.customPlaylists)
                }).catch(e => console.error('Failed to persist playlists:', e));
            },

            showSaveToPlaylistModal() {
                const container = document.getElementById('save-to-playlist-options');
                if (this.customPlaylists.length === 0) {
                    container.innerHTML = '<p style="color: var(--text-secondary); text-align: center;">You have no custom playlists.</p><button class="btn-primary" onclick="app.showCreatePlaylistModal(); document.getElementById(\'modal-save-to-playlist\').style.display=\'none\';">Create Playlist</button>';
                } else {
                    container.innerHTML = this.customPlaylists.map(p => {
                        const hasIt = p.algorithms.includes(this.currentAlgo.id);
                        const btnText = hasIt ? 'Already Added' : 'Add to Playlist';
                        const btnClass = hasIt ? 'btn-secondary' : 'btn-primary';
                        const disabled = hasIt ? 'disabled' : '';
                        return `<div class="card flex-between" style="padding: 10px 15px; margin-bottom: 0;">
                            <span style="font-weight: 600;">${p.name}</span>
                            <button class="${btnClass}" style="padding: 6px 12px; font-size: 0.85rem;" ${disabled} onclick="app.saveToPlaylist('${p.id}')">${btnText}</button>
                        </div>`;
                    }).join('');
                }
                document.getElementById('modal-save-to-playlist').style.display = 'flex';
            },

            saveToPlaylist(playlistId) {
                let p = this.customPlaylists.find(x => x.id === playlistId);
                if (p && !p.algorithms.includes(this.currentAlgo.id)) {
                    p.algorithms.push(this.currentAlgo.id);
                    this.saveCustomPlaylists();
                    document.getElementById('modal-save-to-playlist').style.display = 'none';
                    
                    // Show a tiny non-intrusive notification (re-using the top bar momentarily)
                    const titleEl = document.getElementById('practice-title');
                    const origTitle = titleEl.innerText;
                    titleEl.innerText = `✅ Added to ${p.name}`;
                    titleEl.style.color = 'var(--success)';
                    setTimeout(() => {
                        titleEl.innerText = origTitle;
                        titleEl.style.color = '';
                    }, 2000);
                }
            },

            showPlaylistDetail(id) {
                this.currentPlaylistId = id;
                this.currentPlaylistSnapshot = null;
                const smart = this.getSmartPlaylists();
                let p = smart.find(x => x.id === id) || this.customPlaylists.find(x => x.id === id);
                if(!p) return;
                
                document.getElementById('playlist-detail-title').innerText = p.name;
                document.getElementById('playlist-detail-desc').innerText = p.isDynamic ? "Dynamic smart playlist." : "Custom user playlist.";
                
                if(!p.isDynamic) {
                    document.getElementById('playlist-management-actions').style.display = 'block';
                } else {
                    document.getElementById('playlist-management-actions').style.display = 'none';
                }

                this.renderPlaylistDetailAlgos();
                this.showView('view-playlist-detail');
            },

            renderPlaylistDetailAlgos() {
                const smart = this.getSmartPlaylists();
                let p = smart.find(x => x.id === this.currentPlaylistId) || this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                
                const tbody = document.querySelector('#playlist-algos-table tbody');
                tbody.innerHTML = p.algorithms.map(algoId => {
                    const a = this.algorithms.find(x => x.id === algoId);
                    if(!a) return '';
                    const isMastered = !!this.personalBests[a.id];
                    const statusIcon = isMastered ? '<span class="text-green">✅</span>' : '<span style="color:var(--border-color);">⭕</span>';
                    
                    const practiceBtn = `<button class="btn-primary" style="padding: 4px 8px; font-size: 0.75rem; margin-right: 5px;" onclick="app.startPracticeFromList('${a.id}')">Practice</button>`;
                    const removeBtn = p.isDynamic ? '' : `<button class="btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="app.removeAlgoFromPlaylist('${a.id}')">Remove</button>`;
                    const actionBtn = practiceBtn + removeBtn;
                    
                    return `<tr>
                        <td style="text-align:center;">${statusIcon}</td>
                        <td style="font-weight:600; color:var(--text-primary);">${a.title}</td>
                        <td><span class="badge ${a.difficulty}">${a.difficulty}</span></td>
                        <td>${actionBtn}</td>
                    </tr>`;
                }).join('');
            },

            removeAlgoFromPlaylist(algoId) {
                let p = this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                if(!p) return;
                p.algorithms = p.algorithms.filter(id => id !== algoId);
                this.saveCustomPlaylists();
                this.renderPlaylistDetailAlgos();
            },

            deleteCurrentPlaylist() {
                if(confirm("Delete this custom playlist?")) {
                    this.customPlaylists = this.customPlaylists.filter(x => x.id !== this.currentPlaylistId);
                    this.saveCustomPlaylists();
                    this.showPlaylists();
                }
            },

            showAddAlgoModal() {
                document.getElementById('modal-add-algo').style.display = 'flex';
                this.filterAddAlgo('');
            },

            filterAddAlgo(query) {
                let p = this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                if(!p) return;
                
                let pool = this.activePoolOverride || this.algorithms;
                if(query) {
                    pool = pool.filter(a => a.title.toLowerCase().includes(query.toLowerCase()));
                }
                
                const tbody = document.getElementById('add-algo-tbody');
                tbody.innerHTML = pool.map(a => {
                    const inPlaylist = p.algorithms.includes(a.id);
                    const btn = inPlaylist 
                        ? `<button class="btn-secondary" disabled style="padding: 4px 8px; font-size: 0.75rem;">Added</button>`
                        : `<button class="btn-success" style="padding: 4px 8px; font-size: 0.75rem;" onclick="app.addAlgoToPlaylist('${a.id}')">Add</button>`;
                    return `<tr>
                        <td style="font-weight:600;">${a.title}</td>
                        <td>${btn}</td>
                    </tr>`;
                }).join('');
            },

            addAlgoToPlaylist(algoId) {
                let p = this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                if(!p) return;
                if(!p.algorithms.includes(algoId)) {
                    p.algorithms.push(algoId);
                    this.saveCustomPlaylists();
                    this.renderPlaylistDetailAlgos();
                    this.filterAddAlgo(document.getElementById('add-algo-search').value);
                }
            },

            practicePlaylist(mode) {
                const smart = this.getSmartPlaylists();
                let p = smart.find(x => x.id === this.currentPlaylistId) || this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                if(!p || p.algorithms.length === 0) {
                    alert("This playlist is empty!");
                    return;
                }
                
                // Set the active pool override
                this.activePoolOverride = this.algorithms.filter(a => p.algorithms.includes(a.id));
                this.showModeSelect(mode);
            },

            showProblemList() {
                this.renderProblemList();
                this.showView('view-problems');
            },
            renderProblemList(query = '') {
                const tbody = document.querySelector('#problem-list-table tbody');
                let pool = this.activePoolOverride || this.algorithms;
                if(query) {
                    pool = pool.filter(a => a.title.toLowerCase().includes(query.toLowerCase()) || 
                                          (a.tags && a.tags.join(' ').toLowerCase().includes(query.toLowerCase())));
                }
                
                tbody.innerHTML = pool.map(a => {
                    const isMastered = !!this.personalBests[a.id];
                    const statusIcon = isMastered ? '<span class="text-green" title="Mastered">✅</span>' : '<span style="color:var(--border-color);" title="Unsolved">⭕</span>';
                    const diffBadge = `<span class="badge ${a.difficulty}">${a.difficulty}</span>`;
                    return `<tr>
                        <td style="text-align:center;">${statusIcon}</td>
                        <td style="font-weight:600; color:var(--text-primary);">${a.title}</td>
                        <td>${diffBadge}</td>
                        <td><button class="btn-primary" style="padding: 6px 12px; font-size: 0.85rem;" onclick="app.startPracticeFromList('${a.id}')">Practice</button></td>
                    </tr>`;
                }).join('');
            },
            filterProblemList(val) {
                this.renderProblemList(val);
            },
            startPracticeFromList(id) {
                this.mode = 'pb';
                this.currentAlgo = this.algorithms.find(a => a.id === id);
                
                if (!this.currentPlaylistSnapshot && this.currentPlaylistId) {
                    const smart = this.getSmartPlaylists();
                    let p = smart.find(x => x.id === this.currentPlaylistId) || this.customPlaylists.find(x => x.id === this.currentPlaylistId);
                    if (p) {
                        this.currentPlaylistSnapshot = [...p.algorithms];
                    }
                }

                this.setupPracticeUI();
                this.showView('view-practice');
                setTimeout(() => this.editor.refresh(), 50);
                this.elapsedMs = 0;
                this.startTime = Date.now();
                clearInterval(this.timerInterval);
                this.timerInterval = setInterval(() => this.tickTimer(), 100);
            },

            navigatePlaylist(dir) {
                if (!this.currentPlaylistSnapshot) return;
                
                const algorithms = this.currentPlaylistSnapshot;
                if (!algorithms || algorithms.length === 0) return;
                
                const idx = algorithms.indexOf(this.currentAlgo.id);
                if (idx === -1) return; // Should not happen with snapshot
                
                let nextIdx = idx + dir;
                if (nextIdx < 0) nextIdx = algorithms.length - 1;
                if (nextIdx >= algorithms.length) nextIdx = 0;
                
                this.startPracticeFromList(algorithms[nextIdx]);
            },

            returnFromPB() {
                if (this.currentPlaylistId) {
                    this.showPlaylistDetail(this.currentPlaylistId);
                } else {
                    this.showProblemList();
                }
            },

            showModeSelect(mode) {
                this.mode = mode;
                document.getElementById('mode-title').innerText = mode === 'blitz' ? 'Blitz Mode Setup' : 'Personal Best Setup';
                document.getElementById('blitz-config').style.display = mode === 'blitz' ? 'block' : 'none';
                document.getElementById('pb-config').style.display = mode === 'pb' ? 'block' : 'none';
                this.showView('view-mode-select');
            },
            showHistory() { this.renderHistory(); this.showView('view-history'); },
            clearHistory() {
                if(confirm("Are you sure you want to clear all your solve history and personal bests?")) {
                    this.api('/api/attempts', { method: 'DELETE' }).then(() => {
                        this.attempts = [];
                        this.personalBests = {};
                        this.renderHistory();
                        this.updateHomeStats();
                    }).catch(e => console.error('Failed to clear history:', e));
                }
            },
            showAddAlgo() { this.addTestCaseField(); this.showView('view-add'); },

            updateHomeStats() {
                document.getElementById('stat-attempts').innerText = this.attempts.length;
                const passed = this.attempts.filter(a => a.passed).length;
                const rate = this.attempts.length ? Math.round((passed / this.attempts.length) * 100) : 0;
                document.getElementById('stat-passrate').innerText = `${rate}%`;
                document.getElementById('stat-mastered').innerText = Object.keys(this.personalBests).length;
            },

            shufflePB() {
                if(!this.algorithms.length) return;
                const rand = this.algorithms[Math.floor(Math.random() * this.algorithms.length)];
                document.getElementById('pb-select').value = rand.id;
            },
            
            startPractice(isRetry = false) {
                if(this.mode === 'blitz' && !isRetry) {
                    const mins = parseInt(document.getElementById('blitz-minutes').value) || 10;
                    this.blitzTimeLimitMs = mins * 60 * 1000;
                    const tag = document.getElementById('blitz-tag').value.toLowerCase().trim();
                    
                    let pool = this.activePoolOverride || this.algorithms;
                    if(tag) pool = pool.filter(a => a.tags && a.tags.some(t => t.toLowerCase().includes(tag)) || a.title.toLowerCase().includes(tag));
                    
                    this.blitzQueue = [...pool].sort(() => Math.random() - 0.5);
                    this.blitzResults = [];
                    
                    if(this.blitzQueue.length === 0) {
                        alert("No algorithms match the given tags.");
                        return;
                    }
                    this.elapsedMs = 0; 
                    this.startTime = Date.now();
                } else if(this.mode === 'pb' && !isRetry) {
                    const id = document.getElementById('pb-select').value;
                    this.currentAlgo = this.algorithms.find(a => a.id === id);
                }

                if(this.mode === 'blitz') {
                    if(this.blitzQueue.length === 0) {
                        this.endBlitz();
                        return;
                    }
                    this.currentAlgo = this.blitzQueue.shift();
                }

                this.setupPracticeUI();
                this.showView('view-practice');
                
                setTimeout(() => this.editor.refresh(), 50);
                
                if(this.mode === 'pb') {
                    this.elapsedMs = 0;
                    this.startTime = Date.now();
                }

                clearInterval(this.timerInterval);
                this.timerInterval = setInterval(() => this.tickTimer(), 100);
            },
            
            setupPracticeUI() {
                const a = this.currentAlgo;
                document.getElementById('practice-title').innerText = a.title;
                const badge = document.getElementById('practice-badge');
                badge.innerText = a.difficulty;
                badge.className = `badge ${a.difficulty}`;
                
                document.getElementById('practice-mode-indicator').innerText = this.mode === 'blitz' ? 'Blitz Mode' : 'Practice Session';
                
                if(this.mode === 'blitz') {
                    document.getElementById('btn-skip').style.display = 'inline-block';
                    document.getElementById('btn-give-up').style.display = 'none';
                    document.getElementById('practice-score').innerText = `${this.blitzResults.filter(r=>r.passed).length} Solved`;
                } else {
                    document.getElementById('btn-skip').style.display = 'none';
                    document.getElementById('btn-give-up').style.display = 'inline-block';
                    document.getElementById('practice-score').innerText = '';
                }

                if (this.mode === 'pb' && this.currentPlaylistId) {
                    document.getElementById('practice-btn-prev').style.display = 'inline-block';
                    document.getElementById('practice-btn-next').style.display = 'inline-block';
                    document.getElementById('practice-btn-exit').style.display = 'inline-block';
                    document.getElementById('practice-nav-divider').style.display = 'block';
                    document.getElementById('btn-give-up').style.display = 'none'; // Hide the bottom Give Up button
                } else {
                    document.getElementById('practice-btn-prev').style.display = 'none';
                    document.getElementById('practice-btn-next').style.display = 'none';
                    document.getElementById('practice-btn-exit').style.display = 'none';
                    document.getElementById('practice-nav-divider').style.display = 'none';
                }

                let descHtml = ``;
                if(a.description) {
                    descHtml += `<div style="font-size: 0.95rem; margin-bottom: 20px; color: var(--text-primary); line-height: 1.6;">${a.description}</div>`;
                }
                if(a.inputs_given) {
                    descHtml += `<h4 style="margin: 20px 0 10px 0; color: var(--text-secondary);">Example Inputs:</h4><pre style="background:var(--bg-layer-2);"><code style="color:var(--text-primary);">${this.escapeHtml(a.inputs_given)}</code></pre>`;
                }
                a.test_cases.forEach((tc, i) => {
                    descHtml += `<h4 style="margin: 20px 0 10px 0; color: var(--text-secondary);">Test Case ${i+1} (Internal Eval):</h4><pre><strong>Code:</strong> ${this.escapeHtml(tc.call)}\n<strong>Expected:</strong> ${this.escapeHtml(tc.expected)}</pre>`;
                });
                if(a.tags && a.tags.length) {
                    descHtml += `<div style="margin-top: 2rem; border-top: 1px solid var(--border-color); padding-top: 1rem;"><strong style="color: var(--text-secondary);">Tags:</strong><div style="margin-top: 8px;">${a.tags.map(t => `<span class="badge" style="background:var(--bg-layer-2); color:var(--text-primary); border: 1px solid var(--border-color); margin-right: 6px;">${t}</span>`).join('')}</div></div>`;
                }
                document.getElementById('problem-desc-content').innerHTML = descHtml;

                if (a.solution_code || a.solution_explanation || a.when_to_use) {
                    document.getElementById('insights-section').style.display = 'block';
                    document.getElementById('insights-content').style.display = 'none';
                    document.getElementById('insights-when').innerHTML = a.when_to_use || '<em>No heuristic provided.</em>';
                    document.getElementById('insights-code').innerText = a.solution_code || '# No code provided.';
                    document.getElementById('insights-explain').innerHTML = a.solution_explanation || '<em>No explanation provided.</em>';
                } else {
                    document.getElementById('insights-section').style.display = 'none';
                }

                this.editor.setValue(a.stub);
                document.getElementById('output-panel').style.display = 'none';
                document.getElementById('btn-submit').disabled = true;
                
                const btnRun = document.getElementById('btn-run');
                btnRun.innerText = 'Run Code';
                btnRun.disabled = false;
            },
            
            tickTimer() {
                if(this.mode === 'blitz') {
                    const totalElapsed = Date.now() - this.startTime;
                    const rem = Math.max(0, this.blitzTimeLimitMs - totalElapsed);
                    document.getElementById('practice-timer').innerText = this.formatTime(rem);
                    if(rem === 0) {
                        this.endBlitz();
                    }
                } else {
                    this.elapsedMs = Date.now() - this.startTime;
                    document.getElementById('practice-timer').innerText = this.formatTime(this.elapsedMs);
                }
            },
            
            formatTime(ms) {
                const mins = Math.floor(ms / 60000);
                const secs = Math.floor((ms % 60000) / 1000);
                return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            },

            escapeHtml(unsafe) {
                if (!unsafe) return '';
                return unsafe.toString()
                     .replace(/&/g, "&amp;")
                     .replace(/</g, "&lt;")
                     .replace(/>/g, "&gt;")
                     .replace(/"/g, "&quot;")
                     .replace(/'/g, "&#039;");
            },
            
            cleanupPractice() { clearInterval(this.timerInterval); },

            async runCode() {
                const userCode = this.editor.getValue().replace(/\t/g, '    ');
                const a = this.currentAlgo;
                const panel = document.getElementById('output-panel');
                const content = document.getElementById('output-content');
                const btnRun = document.getElementById('btn-run');
                
                panel.style.display = 'flex';
                content.innerHTML = '<div style="color: var(--text-secondary); display:flex; align-items:center; gap: 10px;"><div class="spinner" style="width:20px;height:20px;border-width:2px;"></div> Executing... <button class="btn-danger" style="padding: 4px 8px; font-size: 0.8rem; margin-left: 10px;" onclick="app.stopCode()">Stop Submission</button></div>';
                document.getElementById('btn-submit').disabled = true;
                btnRun.disabled = true;

                const runId = Date.now();
                this.pendingRunId = runId;
                
                this.runTimeout = setTimeout(() => {
                    if (this.pendingRunId === runId) {
                        if (this.pendingRunCallback) {
                            this.pendingRunCallback({ type: 'run_error', error: 'Time Limit Exceeded (5 seconds). Execution terminated.' });
                            this.pendingRunCallback = null;
                        }
                        this.initPyodideWorker(); // Restart worker
                    }
                }, 5000);

                const resultPromise = new Promise(resolve => {
                    this.pendingRunCallback = resolve;
                });

                this.pyodideWorker.postMessage({
                    id: runId,
                    code: userCode,
                    testCases: JSON.stringify(a.test_cases)
                });

                try {
                    const response = await resultPromise;
                    clearTimeout(this.runTimeout);
                    
                    if (response.type === 'run_error') {
                        content.innerHTML = `<div class="text-red" style="margin-bottom: 1.5rem; background: rgba(239,71,67,0.1); padding: 15px; border-radius: 6px; border: 1px solid rgba(239,71,67,0.2);"><strong>Execution Error:</strong><br><pre style="font-family: var(--font-mono); margin:0; white-space: pre-wrap;">${this.escapeHtml(response.error)}</pre></div>`;
                    } else if (response.type === 'run_success') {
                        const res = JSON.parse(response.result);
                        this.renderOutput(res);
                    }
                } catch(e) {
                    content.innerHTML = `<div class="text-red"><strong>System Error:</strong><br>${this.escapeHtml(e.message)}</div>`;
                } finally {
                    btnRun.disabled = false;
                }
            },
            
            stopCode() {
                if (this.pendingRunCallback) {
                    clearTimeout(this.runTimeout);
                    this.pendingRunCallback({ type: 'run_error', error: 'Execution manually stopped.' });
                    this.pendingRunCallback = null;
                    this.initPyodideWorker();
                }
            },
            
            renderOutput(res) {
                const content = document.getElementById('output-content');
                let html = '';

                if(res.exec_error) {
                    html += `<div class="text-red" style="margin-bottom: 1.5rem; background: rgba(239,71,67,0.1); padding: 15px; border-radius: 6px; border: 1px solid rgba(239,71,67,0.2);">
                        <strong style="display:block; margin-bottom: 8px;">Execution Error:</strong>
                        <pre style="font-family: var(--font-mono); margin:0; white-space: pre-wrap;">${res.exec_error}</pre>
                    </div>`;
                }
                
                if(res.stdout) {
                    html += `<div style="margin-bottom: 1.5rem;">
                        <strong style="color: var(--text-secondary); display:block; margin-bottom: 8px;">stdout:</strong>
                        <pre style="background: var(--bg-base); padding: 12px; border-radius: 6px; border: 1px solid var(--border-color); color: #d4d4d4;">${res.stdout}</pre>
                    </div>`;
                }
                if(res.stderr) {
                    html += `<div style="margin-bottom: 1.5rem;">
                        <strong style="color: var(--error); display:block; margin-bottom: 8px;">stderr:</strong>
                        <pre style="background: rgba(239,71,67,0.1); padding: 12px; border-radius: 6px; border: 1px solid rgba(239,71,67,0.2); color: var(--error);">${res.stderr}</pre>
                    </div>`;
                }

                if(res.results && res.results.length > 0) {
                    let allPass = true;
                    html += `<strong style="color: var(--text-secondary); display:block; margin-bottom: 12px;">Test Cases:</strong>`;
                    res.results.forEach((tc, i) => {
                        const call = this.escapeHtml(this.currentAlgo.test_cases[i].call);
                        if(tc.pass) {
                            html += `<div style="margin-bottom: 10px; padding: 12px 16px; border-radius: 6px; border-left: 4px solid var(--success); background: rgba(44,187,93,0.08);">
                                <span class="text-green" style="font-weight: 600; margin-right: 10px;">✅ Passed</span> <code style="color: #d4d4d4;">${call}</code>
                            </div>`;
                        } else {
                            allPass = false;
                            html += `<div style="margin-bottom: 10px; padding: 12px 16px; border-radius: 6px; border-left: 4px solid var(--error); background: rgba(239,71,67,0.08);">
                                <div style="margin-bottom: 8px;"><span class="text-red" style="font-weight: 600; margin-right: 10px;">❌ Failed</span> <code style="color: #d4d4d4;">${call}</code></div>
                                ${tc.error ? `<div class="text-red" style="margin-top: 8px; font-size: 0.85rem;">Error: ${this.escapeHtml(tc.error)}</div>` : 
                                `<div style="display:flex; gap: 20px; font-size: 0.85rem; margin-top: 8px;">
                                    <div><span style="color: var(--text-secondary);">Expected:</span> <code style="color: var(--success);">${this.escapeHtml(tc.expected)}</code></div>
                                    <div><span style="color: var(--text-secondary);">Actual:</span> <code style="color: var(--error);">${this.escapeHtml(tc.actual)}</code></div>
                                </div>`}
                            </div>`;
                        }
                    });

                    if(allPass) {
                        html = `<div style="background: rgba(44,187,93,0.15); border: 1px solid rgba(44,187,93,0.3); padding: 12px; border-radius: 6px; color: var(--success); text-align: center; font-weight: 700; font-size: 1.1rem; margin-bottom: 1.5rem; display: flex; justify-content: center; align-items: center; gap: 10px;">🎉 All Tests Passed!</div>` + html;
                        document.getElementById('btn-submit').disabled = false;
                    }
                }
                
                content.innerHTML = html;
            },

            skipAlgorithm() {
                const prevTime = this.blitzResults.reduce((sum, r) => sum + r.time_taken_ms, 0);
                const overallElapsed = Date.now() - this.startTime;
                const timeSpent = overallElapsed - prevTime;

                this.saveRecord(false, timeSpent);
                this.blitzResults.push({ id: this.currentAlgo.id, title: this.currentAlgo.title, passed: false, time_taken_ms: timeSpent, skipped: true });
                this.startPractice(); 
            },
            
            giveUp() { this.cleanupPractice();
                this.activePoolOverride = null; this.showHome(); },
            
            submitCode() {
                if(this.mode === 'pb') {
                    this.cleanupPractice();
                this.activePoolOverride = null;
                    this.saveRecord(true, this.elapsedMs);
                    this.showPBResults(this.currentAlgo, this.elapsedMs);
                } else {
                    const prevTime = this.blitzResults.reduce((sum, r) => sum + r.time_taken_ms, 0);
                    const overallElapsed = Date.now() - this.startTime;
                    const timeSpent = overallElapsed - prevTime;
                    
                    this.saveRecord(true, timeSpent);
                    this.blitzResults.push({ id: this.currentAlgo.id, title: this.currentAlgo.title, passed: true, time_taken_ms: timeSpent, skipped: false });
                    this.startPractice();
                }
            },
            
            endBlitz() {
                this.cleanupPractice();
                this.activePoolOverride = null;
                const solved = this.blitzResults.filter(r => r.passed).length;
                const skipped = this.blitzResults.filter(r => r.skipped).length;
                
                document.getElementById('blitz-res-solved').innerText = solved;
                document.getElementById('blitz-res-attempted').innerText = this.blitzResults.length;
                document.getElementById('blitz-res-skipped').innerText = skipped;

                const tbody = document.querySelector('#blitz-breakdown-table tbody');
                tbody.innerHTML = this.blitzResults.map(r => {
                    const resHtml = r.passed ? '<span class="text-green" style="font-weight:600;">Solved</span>' : '<span class="text-red" style="font-weight:600;">Skipped/Failed</span>';
                    return `<tr><td>${r.title}</td><td>${resHtml}</td><td style="font-family: var(--font-mono);">${this.formatTime(r.time_taken_ms)}</td></tr>`;
                }).join('');

                this.showView('view-blitz-results');
            },
            
            showPBResults(algo, timeMs) {
                document.getElementById('pb-res-title').innerText = algo.title;
                document.getElementById('pb-res-time').innerText = this.formatTime(timeMs);
                
                const best = this.personalBests[algo.id];
                const isNewPB = !best || timeMs <= best.best_time_ms;
                
                document.getElementById('pb-new-record').style.display = isNewPB ? 'block' : 'none';
                
                if(best && !isNewPB) {
                    document.getElementById('pb-res-prev').innerText = this.formatTime(best.best_time_ms);
                } else if(best && isNewPB) {
                     const prevAttempts = this.attempts.filter(a => a.algorithm_id === algo.id && a.passed).sort((a,b) => a.time_taken_ms - b.time_taken_ms);
                     const prev = prevAttempts.length > 1 ? prevAttempts[1].time_taken_ms : timeMs;
                     document.getElementById('pb-res-prev').innerText = prevAttempts.length > 1 ? this.formatTime(prev) : '--:--.---';
                } else {
                    document.getElementById('pb-res-prev').innerText = '--:--.---';
                }

                const tbody = document.querySelector('#pb-history-table tbody');
                const history = this.attempts.filter(a => a.algorithm_id === algo.id).sort((a,b) => b.timestamp - a.timestamp);
                tbody.innerHTML = history.map(h => `
                    <tr>
                        <td>${new Date(h.timestamp).toLocaleString()}</td>
                        <td style="font-family: var(--font-mono);">${this.formatTime(h.time_taken_ms)}</td>
                        <td>${h.passed ? '<span class="text-green" style="font-weight:600;">Pass</span>' : '<span class="text-red" style="font-weight:600;">Fail</span>'}</td>
                    </tr>
                `).join('');

                if (this.currentPlaylistId) {
                    document.getElementById('pb-res-btn-next').style.display = 'inline-block';
                } else {
                    document.getElementById('pb-res-btn-next').style.display = 'none';
                }

                this.showView('view-pb-results');
            },

            saveRecord(passed, timeMs) {
                const record = {
                    id: Date.now().toString(),
                    algorithm_id: this.currentAlgo.id,
                    title: this.currentAlgo.title,
                    timestamp: Date.now(),
                    time_taken_ms: timeMs,
                    passed: passed,
                    mode: this.mode
                };
                this.attempts.push(record);
                this.api('/api/attempts', {
                    method: 'POST',
                    body: JSON.stringify(record)
                }).catch(e => console.error('Failed to persist attempt:', e));

                if(passed) {
                    const currentBest = this.personalBests[this.currentAlgo.id];
                    if(!currentBest || timeMs < currentBest.best_time_ms) {
                        this.personalBests[this.currentAlgo.id] = {
                            best_time_ms: timeMs,
                            attempt_count: currentBest ? currentBest.attempt_count + 1 : 1,
                            first_passed_at: currentBest ? currentBest.first_passed_at : Date.now()
                        };
                    } else {
                        currentBest.attempt_count += 1;
                    }
                    // Server recomputes and persists personal_bests.json as part of
                    // POST /api/attempts above - this local copy is just for immediate UI use.
                }
            },
            
            renderHistory() {
                const pbTbody = document.querySelector('#history-pb-table tbody');
                const pbEntries = Object.entries(this.personalBests).map(([id, data]) => {
                    const algo = this.algorithms.find(a => a.id === id);
                    return { title: algo ? algo.title : id, ...data };
                }).sort((a,b) => a.best_time_ms - b.best_time_ms);

                pbTbody.innerHTML = pbEntries.length ? pbEntries.map((p, index) => {
                    let rankBadge = '';
                    if (index === 0) rankBadge = '🥇 ';
                    else if (index === 1) rankBadge = '🥈 ';
                    else if (index === 2) rankBadge = '🥉 ';
                    else rankBadge = `${index + 1}. `;

                    return `<tr><td style="font-weight:600;">${rankBadge}${p.title}</td><td class="text-green" style="font-family: var(--font-mono); font-weight: 700;">${this.formatTime(p.best_time_ms)}</td><td>${p.attempt_count}</td></tr>`;
                }).join('') : '<tr><td colspan="3" style="text-align:center; color:var(--text-secondary); padding: 2rem;">No personal bests achieved yet. Start practicing!</td></tr>';

                const allTbody = document.querySelector('#history-all-table tbody');
                const sortedAttempts = [...this.attempts].sort((a,b) => b.timestamp - a.timestamp);
                allTbody.innerHTML = sortedAttempts.length ? sortedAttempts.map(a => `
                    <tr>
                        <td>${new Date(a.timestamp).toLocaleDateString()}</td>
                        <td style="font-weight:500;">${a.title}</td>
                        <td style="text-transform: capitalize;">${a.mode}</td>
                        <td style="font-family: var(--font-mono);">${this.formatTime(a.time_taken_ms)}</td>
                        <td>${a.passed ? '<span class="text-green" style="font-weight:600;">Pass</span>' : '<span class="text-red" style="font-weight:600;">Fail</span>'}</td>
                    </tr>
                `).join('') : '<tr><td colspan="5" style="text-align:center; color:var(--text-secondary); padding: 2rem;">No attempts recorded yet.</td></tr>';
            },

            addTestCaseField() {
                const container = document.getElementById('add-testcases-container');
                const div = document.createElement('div');
                div.className = 'flex-between';
                div.style.gap = '10px';
                div.style.marginBottom = '10px';
                div.innerHTML = `
                    <input type="text" placeholder="Call (e.g. Solution().solve(1))" class="tc-call" style="flex: 2; margin: 0; font-family: var(--font-mono);">
                    <input type="text" placeholder="Expected String (e.g. '[1, 2]')" class="tc-expected" style="flex: 1; margin: 0; font-family: var(--font-mono);">
                    <button class="btn-danger" onclick="this.parentElement.remove()" style="padding: 12px; border-radius: 6px;">✕</button>
                `;
                container.appendChild(div);
            },
            
            saveCustomAlgorithm() {
                const id = document.getElementById('add-id').value.trim();
                const title = document.getElementById('add-title').value.trim();
                if(!id || !title) return alert("ID and Title are required.");
                if(this.algorithms.some(a => a.id === id)) return alert("An algorithm with this ID already exists.");

                const difficulty = document.getElementById('add-difficulty').value;
                const tags = document.getElementById('add-tags').value.split(',').map(t => t.trim()).filter(Boolean);
                const stub = document.getElementById('add-stub').value;

                const test_cases = [];
                document.querySelectorAll('#add-testcases-container > div').forEach(div => {
                    const call = div.querySelector('.tc-call').value.trim();
                    const expected = div.querySelector('.tc-expected').value.trim();
                    if(call && expected) test_cases.push({ call, expected });
                });

                if(!test_cases.length) return alert("At least one complete test case is required.");

                const obj = { id, title, stub, test_cases, tags, difficulty };

                this.customAlgos.push(obj);
                this.api('/api/custom-algorithms', {
                    method: 'POST',
                    body: JSON.stringify(obj)
                }).catch(e => console.error('Failed to persist custom algorithm:', e));

                this.algorithms.push(obj);
                
                alert("Algorithm added successfully! It is now available to practice.");
                
                document.getElementById('add-id').value = '';
                document.getElementById('add-title').value = '';
                document.getElementById('add-stub').value = '';
                document.getElementById('add-tags').value = '';
                document.getElementById('add-testcases-container').innerHTML = '';
                this.addTestCaseField();
                
                const pbSelect = document.getElementById('pb-select');
                pbSelect.innerHTML += `<option value="${obj.id}">${obj.title} (${obj.difficulty.toUpperCase()})</option>`;
            }
        };

        window.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            app.init();
        });
