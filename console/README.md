# MageBot

MageBot est un jeu de duel magique inspiré de l’univers Harry Potter, où vous affrontez une intelligence artificielle en utilisant des sorts. Développé par l'équipe ZIOS.

## Fonctionnalités

- **Duel magique contre IA** : Système de sorts (attaque, soin, résistance) avec gestion de ressources (PV, Résistance, Mana).
- **Versions disponibles** :
  - Console : Version complète et avancée pour duel en ligne de commande.
  - Discord : (À venir) Intégration avec l'API Discord pour interactions communautaires.
  - Navigateur : (À l'étude) Version web avec graphismes 2D.
- **IA intelligente** : Utilise un algorithme Minimax pour des décisions stratégiques, prenant en compte PV, résistance et mana.
- **Progression et statistiques** : (À venir) Classements, sauvegarde de parties.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-username/magebot.git
   cd magebot
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

   **Dépendances** : `colorama` pour la coloration du texte en console.

## Utilisation

- **Version Console** (recommandée, la plus avancée) :
  ```bash
  python MageBot/console_version/magebotcli.py
  ```
  Tapez `help` pour voir les commandes, `start_dual` pour lancer un duel contre l'IA.

- **Version Discord** : (À venir) Ajoutez le bot à votre serveur et utilisez les commandes.
- **Version Web** : (À venir) Ouvrez dans un navigateur.

## Changelog

| Date       | Version | Nouveautés / Modifications |
|------------|---------|----------------------------|
| 2025-12-10 | 1.1.4   | Améliorations IA (prise en compte mana/résistance dans heuristique, évitement soins à PV max), UI colorée au démarrage, ajout commande 'about', version console la plus avancée |
| 2025-09-24 | 0.1.0   | Création du projet, premières fonctionnalités console et Discord |

## Contributeurs

- Équipe ZIOS : Développement et maintenance.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
