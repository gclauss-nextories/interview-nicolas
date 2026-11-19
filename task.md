# Exercice : piloter la vente de leads par région

## Contexte

Nextories reçoit des demandes de déménagement de particuliers. Une partie de ces demandes est vendue comme **lead** à plusieurs déménageurs partenaires, qui recontactent ensuite le client : c'est la **vente de leads**.

One est l'outil interne avec lequel l'équipe pilote la répartition des demandes. Cet exercice porte sur son écran **Leads**, qui permet de régler, région par région, quelles demandes partent en vente de leads.

## User story

En tant que Head of, je souhaite ajuster les règles de vente de leads par région de départ afin d'adapter le flux aux besoins de l'activité, sans intervention technique.

## Ce qui est attendu

Rendre fonctionnel l'écran Leads de la maquette (`mockup/`, route `/vente-de-leads`), avec un backend qui stocke la configuration et l'applique.

### Écran Leads

- Afficher les régions configurées, avec pour chacune : ses départements, ses seuils Court, Moyen et Long.
- Activer ou désactiver la vente de leads dans une région avec le switch On/Off. Une région désactivée passe en bas de la liste.
- Ajouter une région dans une modale en deux étapes : choix de la région et de ses départements, puis configuration de ses seuils.
- Modifier les départements et les règles d'une région dans une modale.
- Consulter l'historique des versions de la configuration (voir plus bas).

### Réglages d'une région

- **Départements éligibles** : limités aux départements de la région administrative.
- **Court** (distance inférieure à 100 km) : surface maximale vendue en lead.
- **Moyen** (distance de 100 km inclus à moins de 300 km) : surface maximale vendue en lead.
- **Long** (distance de 300 km et plus) : surface maximale vendue en lead.

Les surfaces reprennent les tranches du formulaire du site : moins de 30, 30–50, 50–80, 80–120, 120–180 et plus de 180 m². Chaque distance peut aussi être désactivée.

### Orientation des demandes

La configuration doit être réellement utilisée : le backend expose un moyen de savoir si une demande part en vente de leads. Une demande est décrite par son département de départ, sa distance en km et sa tranche de surface.

Une demande part en vente de leads si :

- son département de départ appartient à une région active ;
- sa distance (Court, Moyen ou Long) n'est pas désactivée dans cette région et sa tranche de surface ne dépasse pas le seuil de cette distance.

### Historique des versions

La configuration Leads a besoin d'un historique des versions. La maquette en montre le point d'entrée, l'icône en haut à droite de l'écran Leads, avec un historique vide.

Le contenu de cet historique et ce qu'on peut en faire sont à votre appréciation.

### Critères d'acceptation

- Les configurations affichées viennent du backend et sont conservées après rechargement.
- Chaque région se configure indépendamment des autres.
- L'ajout d'une région demande au moins un département appartenant à cette région ; le backend le vérifie aussi.
- Annuler une modale ne modifie pas la configuration.
- Pendant la modification des curseurs, le réglage précédent reste discrètement identifiable.
- Une région désactivée ne reçoit plus de demandes orientées vers la vente de leads.
- Les seuils enregistrés sont effectivement utilisés pour l'orientation.
- Les erreurs de lecture ou d'enregistrement sont signalées à l'utilisateur.

## Hors périmètre

- **L'authentification** : pas d'écran de connexion, pas de comptes, pas de gestion des droits. La maquette n'en contient pas.
- Les écrans Vue d'ensemble, Premium et Online : ils apparaissent dans la navigation de la maquette, marqués « Hors périmètre fonctionnel ».
- Les contrats et la tarification des leads.

## Stack imposée

| Partie | Imposé |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Base de données | MySQL |
| Frontend | Vue 3, Vite, TypeScript |

Pour information, les applications existantes (One et l'API Nextories) tournent sur Python 3.14, Django 5.2, Django REST Framework 3.17, MySQL 8.0, Vue 3.5 avec Vite, TypeScript, Pinia, Vue Router et axios, et sont outillées avec uv, pytest-django et ruff. S'aligner sur ces versions et ces outils est bienvenu, sans être obligatoire.

## La maquette

`mockup/` contient la maquette de l'écran, avec des données fictives et sans backend : rien n'est enregistré, un rechargement remet les valeurs initiales. Son `README.md` explique comment la lancer.

Cette maquette a été vibe codée par le product manager, qui n'est pas développeur. Elle fait référence pour l'écran et les interactions, pas pour le code. Le code présenté dans votre PR doit être du niveau attendu d'un développeur, pas de celui d'une maquette de product manager : vous pouvez vous en inspirer, mais pas la recopier telle quelle.

La liste des régions administratives et de leurs départements est dans `mockup/data/regions.ts`.

## Le code en production

Le système est actuellement constitué d'une quinzaine d'applications toutes interconnectées. Le code qui décide de l'orientation des demandes tourne sur le serveur de l'une d'elles, et il doit maintenant lire la configuration depuis le serveur de One, via une API.

`legacy/meeting_utils.py` est le fichier utilisé aujourd'hui en production pour appliquer ces règles : les règles de vente de leads y sont codées en dur. Dans ce code, la vente de leads s'appelle `MER`.

Le volume estimé, en m³, n'est pas un critère de la vente de leads : il ne doit pas être pris en compte, ni dans One, ni dans la nouvelle version de `meeting_utils.py`.

Le fichier est copié en entier, y compris le code qui ne concerne pas la vente de leads. Les modules qu'il importe ne sont pas fournis.

## Livrables

- Le code du backend et du frontend dans ce dépôt.
- Un `README.md` qui permet de lancer le projet depuis un poste vierge.
- Un niveau de qualité prêt pour la production.
- Une nouvelle version de `legacy/meeting_utils.py`, dans la ou les PR.
- Dans la description de la ou des PR, où vous avez mis vos efforts et ce que vous avez choisi de ne pas faire.

Il est attendu que vous anticipiez le déploiement du système en production et que vous expliquiez votre raisonnement.
