# Simulation 3D DICOM avec PyVista et VTK

## Description du projet
Ce projet est une application interactive permettant de charger des fichiers DICOM, de les convertir en un modèle 3D volumique, et d'effectuer des opérations de segmentation. L'application repose sur les bibliothèques PyVista et VTK pour la visualisation 3D et propose une interface utilisateur simple via Tkinter.

## Fonctionnalités principales
- **Chargement des fichiers DICOM** :
  - Parcourir un dossier pour charger les fichiers DICOM.
  - Tri des fichiers selon leur position (InstanceNumber).
- **Conversion en modèle 3D** :
  - Construction d'une grille volumique PyVista.
  - Extraction des espacements pixelaires depuis les métadonnées DICOM.
- **Visualisation 3D** :
  - Affichage volumique des données DICOM.
  - Interaction via PyVista pour dessiner des contours.
- **Segmentation** :
  - Permet de dessiner un polygone sur une tranche DICOM pour segmenter et colorer une région spécifique.
- **Interface utilisateur graphique** :
  - Interface intuitive développée avec Tkinter pour sélectionner un dossier DICOM et démarrer l'analyse.

## Prérequis
Avant de lancer le projet, assurez-vous que les dépendances suivantes sont installées :

- Python 3.7 ou version ultérieure
- Bibliothèques listées dans `requirements.txt` :
  ```
  pyvista
  vtk
  pydicom
  numpy
  ```

## Installation
1. Clonez le dépôt GitHub sur votre machine :
   ```bash
   git clone https://github.com/majdsaadouli/Simulation-3D-DICOM-avec-PyVista-et-VTK
   ```
2. Accédez au répertoire du projet :
   ```bash
   cd <nom-du-repo>
   ```
3. Installez les dépendances avec pip :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. Lancez le script principal :
   ```bash
   python main.py
   ```
2. Une interface s'ouvre avec un bouton "Choisir un dossier DICOM".
3. Sélectionnez un dossier contenant des fichiers DICOM.
4. Visualisez les données sous forme volumique et dessinez des contours pour segmenter une région.

## Explication du fonctionnement
### 1. Chargement des fichiers DICOM
- La fonction `load_dicom_folder` charge tous les fichiers `.dcm` présents dans un dossier et les trie selon leur position dans le volume.
- Les métadonnées DICOM sont utilisées pour extraire des informations comme l'espacement des pixels et l'épaisseur des tranches.

### 2. Conversion en modèle 3D
- La fonction `dicom_to_3d` utilise PyVista pour créer une grille volumique (`ImageData`) et y associe les données scalaires issues des images DICOM.
- Les espacements – `PixelSpacing` (x, y) et `SliceThickness` (z) – sont appliqués pour respecter les dimensions réelles des données.

### 3. Visualisation et segmentation
- La fonction `draw_and_segment` propose une interface PyVista pour :
  - Afficher le volume en niveaux de gris avec des interactions.
  - Dessiner des polygones pour sélectionner une région d'intérêt.
  - Mettre à jour le volume avec les zones segmentées colorées.

### 4. Interface graphique
- L'application Tkinter fournit une interface simple pour charger les dossiers DICOM et démarrer le processus de visualisation.

## Exemples de sortie
### Visualisation volumique initiale
Affichage d'une reconstruction 3D des données DICOM avec PyVista.

### Segmentation interactive
Sélection d'une région spécifique en dessinant un polygone sur une tranche et application de couleurs à cette région dans le modèle 3D.

## Limitations
- Ce projet fonctionne uniquement avec des ensembles de données DICOM structurés contenant des métadonnées cohérentes.
- Une gestion plus avancée des erreurs pourrait être ajoutée pour des fichiers ou dossiers corrompus.

## Améliorations futures
- Ajout de fonctionnalités pour :
  - Exporter les régions segmentées dans un format compatible.
  - Ajouter plus de styles de visualisation (coupes orthogonales, vues multiplanaires, etc.).
  - Intégrer un algorithme de segmentation automatique.
- Amélioration de l'esthétique de l'interface graphique avec des options de personnalisation supplémentaires.

## Contribuer
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet :
1. Forkez le dépôt.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b nouvelle-fonctionnalite
   ```
3. Effectuez vos modifications et testez-les.
4. Soumettez une pull request.

## Auteurs
- **Majd Saadouli (https://github.com/majdsaadouli/majdsaadouli)**  
  Étudiant en Génie Biomédical passionné par la visualisation médicale et les technologies 3D.

## Licence
Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.

---
Merci d'avoir utilisé cette application ! N'hésitez pas à me contacter pour toute question ou suggestion.

