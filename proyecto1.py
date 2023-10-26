import time
import pygame
import copy
#matrix del mundo
worldMatrix = []

agenteCoords = [0, 0] #[y, x] abajo positivo, derecha positivo
metaCoords = [0, 0]

actualNodes = [] #Fila de nodos actuales

#Create a new node
def node(treeCoord, matrizCoord, value, countValue, father, son):
    # Crear un diccionario con los valores dados
    node_dict = {
        "treeCoord": treeCoord,
        "matrizCoord": matrizCoord,
        "value": value,
        "countValue" : countValue,
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

def defaultMatrix2():
    matrix = [[-2, 0, 3, 0, 1, 1, 1, 0], 
              [1, -2, 1, 0, -2, 0, 1, 1],
              [1, 0, 1, 1, 1, 0, 0, -2],
              [1, 0, 1, 0, 1, 0, 1, 1],
              [3, -2, 1, 0, -2, 1, 1, 3]]
    return matrix

#--------- Modificacion a la matriz (solucion a un error) -----

def ajustarMatriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != 0:
                matriz[i][j] += 3
    return matriz

#-------- Funciones analizar matriz ------------

def upValue(matriz, coord):

    if coord[0]-1 >= 0:
        value = matriz[coord[0]-1][coord[1]]
        if value == 0:
            value = None
    else:
        value = None
    return value

def rightValue(matriz, coord):
    if coord[1]+1 < len(matriz[0]):
        value = matriz[coord[0]][coord[1]+1]
        if value == 0:
            value = None
    else:
        value = None
    return value

def downValue(matriz, coord):
    if coord[0]+1 < len(matriz):
        value = matriz[coord[0]+1][coord[1]]
        if value == 0:
            value = None
    else:
        value = None
    return value

def leftValue(matriz, coord):

    if coord[1]-1 >= 0:
        value = matriz[coord[0]][coord[1]-1]
        if value == 0:
            value = None
    else:
        value = None
    return value

#---------- Creacion arbol ---------------------

def getSons(y, x,father, matriz, agenteCoord):
    lst = []

    value = upValue(matriz, agenteCoord)
    if not value == None:
        lst.append(node([y,x], [agenteCoord[0]-1, agenteCoord[1]], value, father["countValue"]+value, father, None))
        x+=1

    value = rightValue(matriz, agenteCoord)
    if not value == None:
        lst.append(node([y,x], [agenteCoord[0], agenteCoord[1]+1], value, father["countValue"]+value, father, None))
        x+=1

    value = downValue(matriz, agenteCoord)
    if not value == None:
        lst.append(node([y,x], [agenteCoord[0]+1, agenteCoord[1]], value, father["countValue"]+value, father, None))
        x+=1

    value = leftValue(matriz, agenteCoord)
    if not value == None:
        lst.append(node([y,x], [agenteCoord[0], agenteCoord[1]-1], value, father["countValue"]+value, father, None))

    return lst


def giveSonsToFather(father, sons):
    father["son"] = sons
    return father

def listOfCosts():
    return 0

def checkMeta(row):
    for i in row:
        if i["matrizCoord"] == metaCoords:
            return i["treeCoord"]
    return None

def createPath(node):
    path = []
    while not node == None:
        path.append(node["matrizCoord"])
        node = node["father"]
    path.reverse()
    return path
#---------- Costo recursivo ----

def costoRecursivo(matriz, agente):
    tree = []

    #Inicializar el arbol
    firstFather = node([0,0], agente, matriz[agente[0]][agente[1]], matriz[agente[0]][agente[1]], None, None) #Generamos el primer padre
    tree.append([firstFather]) #Añadimos el primer padre al arbol
    firstSon = getSons(1, 0, firstFather, matriz, agente) #Generamos los primero hijos
    tree.append(firstSon) #Añadimos los hijos al arbol
    tree[0] = [giveSonsToFather(tree[0][0], firstSon)] #Actualizamos los hijos del primer padre
    
    justInCase = 0
    while True:
        #Check si llego a meta sus hijos
        #if not checkMeta(tree[1]) == None:
        #    return createPath(checkMeta(tree[1]))
        #for n in tree:
        #    if not checkMeta(n) == None:
        #        return createPath(checkMeta(n))
        
        #Buscar el que tenga menor coste segun la profundidad de cada uno
        nodoMenor = None
        for i in tree:
            for j in i:
                if (nodoMenor == None or j["countValue"] < nodoMenor["countValue"]) and j["son"] == None:
                    nodoMenor = j
        
        #Check si es meta
        if nodoMenor["matrizCoord"] == metaCoords:
            path = createPath(nodoMenor)
            return [path, nodoMenor["countValue"]-(len(path)*3), justInCase]

        #sino expandir las ramas de nodoMenor
        y = nodoMenor["treeCoord"][0]
        x = 0
        if y+1 == len(tree):
            tree.append([])
        else:
            x = len(tree[y+1])
        sons = getSons(y+1, x, nodoMenor, matriz, nodoMenor["matrizCoord"]) #Generamos hijos de nodoMenor
        tree[y+1] += sons #Añadimos los hijos al arbol
        tree[nodoMenor["treeCoord"][0]][nodoMenor["treeCoord"][1]] = giveSonsToFather(nodoMenor, sons) #Actualizamos los hijos del primer padre
        print(nodoMenor["matrizCoord"])

        justInCase += 1
        if justInCase == 10000:
           print("error en la matrix")
           return createPath(nodoMenor)
           
           
        

#---------- Busqueda A* -------------------

def findEuristica(agente, meta):
    return abs(agente[1] - meta[1]) + abs(agente[0] - meta[0])


def AEstrella(matriz, agente):
    tree = []

    #Inicializar el arbol
    firstFather = node([0,0], agente, matriz[agente[0]][agente[1]], matriz[agente[0]][agente[1]], None, None) #Generamos el primer padre
    tree.append([firstFather]) #Añadimos el primer padre al arbol
    firstSon = getSons(1, 0, firstFather, matriz, agente) #Generamos los primero hijos
    tree.append(firstSon) #Añadimos los hijos al arbol
    tree[0] = [giveSonsToFather(tree[0][0], firstSon)] #Actualizamos los hijos del primer padre
    
    justInCase = 0
    while True:
        #Check si llego a meta sus hijos
        #if not checkMeta(tree[1]) == None:
        #    return createPath(checkMeta(tree[1]))
        #for n in tree:
        #    if not checkMeta(n) == None:
        #        return createPath(checkMeta(n))
        
        #Buscar el que tenga menor coste segun la profundidad de cada uno
        nodoMenor = None
        for i in tree:
            for j in i:
                if (nodoMenor == None or (j["countValue"]+findEuristica(j["matrizCoord"], metaCoords) < nodoMenor["countValue"])) and j["son"] == None:
                    nodoMenor = j
        
        #Check si es meta
        if nodoMenor["matrizCoord"] == metaCoords:
            path = createPath(nodoMenor)
            return [path, nodoMenor["countValue"]-(len(path)*3), justInCase]


        #sino expandir las ramas de nodoMenor
        y = nodoMenor["treeCoord"][0]
        x = 0
        if y+1 == len(tree):
            tree.append([])
        else:
            x = len(tree[y+1])
        sons = getSons(y+1, x, nodoMenor, matriz, nodoMenor["matrizCoord"]) #Generamos hijos de nodoMenor
        tree[y+1] += sons #Añadimos los hijos al arbol
        tree[nodoMenor["treeCoord"][0]][nodoMenor["treeCoord"][1]] = giveSonsToFather(nodoMenor, sons) #Actualizamos los hijos del primer padre
        print(nodoMenor["matrizCoord"])

        justInCase += 1
        if justInCase == 5000:
           print("error en la matrix")
           break
           #return createPath(nodoMenor)

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

def mostrar_matriz(matriz, path, pathEstrella):
    pathI = 0
    pathIE = 0
    ancho_casilla = 150
    alto_casilla = 150
    ventana_ancho = ancho_casilla * len(matriz[0])
    ventana_alto = alto_casilla * len(matriz)
    estrellaCoords = [0, 0]

    imagen_negro = pygame.image.load("black.png")  # Sustituye "negro.png" con tu imagen
    imagen_verde = pygame.image.load("white.jpg")  # Sustituye "verde.png" con tu imagen
    imagen_naranja = pygame.image.load("Justo.jpg") # Sustituye "naranja.png" con tu imagen
    imagen_rojo = pygame.image.load("katz.jpg")
    imagen_agente = pygame.image.load("coraje.webp")
    imagen_meta = pygame.image.load("Muriel.png")
    imagen_estrella = pygame.image.load("corajeEstrella.png")
    pygame.init()
    pantalla = pygame.display.set_mode((ventana_ancho, ventana_alto))
    pygame.display.set_caption("Corage world")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        pantalla.fill((255, 255, 255))  # Fondo blanco

        #Mover el agente
        if pathI < len(path):
            agenteCoords[0] = path[pathI][0]
            agenteCoords[1] = path[pathI][1]
            pathI +=1
        
        #Mover el agenteEstrella
        if pathIE < len(pathEstrella):
            estrellaCoords[0] = pathEstrella[pathIE][0]
            estrellaCoords[1] = pathEstrella[pathIE][1]
            pathIE +=1

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
                if metaCoords == [i, j]:
                    imagen = imagen_meta
                if estrellaCoords == [i, j]:
                    imagen = imagen_estrella                    
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

            
        pygame.display.update()
        time.sleep(1)




#-------- Implementacion --------------------

#worldMatrix = defaultMatrix()
worldMatrix = defaultMatrix2()

worldMatrixAjustada = copy.deepcopy(worldMatrix)
ajustarMatriz(worldMatrixAjustada)
metaCoords = [2, 0]
#agenteCoords = [2, 7]
#agenteCoords = [1, 7]
#agenteCoords = [2, 3]

#ejemplo matriz 2
#agenteCoords = [1, 4]
#agenteCoords = [1, 6]
agenteCoords = [4, 5]

costoR = costoRecursivo(worldMatrixAjustada, agenteCoords)
aEstrella = AEstrella(worldMatrixAjustada, agenteCoords)

print("CR: " + str(costoR[0]) + ", Costo: " + str(costoR[1])+ ", Iteraciones: " + str(costoR[2]))
print("A*: " + str(aEstrella[0])+ ", Costo: " + str(aEstrella[1])+ ", Iteraciones: " + str(aEstrella[2]))
#Mostrar resultado
mostrar_matriz(worldMatrix, costoR[0], aEstrella[0])
