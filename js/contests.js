Object.assign(app, {

    currentContestId: null,

    async showContestsList() {
        this.showView('view-contests-list');
        const contests = await this.api('/api/contests');
        const tbody = document.querySelector('#contests-list-table tbody');
        tbody.innerHTML = contests.length ? contests.map(c => `
            <tr>
                <td>${c.date}</td>
                <td style="font-weight:600;">${this.escapeHtml(c.name)}</td>
                <td style="text-transform:capitalize;">${c.type}</td>
                <td>${c.num_problems}</td>
                <td>${c.graded ? '<span class="text-green">Graded</span>' : '<span style="color:var(--text-secondary);">Ungraded</span>'}</td>
                <td>
                    <button class="btn-secondary" style="padding:4px 8px; font-size:0.75rem;" onclick="app.showLogContest('${c.id}')">Capture</button>
                    <button class="btn-secondary" style="padding:4px 8px; font-size:0.75rem;" onclick="app.showGeneratePrompt('${c.id}')">Prompt</button>
                    <button class="btn-secondary" style="padding:4px 8px; font-size:0.75rem;" onclick="app.showImportGrading('${c.id}')">Import</button>
                </td>
            </tr>
        `).join('') : '<tr><td colspan="6" style="text-align:center; color:var(--text-secondary); padding:2rem;">No contests logged yet.</td></tr>';
    },

    async showLogContest(existingId) {
        this.showView('view-log-contest');
        const metaSection = document.getElementById('log-contest-meta');
        const captureSection = document.getElementById('log-contest-capture');
        document.getElementById('problems-container').innerHTML = '';

        if (existingId) {
            const contest = await this.api(`/api/contests/${existingId}`);
            this.currentContestId = contest.id;
            metaSection.style.display = 'none';
            captureSection.style.display = 'block';
            document.getElementById('log-contest-title').innerText = `${contest.meta.name} (${contest.meta.date})`;
            if (contest.problems.length) {
                contest.problems.forEach(p => this.addProblemBlock(p));
            } else {
                this.addProblemBlock();
            }
        } else {
            this.currentContestId = null;
            metaSection.style.display = 'block';
            captureSection.style.display = 'none';
            document.getElementById('contest-name').value = '';
            document.getElementById('contest-date').value = new Date().toISOString().slice(0, 10);
            document.getElementById('contest-type').value = 'official';
        }
    },

    async createContest() {
        const name = document.getElementById('contest-name').value.trim();
        const date = document.getElementById('contest-date').value;
        const type = document.getElementById('contest-type').value;
        if (!name || !date) return alert('Name and date are required.');

        const contest = await this.api('/api/contests', {
            method: 'POST',
            body: JSON.stringify({ name, date, type })
        });
        this.currentContestId = contest.id;
        document.getElementById('log-contest-meta').style.display = 'none';
        document.getElementById('log-contest-capture').style.display = 'block';
        document.getElementById('log-contest-title').innerText = `${contest.meta.name} (${contest.meta.date})`;
        document.getElementById('problems-container').innerHTML = '';
        this.addProblemBlock();
    },

    addProblemBlock(existing) {
        const container = document.getElementById('problems-container');
        const div = document.createElement('div');
        div.className = 'problem-block';
        div.innerHTML = `
            <div class="flex-between" style="gap:1rem;">
                <div style="flex:2;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Problem Title</label>
                    <input type="text" class="prob-title" placeholder="e.g. Two Sum">
                </div>
                <div style="flex:1;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Patterns (comma separated)</label>
                    <input type="text" class="prob-patterns" placeholder="e.g. binary_search, greedy">
                </div>
            </div>
            <div class="flex-between" style="gap:1rem;">
                <div style="flex:2;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Link (optional)</label>
                    <input type="text" class="prob-link" placeholder="https://leetcode.com/problems/...">
                </div>
                <div style="flex:1;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Time to Solve (minutes)</label>
                    <input type="number" step="0.5" min="0" class="prob-time" placeholder="e.g. 18">
                </div>
            </div>

            <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Thought Process Narrative</label>
            <p class="practice-note">Write what you were actually thinking, not just what worked - reflection grades your process, not your outcome.</p>
            <textarea class="prob-narrative" rows="4" placeholder="What did you try first? Where did you get stuck? What made you change approach?"></textarea>

            <div class="flex-between" style="margin-bottom: 0.75rem;">
                <label style="color:var(--text-secondary); font-weight:600;">Submissions</label>
                <button class="btn-secondary" onclick="app.addSubmissionField(this)" style="padding: 6px 12px; font-size: 0.85rem;">+ Add Submission</button>
            </div>
            <div class="submissions-container"></div>

            <div class="flex-between" style="margin-top: 1rem;">
                <button class="btn-danger" onclick="this.closest('.problem-block').remove()" style="padding: 6px 12px; font-size: 0.85rem;">Remove</button>
                <button class="btn-success" onclick="app.saveProblemBlock(this)" style="padding: 8px 16px;">Save Problem</button>
            </div>
        `;
        container.appendChild(div);

        if (existing) {
            div.querySelector('.prob-title').value = existing.title || '';
            div.querySelector('.prob-patterns').value = (existing.patterns || []).join(', ');
            div.querySelector('.prob-link').value = existing.link || '';
            div.querySelector('.prob-time').value = existing.time_to_solve_min != null ? existing.time_to_solve_min : '';
            div.querySelector('.prob-narrative').value = existing.narrative || '';
            const subsContainer = div.querySelector('.submissions-container');
            (existing.submissions || []).forEach(s => this.addSubmissionField(subsContainer, s));
        } else {
            this.addSubmissionField(div.querySelector('.submissions-container'));
        }
    },

    addSubmissionField(anchorOrContainer, existing) {
        const container = (anchorOrContainer.classList && anchorOrContainer.classList.contains('submissions-container'))
            ? anchorOrContainer
            : anchorOrContainer.closest('.problem-block').querySelector('.submissions-container');

        const row = document.createElement('div');
        row.className = 'submission-row';
        row.innerHTML = `
            <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Code</label>
            <textarea class="sub-code" rows="6" style="font-family: var(--font-mono); font-size: 0.85rem;" placeholder="Paste your submission code, including your own thinking comments"></textarea>
            <div class="flex-between" style="gap: 1rem;">
                <div style="flex:1;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Verdict</label>
                    <select class="sub-verdict">
                        <option value="accepted">Accepted</option>
                        <option value="wrong_answer">Wrong Answer</option>
                        <option value="tle">Time Limit Exceeded</option>
                        <option value="runtime_error">Runtime Error</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div style="flex:1;">
                    <label style="display:block; margin-bottom:0.5rem; color:var(--text-secondary); font-weight:600;">Failing Test (if any)</label>
                    <input type="text" class="sub-failing-test" placeholder="e.g. nums=[1,2], target=5">
                </div>
            </div>
            <button class="btn-danger" onclick="this.parentElement.remove()" style="padding: 6px 12px; font-size: 0.8rem;">Remove Submission</button>
        `;
        container.appendChild(row);

        if (existing) {
            row.querySelector('.sub-code').value = existing.code || '';
            row.querySelector('.sub-verdict').value = existing.verdict || 'accepted';
            row.querySelector('.sub-failing-test').value = existing.failing_test || '';
        }
    },

    async saveProblemBlock(btn) {
        const block = btn.closest('.problem-block');
        const title = block.querySelector('.prob-title').value.trim();
        if (!title) return alert('Problem title is required.');

        const patterns = block.querySelector('.prob-patterns').value.split(',').map(t => t.trim()).filter(Boolean);
        const link = block.querySelector('.prob-link').value.trim() || null;
        const timeRaw = block.querySelector('.prob-time').value.trim();
        const time_to_solve_min = timeRaw ? parseFloat(timeRaw) : null;
        const narrative = block.querySelector('.prob-narrative').value;
        const submissions = [...block.querySelectorAll('.submission-row')].map(row => ({
            code: row.querySelector('.sub-code').value,
            verdict: row.querySelector('.sub-verdict').value,
            failing_test: row.querySelector('.sub-failing-test').value.trim() || null
        }));

        try {
            await this.api(`/api/contests/${this.currentContestId}/problems`, {
                method: 'POST',
                body: JSON.stringify({ title, link, patterns, submissions, narrative, time_to_solve_min })
            });
            const original = btn.innerText;
            btn.innerText = 'Saved ✓';
            setTimeout(() => { btn.innerText = original; }, 1500);
        } catch (e) {
            alert('Failed to save problem: ' + e.message);
        }
    },

    async showGeneratePrompt(contestId) {
        this.currentContestId = contestId;
        this.showView('view-generate-prompt');

        const contest = await this.api(`/api/contests/${contestId}`);
        document.getElementById('prompt-contest-title').innerText = `${contest.meta.name} (${contest.meta.date})`;

        const warning = document.getElementById('prompt-same-day-warning');
        const today = new Date().toISOString().slice(0, 10);
        if (contest.meta.date === today) {
            warning.style.display = 'block';
            warning.innerText = "This contest was today - reflecting the same day is intentionally discouraged. Memory consolidates with a delay (the spacing effect), so the critique you get tomorrow will be sharper than one you'd get right now. Consider coming back tomorrow.";
        } else {
            warning.style.display = 'none';
        }

        const { prompt } = await this.api(`/api/contests/${contestId}/grading-prompt`);
        document.getElementById('grading-prompt-text').value = prompt;
    },

    copyGradingPrompt() {
        const text = document.getElementById('grading-prompt-text').value;
        navigator.clipboard.writeText(text).then(() => alert('Copied to clipboard.'));
    },

    async showImportGrading(contestId) {
        if (contestId) this.currentContestId = contestId;
        this.showView('view-import-grading');

        const contest = await this.api(`/api/contests/${this.currentContestId}`);
        document.getElementById('import-contest-title').innerText = `${contest.meta.name} (${contest.meta.date})`;
        document.getElementById('import-grading-text').value = '';
        document.getElementById('import-error').style.display = 'none';
        document.getElementById('import-result-preview').style.display = 'none';
    },

    async importGrading() {
        const raw = document.getElementById('import-grading-text').value;
        const errorEl = document.getElementById('import-error');
        errorEl.style.display = 'none';

        let parsed;
        try {
            parsed = JSON.parse(raw);
        } catch (e) {
            errorEl.innerText = 'That is not valid JSON: ' + e.message;
            errorEl.style.display = 'block';
            return;
        }

        try {
            const result = await this.api(`/api/contests/${this.currentContestId}/import-grading`, {
                method: 'POST',
                body: JSON.stringify(parsed)
            });

            document.getElementById('import-result-preview').style.display = 'block';
            document.getElementById('import-result-summary').innerText =
                `${result.added_flashcards} flashcard(s), ${result.added_edge_cases} edge case(s), ${result.added_specimen_proposals} specimen proposal(s) added.`;

            if (result.added_specimen_proposals > 0) {
                await this.renderSpecimenProposals();
            } else {
                document.getElementById('specimen-approval-section').style.display = 'none';
            }
        } catch (e) {
            errorEl.innerText = 'Import failed: ' + e.message;
            errorEl.style.display = 'block';
        }
    },

    async renderSpecimenProposals() {
        const proposals = await this.api('/api/specimen-proposals');
        const relevant = proposals.filter(p => p.source_contest === this.currentContestId);
        const section = document.getElementById('specimen-approval-section');
        const list = document.getElementById('specimen-proposals-list');

        if (!relevant.length) {
            section.style.display = 'none';
            return;
        }
        section.style.display = 'block';
        list.innerHTML = relevant.map(p => `
            <div class="card flex-between" style="padding: 12px 18px; margin-bottom: 0.75rem;">
                <div>
                    <div style="font-weight:600;">${this.escapeHtml(p.title)}</div>
                    <div style="color:var(--text-secondary); font-size:0.85rem;">${this.escapeHtml(p.reason)}</div>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn-success" style="padding:6px 12px; font-size:0.8rem;" onclick="app.approveSpecimen('${p.id}')">Approve</button>
                    <button class="btn-danger" style="padding:6px 12px; font-size:0.8rem;" onclick="app.rejectSpecimen('${p.id}')">Reject</button>
                </div>
            </div>
        `).join('');
    },

    async approveSpecimen(id) {
        await this.api(`/api/specimen-proposals/${id}/approve`, { method: 'POST' });
        await this.renderSpecimenProposals();
    },

    async rejectSpecimen(id) {
        await this.api(`/api/specimen-proposals/${id}/reject`, { method: 'POST' });
        await this.renderSpecimenProposals();
    }

});
