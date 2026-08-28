let map, originMarker, destMarker, routePolyline;

document.addEventListener('DOMContentLoaded', () => {
    // Inicializa o mapa centralizado em Fortaleza
    map = L.map('map').setView([-3.7319, -38.5267], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Seleção com clique duplo no mapa
    map.on('dblclick', function(e) {
        const { lat, lng } = e.latlng;
        
        const originInput = document.getElementById('origin-input');
        const destInput = document.getElementById('destination-input');

        // Se a origem ainda não estiver definida, define a origem; caso contrário, o destino
        if (!originInput.dataset.lat) {
            setOriginMarker(lat, lng);
            reverseGeocode(lat, lng, 'origin');
        } else {
            setDestMarker(lat, lng);
            reverseGeocode(lat, lng, 'destination');
        }
    });
});

function setOriginMarker(lat, lng) {
    if (originMarker) map.removeLayer(originMarker);
    originMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'custom-icon-origin',
            html: '<i class="fa-solid fa-circle-dot text-emerald-600 text-2xl"></i>',
            iconSize: [24, 24]
        })
    }).addTo(map);

    const originInput = document.getElementById('origin-input');
    originInput.dataset.lat = lat;
    originInput.dataset.lon = lng;
}

function setDestMarker(lat, lng) {
    if (destMarker) map.removeLayer(destMarker);
    destMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'custom-icon-dest',
            html: '<i class="fa-solid fa-location-dot text-red-600 text-2xl"></i>',
            iconSize: [24, 24]
        })
    }).addTo(map);

    const destInput = document.getElementById('destination-input');
    destInput.dataset.lat = lat;
    destInput.dataset.lon = lng;
}

function drawRouteOnMap(coords) {
    if (routePolyline) map.removeLayer(routePolyline);
    if (!coords || coords.length === 0) return;

    routePolyline = L.polyline(coords, { color: '#00A859', weight: 5 }).addTo(map);
    map.fitBounds(routePolyline.getBounds(), { padding: [50, 50] });
}

function reverseGeocode(lat, lon, target) {
    fetch(`/api/reverse-geocode?lat=${lat}&lon=${lon}`)
        .then(res => res.json())
        .then(data => {
            if (target === 'origin') {
                document.getElementById('origin-input').value = data.address || `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
            } else {
                document.getElementById('destination-input').value = data.address || `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
            }
        })
        .catch(() => {
            if (target === 'origin') {
                document.getElementById('origin-input').value = `Local Selecionado (${lat.toFixed(4)}, ${lon.toFixed(4)})`;
            } else {
                document.getElementById('destination-input').value = `Local Selecionado (${lat.toFixed(4)}, ${lon.toFixed(4)})`;
            }
        });
}