# Maquette One — Leads

Maquette interactive de l'écran Leads de One. Les écrans et les interactions fonctionnent, mais les données sont fictives et rien n'est enregistré : un rechargement de la page remet les valeurs initiales.

Cette maquette a été vibe codée par le product manager, qui n'est pas développeur. Elle sert de référence pour l'écran et les interactions, pas pour le code : son code n'est pas un modèle à suivre.

## Lancer la maquette

Node.js 20 ou plus récent est requis.

```bash
./run.sh
```

Le script installe les dépendances, construit la maquette et la sert sur http://localhost:3001/vente-de-leads. Un autre port se choisit avec `PORT=3002 ./run.sh`.

## Écrans

| Route | Contenu |
|---|---|
| `/vente-de-leads` | Écran Leads : liste des régions, switch On/Off, ajout et modification d'une région, historique |
| `/` | Vue d'ensemble — hors périmètre fonctionnel |
| `/premium` | Premium — hors périmètre fonctionnel |
| `/online` | Online — hors périmètre fonctionnel |

L'ajout d'une région s'ouvre avec le bouton « Ajouter une région » en bas à droite ; la modification, en cliquant sur une carte de région ; l'historique, avec l'icône en haut à droite.

## Organisation du code

```text
pages/vente-de-leads.vue          Écran Leads
components/AddRegionModal.vue     Ajout d'une région, en deux étapes
components/RegionFlowModal.vue    Modification d'une région
components/SurfaceSelector.vue    Sélecteur de tranche de surface
components/FlowHistory.vue        Historique des modifications
data/regions.ts                   Régions administratives et départements
data/zones.ts                     Régions configurées, données fictives
types/domain.ts                   Types partagés
```
