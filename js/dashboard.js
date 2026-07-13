Object.assign(app, {

    async showDashboard() {
        this.showView('view-dashboard');
        await this.renderEloRatingsList();
        await this.renderDashboardContests();
    },

    async renderEloRatingsList() {
        const ratings = await this.api('/api/elo');
        const categories = Object.keys(ratings).sort();
        const container = document.getElementById('elo-ratings-list');

        container.innerHTML = categories.length ? categories.map(cat => `
            <div class="card" style="padding: 12px 20px; min-width: 140px; text-align:center;">
                <div style="color:var(--text-secondary); font-size:0.8rem; text-transform:uppercase;">${this.escapeHtml(cat)}</div>
                <div style="font-size:1.5rem; font-weight:700; margin-top:4px;">${Math.round(ratings[cat].rating)}</div>
            </div>
        `).join('') : '<p style="color:var(--text-secondary);">No graded contests yet - ratings appear here once you import a grading result.</p>';

        const select = document.getElementById('elo-category-select');
        select.innerHTML = categories.map(cat => `<option value="${cat}">${cat}</option>`).join('');

        if (categories.length) {
            await this.renderEloTrend(categories[0]);
        } else {
            document.getElementById('elo-chart').innerHTML = '';
        }
    },

    async renderEloTrend(category) {
        const history = await this.api(`/api/elo/history?category=${encodeURIComponent(category)}`);
        const svg = document.getElementById('elo-chart');

        if (!history.length) {
            svg.innerHTML = '<text x="350" y="150" fill="var(--text-secondary)" text-anchor="middle">No history yet</text>';
            return;
        }

        const values = history.map(h => h.new_rating);
        const minV = Math.min(...values) - 20;
        const maxV = Math.max(...values) + 20;
        const w = 700, h = 300, pad = 40;
        const xStep = values.length > 1 ? (w - 2 * pad) / (values.length - 1) : 0;
        const yFor = v => h - pad - ((v - minV) / (maxV - minV || 1)) * (h - 2 * pad);

        const points = values.map((v, i) => `${pad + i * xStep},${yFor(v)}`).join(' ');
        const dots = values.map((v, i) => `<circle cx="${pad + i * xStep}" cy="${yFor(v)}" r="4" fill="var(--accent)"></circle>`).join('');

        svg.innerHTML = `
            <line x1="${pad}" y1="${h - pad}" x2="${w - pad}" y2="${h - pad}" stroke="var(--border-color)"></line>
            <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h - pad}" stroke="var(--border-color)"></line>
            <polyline points="${points}" fill="none" stroke="var(--accent)" stroke-width="2"></polyline>
            ${dots}
            <text x="${pad}" y="${pad - 10}" fill="var(--text-secondary)" font-size="12">${Math.round(maxV)}</text>
            <text x="${pad}" y="${h - pad + 15}" fill="var(--text-secondary)" font-size="12">${Math.round(minV)}</text>
        `;
    },

    async renderDashboardContests() {
        const contests = await this.api('/api/contests');
        const tbody = document.querySelector('#dashboard-contests-table tbody');
        tbody.innerHTML = contests.length ? contests.map(c => `
            <tr>
                <td>${c.date}</td>
                <td style="font-weight:600;">${this.escapeHtml(c.name)}</td>
                <td style="text-transform:capitalize;">${c.type}</td>
                <td>${c.num_problems}</td>
                <td>${c.graded ? '<span class="text-green">Graded</span>' : '<span style="color:var(--text-secondary);">Ungraded</span>'}</td>
            </tr>
        `).join('') : '<tr><td colspan="5" style="text-align:center; color:var(--text-secondary); padding:2rem;">No contests logged yet.</td></tr>';
    }

});
