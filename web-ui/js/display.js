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

        // Create word family list HTML
        const wordFamilyList = (word.word_family || []).slice(0, 20).join(', ');
        const hasMoreFamily = (word.word_family || []).length > 20;

        // Dictionary links
        const dictUrls = {
            cambridge: `https://dictionary.cambridge.org/dictionary/english/${word.word}`,
            merriam: `https://www.merriam-webster.com/dictionary/${word.word}`,
            google: `https://www.google.com/search?q=define+${word.word}`
        };

        return `
            <div class="word-card ${isSelected ? 'selected' : ''}" data-word="${word.word}">
                ${isSelected ? '' : `<input type="checkbox" class="select-checkbox" data-word="${word.word}">`}
                <div class="word-main">
                    <span class="word-text">${word.word}</span>
                    <div class="badges">
                        ${band ? `<span class="badge badge-band band-${band.level}" title="Frequency: ${band.label}">${band.label}</span>` : ''}
                        ${emotion && emotion !== 'neutral' ? `<span class="badge badge-emotion emotion-${emotion}" title="Emotion: ${emotion}">${this._emotionEmoji(emotion)}</span>` : ''}
                        ${register ? `<span class="badge badge-register register-${register}" title="Register: ${register}">${this._registerLabel(register)}</span>` : ''}
                    </div>
                </div>
                <div class="word-meta">
                    <span class="word-family-size clickable"
                          title="Click to see word family"
                          data-word="${word.word}"
                          data-family='${JSON.stringify(word.word_family || [])}'>
                        ${word.word_family?.length || 1} forms
                    </span>
                    ${word.pos ? `<span class="badge" title="Part of Speech">${word.pos}</span>` : ''}
                    <a href="${dictUrls.cambridge}" target="_blank" class="dict-link" title="View in Cambridge Dictionary" data-word="${word.word}">📖</a>
                </div>
                <div class="word-family-tooltip" id="family-${word.word.replace(/\s/g, '-')}" style="display: none;">
                    <strong>Word Family:</strong><br>
                    ${wordFamilyList}${hasMoreFamily ? '...' : ''}
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
                // Check if clicking on forms
                if (e.target.classList.contains('word-family-size') && e.target.classList.contains('clickable')) {
                    e.stopPropagation();
                    this._toggleWordFamily(e.target);
                    return;
                }

                // Don't toggle if clicking on dictionary link or checkbox
                if (e.target.classList.contains('dict-link') || e.target.type === 'checkbox') {
                    return;
                }

                const wordId = card.dataset.word;
                this.data.toggleSelect(wordId);
                this.render(); // Re-render to update selection state
            });
        });
    }

    _toggleWordFamily(element) {
        const word = element.dataset.word;
        const tooltipId = `family-${word.replace(/\s/g, '-')}`;
        const tooltip = document.getElementById(tooltipId);

        if (tooltip) {
            const isVisible = tooltip.style.display !== 'none';
            tooltip.style.display = isVisible ? 'none' : 'block';
            element.style.color = isVisible ? '' : '#667eea';
            element.style.fontWeight = isVisible ? '' : 'bold';
        }
    }

    toggleShowSelectedOnly() {
        this.showSelectedOnly = !this.showSelectedOnly;
        this.render();
    }

    _extractBand(bandStr) {
        if (!bandStr) return null;

        // Extract band information
        if (bandStr.includes('BEYOND') || bandStr.includes('beyond')) {
            return { level: 'beyond', label: 'Rare' };
        }

        const match = bandStr.match(/\d+/);
        if (match) {
            const bandNum = match[0];
            const labels = {
                '1': 'Top 3K',
                '2': 'Common',
                '3': 'Moderate',
                '4': 'Low',
                '5': 'Rare'
            };
            return { level: bandNum, label: labels[bandNum] || `Band ${bandNum}` };
        }

        return null;
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

    _registerLabel(register) {
        const labels = {
            'formal': '🎩 Formal',
            'neutral': '😐 Neutral',
            'informal': '💬 Informal',
            'slang': '🤪 Slang'
        };
        return labels[register] || register;
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

// Global display instance (set by main.js)
let display = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // display will be initialized by main.js
});
