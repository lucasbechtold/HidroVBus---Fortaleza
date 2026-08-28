function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    setupAutocomplete('origin-input', 'origin-results', 'origin');
    setupAutocomplete('destination-input', 'destination-results', 'destination');

    document.getElementById('search-btn').addEventListener('click', searchRoutes);
});

function setupAutocomplete(inputId, resultsId, type) {
    const input = document.getElementById(inputId);
    const results = document.getElementById(resultsId);

    input.addEventListener('input', debounce((e) => {
        const q = e.target.value.trim();
        if (q.length < 3) {
            results.classList.add('hidden');
            return;
        }

        fetch(`/api/geocode?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                results.innerHTML = '';
                if (!data || data.length === 0) {
                    results.classList.add('hidden');
                    return;
                }
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'p-2 hover:bg-slate-100 cursor-pointer border-b border-slate-100';
                    div.textContent = item.display_name;
                    div.onclick = () => {
                        input.value = item.display_name;
                        input.dataset.lat = item.lat;
                        input.dataset.lon = item.lon;

                        if (type === 'origin') setOriginMarker(item.lat, item.lon);
                        else setDestMarker(item.lat, item.lon);

                        results.classList.add('hidden');
                    };
                    results.appendChild(div);
                });
                results.classList.remove('hidden');
            });
    }, 300));
}

function searchRoutes() {
    const oInput = document.getElementById('origin-input');
    const dInput = document.getElementById('destination-input');
    const container = document.getElementById('results-container');

    let oLat = oInput.dataset.lat || -3.7319;
    let oLon = oInput.dataset.lon || -38.5267;
    let dLat = dInput.dataset.lat || -3.7440;
    let dLon = dInput.dataset.lon || -38.4860;

    container.innerHTML = `
        <div class="p-4 bg-white rounded-lg border text-center text-xs text-slate-500">
            <i class="fa-solid fa-spinner fa-spin mr-2"></i> Mapeando itinerário da linha pelas ruas...
        </div>`;

    const departureTime = document.getElementById('departure-time').value || '13:00';
    const url = `/api/route-search?o_lat=${oLat}&o_lon=${oLon}&d_lat=${dLat}&d_lon=${dLon}&departure=${departureTime}`;

    fetch(url)
        .then(res => res.json())
        .then(response => {
            container.innerHTML = '';
            if (response.status !== 'success' || !response.routes || response.routes.length === 0) {
                container.innerHTML = `<div class="p-4 bg-white rounded-lg border text-xs text-red-500">Não encontramos uma rota de transporte público entre esses locais.</div>`;
                return;
            }

            container.innerHTML += `<div class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-2">Fonte: ${response.data_source_mode}</div>`;

            response.routes.forEach((route) => {
                const card = document.createElement('div');
                card.className = 'bg-white p-4 rounded-xl border border-slate-200 hover:border-brand-green shadow-sm cursor-pointer transition space-y-2 mb-3';
                card.onclick = () => drawRouteOnMap(route.path_coords);

                card.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex items-center space-x-2">
                            <span class="bg-emerald-600 text-white font-bold text-xs px-2 py-1 rounded-md shadow-sm">
                                Linha ${route.line_number}
                            </span>
                            <span class="font-bold text-sm text-slate-800">${route.title}</span>
                        </div>
                        <span class="text-xs font-extrabold text-brand-green bg-emerald-50 px-2 py-0.5 rounded">${route.total_time}</span>
                    </div>
                    <div class="text-xs text-slate-600 space-y-1.5 pt-1">
                        ${route.steps.map(s => `
                            <div class="flex items-start space-x-1.5">
                                <span class="text-slate-400 font-bold">•</span>
                                <span>${s.desc || s.line}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="text-[10px] text-emerald-700 font-medium mt-1 bg-emerald-50/50 p-1 rounded border border-emerald-100">${route.data_type}</div>
                `;
                container.appendChild(card);
            });

            if (response.routes[0] && response.routes[0].path_coords) {
                drawRouteOnMap(response.routes[0].path_coords);
            }
        })
        .catch(err => {
            console.error("Erro na requisição:", err);
            container.innerHTML = `<div class="p-4 bg-white rounded-lg border text-xs text-red-500">Os dados de transporte estão temporariamente indisponíveis. Tente novamente.</div>`;
        });
}