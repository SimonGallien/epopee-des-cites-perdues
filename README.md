# 🗺️ L'Épopée des Cités Perdues

**L'Épopée des Cités Perdues** est un jeu de rôle (RPG) textuel développé en Python. Le joueur incarne un explorateur chargé de redonner vie à des mondes oubliés. Il doit voyager à travers différentes contrées, gérer son inventaire, récolter des ressources et survivre face aux ennemis.

Au-delà de l'aspect ludique, ce projet sert de **bac à sable technique** (Proof of Concept) pour expérimenter et valider des concepts d'architecture logicielle de niveau professionnel.

---

## 🚀 Fonctionnalités du jeu (V1)
- Création de profil de joueur robuste.
- Génération du monde (Lieux, Monstres, Ressources) dynamiquement via un fichier `data.json`.
- Système de voyage et d'exploration.
- Gestion d'inventaire.
- Interface utilisateur ergonomique dans le terminal (navigation aux flèches via `questionary`).

---

## 🧠 Démarche de Conception & Architecture

Ce projet a été conçu avec une attention particulière portée aux bonnes pratiques de l'ingénierie logicielle et du **Clean Code** :

*   **Architecture MVC (Modèle-Vue-Contrôleur) stricte :**
    *   **Modèle (`modeles.py`) :** Les entités (`Joueur`, `Lieu`, `Ressource`) gèrent leur propre intégrité.
    *   **Vue (`vue.py`) :** Séparation totale de l'interface (UI). Le moteur logique ne contient aucun `print()` ni `input()`.
    *   **Contrôleur (`moteur.py`) :** Orchestre la logique du jeu sans interagir directement avec le joueur.
*   **Séparation des responsabilités (Data vs Logic) :** L'intégralité du contenu du jeu est externalisée dans des fichiers `.json`. Le code Python agit comme un moteur universel capable de charger n'importe quel univers.
*   **Robustesse et Gestion des erreurs :** Création d'Exceptions personnalisées (ex: `NomInvalideError`) pour gérer les règles métier directement au niveau des modèles, garantissant une application anti-crash.

---

## 🛠️ Installation et Lancement

Ce projet utilise l'outil moderne de gestion de paquets Python `uv`.