import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from collections import deque
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from collections import defaultdict
from heapq import heappush, heappop
import heapq







df = pd.read_csv(r'bases_de_datos/tcc_ceds_music.csv')
relacion1=df[["track_name","genre"]]
#relacion2=df[["track_name","topic"]]
#relacion3=df[["track_name","lyrics"]]


#gm=nx.Graph()

#creamos los nodos

#for i in range(len(relacion1["track_name"])):
#    gm.add_node(df.loc[i,"track_name"])

#creamos las aristas 
'''for i in range(len(df["track_name"])):
    for j in range(i+1,len(df["track_name"])):
        if relacion1.loc[i,"genre"] == relacion1.loc[j,"genre"]:
            gm.add_edge(relacion1.loc[i,"track_name"],relacion1.loc[j,"track_name"])

pos = nx.spring_layout(gm)
print("Estado: Dibujando Aristas")
nx.draw(gm, pos, with_labels=True, font_weight='bold')
print("Estado: Mostrando")
plt.show()
print("Estado: Terminado")'''




# Extraer columnas relevantes y limpiar la información
nombre = df['track_name']
lyrics = df['lyrics']
genre = df['genre']
lyrics = [lyric.split(" ") for lyric in lyrics] # Separar un string con todos los lyrics en una lista de palabras
lyrics = [list(set(lyric)) for lyric in lyrics] # Eliminar palabras duplicadas
stop_words = set(stopwords.words('english'))
lyrics = [[word for word in lyric if word.lower() not in stop_words] for lyric in lyrics]

gm = nx.Graph()


#nodos
for i in range(len(nombre)):
    gm.add_node(nombre[i])
    
#aristas 
for i in range(len(lyrics)):
    for j in range(i + 1, len(lyrics)):
        palabras_comun = set(lyrics[i]).intersection(set(lyrics[j]))
        if len(palabras_comun) > 0: 
            gm.add_edge(nombre[i], nombre[j], weight=len(palabras_comun))
            
            mostrar_palabra = list(palabras_comun)[0]
            gm[nombre[i]][nombre[j]]['palabra'] = mostrar_palabra
            

#creamos un dataframe en el cual contiene cada una de las relaciones

lista=list(gm.edges(data=True))
dt = pd.DataFrame([(u, v, attr['weight'], attr['palabra']) for u, v, attr in lista], columns=['Nodo1', 'Nodo2', 'peso', 'Nombrearis'])


#colores de los nodos
g_colores = {gen: color for gen, color in zip(set(genre), cm.tab20.colors)}
for i in range(len(nombre)):
    gm.nodes[nombre[i]]['color'] = g_colores[genre[i]]
            
pos = nx.circular_layout(gm)
#dibujar los nodos
color_nodos = [gm.nodes[nodo]['color'] for nodo in gm.nodes]
nx.draw_networkx_nodes(gm, pos, node_color=color_nodos, node_size= 700)

#dibujar las aristas
nx.draw_networkx_edges(gm, pos, width=2, edge_color='black')

nx.draw_networkx_labels(gm, pos, font_size = 10, font_weight='bold')

#las etiquetas de las aristas
etiquetas= {(u,v): gm[u][v]['palabra'] for u, v in gm.edges}
nx.draw_networkx_edge_labels(gm, pos, edge_labels=etiquetas, font_color='blue')



print("Estado: Dibujando Aristas")
#nx.draw(gm, pos, with_labels=True, font_weight='bold')
print("Estado: Mostrando")
plt.show()
print("Estado: Terminado")

"""
def dfs_explore(graph, start_node):
    visited = set()
    stack = [start_node]  # Usamos una pila (stack)
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            # Agregamos los nodos vecinos al stack
            stack.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)

    return result
"""

def buscar_generocan(nombre_cancion):
    genero=""
    for i in range(len(relacion1['track_name'])):
        if nombre_cancion == relacion1.loc[i,'track_name']:
            genero= relacion1.loc[i,'genre']
            break
    return genero
''''
def bfs_explore(graph, start_node):
    visited = set()
    queue = deque([start_node])  # Usamos una cola (queue)
    result = []

    while queue:
        i=0
        node = queue.popleft()
        if node not in visited:
            
            visited.add(node)
            result.append((node,buscar_generocan(node)))
            # Agregamos los nodos vecinos a la cola
            queue.extend(neighbor for neighbor in graph.neighbors(node) if neighbor not in visited)
        i+=1
    return result
nodo_inicial = nombre[0] '''

def bfs_ponderada(graph, start_node):
    visited = set()
    priority_queue = []  # Usamos una cola de prioridad
    result = []

    # Iniciar con el nodo inicial
    heappush(priority_queue, (-float('inf'), start_node))  # Pesos negativos para simular una "máxima prioridad"

    while priority_queue:
        _, node = heappop(priority_queue)
        if node not in visited:
            visited.add(node)
            result.append(node)

            # Agregar vecinos ordenados por peso
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    weight = graph[node][neighbor]['weight']
                    heappush(priority_queue, (-weight, neighbor))  # Peso negativo para priorizar mayor peso

    return result

"""
dfs_result = dfs_explore(gm, nodo_inicial)
print(dfs_result)
"""

'''''
bfs_result = pd.DataFrame([(u,v) for u,v in bfs_explore(gm, nodo_inicial)],columns =['track_name','genre'])
print(bfs_result)
'''



#-------------------------------------------------------------------

genero_palabras = defaultdict(set)
for i in range(len(genre)):
    genero_palabras[genre[i]].update(lyrics[i])

# Crear el grafo de géneros
gm_generos = nx.Graph()

# Añadir nodos (géneros)
for gen in genero_palabras:
    gm_generos.add_node(gen)

# Añadir aristas basadas en palabras comunes entre géneros
for gen1 in genero_palabras:
    for gen2 in genero_palabras:
        if gen1 != gen2:
            palabras_comun = genero_palabras[gen1].intersection(genero_palabras[gen2])
            if len(palabras_comun) > 0:
                gm_generos.add_edge(gen1, gen2, weight=len(palabras_comun))

# Dibujar el grafo
pos = nx.spring_layout(gm_generos)
nx.draw_networkx_nodes(gm_generos, pos, node_color="lightblue", node_size=700)
nx.draw_networkx_edges(gm_generos, pos, edge_color="gray", width=2)
nx.draw_networkx_labels(gm_generos, pos, font_size=10, font_weight="bold")

# Etiquetas para las aristas (número de palabras comunes)
edge_labels = {(u, v): gm_generos[u][v]['weight'] for u, v in gm_generos.edges}
nx.draw_networkx_edge_labels(gm_generos, pos, edge_labels=edge_labels, font_color="red")

plt.show()

# Crear una lista con relaciones únicas (evitar duplicados como pop-rock y rock-pop)
relaciones_generos_unicas = [(min(u, v), max(u, v), gm_generos[u][v]['weight']) for u, v in gm_generos.edges]

# Convertir a DataFrame
df_relaciones_unicas = pd.DataFrame(relaciones_generos_unicas, columns=['Género 1', 'Género 2', 'Palabras Comunes'])

# Imprimir el DataFrame
print(df_relaciones_unicas)

bfs_result_ponderada = bfs_ponderada(gm_generos, "jazz")  # Cambia "pop" por el nodo inicial deseado
print("Orden de géneros por relación (búsqueda ponderada):")
print(bfs_result_ponderada)









