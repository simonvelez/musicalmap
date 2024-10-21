import h5py
import pandas as pd
import os

folder_path = "C:\\Users\\pacm6\\Downloads\\millionsongsubset"

data_frames = []

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".h5"):  # Verifica si el archivo es de tipo .h5
            file_path = os.path.join(root, filename)
            
            # Abre el archivo .h5
            with h5py.File(file_path, 'r') as h5file:
                # Accede al dataset dentro del archivo .h5 (ajusta si es necesario)
                if 'metadata/songs' in h5file:  # Verifica que el dataset existe
                    data = h5file['metadata/songs'][:]
                    df = pd.DataFrame(data)
                    data_frames.append(df)

combined_df = pd.concat(data_frames, ignore_index=True)

# Guarda el DataFrame combinado como CSV
output_csv_path = r"C:\Users\pacm6\Downloads\songs_data.csv"
combined_df.to_csv(output_csv_path, index=False)

#print("Directorio de trabajo actual:", os.getcwd())
