// TOEFL Vocabulary Classifier - Main Application
// Initializes all modules and handles DOM ready event

let vocabularyData = null;
let vocabularyFilters = null;
let vocabularyDisplay = null;
let vocabularyExport = null;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('TOEFL Vocabulary Classifier initializing...');

    // Initialize modules
    vocabularyData = new VocabularyData();
    vocabularyFilters = new VocabularyFilters(vocabularyData);
    vocabularyDisplay = new VocabularyDisplay(vocabularyData);
    vocabularyExport = new VocabularyExport(vocabularyData);

    // Make modules globally available
    window.vocabularyData = vocabularyData;
    window.vocabularyFilters = vocabularyFilters;
    window.vocabularyDisplay = vocabularyDisplay;
    window.vocabularyExport = vocabularyExport;

    // Also set display for compatibility with filters.js
    window.display = vocabularyDisplay;

    // Show loading state
    vocabularyDisplay.showLoading();

    // Load vocabulary data
    const dataPath = 'data/vocabulary/TOEFL_CLASSIFIED.json';
    const success = await vocabularyData.loadFromJSON(dataPath);

    if (!success) {
        vocabularyDisplay.showError(
            'Could not load vocabulary data. Please run the classifier first:<br><br>' +
            '<code>python process_toefl_words.py</code><br><br>' +
            'Then refresh this page.'
        );
        return;
    }

    console.log(`Loaded ${vocabularyData.words.length} words`);

    // Check if all words are BEYOND (no COCA data)
    const allBeyond = vocabularyData.words.every(word => {
        const band = word.frequency?.band || '';
        return band.includes('BEYOND') || band.includes('beyond');
    });

    if (allBeyond) {
        const dataInfo = document.getElementById('dataInfo');
        if (dataInfo) {
            dataInfo.style.display = 'block';
        }
    }

    // Bind filters to DOM
    vocabularyFilters.bindToDOM();

    // Setup show selected only toggle
    const showSelectedCheckbox = document.getElementById('showSelectedOnly');
    if (showSelectedCheckbox) {
        showSelectedCheckbox.addEventListener('change', () => {
            vocabularyDisplay.toggleShowSelectedOnly();
        });
    }

    // Setup select all button
    const selectAllBtn = document.getElementById('selectAllBtn');
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', () => {
            if (vocabularyData.getSelectedWords().length === vocabularyData.filteredWords.length) {
                // Deselect all
                vocabularyData.clearSelection();
            } else {
                // Select all
                vocabularyData.selectAll();
            }
            vocabularyDisplay.render();
        });
    }

    // Initial render
    vocabularyDisplay.render();

    console.log('TOEFL Vocabulary Classifier ready!');
    console.log('Use filters to narrow down your vocabulary for focused study.');
});

// Utility function to get current filter stats
function getFilterStats() {
    if (!vocabularyData || !vocabularyFilters) {
        return null;
    }

    const total = vocabularyData.filteredWords.length;
    const selected = vocabularyData.getSelectedWords().length;

    return {
        total,
        selected,
        hasFilters: vocabularyFilters.hasFilters(),
        filters: vocabularyFilters.filters
    };
}

// Auto-apply filters on search (with debounce)
let searchTimeout;
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {
                vocabularyFilters.setSearch(e.target.value);
                vocabularyDisplay.render();
            }, 300); // 300ms debounce
        });
    }
});
