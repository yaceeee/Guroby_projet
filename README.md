Auteur : Yacine Znedi
Date : Décembre 2025

Description du projet

Ce projet implémente la résolution du problème “HashCode 2017 – Video Streaming” à l’aide du solveur Gurobi.
Le programme lit un fichier de données, construit un modèle d’optimisation linéaire mixte, l’optimise, et génère un fichier de sortie au format demandé dans l’énoncé.

Contenu du dépôt
	•	videos.py : script Python principal
	•	videos.out : résultat obtenu avec un gap ≤ 0.5 %
	•	videos.mps : modèle exporté au format MPS
	•	requirements.txt : dépendances Python
	•	datasets/ : dossiers contenant les fichiers d’entrée
	•	README.md : description du projet

Installation

Pour installer les dépendances :

pip install -r requirements.txt

Exécution

Pour lancer une optimisation :

python3 videos.py datasets/trending_4000_10k.in

Le programme génère automatiquement deux fichiers :
	•	videos.mps
	•	videos.out

Conformité avec l’énoncé

Le projet respecte les consignes :
	•	Structure du dépôt conforme
	•	Export du modèle en .mps
	•	Génération d’un fichier videos.out valide
	•	Utilisation du solveur Gurobi avec un MIPGap ≤ 0.5 %
	•	Le script accepte un argument : le chemin du dataset