import rasterio
from rasterio.features import shapes
import geopandas as gpd
from pathlib import Path

# Chemins
base_dir = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent_results")
input_raster = base_dir / "refuges_rm1_intersection.tif"
output_geojson = base_dir / "zone_parc_ciblee_2080.geojson"

# 1. Lire le raster binaire
with rasterio.open(input_raster) as src:
    image = src.read(1)
    transform = src.transform
    crs = src.crs
    
    # 💡 LE SECRET : Créer un masque pour ne traiter QUE les pixels valides (valeur 1)
    # Cela évite de saturer la mémoire avec le reste de la carte mondiale
    mask = (image == 1)
    
    # Extraire uniquement les polygones des zones viables grâce au masque
    vector_generator = (
        {'properties': {'co_viability': 1}, 'geometry': s}
        for s, v in shapes(image, mask=mask, transform=transform)
    )

# Forcer le CRS si le raster n'en a pas
if crs is None:
    crs = "EPSG:4326"

# 2. Convertir en GeoDataFrame GeoPandas
features_list = list(vector_generator)

if not features_list:
    print("❌ Aucun polygone trouvé. Le masque est vide (aucune zone ne remplit la condition).")
else:
    gdf = gpd.GeoDataFrame.from_features(features_list, crs=crs)
    
    # 3. Reprojeter en coordonnées métriques (EPSG:3577 - Australian Albers) pour les surfaces en km²
    gdf_metric = gdf.to_crs(epsg=3577)
    
    # Calculer la surface de chaque îlot de refuge en km²
    gdf_metric['surface_km2'] = gdf_metric.geometry.area / 10**6
    total_surface = gdf_metric['surface_km2'].sum()
    
    print(f"\n--- BILAN DE LA ZONE DE CONSERVATION ---")
    print(f"Nombre d'îlots de refuges identifiés : {len(gdf)}")
    print(f"Surface totale cumulée : {total_surface:,.2f} km²")
    
    # 4. Sauvegarder le contour final au format GeoJSON
    gdf_final = gdf_metric.to_crs(epsg=4326)
    gdf_final.to_file(output_geojson, driver="GeoJSON")
    
    print(f"✅ Fichier vectoriel du parc enregistré avec succès : {output_geojson.name}")