// TOEFL Vocabulary Data Manager
// Handles loading and managing vocabulary data

class VocabularyData {
    constructor() {
        this.words = [];
        this.filteredWords = [];
        this.selectedWords = new Set();
    }

    async loadFromJSON(url) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            this.words = data;
            this.filteredWords = data;
            return true;
        } catch (error) {
            console.error('Failed to load vocabulary:', error);
            return false;
        }
    }

    search(query) {
        if (!query) {
            return this.words;
        }

        const q = query.toLowerCase();
        return this.words.filter(word =>
            word.word.toLowerCase().includes(q) ||
            word.lemma.toLowerCase().includes(q) ||
            word.word_family.some(f => f.toLowerCase().includes(q))
        );
    }

    applyFilters(filters) {
        this.filteredWords = this.words.filter(word => {
            // Search filter
            if (filters.search && !this._matchesSearch(word, filters.search)) {
                return false;
            }

            // Frequency bands
            if (filters.frequencyBands.length > 0) {
                const band = this._extractBand(word.frequency?.band);
                if (!filters.frequencyBands.includes(band)) {
                    return false;
                }
            }

            // Emotions
            if (filters.emotions.length > 0) {
                const emotion = this._normalizeEmotion(word.emotion?.primary);
                if (!filters.emotions.includes(emotion)) {
                    return false;
                }
            }

            // Registers
            if (filters.registers.length > 0) {
                const register = this._normalizeRegister(word.register?.register);
                if (!filters.registers.includes(register)) {
                    return false;
                }
            }

            // POS
            if (filters.pos.length > 0) {
                const pos = word.pos || '';
                if (!filters.pos.includes(pos)) {
                    return false;
                }
            }

            return true;
        });

        return this.filteredWords;
    }

    getSelectedWords() {
        return Array.from(this.selectedWords).map(id =>
            this.words.find(w => w.word === id)
        ).filter(w => w !== undefined);
    }

    toggleSelect(wordId) {
        if (this.selectedWords.has(wordId)) {
            this.selectedWords.delete(wordId);
        } else {
            this.selectedWords.add(wordId);
        }
    }

    isSelected(wordId) {
        return this.selectedWords.has(wordId);
    }

    clearSelection() {
        this.selectedWords.clear();
    }

    selectAll() {
        this.filteredWords.forEach(word => {
            this.selectedWords.add(word.word);
        });
    }

    getSelectionStats() {
        const selected = this.getSelectedWords();
        const total = this.filteredWords.length;

        return {
            selected: selected.length,
            total: total,
            percentage: total > 0 ? (selected.length / total * 100).toFixed(1) : 0
        };
    }

    // Private helper methods
    _matchesSearch(word, query) {
        if (!query) return true;
        const q = query.toLowerCase();
        return word.word.toLowerCase().includes(q) ||
               word.lemma.toLowerCase().includes(q);
    }

    _extractBand(bandStr) {
        if (!bandStr) return '';

        // Handle "FrequencyBand.BEYOND" format
        if (bandStr.includes('BEYOND') || bandStr.includes('beyond')) {
            return 'beyond';
        }

        // Extract numeric band from "FrequencyBand.BAND_X" or just "X"
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
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VocabularyData;
}
