// TOEFL Vocabulary Filters
// Handles all filtering logic for vocabulary

class VocabularyFilters {
    constructor(dataManager) {
        this.data = dataManager;
        this.filters = {
            search: '',
            frequencyBands: [],
            emotions: [],
            registers: [],
            pos: []
        };
        this.activeFilters = false;
    }

    setSearch(query) {
        this.filters.search = query;
        this.activeFilters = true;
        this.data.applyFilters(this.filters);
        this._render();
    }

    toggleFrequencyBand(band) {
        const index = this.filters.frequencyBands.indexOf(band);
        if (index > -1) {
            this.filters.frequencyBands.splice(index, 1);
        } else {
            this.filters.frequencyBands.push(band);
        }
        this.activeFilters = true;
        this.data.applyFilters(this.filters);
        this._render();
    }

    toggleEmotion(emotion) {
        const index = this.filters.emotions.indexOf(emotion);
        if (index > -1) {
            this.filters.emotions.splice(index, 1);
        } else {
            this.filters.emotions.push(emotion);
        }
        this.activeFilters = true;
        this.data.applyFilters(this.filters);
        this._render();
    }

    toggleRegister(register) {
        const index = this.filters.registers.indexOf(register);
        if (index > -1) {
            this.filters.registers.splice(index, 1);
        } else {
            this.filters.registers.push(register);
        }
        this.activeFilters = true;
        this.data.applyFilters(this.filters);
        this._render();
    }

    togglePOS(pos) {
        const index = this.filters.pos.indexOf(pos);
        if (index > -1) {
            this.filters.pos.splice(index, 1);
        } else {
            this.filters.pos.push(pos);
        }
        this.activeFilters = true;
        this.data.applyFilters(this.filters);
        this._render();
    }

    _render() {
        // Trigger display update
        if (window.vocabularyDisplay) {
            window.vocabularyDisplay.render();
        }
    }

    clear() {
        this.filters = {
            search: '',
            frequencyBands: [],
            emotions: [],
            registers: [],
            pos: []
        };
        this.activeFilters = false;
        this.data.applyFilters(this.filters);
    }

    isActive() {
        return this.activeFilters;
    }

    hasFilters() {
        return this.filters.search !== '' ||
               this.filters.frequencyBands.length > 0 ||
               this.filters.emotions.length > 0 ||
               this.filters.registers.length > 0 ||
               this.filters.pos.length > 0;
    }

    // Checkbox change handlers
    onSearchChange(event) {
        this.setSearch(event.target.value);
    }

    onFrequencyBandChange(event) {
        this.toggleFrequencyBand(event.target.value);
    }

    onEmotionChange(event) {
        this.toggleEmotion(event.target.value);
    }

    onRegisterChange(event) {
        this.toggleRegister(event.target.value);
    }

    onPOSChange(event) {
        this.togglePOS(event.target.value);
    }

    // Bind to DOM elements
    bindToDOM() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.onSearchChange.bind(this));
        }

        // Frequency checkboxes
        const freqBands = ['freqBand1', 'freqBand2', 'freqBand3', 'freqBand4', 'freqBand5'];
        freqBands.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.addEventListener('change', this.onFrequencyBandChange.bind(this));
            }
        });

        // Emotion checkboxes
        const emotions = ['emotionPositive', 'emotionNegative', 'emotionNeutral'];
        emotions.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.addEventListener('change', this.onEmotionChange.bind(this));
            }
        });

        // Register checkboxes
        const registers = ['registerFormal', 'registerNeutral', 'registerInformal', 'registerSlang'];
        registers.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.addEventListener('change', this.onRegisterChange.bind(this));
            }
        });

        // POS checkboxes
        const posTags = ['posNoun', 'posVerb', 'posAdj', 'posAdv'];
        posTags.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.addEventListener('change', this.onPOSChange.bind(this));
            }
        });

        // Action buttons
        const applyBtn = document.getElementById('applyFiltersBtn');
        if (applyBtn) {
            applyBtn.addEventListener('click', () => {
                this.data.applyFilters(this.filters);
                window.vocabularyDisplay.render();
            });
        }

        const clearBtn = document.getElementById('clearFiltersBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clear();
                this._updateFilterCheckboxes();
                window.vocabularyDisplay.render();
            });
        }
    }

    _updateFilterCheckboxes() {
        // Update checkboxes to match internal state
        const freqBands = ['freqBand1', 'freqBand2', 'freqBand3', 'freqBand4', 'freqBand5'];
        freqBands.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.checked = this.filters.frequencyBands.includes(checkbox.value);
            }
        });

        const emotions = ['emotionPositive', 'emotionNegative', 'emotionNeutral'];
        emotions.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.checked = this.filters.emotions.includes(checkbox.value);
            }
        });

        const registers = ['registerFormal', 'registerNeutral', 'registerInformal', 'registerSlang'];
        registers.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.checked = this.filters.registers.includes(checkbox.value);
            }
        });

        const posTags = ['posNoun', 'posVerb', 'posAdj', 'posAdv'];
        posTags.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.checked = this.filters.pos.includes(checkbox.value);
            }
        });

        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = this.filters.search;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VocabularyFilters;
}
