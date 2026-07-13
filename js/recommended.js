Object.assign(app, {

    async showRecommendedSession() {
        this.showView('view-recommended-session');
        const session = await this.api('/api/recommended-session');
        const container = document.getElementById('recommended-session-content');

        let html = '';

        if (session.weakest_category) {
            html += `<h3 style="margin-bottom:0.5rem;">Weakest Category: <span style="color:var(--accent); text-transform:capitalize;">${this.escapeHtml(session.weakest_category)}</span></h3>`;
        } else {
            html += `<p style="color:var(--text-secondary);">No graded contests yet - grade a contest to unlock a targeted recommendation.</p>`;
        }

        if (session.atomic_drills.length) {
            html += `<h4 style="margin: 1.5rem 0 0.75rem 0; color:var(--text-secondary);">Atomic Drills</h4>`;
            html += session.atomic_drills.map(d => `
                <div class="card flex-between" style="padding:12px 18px; margin-bottom:0.5rem;">
                    <span style="font-weight:600;">${this.escapeHtml(d.title)}</span>
                    <button class="btn-primary" style="padding:6px 14px; font-size:0.85rem;" onclick="app.startPracticeFromList('${d.id}')">Start</button>
                </div>
            `).join('');
        }

        if (session.specimens.length) {
            html += `<h4 style="margin: 1.5rem 0 0.75rem 0; color:var(--text-secondary);">Specimen Examples</h4>`;
            html += session.specimens.map(s => `
                <div class="card" style="padding:12px 18px; margin-bottom:0.5rem;">
                    <div style="font-weight:600; margin-bottom:0.5rem;">${this.escapeHtml(s.title)}</div>
                    <div style="color:var(--text-secondary); font-size:0.9rem; margin-bottom:0.5rem;">${this.escapeHtml(s.solution_explanation || '')}</div>
                    <pre style="background:var(--bg-base); padding:10px; border-radius:6px; font-size:0.8rem; overflow-x:auto;"><code>${this.escapeHtml(s.solution_code || '')}</code></pre>
                </div>
            `).join('');
        }

        html += `<h4 style="margin: 1.5rem 0 0.75rem 0; color:var(--text-secondary);">Due Practice</h4>`;
        html += `<div class="card flex-between" style="padding:12px 18px; margin-bottom:0.5rem;">
            <span>${session.due_flashcards.length} flashcard(s) due</span>
            <button class="btn-secondary" style="padding:6px 14px; font-size:0.85rem;" ${session.due_flashcards.length ? '' : 'disabled'} onclick="app.showFlashcardReview()">Review</button>
        </div>`;
        html += `<div class="card flex-between" style="padding:12px 18px; margin-bottom:0.5rem;">
            <span>${session.due_edge_cases.length} edge case(s) due</span>
            <button class="btn-secondary" style="padding:6px 14px; font-size:0.85rem;" ${session.due_edge_cases.length ? '' : 'disabled'} onclick="app.showEdgeCaseDrills()">Review</button>
        </div>`;

        container.innerHTML = html;
    }

});
