import time
import pygame
#matrix del mundo
worldMatrix = [[0] * 5 for _ in range(8)]

agenteCoords = [0, 0] #[y, x] abajo positivo, derecha positivo
metaCoords = [0, 0]

actualNodes = [] #Fila de nodos actuales

#Create a new node
def node(position, value, father, son):
    # Crear un diccionario con los valores dados
    node_dict = {
        "coords": position,
        "value": value,
        "father": father,
        "son": son
    }
    return node_dict

def defaultMatrix():
    matrix = [[1, 1, 3, 1, 1, 1, 1, 1], 
                   [1, -2, 0, 0, -2, 0, 0, 1],
                   [1, 0, 1, 1, 1, 0, 0, 1],
                   [1, 0, 1, 0, 0, 0, 1, 1],
                   [1, -2, 1, 3, 1, 1, 1, 1]]
    return matrix

#-------- Funciones analizar matriz ------------

def upValue(matriz, coord):

    if coord[0]-1 >= 0:
        value = matriz[coord[0]-1][coord[1]]
    else:
        value = None
    return value

def rightValue(matriz, coord):
    if coord[1]+1 < len(matriz[0]):
        value = matriz[coord[0]][coord[1]+1]
    else:
        value = None
    return value

def downValue(matriz, coord):
    if coord[0]+1 < len(matriz):
        value = matriz[coord[0]+1][coord[1]]
    else:
        value = None
    return value

def leftValue(matriz, coord):

    if coord[1]-1 >= 0:
        value = matriz[coord[0]][coord[1]-1]
    else:
        value = None
    return value

#-----------Interfaz grafica---------------------

# Constantes de colores 
colores = {
    0: (0, 0, 0),      # Negro
    1: (0, 255, 0),    # Verde
    -2: (255, 165, 0),  # Naranja
    3: (255, 0, 0),    # Rojo
}
AGENTECOLOR = (255, 11, 207 )
METACOLOR = (255, 244, 11 )
BLACK = (0,0,0)

def mostrar_matriz(matriz):

    ancho_casilla = 100
    alto_casilla = 100
    ventana_ancho = ancho_casilla * len(matriz[0])
    ventana_alto = alto_casilla * len(matriz)

    imagen_negro = pygame.image.load("proyecto1IA/black.png")  # Sustituye "negro.png" con tu imagen
    imagen_verde = pygame.image.load("proyecto1IA/white.jpg")  # Sustituye "verde.png" con tu imagen
    imagen_naranja = pygame.image.load("proyecto1IA/Justo.jpg") # Sustituye "naranja.png" con tu imagen
    imagen_rojo = pygame.image.load("proyecto1IA/katz.jpg")
    imagen_agente = pygame.image.load("proyecto1IA/coraje.webp")

    pygame.init()
    pantalla = pygame.display.set_mode((ventana_ancho, ventana_alto))
    pygame.display.set_caption("Corage world")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        pantalla.fill((255, 255, 255))  # Fondo blanco

        # Dibujar la matriz en la ventana
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                x = j * ancho_casilla
                y = i * alto_casilla
                valor = matriz[i][j]

                # Determinar la imagen a mostrar en función del valor en la matriz
                if valor == 0:
                    imagen = imagen_negro
                elif valor == 1:
                    imagen = imagen_verde
                elif valor == -2:
                    imagen = imagen_naranja
                elif valor == 3:
                    imagen = imagen_rojo
                if agenteCoords == [i, j]:
                    imagen = imagen_agente

                # Redimensionar la imagen al tamaño de la casilla
                imagen = pygame.transform.scale(imagen, (ancho_casilla, alto_casilla))

                # Dibujar la imagen en la casilla
                pantalla.blit(imagen, (x, y))

        for i in range(0, len(matriz)+1):
            pygame.draw.line(pantalla, BLACK, (0, alto_casilla*i), (ancho_casilla * len(matriz[0]), alto_casilla*i))
        for i in range(0, len(matriz[0])+1):
            pygame.draw.line(pantalla, BLACK, (ancho_casilla*i, 0), (ancho_casilla * i, alto_casilla*len(matriz)))

        print(leftValue(worldMatrix, [1,2]))
        pygame.display.update()
        time.sleep(1)




#-------- Implementacion --------------------

worldMatrix = defaultMatrix()
metaCoords = [2, 0]
agenteCoords = [2, 7]
mostrar_matriz(worldMatrix)