#Nombre del autor: Cristhian Adal Garcia Hernandez

#Esta es la segunda version se hara que el programa funcione de manera
#correcta y encuentre el resultado por si mismo

#Esta 6ta version se incluira los hilos para ir pintando por pasos
#Teoricamente es la ultima puesto que el agregado se finalizo con exito

import random
import math
import matplotlib.pyplot as plt #Esta libreria es para poder graficar

from tkinter.filedialog import asksaveasfile #Para poder guardar archivos eligiendo ubicación en el explorador
from tkinter import *     # Funciones de GUI
from tkinter import filedialog  # Para cargar archivos desde explorador
from tkinter import ttk  # Para poder usar combobox
from tkinter import messagebox #Para mostrar mensajes simples al usuario
import time #Para la ejecución paso a paso
from threading import Thread #Para la ejecución paso a paso

thread = Thread()
realTimeExecFlag = None #Bandera para validar si el usuario quiere o no ejecución a tiempo real
graph = []  #Esta estructura se generara a partir del fitness
ciudades = 5 #El numero de ciudades es preterminado, pero puede cambiar siempre
individuos = 0 #Esto son los individuos totales de la poblacion
matrix_individuos = None #Esta matriz guardara a los individuos
matrix_nueva = [] #Esta matriz se llenara con los cruces y mutaciones, para despues reemplazar a la anterior
ubicaciones = [] #Esta matriz guardara las coordenadas de las ciudades para ya nos buscarlas
mutacion = 0
mapa = None
last_way = None
bandera = 0

#Esa variable es para ver si se queda en una valor 1 o 2 porque es duplicar la mutacion para verse mas agresiva
mutacion_variciacional = 1 

#Es una imagen que la almacenamos 
back_Image = None

#Estas variables son para controlar las ventanas desde diversas funciones
win_Welcome = None
win_askMeasurements = None
win_createMap = None
modulo = 3
#Este es un boton que sera controlado desde dos funciones distintas
continue_b = None

# Leer desde un txt mapa guardado ----------------------------------------------------------------------------------
def readfile():
    global mapa
    global ubicaciones
    global ciudades

    mapa = []
    # Abrir el explorador de archivos
    filename = filedialog.askopenfile(title="Select file",
                                      filetypes=(("text files", "*.txt"), ("all files", "*.*")))

    # Es necesario validar que si se haya cargado un archivo (que el usuario no haya cancelado la carga) antes de intentar manipular los datos
    if filename is not None:
        # Lee el archivo seleccionado por líneas
        read_map = filename.readlines()  # saves the data from the opened

        # A cada lista que se leyó se le aplica el siguiente procedimiento
        row = 0
        for line in read_map:
            mapa.append([])  # Creamos la "lista de listas" y en cada una de esas listas:
            list_chars = line.split()  # Se separan los caracteres dentro de la lista
            mapa[row].extend(
                list(map(int, list_chars)))  # Convierte todos los caracteres leídos en la lista a enteros
            # se convierten para facilitar su uso dentro del programa
            row += 1
        if (len(mapa) is len(read_map)):  # cuando todo el mapa leído ha sido convertido y guardado en mapa se manda a mostrar
            maximo = 0
            #Este primer ciclo lo que hara es saber cuantas ciudades hay en el mapa
            for x in mapa:
                for y in x:
                    if maximo > y:
                        maximo = maximo
                    else:
                        maximo = y
            ciudades = maximo
            ubicaciones = [0] * ciudades
            index = 0
            #Este segundo ciclo buscara las ubicaciones de todas las cidades una sola vez
            for x in mapa:
                two = 0
                for y in x:
                    if y != 0:
                        ubicaciones[y-1]=[two, index]
                    two += 1
                index +=1
            Begin(1)

# Guardar el mapa que se creo a un archivo de texto
def savefile():
    global mapa
    dale = 1
    if (dale != 1):
        messagebox.showerror('Error', "You can't save a map without points A and B")
    else:
        file = asksaveasfile(mode='w',
                                defaultextension=".txt")  # Abre el explorador para permitir elegir ubicación para guardar el archivo
                                                                # y lo guarda en un txt
        if (file is not None):
            for row in mapa:
                for element in row:
                    file.write(str(element) + ' ')  # Guarda valor por valor de una fila separándolo por espacios
                file.write('\n')  # Cambia de linea
            file.close()  # Deja de escribir en el archivo

#Esta funcion anadira mas ciudades al mapa actual
def aumentar():

    def validacion():     
        global mapa
        global ciudades
        global ubicaciones
        global win_createMap

        try:
            temp1 = int(Combobox1.get())
            temp2 = int(Combobox2.get())
        except ValueError:
            messagebox.showerror('Error', "No se pueden ingresar letras o espacios vacios")
            banderazo = 0
            return 0

        banderazo = 1
        if banderazo == 1:
            if (temp1 and temp2) < 20:
                if mapa[temp1][temp2] != 0:
                    messagebox.showerror('Error', "Ya hay una ciudad en esa ubicacion")
                else:
                    ciudades = ciudades + 1
                    mapa[temp1][temp2] = ciudades
                    ubicaciones.append([temp1,temp2])
                    circulo = Canvas(win_createMap, width=15, height=15, bg='white') 
                    circulo.pack(expand=YES, fill=BOTH) 
                    circulo.create_oval(2, 2, 15, 15, width=1, fill='black') 
                    circulo.place(x=temp2*29, y=temp1*29)
                    win_coordenadas.destroy()
            if (temp1 or temp2) >= 20:
                messagebox.showerror('Error', "Coordenadas fuera de rango")

    win_coordenadas = Tk()
    win_coordenadas.title("Agregar coordenadas")
    win_coordenadas.geometry("370x300")
    
    etiqueta1 = Label(win_coordenadas, text='Ingresa las coordenadas', font='Helvetica 14 bold').place(x=70, y=20)
    etiqueta2 = Label(win_coordenadas, text='del nuevo punto:', font='Helvetica 14 bold').place(x=105, y=50)
    etiqueta3 = Label(win_coordenadas, text='Coordenada X:', font='Helvetica 12 bold').place(x=50, y=110)
    etiqueta4 = Label(win_coordenadas, text='Coordenada Y:', font='Helvetica 12 bold').place(x=50, y=140)
    etiqueta5 = Label(win_coordenadas, text='Las coordenadas van de 0,0 a 19,19', 
                                        font='Helvetica 10 bold italic').place(x=50, y=180)

    Combobox1 = ttk.Entry(win_coordenadas, width =7)
    Combobox1.place(x=210, y=110)
    
    Combobox2 = ttk.Entry(win_coordenadas, width =7)
    Combobox2.place(x=210, y=140)

    agregarP = Button(win_coordenadas, back_Image, text='Agregar', relief='flat', font='Verdana 15 bold', bg='SeaGreen2', fg='black',
                    activebackground='dodgerblue4', activeforeground='black', command=validacion).place(x=125, y=240)
    
    win_coordenadas.resizable(width=False, height=False)
    win_coordenadas.mainloop()

def pintar():
    global matrix_individuos
    global ciudades
    global ubicaciones

    last_way = matrix_individuos[0]
    cont = 0
    coor = []
    coor2 = []
    for index in last_way:    
        if cont < ciudades:
            ner = index - 1
            coor[:] = ubicaciones[ner]
            coorX = coor[0]
            coorY = coor[1]

            nest = last_way[cont + 1] - 1        
            coor2[:] = ubicaciones[nest]
            coor2X = coor2[0]
            coor2Y = coor2[1]
                
            distancia0 = coor2X - coorX
            distancia1 = coor2Y - coorY
            incremento0 = distancia0 / 10
            incremento1 = distancia1 / 10
            #Aqui es donde dibujara el camino
            for two in range(0,10):
                inst10 = Label(win_createMap, width=0, height=0,bg='tan2',text='.', 
                                font='Helvetica 1 italic').place(x=(coorX+incremento0)*29, y=(coorY+incremento1)*29)
                coorX = coorX + incremento0
                coorY = coorY + incremento1

            del coor[:]
            del coor2[:]
            cont += 1
    #time.sleep(0.5)#Se detiene para poder apreciar la ejecución a tiempo real

    last_way = matrix_individuos[0]
    cont = 0
    coor = []
    coor2 = []
    #Esto busca las coordenadas
    for index in last_way:    
        if cont < ciudades:
            ner = index - 1
            coor[:] = ubicaciones[ner]
            coorX = coor[0]
            coorY = coor[1]

            nest = last_way[cont + 1] - 1        
            coor2[:] = ubicaciones[nest]
            coor2X = coor2[0]
            coor2Y = coor2[1]
                
            distancia0 = coor2X - coorX
            distancia1 = coor2Y - coorY
            incremento0 = distancia0 / 10
            incremento1 = distancia1 / 10
            #Aqui es donde dibujara el camino
            for two in range(0,10):
                inst0 = Label(win_createMap, width=0, height=0,bg='gray93',text='.', 
                                font='Helvetica 1 italic').place(x=(coorX+incremento0)*29, y=(coorY+incremento1)*29)
                coorX = coorX + incremento0
                coorY = coorY + incremento1

            del coor[:]
            del coor2[:]
            cont += 1
    #time.sleep(0.05)

    #for two in ubicaciones:
    #        circulo = Canvas(win_createMap, width=15, height=15, bg='white') 
    #        circulo.pack(expand=YES, fill=BOTH) 
    #        circulo.create_oval(2, 2, 15, 15, width=1, fill='black') 
    #        circulo.place(x=two[0]*29, y=two[1]*29)
    
#Esta funcion contiene los datos de individuos y mutacion
def ingreso_datos():

    global individuos
    global mutacion

    #Aqui vamos a ingresar los datos para generar el numero de bits de cada individuo
    individuos = 7 #int(input('Ingresa el numero total de individuos: '))
    mutacion = 1.0 #float(input('Ingrese el porcentaje de mutacion (de 0.0 al 1.0): '))

#Esta funcion creo una matriz como un tipo mapa de manera aleatoria
def CreateMap():    
    global mapa
    global ubicaciones
    global ciudades

    #Aqui generamos el mapa de 20x20 como maximo
    mapa = [[0 for index in range(0, 20)]  for two in range(0, 20)]
    ubicaciones = []
    ubicaciones = [0] * ciudades
    ubi_1 = random.randrange(20)
    ubi_2 =random.randrange(20)
    for x in range(0,ciudades):
        #Este ciclo servira para evitar meter a dos individuos en una misma locacion
        while( mapa[ubi_2][ubi_1] !=0):
            ubi_1 = random.randrange(20)
            ubi_2 = random.randrange(20)

        mapa[ubi_2][ubi_1] = x + 1
        #Guardamos las coordenadas de cada ciudad para utilizarlas mas tarde
        ubicaciones[x] = [ubi_1, ubi_2]

#Esta funcion lo que hace es crear un mapa de donde van a quedar localizados las ciudades
def createPoblacion():
    
    global matrix_individuos  
    global ciudades
    global individuos
    
    #Generamos una matriz que va a guardar los indiviudos 
    matrix_individuos = [[0 for index in range(0,ciudades+1)] for two in range(0, individuos)]
    
    #Estos ciclos lo que haran sera llenar una matriz con los caminos que se generan de manera ramdon
    for x in range(0,individuos):
        ubicacion = random.randrange(ciudades)
        for y in range(0,ciudades):
            
            #Este ciclo lo que hace es verificar que en algun espacio del individuo
            #pueda ya estar lleno por otra ciudad y asi evitar que queden espacios vacios
            #y para controlar que el camino sea unico y si ciudades repetidas
            while( matrix_individuos[x][ubicacion] != 0 ):
                ubicacion = random.randrange(ciudades)

            #Llenamos al individuo y le pegamos al final la primera ciudad
            matrix_individuos[x][ubicacion] = y + 1
        matrix_individuos[x][ciudades] = matrix_individuos[x][0]

#Esta funciones genera el fitness de cada individuo para poder mutar
def crear_fitness():
    global matrix_individuos
    global graph
    global ubicaciones

    #Utilizaremos la regla euclidiana
    for index in matrix_individuos:
        suma = 0
        cont = 0
        coor = []
        coor2 = []
        #Este ciclo buscara las coordenadas de las ciudades de un individuo (obviamente pasando por todos)
        #y hara una operacion de distancia en donde podremos saber que camino es el mas corto
        for arreglo in index:
            if cont < ciudades:
                
                ner = arreglo - 1
                coor[:] = ubicaciones[ner]
                coorX = coor[0]
                coorY = coor[1]

                nest = index[cont + 1] - 1        
                coor2[:] = ubicaciones[nest]
                coor2X = coor2[0]
                coor2Y = coor2[1]

                distancia0 = coor2X - coorX
                distancia1 = coor2Y - coorY
                distancia = abs(distancia0) + abs(distancia1)
                
                del coor[:]
                del coor2[:]

                suma = suma + distancia
                cont += 1

        temp2 = suma
        
        graph.append( temp2 )

#Esta funcion mutara las ciudades
def mutacion_sele():
    
    global individuos
    global matrix_individuos
    global matrix_nueva
    global mutacion
    global mutacion_variciacional
    global ciudades

    zombie = 0 #esta variable se usara para la mutacion

    #Esto se copian todos los individuos para que se agreguen mas
    matrix_nueva[:] = matrix_individuos[:]

    zombie = int((mutacion*individuos))    
    temp = []
    temp2 = []
    device = 0
    for cat in range(zombie):
        azar = random.randrange(individuos)
        azar1 = random.randrange(ciudades)
        azar3 = random.randrange(ciudades)
        #Este while impediara que se cambie la primera y ultima ciudad y asi no alterar todo
        #el camino de manera drastica, por ende solo se podra cambiar las ciudades 
        #que esten en medio
        while ( azar1 == 0 or azar1 == ciudades or azar3 == 0 or azar3 == ciudades):
            azar1 = random.randrange(ciudades)
            azar3 = random.randrange(ciudades)

        temp[:] = matrix_individuos[azar][:]
        temp2[:] = temp[:]

        numero1 = temp[azar1]
        numero2 = temp[azar3]

        temp2[azar1] = numero2
        temp2[azar3] = numero1
        
        matrix_nueva.append(temp2)
        temp = []
        temp2 = []

def seleccion():
    global matrix_individuos
    global matrix_nueva
    global individuos
    global graph
    #aqui lo que haremos sera evaluar el fitness de todos
    #y hacer que solo pase los mejores
    
    ordenado = []
    desordenado = []
    buscar = 0
    encontrado = 0
    inicio = 0 

    #Se sacara el fitness de la matriz nueva para poder saber quienes son los mejores
    for index in matrix_nueva:
        suma = 0
        cont = 0
        coor = []
        coor2 = []
        for arreglo in index:
            if cont < ciudades:
                
                ner = arreglo - 1
                coor[:] = ubicaciones[ner]
                coorX = coor[0]
                coorY = coor[1]

                nest = index[cont + 1] - 1        
                coor2[:] = ubicaciones[nest]
                coor2X = coor2[0]
                coor2Y = coor2[1]

                distancia0 = coor2X - coorX
                distancia1 = coor2Y - coorY
                distancia = abs(distancia0) + abs(distancia1)
                
                del coor[:]
                del coor2[:]

                suma = suma + distancia
                cont += 1

        temp2 = suma
    
        ordenado.append( temp2 )
        desordenado.append( temp2 )

    ordenado.sort()

    inicio = 0
    index = 0
    #Aqui hacemos la busqueda de mejores y los pasamos a la nueva generacion
    #los  mejores son los mas bajos fitness
    while (index < individuos):
        encontrado = ordenado[inicio]
        buscar = desordenado[0]
        two=0
        while( buscar != encontrado ):
            buscar = desordenado[two]
            two += 1
        #Aqui hacemos la verificacion si es que el indice esta en 0 y no busque en arr[-1]
        if (two > 0):
            matrix_individuos[index] = matrix_nueva[two-1]
        else:
            matrix_individuos[index] = matrix_nueva[0]
        inicio += 1
        index += 1

#Esta funcion contiene las funciones para accionar todo el algoritmo de busqueda evolutiva
def beginAlgorit():
    global graph
    global win_createMap
    global ubicaciones
    global continue_b
    global modulo
    
    continue_b = Button(win_createMap, text='Comenzar', font='Helvetica 13 bold', bg='greenyellow', height=1, width=20,
                            relief='flat', command = beginAlgorit, state = DISABLED).place(x=634, y=416)
                            
    agregar = Button(win_createMap, text='Agregar ciudad', font='Helvetica 13 bold', bg='salmon', height=1, width=20,
                          relief='flat', command = aumentar, state = DISABLED).place(x=634, y=456)

    #Esto es para que el programa principal compile enteramente llamando a las funciones
    #dando solo una vez el ingreso de datos y la creacion de la poblacion
    promedios = []
    ingreso_datos()
    createPoblacion()
    if ciudades >= 2:
        modulo = 7
    if ciudades > 10:
        modulo = 19
    if ciudades > 35:
        modulo = 61
    if ciudades > 100:
        modulo = 103
    if ciudades > 200:
        modulo = 347      
        
    print(modulo)
    #Estas variables se usan para que el programa se pare solo "En teoria"
    indice = 0
    maximo = 5000
    mut = 0
    arbol = 0
    #Este ciclo lo que hace es que el programa se detenga solo, poniendo 
    #reglas de que si despues de ciertas repeticiones el maximo es el mismo
    #este ya encontro el maximo
    iteraciones = 0
    vaso = 0
    while(arbol < 110):
        
        iteraciones +=1
        crear_fitness()
        mutacion_sele()
        seleccion()
        temp = sum(graph)/individuos
        maxum = temp

        if( maxum < maximo ):
            maximo = maxum
            indice = 0
            if vaso%modulo ==0:
                pintar()
            vaso += 1

        if( maxum > maximo):
            maximo = maximo
            indice += 1

        if ( maxum == maximo ):
            indice +=1

        promedios.append(temp)
        temp = 0
        graph = []  
        matrix_nueva = []
    
        if( indice == 200 and mut == 0 ):
            mutacion_variciacional =  2        
            mut = 1
    
        if (indice == 199 and mut == 1):
            mut = 0
            mutacion_variciacional = 1
            indice = 0

        if (indice == 500 and mut == 1):
            mut = 2

        if indice >= 401 :
            arbol +=1

    #Aqui nos sercioraremos de que de verdad el ultimo camino sea el mas optimo
    graph = []
    ordenado = []
    crear_fitness()
    ordenado[:] = graph[:]
    ordenado.sort()

    inicio = 0
    index = 0
    encontrado = ordenado[inicio]
    buscar = graph[0]
    two=0
    while( buscar != encontrado ):
        buscar = graph[two]
        two += 1
    if (two > 0):
        last_way = matrix_individuos[two-1]
    else:
        last_way = matrix_individuos[0]    

    del graph[:]
    
    mejor_fitness = ordenado[0]

    del ordenado[:]
    #Esta parte del codigo dibujara el camino mas optimo encontrado
    cont = 0
    coor = []
    coor2 = []
    #Esto busca las coordenadas
    for index in last_way:    
        if cont < ciudades:
            ner = index - 1
            coor[:] = ubicaciones[ner]
            coorX = coor[0]
            coorY = coor[1]

            nest = last_way[cont + 1] - 1        
            coor2[:] = ubicaciones[nest]
            coor2X = coor2[0]
            coor2Y = coor2[1]
                
            distancia0 = coor2X - coorX
            distancia1 = coor2Y - coorY
            incremento0 = distancia0 / 30
            incremento1 = distancia1 / 30
            #Aqui es donde dibujara el camino
            for two in range(0,30):
                inst10 = Label(win_createMap, width=0, height=0,bg='DarkOrchid4',text='.', 
                                font='Helvetica 1 italic').place(
                                                            x=(coorX+incremento0)*29, y=(coorY+incremento1)*29)
                coorX = coorX + incremento0
                coorY = coorY + incremento1
            time.sleep(0.02)
            del coor[:]
            del coor2[:]
            cont += 1
    
    #Lo siguiente solo dibuja otra vez los circulos para cuestiones esteticas      
    for two in ubicaciones:
        circulo = Canvas(win_createMap, width=15, height=15, bg='white') 
        circulo.pack(expand=YES, fill=BOTH) 
        circulo.create_oval(2, 2, 15, 15, width=1, fill='black') 
        circulo.place(x=two[0]*29, y=two[1]*29)
    
    #Colocaremos cierta informacion sobre el ultimo camino
    #y etiquetas
    inst2 = Label(win_createMap, text='El mejor fitness es la', font= 'Arial 12 bold').place(x=650,y=210)
    inst3 = Label(win_createMap, text='menor distancia recorrida:', font= 'Arial 12 bold').place(x=650,y=230)
    inst4 = Label(win_createMap, text=mejor_fitness, font= 'Arial 12 bold').place(x=650,y=250)

    inst1 = Label(win_createMap, text='El numero de iteraciones:', font= 'Arial 12 bold').place(x=650,y=280)
    inst5 = Label(win_createMap, text=iteraciones, font= 'Arial 12 bold').place(x=650,y=300)



    #Aqui dibujamos la primera ciudad y la ultima para saber que se completo el camino
    #Azul primera ciudad, roja ultima ciudad
    one = last_way[ciudades]

    two = ubicaciones[one-1]
    circulo = Canvas(win_createMap, width=15, height=15, bg='white') 
    circulo.pack(expand=YES, fill=BOTH) 
    circulo.create_oval(2, 2, 15, 15, width=1, fill='blue') 
    circulo.place(x=two[0]*29, y=two[1]*29)
        
#Este programa termina todo
def exitProgram():
    sys.exit()

#Este programa va a la 2da fase del programa para la eleccion de ciudades
def Begin(variable):
    global win_askMeasurements
    global bandera
    global continue_b
    global win_Welcome
    
    #Esta funcion va a la parte ya de ejecucion donde ya mostro el mapa de puntos
    def continuacion():
        global mapa
        global ciudades
        global ubicaciones
        global win_createMap
        global continue_b
        global realTimeExecFlag
        global thread
        # Permite al usuario volver al menú principal.
        def backToMainMenu():
            global bandera
            win_createMap.destroy()
            # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
            bandera = 0
            Interfaz()

        #Lo que hace esta funcion es regresar a la ventana para seleccionar ciudaes
        def clearAll(rows, col):
            global mapa
            win_createMap.destroy()
            del mapa[:]
            del ubicaciones[:]         
            Begin(0)

        # Recuperamos los valores ingresados por el usuario en el spinbox
        # con esto recuperamos
        if  variable == 0:
            ciudades = int(spin_rows.get())
            CreateMap()
        if variable == 1:
            win_Welcome.destroy()

        rows = int(20)
        col = int(20)

        # Destruimos la ventana vieja para seguir trabajando con la nueva ventana "Create Map
        if variable == 0:
            win_askMeasurements.destroy()
        win_createMap = Tk()
        win_createMap.title("Mapa de las ciudades")
        win_createMap.geometry("870x600")

        thread = Thread(target=beginAlgorit)

        # Generación del mapa
        index = 0
        #Aqui dibujamos en el mapa los circulos
        for two in ubicaciones:
            circulo = Canvas(win_createMap, width=15, height=15, bg='white') 
            circulo.pack(expand=YES, fill=BOTH) 
            circulo.create_oval(2, 2, 15, 15, width=1, fill='black') 
            circulo.place(x=two[0]*29, y=two[1]*29)
        
        # Instrucciones, botones  y combobox --------------------------------------------------------------------
        inst1 = Label(win_createMap, text='Construido', font='Helvetica 24 bold').place(x=650, y=20)
        inst6 = Label(win_createMap, text="Si no le gusta el mapa", font='Helvetica 13 italic').place(x=650, y=75)
        inst7 = Label(win_createMap, text="puede generar uno nuevo", font='Helvetica 13 italic').place(x=650, y=100)
        inst8 = Label(win_createMap, text='dando clic en Atras', font='Helvetica 13 italic').place(x=650, y=125)
        inst9 = Label(win_createMap, text='y volviendo a la ', font='Helvetica 13 italic').place(x=650, y=150)
        inst10 = Label(win_createMap, text='ventana anterior', font='Helvetica 13 italic').place(x=650, y=175)

        inst2 = Label(win_createMap, text='Inicio del camino: Azul', font = 'Arial 12 bold').place(x=650,y=340)

        def startRealTime():#Acción del botón b_beginSearch, activa la bandera de ejeución a tiempo real
            thread.start()

        #Botón para limpiar el mapa, limpia "current_map" y devuelve los botones al formato original
        restart_b = Button(win_createMap, text='Nuevo mapa al azar', font='Helvetica 13 bold', bg='darkslategray2', height=1,
                            relief='flat', width=20, command=lambda r1=rows, c1=col: clearAll(r1, c1)).place(x=634, y=376)
        # Para continuar a la selección de algoritmos
        continue_b = Button(win_createMap, text='Comenzar', font='Helvetica 13 bold', bg='greenyellow', height=1, width=20,
                            relief='flat', command = startRealTime).place(x=634, y=416)

        # Para permitir al usuario volver al menú principal
        return_b = Button(win_createMap, text='Menu Principal', font='Helvetica 13 bold', bg='indianred1', height=1, width=20,
                          relief='flat', command=backToMainMenu).place(x=634, y=536)

        guardar = Button(win_createMap, text='Guardar Mapa', font='Helvetica 13 bold', bg='orchid2', height=1, width=20,
                          relief='flat', command=savefile).place(x=634, y=496)

        agregar = Button(win_createMap, text='Agregar ciudad', font='Helvetica 13 bold', bg='salmon', height=1, width=20,
                          relief='flat', command = aumentar).place(x=634, y=456)


        # Bloquea el cambio de tamaño de la ventana por cuestiones de formato
        win_createMap.resizable(width=False, height=False)
        win_createMap.mainloop()
    #---------------------------------------------------------------------------------------------------------
    #Esta funcion regresa al menu principal
    def backtoMenu():
        global bandera
        win_askMeasurements.destroy()
        # Antes de regreasr al menú principal es necesario limpiar el mapa para evitar que se tomen datos basura en el siguiente mapa
        bandera = 0
        Interfaz()

    if variable == 1:
        bandera = 1
        continuacion()
    else:
        #Evitamos que genere un error por destruir algo que no existe
        win_askMeasurements = Tk()
        if bandera == 0:
            win_Welcome.destroy()
            bandera = 1
    
        # Primero se necesita una ventana para solicitar las dimensiones del mapa a crear
        win_askMeasurements.title("Numero de ciudades")
        win_askMeasurements.geometry('500x200')

        #Todo lo siguiente son etiquetas y una cosita para seleccionar
        spin_rows = Spinbox(win_askMeasurements, from_=2, to=401, width=4, relief='flat', buttondownrelief='flat',
                            buttonuprelief='flat',
                            state='readonly', justify=CENTER, font='Helvetica 12', buttonbackground='lightskyblue1')

        spin_rows.place(x=320, y=101)

        Label(win_askMeasurements, text='En este apartado elegira el numero', font='Helvetica 14 bold').place(x=80,y=15)

        Label(win_askMeasurements, text='de ciudades a recorrer.', font='Helvetica 14 bold').place(x=130, y=40)
    
        Label(win_askMeasurements, text='*Por favor meter un numero entre 2 y 400*',
                font='Helvetica 12').place(x=95, y=68)

        Label(win_askMeasurements, text="Numero de ciudades: ", font='Helvetica 12').place(x=170, y=100)

        continue_b = Button(win_askMeasurements, text="Continuar", width=15, height=2, font='Helvetica 12 bold',
                            relief='flat', bg='orange', command = continuacion)
        continue_b.place(x=270, y=135)

        goback_b = Button(win_askMeasurements, text="Regresar al menu", width=15, height=2, font='Helvetica 12 bold',
                            relief='flat', bg='orange', command = backtoMenu).place(x=90, y=135)
    
        win_askMeasurements.resizable(width=False, height=False)
        win_askMeasurements.mainloop()  # al final del programa (mantiene la ventana )

# Interfaz principal del programa 
def Interfaz():
    
    global win_Welcome

    win_Welcome = Tk()

    win_Welcome.title("Algoritmo del Viajero")

    #Aqui anadimos la imagen
    image1 = PhotoImage(file="main_pict.gif")

    # Ajustar el tamaño de la ventana al tamaño de la imagen que tiene el diseño de la interfaz principal
    w = image1.width()
    h = image1.height()
    win_Welcome.geometry("%dx%d+0+0" % (w, h))

    # Ahora se hace un Label en el que se muestre la imagen y se configura para llenar la ventana
    back_Image = Label(win_Welcome, image=image1)
    back_Image.pack(side='top', fill='both', expand='yes')

    # Genera los tres botones: Crear mapa, Cargar mapa y Salir del programa
    b_Create = Button(back_Image, text='COMENZAR', relief='flat', font='Verdana 20 bold', bg="chartreuse3",
                      fg='black', activebackground='darkgreen', activeforeground='black', command=lambda:Begin(0))
    b_Create.place(x=24, y=290, width=442, height=118)
    
    b_Load = Button(back_Image, text='LOAD MAP', relief='flat', font='Verdana 20 bold', bg='plum2', fg='black',
                    activebackground='darkorange4', activeforeground='black', command=readfile)
    b_Load.place(x=186, y=420, width=280, height=118)

    b_Exit = Button(back_Image, text='EXIT', relief='flat', font='Verdana 20 bold', bg='deepskyblue1', fg='black',
                    activebackground='dodgerblue4', activeforeground='black', command=exitProgram)
    b_Exit.place(x=24, y=420, width=150, height=118)

    # Almacena la imagen
    back_Image.image = image1

    # No permite redimiensionar la ventana por cuestiones de formato
    win_Welcome.resizable(width=False, height=False)

    win_Welcome.mainloop()


#Damos inicio a TODO
Interfaz()
