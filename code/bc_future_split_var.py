import rasterio
from pathlib import Path

future_tif = Path("C:/Users/THEO/Documents/Projet/PROJET_kaliptus/original_data/wc2.1_10m_bioc_ACCESS-CM2_ssp585_2081-2100.tif")
output_dir = Path("C:/Users/THEO/Documents/Projet/PROJET_kaliptus/old_data/BioClim variables/wc_biovar2080_tif")
output_dir.mkdir(parents=True, exist_ok=True)

# Correspondance entre le numéro de bande et le nom de la variable Bioclim
# Bande 1 = bio1, Bande 5 = bio5, etc.
target_bands = {
    1: "wc2.1_10m_bio_1",
    5: "wc2.1_10m_bio_5",
    6: "wc2.1_10m_bio_6",
    12: "wc2.1_10m_bio_12",
    14: "wc2.1_10m_bio_14",
    15: "wc2.1_10m_bio_15"
}

with rasterio.open(future_tif) as src:
    for band_num, var_name in target_bands.items():
        # Lecture de la bande spécifique
        data = src.read(band_num)
        
        # Copie des métadonnées et mise à jour pour 1 seule bande
        meta = src.meta.copy()
        meta.update(count=1)
        
        output_file = output_dir / f"{var_name}.tif"
        with rasterio.open(output_file, 'w', **meta) as dst:
            dst.write(data, 1)
        
        print(f"Extraction réussie : {var_name}.tif")

print("Toutes les variables bioclimatiques futures ont été extraites avec succès !")