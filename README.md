# 🗺️ L'Épopée des Cités Perdues

> Moteur de jeu RPG textuel en Python — bac à sable technique pour l'apprentissage des pratiques MLOps et Software Engineering.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2%20%2B%20RDS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
[![Python package](https://github.com/SimonGallien/epopee-des-cites-perdues/actions/workflows/ci.yml/badge.svg)](https://github.com/SimonGallien/epopee-des-cites-perdues/actions/workflows/ci.yml)

---

## 🎯 Objectif du projet

Ce projet est avant tout un **bac à sable technique (Proof of Concept)** conçu pour pratiquer une chaîne complète de développement logiciel professionnel. Le jeu RPG textuel est le prétexte — l'architecture et les outils sont l'objectif.

### Ce que ce projet adresse

| Compétence | Outil / Pratique |
|---|---|
| Architecture logicielle | MVC strict, séparation des responsabilités |
| Persistance des données | PostgreSQL + SQLAlchemy 2.0 (ORM moderne) |
| Tests unitaires | Pytest + unittest.mock |
| Containerisation | Docker + Docker Compose |
| API REST | FastAPI ✅ |
| CI/CD | GitHub Actions ✅ |
| Déploiement cloud | AWS EC2 + RDS ✅ |
| Gestion des dépendances | `uv` (packaging moderne Python) |

---

## 🎮 Le jeu — fonctionnalités V1

Le joueur incarne un explorateur chargé de redonner vie à des mondes oubliés.

- Création de profil joueur avec validation métier
- Génération du monde (Lieux, Personnages, Ressources) via PostgreSQL
- Système de voyage et d'exploration
- Gestion d'inventaire avec récolte de ressources
- Sauvegarde et chargement de parties
- Interface terminal ergonomique (navigation aux flèches via `questionary`)

---

## 🌐 API REST — déployée sur AWS

L'API FastAPI est accessible en ligne :

**Documentation interactive (Swagger) :** [http://35.180.140.255:8000/docs](http://35.180.140.255:8000/docs)

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/lieux` | Liste tous les lieux avec inventaire |
| GET | `/personnages` | Liste tous les personnages |
| GET | `/joueurs` | Liste tous les joueurs |
| GET | `/joueurs/{id}` | Récupère un joueur par id |
| POST | `/joueurs` | Crée un nouveau joueur |
| PUT | `/joueurs/{id}` | Met à jour un joueur |
| DELETE | `/joueurs/{id}` | Supprime un joueur |

---

## 🧠 Architecture

### Structure du projet
```
epopee-des-cites-perdues/
├── src/
│   ├── __init__.py
│   ├── modeles.py       # Entités SQLAlchemy (Joueur, Lieu, Ressource...)
│   ├── moteur.py        # Contrôleur — logique du jeu
│   ├── vue.py           # Vue console — toute l'UI terminal
│   └── erreur.py        # Exceptions métier personnalisées
├── app/
│   ├── __init__.py
│   ├── main.py          # Point d'entrée FastAPI
│   ├── schemas.py       # Schemas Pydantic
│   └── routers/
│       ├── lieux.py
│       ├── personnages.py
│       └── joueurs.py
├── scripts/
│   ├── init_db.py       # Configuration SQLAlchemy + création des tables
│   └── seed.py          # Initialisation des données en base
├── tests/
│   ├── __init__.py
│   └── test_moteur.py   # Tests unitaires Pytest
├── data/
│   └── data.json        # Contenu du jeu (lieux, personnages, ressources)
├── .github/
│   └── workflows/
│       ├── ci.yml       # Pipeline CI — tests automatiques
│       └── cd.yml       # Pipeline CD — déploiement AWS
├── main.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── pyproject.toml
└── .env                 # Variables d'environnement (non versionné)
```

### Architecture cloud
```
Internet → EC2 (FastAPI + Docker) → RDS (PostgreSQL 17)
```

### Pattern MVC — séparation stricte
```
Vue (vue.py)           →  Uniquement print() et questionary
                               ↕
Contrôleur (moteur.py) →  Logique du jeu, aucun print() direct
                               ↕
Modèle (modeles.py)    →  Entités, règles métier, intégrité des données
```

### Schéma de base de données
```
Joueur ──────────────── RessourceJoueur ──── Ressource
Lieu  ──────────────── RessourceLieu   ──── Ressource
Personnage ─────────── RessourcePersonnage ─ Ressource
```

Les tables de liaison portent le champ `quantite`, ce qui permet de modéliser proprement les inventaires sans colonne JSON.

---

## 🚀 Installation et lancement

### Prérequis

- [Python 3.14+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) — gestionnaire de paquets moderne
- [Docker](https://www.docker.com/) + Docker Compose

### 1. Cloner le repo
```bash
git clone https://github.com/SimonGallien/epopee-des-cites-perdues.git
cd epopee-des-cites-perdues
```

### 2. Installer les dépendances
```bash
uv sync
```

### 3. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditez .env avec vos valeurs
```
```env
DB_USER=postgres
DB_PASSWORD=postgres
POSTGRES_DB=epopee
DB_HOST=localhost
DB_PORT=5432
```

### 4. Lancer la base de données et l'app
```bash
docker compose up -d
```

### 5. Lancer le jeu
```bash
uv run main.py
```

---

## 🧪 Tests
```bash
uv run pytest
```
```bash
uv run pytest -v          # Mode verbose
uv run pytest --tb=short  # Traceback court
```

### Stratégie de test

Les tests unitaires isolent chaque comportement via `unittest.mock.MagicMock` pour ne jamais dépendre d'une vraie base de données ou d'une interaction terminal.
```python
# Exemple — tester le routing du menu sans I/O réel
ma_partie.vue.afficher_menu_accueil = MagicMock(return_value="1")
ma_partie.nouveau_joueur = MagicMock()
ma_partie.menu_accueil()
ma_partie.nouveau_joueur.assert_called_once()
```

---

## 🛣️ Roadmap

- [x] Architecture MVC
- [x] Modèles SQLAlchemy 2.0
- [x] Docker Compose + PostgreSQL
- [x] Tests unitaires Pytest
- [x] Migration JSON → PostgreSQL
- [x] API REST FastAPI — CRUD joueurs, lieux, personnages
- [x] CI/CD GitHub Actions
- [x] Déploiement AWS (EC2 + RDS)
- [ ] Prometheus + Grafana (monitoring)
- [ ] Inventaire joueur via API