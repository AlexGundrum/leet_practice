Object.assign(app, {

    edgeCaseQueue: [],
    edgeCaseIndex: 0,

    async showEdgeCaseDrills() {
        this.showView('view-edge-case-drills');
        this.edgeCaseQueue = await this.api('/api/edge-cases/due');
        this.edgeCaseIndex = 0;
        this.renderCurrentEdgeCase();
    },

    renderCurrentEdgeCase() {
        const empty = document.getElementById('edgecase-empty');
        const content = document.getElementById('edgecase-content');
        const progress = document.getElementById('edgecase-progress');

        if (this.edgeCaseIndex >= this.edgeCaseQueue.length) {
            empty.style.display = 'block';
            content.style.display = 'none';
            progress.innerText = this.edgeCaseQueue.length ? 'All done for now.' : '';
            return;
        }

        empty.style.display = 'none';
        content.style.display = 'block';
        progress.innerText = `Case ${this.edgeCaseIndex + 1} of ${this.edgeCaseQueue.length}`;

        const ec = this.edgeCaseQueue[this.edgeCaseIndex];
        document.getElementById('edgecase-category').innerText = ec.category;
        document.getElementById('edgecase-description').innerText = ec.description;
        document.getElementById('edgecase-lesson').innerText = ec.generalized_lesson;
        document.getElementById('edgecase-lesson-section').style.display = 'none';
        document.getElementById('edgecase-reveal-btn').style.display = 'inline-block';
    },

    revealEdgeCaseLesson() {
        document.getElementById('edgecase-lesson-section').style.display = 'block';
        document.getElementById('edgecase-reveal-btn').style.display = 'none';
    },

    async gradeEdgeCase(remembered) {
        const ec = this.edgeCaseQueue[this.edgeCaseIndex];
        await this.api(`/api/edge-cases/${ec.id}/review`, {
            method: 'POST',
            body: JSON.stringify({ remembered })
        });
        this.edgeCaseIndex += 1;
        this.renderCurrentEdgeCase();
    }

});
