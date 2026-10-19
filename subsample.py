import pandas as pd
fichier = "/Users/THEO/Documents/Projet/PROJET_kaliptus/petauroides/0005928-260928105237408.csv"

df = pd.read_csv(fichier, sep='\t', low_memory=False)

# Définir la taille de la grille 
cell_size = 0.16667

df = df.dropna(subset=['decimalLongitude', 'decimalLatitude'])

df['grid_x'] = (df['decimalLongitude'] / cell_size).astype(int)
df['grid_y'] = (df['decimalLatitude'] / cell_size).astype(int)

# Ne garder qu'un point par cellule
df_clean = df.drop_duplicates(subset=['grid_x', 'grid_y'])

# Exporter pour Maxent
df_clean[['species', 'decimalLongitude', 'decimalLatitude']].to_csv("petauroides.csv", index=False)