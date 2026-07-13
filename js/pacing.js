Object.assign(app, {

    async renderPacingBanner() {
        const banner = document.getElementById('pacing-banner');
        try {
            const status = await this.api('/api/pacing-status');
            banner.style.display = 'block';
            if (status.behind) {
                banner.style.background = 'rgba(239,71,67,0.12)';
                banner.style.border = '1px solid rgba(239,71,67,0.3)';
                banner.style.color = 'var(--error)';
                banner.innerText = `Behind pace: ${status.logged}/${status.expected} contests logged this week. Log one today.`;
            } else {
                banner.style.background = 'rgba(44,187,93,0.12)';
                banner.style.border = '1px solid rgba(44,187,93,0.3)';
                banner.style.color = 'var(--success)';
                banner.innerText = `On pace: ${status.logged}/${status.expected} contests logged this week.`;
            }
        } catch (e) {
            banner.style.display = 'none';
        }
    }

});
