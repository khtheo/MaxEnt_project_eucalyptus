import rasterio
import numpy as np
from pathlib import Path

# Dossier contenant vos fichiers .tif (ex: bio1.tif, bio5.tif, etc.)
input_dir = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\tif_input")
# Dossier où seront enregistrés les fichiers .asc
output_dir = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\asc_output")

output_dir.mkdir(parents=True, exist_ok=True)

NODATA_VAL = -9999

# Boucle sur tous les fichiers .tif du dossier
for input_tif in input_dir.glob("*.tif"):
    # Crée le nom du fichier de sortie .asc en gardant le même nom de base (ex: bio1.asc)
    output_asc = output_dir / f"{input_tif.stem}.asc"
    
    with rasterio.open(input_tif) as src:
        meta = src.meta.copy()

        # 1. Lire la bande 1 (vos fichiers extraits n'ont qu'une seule bande)
        data = src.read(1)

        # 2. Remplacer les NaN par une valeur nodata numérique
        data = np.where(np.isnan(data), NODATA_VAL, data)

        # 3. Configurer l'export pour le format ASCII Grid (AAIGrid)
        meta.update(
            driver="AAIGrid",
            count=1,
            dtype="float32",
            nodata=NODATA_VAL
        )

        # 4. Ecrire le fichier .asc
        with rasterio.open(output_asc, 'w', **meta) as dst:
            dst.write(data, 1)

    print(f"Conversion réussie : {input_tif.name} -> {output_asc.name}")

print("Toutes les conversions en .asc sont terminées avec succès !")