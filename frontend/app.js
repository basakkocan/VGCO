document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const queryInput = document.getElementById('nl-query-input');
    const searchBtn = document.getElementById('search-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');
    const errorBanner = document.getElementById('error-banner');
    const errorMessage = document.getElementById('error-message');
    const sparqlCode = document.getElementById('sparql-code');
    const resultsCount = document.getElementById('results-count');
    const tableContainer = document.getElementById('table-container');
    const copyBtn = document.getElementById('copy-sparql-btn');
    const chips = document.querySelectorAll('.chip');

    // Clipboard Copy for SPARQL
    copyBtn.addEventListener('click', async () => {
        const codeText = sparqlCode.textContent;
        if (!codeText || codeText.startsWith('# Submit')) return;
        
        try {
            await navigator.clipboard.writeText(codeText);
            const originalHTML = copyBtn.innerHTML;
            copyBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                Copied!
            `;
            setTimeout(() => {
                copyBtn.innerHTML = originalHTML;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });

    // Chip click handler
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-query');
            queryInput.value = query;
            executeQuery(query);
        });
    });

    // Button click handler
    searchBtn.addEventListener('click', () => {
        const query = queryInput.value.trim();
        if (query) {
            executeQuery(query);
        }
    });

    // Enter key handler
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const query = queryInput.value.trim();
            if (query) {
                executeQuery(query);
            }
        }
    });

    // Execute query via API
    async function executeQuery(question) {
        // UI Loading State
        setLoading(true);
        errorBanner.classList.add('hidden');
        resultsCount.classList.add('hidden');
        
        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });

            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                // Update SPARQL Query
                sparqlCode.textContent = data.sparql;
                
                // Update Table
                renderResults(data.headers, data.results);
            } else {
                showError(data.error || 'Failed to execute query.');
                if (data.sparql) {
                    sparqlCode.textContent = data.sparql;
                } else {
                    sparqlCode.textContent = '# Query translation failed.';
                }
                renderEmptyState('error');
            }
        } catch (err) {
            showError(err.message || 'A network error occurred.');
            sparqlCode.textContent = '# Connection error.';
            renderEmptyState('error');
        } finally {
            setLoading(false);
        }
    }

    // Toggle loading states
    function setLoading(isLoading) {
        if (isLoading) {
            queryInput.disabled = true;
            searchBtn.disabled = true;
            btnText.textContent = 'Thinking...';
            btnLoader.classList.remove('hidden');
            searchBtn.style.opacity = '0.8';
        } else {
            queryInput.disabled = false;
            searchBtn.disabled = false;
            btnText.textContent = 'Execute Query';
            btnLoader.classList.add('hidden');
            searchBtn.style.opacity = '1';
        }
    }

    // Display error banner
    function showError(msg) {
        errorMessage.textContent = msg;
        errorBanner.classList.remove('hidden');
    }

    // Render results in table
    function renderResults(headers, results) {
        tableContainer.innerHTML = '';
        
        if (!results || results.length === 0) {
            resultsCount.textContent = '0 results';
            resultsCount.classList.remove('hidden');
            renderEmptyState('no-results');
            return;
        }

        resultsCount.textContent = `${results.length} result${results.length > 1 ? 's' : ''}`;
        resultsCount.classList.remove('hidden');

        const table = document.createElement('table');
        
        // Create headers
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Create body
        const tbody = document.createElement('tbody');
        results.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                // Check if it looks like a URL (to make clickable link) or cover art URL
                const cellStr = String(cell);
                if (cellStr.startsWith('http://') || cellStr.startsWith('https://')) {
                    if (cellStr.match(/\.(jpeg|jpg|gif|png|webp)/i)) {
                        td.innerHTML = `<a href="${cellStr}" target="_blank" class="table-img-link">View Image</a>`;
                    } else {
                        td.innerHTML = `<a href="${cellStr}" target="_blank">${cellStr}</a>`;
                    }
                } else {
                    td.textContent = cellStr;
                }
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        tableContainer.appendChild(table);
    }

    // Render empty / helper states
    function renderEmptyState(type) {
        tableContainer.innerHTML = '';
        const emptyDiv = document.createElement('div');
        emptyDiv.className = 'empty-state';

        if (type === 'no-results') {
            emptyDiv.innerHTML = `
                <div class="empty-icon">📭</div>
                <p>No matching games or metadata were found in the ontology for this question.</p>
            `;
        } else if (type === 'error') {
            emptyDiv.innerHTML = `
                <div class="empty-icon">❌</div>
                <p>An error occurred while running the query. See the error banner above for details.</p>
            `;
        }
        
        tableContainer.appendChild(emptyDiv);
    }
});
