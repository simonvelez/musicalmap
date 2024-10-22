import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(r'tcc_ceds_music.csv')

# Extract the relevant columns
nom = df[['track_name', 'genre']].values.tolist()
top = df[['track_name', 'topic']].values.tolist()

# Create the relationship lists
relacion1 = [[i[0], i[1]] for i in nom]
relacion2 = [[i[0], i[1]] for i in top]

# Create a graph
gm = nx.Graph()

# Add nodes to the graph based on track names
for i in range(len(nom)):
    gm.add_node(i, label=nom[i][0])

# Diccionario para agrupar canciones por género
genre_dict = {}

for i, track in enumerate(nom):
    track_name, genre = track
    if genre not in genre_dict:
        genre_dict[genre] = []
    genre_dict[genre].append(i)

# Agregar aristas solo entre tracks del mismo género
print("Estado: Creando las aristas")
for genre, tracks in genre_dict.items():
    for i in range(len(tracks)):
        for j in range(i + 1, len(tracks)):  # Para evitar duplicación de aristas
            gm.add_edge(tracks[i], tracks[j])

print(":3")
# Dibujar un grafo bien bonito
pos = nx.spring_layout(gm)
print("Estado: Dibujando Aristas")
nx.draw(gm, pos, with_labels=True, font_weight='bold')
print("Estado: Mostrando")
plt.show()
print("Estado: Terminado")