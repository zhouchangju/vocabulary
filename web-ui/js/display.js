// TOEFL Vocabulary Display Manager
// Handles rendering word cards and updating the UI

class VocabularyDisplay {
    constructor(dataManager) {
        this.data = dataManager;
        this.wordGrid = document.getElementById('wordGrid');
        this.resultCount = document.getElementById('resultCount');
        this.showSelectedOnly = false;
    }

    render() {
        if (!this.wordGrid) return;

        const words = this.showSelectedOnly ?
            this.data.getSelectedWords() :
            this.data.filteredWords;

        if (words.length === 0) {
            this._renderEmptyState();
            this._updateResultCount(0, 0);
            return;
        }

        // Render word cards
        this.wordGrid.innerHTML = words.map(word => this._createWordCard(word)).join('');
        this._updateResultCount(words.length, this.data.getSelectionStats().selected);

        // Bind click handlers
        this._bindCardEvents();

        // Update select all checkbox
        const selectAllBtn = document.getElementById('selectAllBtn');
        if (selectAllBtn) {
            selectAllBtn.textContent = 'Select All';
        }
    }

    _createWordCard(word) {
        const isSelected = this.data.isSelected(word.word);
        const band = this._extractBand(word.frequency?.band);
        const emotion = this._normalizeEmotion(word.emotion?.primary);
        const register = this._normalizeRegister(word.register?.register);

        return `
            <div class="word-card ${isSelected ? 'selected' : ''}" data-word="${word.word}">
                ${isSelected ? '' : `<input type="checkbox" class="select-checkbox" data-word="${word.word}">`}
                <div class="word-main">
                    <span class="word-text">${word.word}</span>
                    <div class="badges">
                        ${band ? `<span class="badge badge-band band-${band}">${band}</span>` : ''}
                        ${emotion && emotion !== 'neutral' ? `<span class="badge badge-emotion emotion-${emotion}">${this._emotionEmoji(emotion)}</span>` : ''}
                        ${register ? `<span class="badge badge-register register-${register}">${this._registerEmoji(register)}</span>` : ''}
                    </div>
                </div>
                <div class="word-meta">
                    <span class="word-family-size">${word.word_family?.length || 1} forms</span>
                    ${word.pos ? `<span class="badge">${word.pos}</span>` : ''}
                </div>
            </div>
        `;
    }

    _renderEmptyState() {
        this.wordGrid.innerHTML = `
            <div class="empty-state">
                <p>No words match your current filters.</p>
                <p>Try adjusting your filters or search query.</p>
            </div>
        `;
    }

    _updateResultCount(total, selected) {
        if (this.resultCount) {
            this.resultCount.textContent = `Showing ${total} words (${selected} selected)`;
        }
    }

    _bindCardEvents() {
        // Handle card clicks for selection
        const cards = this.wordGrid.querySelectorAll('.word-card');
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                if (e.target.type === 'checkbox') return; // Don't toggle if clicking checkbox

                const wordId = card.dataset.word;
                this.data.toggleSelect(wordId);
                this.render(); // Re-render to update selection state
            });
        });
    }

    toggleShowSelectedOnly() {
        this.showSelectedOnly = !this.showSelectedOnly;
        this.render();
    }

    _extractBand(bandStr) {
        if (!bandStr) return '';
        const match = bandStr.match(/\d+/);
        return match ? match[0] : '';
    }

    _normalizeEmotion(emotion) {
        if (!emotion) return 'neutral';
        const e = emotion.toLowerCase();
        if (e.includes('posit')) return 'positive';
        if (e.includes('negat')) return 'negative';
        return 'neutral';
    }

    _normalizeRegister(register) {
        if (!register) return 'neutral';
        const r = register.toLowerCase();
        if (r.includes('formal')) return 'formal';
        if (r.includes('informal')) return 'informal';
        if (r.includes('slang')) return 'slang';
        return 'neutral';
    }

    _emotionEmoji(emotion) {
        const emojis = {
            'positive': '😊',
            'negative': '😞',
            'neutral': '😐',
            'joy': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😨',
            'disgust': '🤢',
            'surprise': '😲'
        };
        return emojis[emotion] || '😐';
    }

    _registerEmoji(register) {
        const emojis = {
            'formal': '🎩',
            'neutral': '😐',
            'informal': '💬',
            'slang': '🤪'
        };
        return emojis[register] || '😐';
    }

    showLoading() {
        if (this.wordGrid) {
            this.wordGrid.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading vocabulary...</p>
                </div>
            `;
        }
        if (this.resultCount) {
            this.resultCount.textContent = 'Loading...';
        }
    }

    showError(message) {
        if (this.wordGrid) {
            this.wordGrid.innerHTML = `
                <div class="empty-state">
                    <p style="color: #d32f2f;">⚠️ ${message}</p>
                </div>
            `;
        }
    }
}

// Global display instance
let display = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // display will be initialized by main.js
});
