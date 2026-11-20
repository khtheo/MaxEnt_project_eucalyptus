import rasterio
import numpy as np
from pathlib import Path

# Dossier principal et sous-dossier rm1
base_dir = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent_results")

# Chemins vers tes fichiers .asc (adapte les noms si besoin selon tes sous-dossiers)
path_koala = base_dir / "koala_rm1.0" / "Phascolarctos_cinereus.asc"
path_euc = base_dir / "eucalyptus_rm1.0" / "Eucalyptus_viminalis.asc"
path_peta = base_dir / "petauroides_rm1.0" / "Petauroides_volans.asc"
output_raster = base_dir / "refuges_rm1_intersection.tif"

# 1. Ouvrir et lire les 3 rasters rm1
with rasterio.open(path_koala) as src_k, \
     rasterio.open(path_euc) as src_e, \
     rasterio.open(path_peta) as src_p:
     
    koala_arr = src_k.read(1)
    euc_arr = src_e.read(1)
    peta_arr = src_p.read(1)
    profile = src_k.profile

# 2. Binarisation (Seuil à 0.5)
threshold = 0.5
koala_bin = (koala_arr >= threshold).astype(int)
euc_bin = (euc_arr >= threshold).astype(int)
peta_bin = (peta_arr >= threshold).astype(int)

# 3. Intersection (ET logique : les zones où les 3 espèces coexistent sous rm1)
refuge_grid = (koala_bin * euc_bin * peta_bin)

# 4. Sauvegarder le résultat de l'intersection en GeoTIFF
profile.update(dtype=rasterio.int32, count=1, nodata=-9999)
with rasterio.open(output_raster, 'w', **profile) as dst:
    dst.write(refuge_grid.astype(rasterio.int32), 1)

# 5. Compter les pixels pour un premier aperçu de la surface
pixel_count = np.sum(refuge_grid == 1)
print(f"✅ Intersection rm1 exécutée avec succès !")
print(f"Nombre de pixels de refuges communs : {pixel_count}")