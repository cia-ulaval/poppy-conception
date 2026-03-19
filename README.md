# Poppy Humanoid (Conception) 🛠️

## Documentation (_How to Poppy_)
- Visiter ce [Google Docs](https://docs.google.com/document/d/1xX1RbV6WdlQWjZE55EWiICiZSR_HosOSyKKz-T2dgOk/edit?usp=sharing).
- Tu trouveras dans ce document les points marquants de la conception du robot, ainsi que de toutes les manoeuvres et manipulations nécessaires à son bon fonctionnement.


## Fiche d'Identité

*   **Type de projet :** Projet Club
*   **Team Lead :** Cyrille Bernier
*   **Partenaire Académique/Industriel :** N/A
*   **Effectif recherché :** 4 membres
*   **Profils recherchés :** Génie mécanique, Impression 3D, Robotique, Électronique

## Description du Projet

Imprimer en 3D et assembler un robot humanoïde Poppy open-source, comprenant l'impression des composants, l'assemblage des 25 articulations motorisées et l'intégration des systèmes électroniques pour créer un robot fonctionnel.

## Objectifs & Livrables

*   **Objectif Principal :** Construire un robot humanoïde Poppy entièrement fonctionnel pour la session d'automne.
*   **Livrables attendus :**
    *   Pièces imprimées en 3D et post-traitées
    *   Structure mécanique assemblée avec 25 articulations
    *   Système électronique intégré et câblé
    *   Documentation complète du processus d'assemblage
    *   Robot fonctionnel prêt pour la programmation

## Timeline Prévisionnelle de la Session

| Semaine | Activité/Phase |
| :-----: | :------------- |
|  **1-2**  | **Planification** - Étude des plans |
|  **3-6**  | **Impression 3D** - Production intensive des composants mécaniques |
|  **7-8**  | **Post-traitement** - Finition et préparation des pièces imprimées |
|  **9-12** | **Assemblage mécanique** - Montage des articulations et structure |
|  **13-15**| **Intégration électronique** - Câblage moteurs et capteurs |

## Technologies & Compétences Visées

*   **Logiciels :** Logiciels CAO (SolidWorks/Fusion360), Slicers impression 3D
*   **Matériels :** Imprimantes 3D, moteurs Dynamixel, composants électroniques
*   **Compétences :** Impression 3D, assemblage mécanique, lecture plans techniques, soudure, câblage

## Pourquoi rejoindre ce projet ?

Tu vas aimer ce projet si :
*   Tu aimes travailler de tes mains et voir un projet concret prendre forme
*   Tu es passionné par la robotique et la mécanique
*   Tu veux apprendre les techniques d'impression 3D et d'assemblage robotique professionnel

## Contact & Liens Utiles
*   **Documentation :** [Poppy Project Documentation](https://docs.poppy-project.org/en/assembly-guides/poppy-humanoid/)
*   **Référence :** [GitHub Poppy](https://github.com/poppy-project)
*   **Fichiers imprimables des Body Parts de Poppy:** [Fichiers imprimables](https://github.com/poppy-project/poppy-humanoid/releases/download/hardware_1.0.1/STL_3D_printed_parts.zip)
*   **Excel des pièces:** [Excel](https://ulavaldti-my.sharepoint.com/:x:/r/personal/cyber18_ulaval_ca/Documents/Poppy%20pi%C3%A8ces.xlsx?d=we67d0848775541a08d8f85ca3fd67f8b&csf=1&web=1&e=Fpmc5E)
*   **Playlist vidéos d'assemblage:** [Playlist](https://www.youtube.com/watch?v=SUlM_mE3plc&list=PL8wg9_Kkof8wwqgfFu0iCij73C-4gt95x&index=2)
*   **[Body parts en format .sldprt](https://github.com/poppy-project/Poppy-multiarticulated-torso/tree/dffc1e8f4aaba17622789be21f6563d275080ec6/parts)**

- **[Documentation des moteurs qui n'avaient pas d'allure](https://ulavaldti-my.sharepoint.com/:x:/g/personal/cyber18_ulaval_ca/IQDmeS0tiUcpSrYruJAAcc10AX4TU4iCfaX-LsLGC0McrcA?e=XblEjz)**
- [Documentation Poppy Eve](https://github.com/poppy-project/Poppy-eva-head-design#poppy-eve-head-design)

# Démarrage du projet

---

## Prérequis

- Dockers : <https://docs.docker.com/desktop/#next-steps>

---

## Démarrage rapide

```bash
docker compose up -d
```

une fois démaré le conteneur est relié en temps réel au dossier src du projet.

---

## Commandes utiles

```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Attacher au conteneur
sudo docker attach poppy-dev

#détacher du conteneur (ne pas executer dans ton terminal)
exit

# Voir les logs
docker compose logs -f

# Reconstruire après modification de Package.json ou Dockerfile
docker compose up -d --build

# pour avoir de l'aide à propos des commandes dockers
docker --help
docker compose --help

```

