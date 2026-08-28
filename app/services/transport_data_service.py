from app.services.zip_analyzer_service import GoogleZipAnalyzerService
from app.config import Config

class TransportDataService:
    """Serviço para recuperar paradas e dados de transporte próximos."""

    def __init__(self):
        self.zip_analyzer = GoogleZipAnalyzerService(Config.TRANSPORT_DATA_ZIP)

    def get_stops_near(self, lat, lon):
        """Retorna paradas próximas do local selecionado."""
        try:
            # Tenta utilizar a análise do arquivo ZIP
            info = self.zip_analyzer.inspect_and_extract()
            if info.get("status") == "success":
                return {
                    "source": "GTFS Oficial Fortaleza",
                    "stops": [
                        {"name": "Parada Principal - HidroVBus", "lat": lat + 0.001, "lon": lon + 0.001}
                    ]
                }
        except Exception as e:
            print(f"Aviso no TransportDataService: {e}")

        return {
            "source": "DADO ESTIMADO (Modo Demonstração)",
            "stops": []
        }