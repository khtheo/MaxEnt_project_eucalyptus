import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import numpy as np

# Chemin vers ton fichier .asc de sortie MaxEnt
asc_file = r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\refuges_climatiques_mondial_2080.asc"
with rasterio.open(asc_file) as src:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Lire les données et masquer les valeurs négatives (NoData de MaxEnt)
    data = src.read(1)
    data_masked = np.ma.masked_where(data < 0, data)
    
    # Afficher la carte avec les coordonnées géographiques réelles (grâce à src.transform)
    show(data_masked, transform=src.transform, ax=ax, cmap='terrain', vmin=0, vmax=1)
    
    # --- AJOUT DE LA COLORBAR ---
    im = ax.get_images()[0]  # Récupère l'affichage raster de la carte
    fig.colorbar(im, ax=ax, label="Suitability (0 to 1)", shrink=0.7)
    
    plt.title("Refuges climatiques Elapid - 2080", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    
    # Optionnel : réactiver les axes pour voir les frontières de l'Australie en coordonnées
    # plt.grid(True, linestyle='--', alpha=0.5)
    
    # Sauvegarder l'image propre pour ton rapport LaTeX
    plt.savefig(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\img\refuges_climatiques_mondial_2080.png", dpi=300, bbox_inches='tight')
    plt.show()














# import matplotlib.pyplot as plt
# import rasterio
# from rasterio.plot import show
# import numpy as np

# # Chemin vers ton fichier .tif final (après binarisation/intersection)
# tif_file = r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent_results\refuges_rm1_intersection.tif"

# with rasterio.open(tif_file) as src:
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # 1. Lire les données du fichier TIF
#     data = src.read(1)
    
#     # 2. Gérer le masque (NoData ou zones à 0)
#     # Si ton fichier binaire a des 0 pour les zones non-retenues et des 1 pour les refuges :
#     # On masque les valeurs <= 0 pour qu'elles apparaissent transparentes
#     data_masked = np.ma.masked_where(data <= 0, data)
    
#     # 3. Afficher la carte avec les coordonnées géographiques réelles
#     # 'viridis' ou 'cividis' fonctionnent très bien pour des cartes binaires ou continues
#     show(data_masked, transform=src.transform, ax=ax, cmap='terrain', vmin=0, vmax=1)
    
#     # --- AJOUT DE LA COLORBAR ---
#     im = ax.get_images()[0]  
#     fig.colorbar(im, ax=ax, label="Adéquation / Refuges (0 à 1)", shrink=0.7)
    
#     # Habillage
#     plt.title("Refuges climatiques - 2080 (Données TIF)", fontsize=14)
#     ax.set_xlabel("Longitude")
#     ax.set_ylabel("Latitude")
#     plt.grid(True, linestyle='--', alpha=0.5)
    
#     # Sauvegarder l'image propre pour ton rapport LaTeX
#     output_path = r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\carte_tif_propre.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     print(f"Carte TIF sauvegardée ici : {output_path}") 
#     plt.show()




# import matplotlib.pyplot as plt
# import rasterio
# from rasterio.plot import show
# import numpy as np

# # Chemin vers ton fichier .tif final (après binarisation/intersection)
# tif_file = r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent_results\refuges_rm1_intersection.tif"
# with rasterio.open(tif_file) as src:
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # 1. Lire les données du fichier TIF
#     data = src.read(1)
    
#     # 2. Masquer uniquement les valeurs invalides (NoData de rasterio, souvent -9999 ou NaN)
#     # On ne touche pas aux 0 pour garder un fond propre
#     nodata_val = src.nodatavals[0]
#     if nodata_val is not None:
#         data_masked = np.ma.masked_equal(data, nodata_val)
#     else:
#         data_masked = data

#     # Pour les zones à 0 (non-refuges), on peut les masquer pour qu'elles soient transparentes, 
#     # mais on utilise un colormap bien visible pour les refuges (ex: 'Reds')
#     data_masked = np.ma.masked_where(data_masked <= 0, data_masked)
    
#     # 3. Afficher avec une couleur vive (ex: 'Reds') pour les refuges
#     ax.set_facecolor('#f0f0f0')  # Fond gris clair pour contraster
    
#     show(data_masked, transform=src.transform, ax=ax, cmap='Reds', vmin=0, vmax=1)
    
#     # --- AJOUT DE LA COLORBAR ---
#     im = ax.get_images()[0]  
#     fig.colorbar(im, ax=ax, label="Présence de Refuges (0 ou 1)", shrink=0.7)
    
#     # Habillage
#     plt.title("Refuges climatiques - 2080 (Intersection)", fontsize=14)
#     ax.set_xlabel("Longitude")
#     ax.set_ylabel("Latitude")
#     plt.grid(True, linestyle='--', alpha=0.5)
    
#     # Sauvegarder l'image propre pour ton rapport LaTeX
#     output_path = r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\carte_tif_visible.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     print(f"Carte TIF sauvegardée ici : {output_path}")
    
#     plt.show()