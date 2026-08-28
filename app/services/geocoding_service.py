import httpx
from app.config import Config

class GeocodingService:
    @staticmethod
    def search_address(query: str):
        """Autocomplete de endereços restrito a Fortaleza e Ceará usando Nominatim com Debounce/Headers apropriados."""
        url = f"{Config.GEOCODING_API_URL}/search"
        params = {
            'q': f"{query}, Fortaleza, Ceara, Brasil",
            'format': 'json',
            'addressdetails': 1,
            'limit': 5
        }
        headers = {'User-Agent': 'HidroVBus-Fortaleza-App/1.0'}
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    return [{
                        'display_name': item['display_name'],
                        'lat': float(item['lat']),
                        'lon': float(item['lon'])
                    } for item in data]
        except Exception:
            pass
        return []

    @staticmethod
    def reverse_geocode(lat: float, lon: float):
        """Geocodificação reversa para clique no mapa."""
        url = f"{Config.GEOCODING_API_URL}/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        headers = {'User-Agent': 'HidroVBus-Fortaleza-App/1.0'}
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    return data.get('display_name', f"{lat:.4f}, {lon:.4f}")
        except Exception:
            pass
        return f"Coordenadas: {lat:.4f}, {lon:.4f}"