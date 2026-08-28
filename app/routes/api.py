from flask import Blueprint, request, jsonify
from app.services.geocoding_service import GeocodingService
from app.services.transport_data_service import TransportDataService
from app.utils.router import RoutePlanner

api_bp = Blueprint('api', __name__)
transport_service = TransportDataService()

@api_bp.route('/geocode', methods=['GET'])
def geocode():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = GeocodingService.search_address(query)
    return jsonify(results)

@api_bp.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        address = GeocodingService.reverse_geocode(lat, lon)
        return jsonify({"address": address, "lat": lat, "lon": lon})
    except Exception as e:
        return jsonify({"error": f"Parâmetros inválidos: {str(e)}"}), 400

@api_bp.route('/route-search', methods=['GET', 'POST'])
def route_search():
    try:
        # Pega parâmetros da URL ou usa padrões do Centro de Fortaleza
        o_lat = float(request.args.get('o_lat', -3.7319))
        o_lon = float(request.args.get('o_lon', -38.5267))
        d_lat = float(request.args.get('d_lat', -3.7440))
        d_lon = float(request.args.get('d_lon', -38.4860))
        dep_time = request.args.get('departure', '13:00')

        print(f"--> [BUSCA DE ROTA] Origem: ({o_lat}, {o_lon}) | Destino: ({d_lat}, {d_lon})")

        routes = RoutePlanner.calculate_routes(o_lat, o_lon, d_lat, d_lon, dep_time)
        stops_info = transport_service.get_stops_near(o_lat, o_lon)

        return jsonify({
            "status": "success",
            "data_source_mode": stops_info.get("source", "GTFS Oficial Fortaleza"),
            "routes": routes
        })
    except Exception as e:
        print(f"--> [ERRO NO ROUTE-SEARCH]: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Erro interno ao buscar rota: {str(e)}"
        }), 500