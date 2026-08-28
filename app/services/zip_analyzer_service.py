import zipfile
import os
import pandas as pd

class GoogleZipAnalyzerService:
    """Serviço para análise e extração de dados do GTFS (arquivos_google.zip)."""
    
    def __init__(self, zip_path):
        self.zip_path = zip_path

    def inspect_and_extract(self):
        if not os.path.exists(self.zip_path):
            return {"status": "error", "message": "Arquivo ZIP não encontrado."}
        
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as z:
                files = z.namelist()
                return {
                    "status": "success",
                    "total_files": len(files),
                    "files": files
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_shape_coordinates(self, shape_id):
        """Retorna a sequência exata de coordenadas [lat, lon] do shape_id."""
        if not os.path.exists(self.zip_path) or not shape_id:
            return []

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as z:
                shape_files = [f for f in z.namelist() if f.endswith('shapes.txt')]
                if not shape_files:
                    return []

                with z.open(shape_files[0]) as f:
                    df = pd.read_csv(f, dtype=str)  # Lê tudo como string para evitar inconsistência de tipo
                    df.columns = df.columns.str.strip()
                    
                    df_shape = df[df['shape_id'].str.strip() == str(shape_id).strip()]
                    if df_shape.empty:
                        return []
                    
                    # Converte sequência e coordenadas para tipos numéricos
                    df_shape['shape_pt_sequence'] = pd.to_numeric(df_shape['shape_pt_sequence'])
                    df_shape['shape_pt_lat'] = pd.to_numeric(df_shape['shape_pt_lat'])
                    df_shape['shape_pt_lon'] = pd.to_numeric(df_shape['shape_pt_lon'])
                    
                    df_sorted = df_shape.sort_values(by='shape_pt_sequence')
                    
                    # Retorna lista de pares [lat, lon]
                    return df_sorted[['shape_pt_lat', 'shape_pt_lon']].values.tolist()
        except Exception as e:
            print(f"Erro ao extrair shape {shape_id}: {e}")
            return []

    def get_route_info(self, route_short_name=None):
        """Recupera informações da rota e o shape_id associado."""
        if not os.path.exists(self.zip_path):
            return None

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as z:
                routes_files = [f for f in z.namelist() if f.endswith('routes.txt')]
                trips_files = [f for f in z.namelist() if f.endswith('trips.txt')]

                if not routes_files or not trips_files:
                    return None

                with z.open(routes_files[0]) as f_routes, z.open(trips_files[0]) as f_trips:
                    df_routes = pd.read_csv(f_routes, dtype=str)
                    df_trips = pd.read_csv(f_trips, dtype=str)

                    df_routes.columns = df_routes.columns.str.strip()
                    df_trips.columns = df_trips.columns.str.strip()

                    if route_short_name:
                        matched = df_routes[df_routes['route_short_name'].str.strip() == str(route_short_name).strip()]
                        if matched.empty:
                            matched = df_routes.iloc[[0]]
                    else:
                        matched = df_routes.iloc[[0]]

                    route_id = matched.iloc[0]['route_id']
                    short_name = matched.iloc[0].get('route_short_name', '026')
                    long_name = matched.iloc[0].get('route_long_name', f"Linha {short_name}")
                    
                    trips_matched = df_trips[df_trips['route_id'].str.strip() == str(route_id).strip()]
                    shape_id = trips_matched.iloc[0]['shape_id'] if not trips_matched.empty else None

                    return {
                        "route_id": route_id,
                        "short_name": short_name,
                        "long_name": long_name,
                        "shape_id": shape_id
                    }
        except Exception as e:
            print(f"Erro ao ler informações da rota: {e}")
            return None