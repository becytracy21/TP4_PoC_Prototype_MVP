# TP4 — PoC / Prototype / MVP

Ce dossier contient :

- **yrr_poc** : preuve de concept  
- **yrr_prototype** : prototype HTML/CSS  
- **yrr_mvp** : version MVP fonctionnelle (Svelte + Django + MongoDB)

---

## 🐳 Démarrage avec Docker Desktop

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé

### Lancer l'application

```bash
docker compose up --build
```

Cette commande démarre les 3 services :

| Service   | URL d'accès                 |
|-----------|-----------------------------|
| Frontend  | http://localhost:5173       |
| Backend   | http://localhost:8000/api   |
| MongoDB   | localhost:27017 (debug)     |

### Après un redémarrage de session (poste école)

Docker Desktop repart à zéro entre les sessions. Il suffit de relancer :

```bash
docker compose up --build
```

Toutes les dépendances sont réinstallées automatiquement. Les données MongoDB sont persistées dans un volume Docker (`mongo_data`) qui survit aux redémarrages de container, mais est perdu si Docker Desktop lui-même est réinitialisé.

### Commandes utiles

```bash
# Voir les logs en temps réel
docker compose logs -f

# Arrêter les services
docker compose down

# Supprimer les volumes (données MongoDB) et repartir de zéro
docker compose down -v

# Supprimer les images inutilisées
docker image prune
```
