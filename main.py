import os
import tkinter as tk
from tkinter import ttk, filedialog
import pydicom
import pyvista as pv
import numpy as np
from skimage.draw import polygon


# Fonction pour charger les fichiers DICOM
def load_dicom_folder(folder_path):
    """Charge tous les fichiers DICOM dans un dossier et les trie par leur position."""
    dicom_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.dcm')]
    if not dicom_files:
        print("Aucun fichier DICOM trouvé dans le dossier.")
        return None

    dicom_data = [pydicom.dcmread(file) for file in dicom_files]
    dicom_data.sort(key=lambda d: d.InstanceNumber if 'InstanceNumber' in d else float('inf'))
    print(f"{len(dicom_data)} fichiers DICOM chargés.")
    return dicom_data


# Fonction pour convertir les fichiers DICOM en modèle 3D
def dicom_to_3d(dicom_data):
    """Convertit les données DICOM en un modèle 3D volumique."""
    pixel_array = np.stack([d.pixel_array for d in dicom_data], axis=-1)

    # Extraire les espacements depuis les métadonnées
    spacing_x, spacing_y = map(float, dicom_data[0].PixelSpacing)
    spacing_z = float(dicom_data[0].SliceThickness)

    print(f"Espacement (x, y, z) : ({spacing_x}, {spacing_y}, {spacing_z})")

    # Créer une grille volumique pour PyVista
    grid = pv.ImageData()
    grid.dimensions = pixel_array.shape
    grid.origin = (0, 0, 0)
    grid.spacing = (spacing_x, spacing_y, spacing_z)

    # Ajouter les données scalaires
    grid.point_data["values"] = pixel_array.flatten(order="F")
    return grid, pixel_array, (spacing_x, spacing_y, spacing_z)


# Fonction pour afficher le volume et dessiner des contours
def draw_and_segment(grid, pixel_array, spacing):
    """Permet de sélectionner une région en dessinant un polygone et de colorer l'organe."""
    plotter = pv.Plotter()
    plotter.add_volume(grid, scalars="values", cmap="gray", opacity="sigmoid")
    plotter.show_axes()

    contour_points = []
    slice_index = 0  # Exemple : Travailler sur la première tranche
    mask = np.zeros(pixel_array.shape, dtype=bool)  # Masque 3D

    def callback_pick(point):
        """Ajoute un point au contour lorsqu'un clic est détecté."""
        contour_points.append(point)
        print(f"Point ajouté : {point}")

        # Dessiner les lignes entre les points
        if len(contour_points) > 1:
            line = pv.lines_from_points(contour_points)
            plotter.add_mesh(line, color="red", line_width=2)

        plotter.render()

    def finish_contour():
        """Finalise le contour, génère le masque, et colore la région."""
        if len(contour_points) < 3:
            print("Contour trop petit. Sélectionnez plus de points.")
            return

        contour_points.append(contour_points[0])  # Fermer le polygone
        line = pv.lines_from_points(contour_points)
        plotter.add_mesh(line, color="red", line_width=2)
        plotter.render()

        # Transformer les points en indices 2D
        points_2d = np.array([[p[0], p[1]] for p in contour_points])
        rr, cc = polygon(points_2d[:, 0], points_2d[:, 1], pixel_array.shape[:2])

        # Mettre à jour le masque 2D pour la tranche sélectionnée
        mask[rr, cc, slice_index] = True

        # Colorer la région dans la vue
        masked_volume = np.copy(pixel_array)
        masked_volume[~mask] = 0  # Masquer tout sauf la région sélectionnée
        grid.point_data["values"] = masked_volume.flatten(order="F")
        plotter.update()

        print("Contour terminé, polygone fermé, et région colorée.")

    plotter.enable_point_picking(callback_pick, show_message=True, color="blue", point_size=8)
    plotter.add_text("Cliquez pour dessiner un contour. Appuyez sur 'F' pour finir.", font_size=10)
    plotter.add_key_event("f", finish_contour)
    plotter.show()


# Fonction pour ouvrir un dossier
def open_folder():
    """Ouvre un sélecteur de dossiers, charge les fichiers DICOM et affiche le volume."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        print(f"Dossier sélectionné : {folder_path}")
        dicom_data = load_dicom_folder(folder_path)
        if dicom_data:
            grid, pixel_array, spacing = dicom_to_3d(dicom_data)
            draw_and_segment(grid, pixel_array, spacing)
    else:
        print("Aucun dossier sélectionné.")


# Interface Tkinter
def create_gui():
    root = tk.Tk()
    root.title("Application DICOM 3D")
    root.geometry("800x500")

    # Charger une image de fond
    background_image = tk.PhotoImage(file="back.png")  # Remplacez par votre fichier image
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Style personnalisé pour les boutons
    style = ttk.Style()
    style.configure(
        "Custom.TButton",
        font=("Arial", 16, "bold"),
        foreground="white",
        background="#007ACC",
        padding=10
    )

    # Bouton pour sélectionner un dossier
    select_folder_btn = ttk.Button(
        root,
        text="Choisir un dossier DICOM",
        command=open_folder,
        style="Custom.TButton"
    )
    select_folder_btn.place(relx=0.5, rely=0.5, anchor="center")

    root.mainloop()


# Lancer l'application
if __name__ == "__main__":
    create_gui()
