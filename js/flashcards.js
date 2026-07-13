Object.assign(app, {

    flashcardQueue: [],
    flashcardIndex: 0,

    async showFlashcardReview() {
        this.showView('view-flashcard-review');
        this.flashcardQueue = await this.api('/api/flashcards/due');
        this.flashcardIndex = 0;
        this.renderCurrentFlashcard();
    },

    renderCurrentFlashcard() {
        const empty = document.getElementById('flashcard-empty');
        const content = document.getElementById('flashcard-content');
        const progress = document.getElementById('flashcard-progress');

        if (this.flashcardIndex >= this.flashcardQueue.length) {
            empty.style.display = 'block';
            content.style.display = 'none';
            progress.innerText = this.flashcardQueue.length ? 'All done for now.' : '';
            return;
        }

        empty.style.display = 'none';
        content.style.display = 'block';
        progress.innerText = `Card ${this.flashcardIndex + 1} of ${this.flashcardQueue.length}`;

        const card = this.flashcardQueue[this.flashcardIndex];
        document.getElementById('flashcard-front').innerText = card.front;
        document.getElementById('flashcard-back').innerText = card.back;
        document.getElementById('flashcard-tag').innerHTML = card.tag
            ? `<span class="badge" style="background:var(--bg-layer-1); border:1px solid var(--border-color); color:var(--text-secondary);">${this.escapeHtml(card.tag)}</span>`
            : '';
        document.getElementById('flashcard-back-section').style.display = 'none';
        document.getElementById('flashcard-reveal-btn').style.display = 'inline-block';
    },

    revealFlashcardAnswer() {
        document.getElementById('flashcard-back-section').style.display = 'block';
        document.getElementById('flashcard-reveal-btn').style.display = 'none';
    },

    async gradeFlashcard(grade) {
        const card = this.flashcardQueue[this.flashcardIndex];
        await this.api(`/api/flashcards/${card.id}/review`, {
            method: 'POST',
            body: JSON.stringify({ grade })
        });
        this.flashcardIndex += 1;
        this.renderCurrentFlashcard();
    }

});
