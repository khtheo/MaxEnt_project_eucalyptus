import subprocess
from pathlib import Path

java_exe = Path(r"C:\Program Files\Java\jre1.8.0_471\bin\java.exe")
maxent_jar = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent\maxent.jar")

# Dossiers de données
env_present = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\bioclimatic_var_present")
env_future = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\bioclimatic_var_2080_ssp585")
occ_dir = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\occurences")

output_root = Path(r"C:\Users\THEO\Documents\Projet\PROJET_kaliptus\maxent_results")
output_root.mkdir(parents=True, exist_ok=True)

# Vos 3 espèces (attention à bien nommer vos fichiers CSV de la même manière)
species_list = ["koala", "eucalyptus", "petauroides"]
regularization_multipliers = [0.5, 1.0, 2.0] # Test de différents paramètres de régularisation

for species in species_list:
    occ_file = occ_dir / f"{species}.csv"
    
    for rm in regularization_multipliers:
        exp_name = f"{species}_rm{rm}"
        current_output = output_root / exp_name
        current_output.mkdir(exist_ok=True)
        
        cmd = [
            str(java_exe),
            "-mx2048m",
            "-jar", str(maxent_jar),
            f"samplesfile={occ_file}",
            f"environmentallayers={env_present}",
            f"projectionlayers={env_future}", # Permet de projeter directement sur le climat 2080 !
            f"outputdirectory={current_output}",
            f"betamultiplier={rm}",
            "autorun",
            "outputformat=logistic",
            "randomseed=true"
            "replicas=5", # Validation croisée (folds) demandée par le sujet
            "replicatype=crossvalidate"
        ]
        
        print(f"Exécution de MaxEnt pour : {exp_name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"-> Succès pour {exp_name}")
        else:
            print(f"-> Erreur sur {exp_name} : {result.stderr}")

print("Toutes les modélisations et projections 2080 sont terminées !")