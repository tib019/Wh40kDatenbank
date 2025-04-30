document.addEventListener('DOMContentLoaded', () => {
    // DOM Elemente
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const chapterList = document.getElementById('chapter-list');
    const sortSelect = document.getElementById('sort-select');
    const resetFiltersButton = document.getElementById('reset-filters');
    const statusMessage = document.getElementById('status-message');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Globale Variablen
    let allChapters = [];
    let selectedChapterId = null;

    // Event Listeners
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    sortSelect.addEventListener('change', applySort);
    resetFiltersButton.addEventListener('click', resetFilters);

    // Initialisierung
    loadChapters();

    // Funktionen
    function updateStatus(message) {
        statusMessage.textContent = message;
        console.log(message); // Für Debug-Zwecke
    }

    function showLoading(show = true) {
        if (show) {
            loadingOverlay.classList.add('active');
        } else {
            loadingOverlay.classList.remove('active');
        }
    }

    async function loadChapters() {
        updateStatus('Lade Kapitel...');
        showLoading(true);

        try {
            const response = await fetch('/chapters');
            if (!response.ok) throw new Error('Fehler beim Laden der Kapitel');

            allChapters = await response.json();
            updateStatus(`${allChapters.length} Kapitel geladen`);

            displayChapters(allChapters);

            // Wähle das erste Kapitel aus, wenn verfügbar
            if (allChapters.length > 0) {
                showChapterDetails(allChapters[0].id);
            }
        } catch (error) {
            updateStatus(`Fehler: ${error.message}`);
            console.error(error);
        } finally {
            showLoading(false);
        }
    }

    function displayChapters(chapters) {
        chapterList.innerHTML = '';

        if (chapters.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'chapter-item';
            noResults.textContent = 'Keine Kapitel gefunden';
            chapterList.appendChild(noResults);
            return;
        }

        chapters.forEach(chapter => {
            const chapterItem = document.createElement('div');
            chapterItem.className = 'chapter-item';
            if (selectedChapterId === chapter.id) {
                chapterItem.classList.add('active');
            }
            chapterItem.textContent = chapter.name;
            chapterItem.addEventListener('click', () => showChapterDetails(chapter.id));
            chapterList.appendChild(chapterItem);
        });
    }

    async function showChapterDetails(chapterId) {
        updateStatus(`Lade Details...`);
        showLoading(true);
        selectedChapterId = chapterId;

        // Alle aktiven Elemente zurücksetzen und das neue aktivieren
        const activeItems = document.querySelectorAll('.chapter-item.active');
        activeItems.forEach(item => item.classList.remove('active'));

        try {
            const response = await fetch(`/chapters/${chapterId}`);
            if (!response.ok) throw new Error('Kapitel nicht gefunden');

            const chapter = await response.json();

            // Aktualisiere die UI
            document.getElementById('chapter-name').textContent = chapter.name || 'Unbekannt';
            document.getElementById('homeworld').textContent = chapter.homeworld || 'Unbekannt';
            document.getElementById('leader').textContent = chapter.leader || 'Unbekannt';
            document.getElementById('champion').textContent = chapter.champion || 'Unbekannt';
            document.getElementById('primarch').textContent = chapter.primarch || 'Unbekannt';
            document.getElementById('legion').textContent = chapter.legion || 'Unbekannt';
            document.getElementById('weapons').textContent = chapter.weapons || 'Unbekannt';
            document.getElementById('colors').textContent = chapter.colors || 'Unbekannt';
            document.getElementById('successor').textContent = chapter.successor_chapter || 'Unbekannt';
            document.getElementById('founding-badge').textContent = chapter.founding || 'Unbekannt';
            document.getElementById('description-text').textContent = chapter.description || 'Keine Beschreibung verfügbar.';

            // Bild setzen oder Platzhalter anzeigen
            const imageElement = document.getElementById('chapter-image');
            if (chapter.image_url) {
                imageElement.src = chapter.image_url;
                imageElement.alt = `${chapter.name} Emblem`;
            } else {
                imageElement.src = '/static/placeholder-emblem.png';
                imageElement.alt = 'Kein Bild verfügbar';
            }

            // Details-Bereich sichtbar machen
            document.getElementById('chapter-details').style.display = 'block';

            // Markiere das ausgewählte Kapitel in der Liste
            const selectedItem = Array.from(document.querySelectorAll('.chapter-item'))
                .find(item => item.textContent === chapter.name);
            if (selectedItem) {
                selectedItem.classList.add('active');
            }

            updateStatus(`Details für ${chapter.name} geladen`);
        } catch (error) {
            updateStatus(`Fehler: ${error.message}`);
            console.error(error);
        } finally {
            showLoading(false);
        }
    }

    async function performSearch() {
        const searchTerm = searchInput.value.trim();
        if (!searchTerm) {
            resetFilters();
            return;
        }

        updateStatus(`Suche nach "${searchTerm}"...`);
        showLoading(true);

        try {
            const response = await fetch(`/chapters/name/${searchTerm}`);
            if (!response.ok) throw new Error('Fehler bei der Suche');

            const results = await response.json();
            displayChapters(results);

            if (results.length > 0) {
                showChapterDetails(results[0].id);
                updateStatus(`${results.length} Kapitel gefunden`);
            } else {
                updateStatus('Keine Kapitel gefunden');
            }
        } catch (error) {
            updateStatus(`Fehler: ${error.message}`);
            console.error(error);
        } finally {
            showLoading(false);
        }
    }

    function applySort() {
        const sortValue = sortSelect.value;
        let sortedChapters = [...allChapters];

        switch (sortValue) {
            case 'name-asc':
                sortedChapters.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'name-desc':
                sortedChapters.sort((a, b) => b.name.localeCompare(a.name));
                break;
            case 'founding-asc':
                sortedChapters.sort((a, b) => {
                    // Behandle 'Unbekannt' als letztes
                    if (!a.founding && !b.founding) return 0;
                    if (!a.founding) return 1;
                    if (!b.founding) return -1;
                    return a.founding.localeCompare(b.founding);
                });
                break;
            case 'founding-desc':
                sortedChapters.sort((a, b) => {
                    if (!a.founding && !b.founding) return 0;
                    if (!a.founding) return 1;
                    if (!b.founding) return -1;
                    return b.founding.localeCompare(a.founding);
                });
                break;
        }

        displayChapters(sortedChapters);
        updateStatus('Sortierung angewendet');
    }

    function resetFilters() {
        searchInput.value = '';
        sortSelect.value = 'name-asc';
        loadChapters();
    }

    // Hilfsmethode, um Errors bei fehlenden Bildern zu behandeln
    document.getElementById('chapter-image').addEventListener('error', function() {
        this.src = '/static/placeholder-emblem.png';
        this.alt = 'Bild nicht verfügbar';
    });
});