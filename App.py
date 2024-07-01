import requests
import json
from Equipo import Equipo
from Estadio import Estadio
from Partido import Partido
import random
from Cliente import Cliente
from Boleto import Boleto
from Bebida import Bebida
from Alimento import Alimento
from Restaurante import Restaurante
import matplotlib.pyplot as plt
from tabulate import tabulate

def crear_estadio(filas,columnas):
    #Creamos una liosta vacia para representar el mapa del estadio 
    mapa = []
    for y in range(filas):
        #lista aux representa las filas del mapa 
        aux = []
        for x in range(columnas):
            #iniciamos los acientos como no ocupados 
            aux.append(False)
        mapa.append(aux)
    return mapa

def registrar_equipos():
    ''' Toma la estructura de la api, convierte cada elemento en un objeto y lo agrega a una nueva estructura(Lista equipos) '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
    r=requests.get(url)
    equipos_json=r.json()
    equipos=[]

    for equipo in equipos_json:
        aux=[]
        for k,v in equipo.items():
            aux.append(v)

        equipo_nuevo=Equipo(aux[0],aux[1],aux[2],aux[3])
        equipos.append(equipo_nuevo)

    return equipos

def registrar_restaurantes():
    
    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    r=requests.get(url)
    estadios_json=r.json()
    restaurantes=[]

    for estadio in estadios_json:
        for k,v in estadio.items():
            if k == "restaurants":
                #filtramos k = restaurantes por que lo que nos importa
                for restaurante in v:
                    #iteremos sobre"v" porque es la lista que contiene los restaurantes
                    aux=[]
                    #aux= ["solorzano",[.....productos....]]
                     # iteramos sobre el diccionario de restaurantes donde la primera key es el 
                    # nombre del restaurante y la segunda key es la lista de productos
                    for ke,ve in restaurante.items():
                        aux.append(ve)
                        productos=[]
                        #iteremos sobre la lista de productos del restaurente
                    for producto in aux[1]:
                        aux2=[]
                        # aux2 = ["Increible Plástico Pescado",quantity,price,stock,adicional]

                        for key,value in producto.items():
                            aux2.append(value)
                        # Creamos un objeto de tipo Alimento si el tipo de producto es "plate" o "package" 
                        # o un objeto de tipo Bebida si el tipo de producto es cualquier otro
                        #convertimos los elementos de la lista aux2 de la poscion 3 que seria el precio
                        # a flotantes, para poder hacer operaciones matematicas 
                        iva=float(aux2[2])*0.16
                        precio=iva+float(aux2[2])
                        if aux2[4]=="plate" or aux2[4]=="package":
                            nuevo_producto=Alimento(aux2[0],aux2[1],precio,aux2[3],aux2[4])
                            productos.append(nuevo_producto)
                        else:
                            nuevo_producto=Bebida(aux2[0],aux2[1],precio,aux2[3],aux2[4])
                            productos.append(nuevo_producto)
                    existe=False
                    #iteramos lista restaurantes y verificamos que si exiten los mismos restaurantes
                        # en dos estadios distintos solo se guarden una vez, por eso el condicional
                        # y luego el if not 
                    for restaurante in restaurantes:
            
                        if restaurante.nombre == aux[0]:
                            existe=True
                            break

                    if not existe:
                        nuevo_restaurante=Restaurante(aux[0],productos)
                        restaurantes.append(nuevo_restaurante)
    return restaurantes           

def registrar_estadios(restaurantes):
     
    ''' Toma la estructura de la api, convierte cada elemento en un objeto y lo agrega a una nueva estructura '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    r=requests.get(url)
    estadios_json=r.json()
    estadios=[]

    for estadio in estadios_json:
        aux=[]
        for k,v in estadio.items():
            aux.append(v)


        # aux = ["id","name","city",[capacity],[.....restaurants.........]]

        restaurantes_estadios=[]
        for restaurante_dict in aux[4]:
            
        #iteramos la lista de restaurantes que es la posicion numero 4 en la lista aux
            nombre=restaurante_dict["name"]

            for restaurante in restaurantes:
                if restaurante.nombre == nombre:
                    restaurantes_estadios.append(restaurante)
                    break
                #creamos el objeto estdio con la lista de objetos de restorentes
        
        # convertimos a las capacidades obtenidas de la estructura de datos en dos variables manejables 
        #para hacer la capacidad total de cada estadio
        i=int(aux[3][0])
        g=int(aux[3][1])
        capacidad=i+g
        
        nuevo_estadio=Estadio(aux[0],aux[1],aux[2],capacidad,restaurantes_estadios)
        estadios.append(nuevo_estadio)

    return estadios
   
def registrar_partidos(equipos,estadios):
    ''' Toma la estructura de la api, con objetos ya creados anteriormente y ciertos elementos de la api, crea un nuevo objeto y lo agrega a una nueva estructura '''

    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
    r=requests.get(url)
    partidos_json=r.json()
    partidos=[]

    for partido in partidos_json:
        aux=[]
        for k,v in partido.items():
            aux.append(v)
        # aux = ["id","number","equipo_l Dict","equipo_v Dict","date","group","stadium_id"]
        id_l=aux[2]["id"]
        id_v=aux[3]["id"]

        for equipo in equipos:
            if equipo.id == id_l:
                equipo_l=equipo
                break

        for equipo in equipos:
            if equipo.id == id_v:
                equipo_v=equipo
                break

        aux[2]=equipo_l
        aux[3]=equipo_v
        # aux = ["id","number","OBJ equipo_l","OBJ equipo_v","date","group","stadium_id"]

        id_equipo=aux[6]
        for estadio in estadios:
            if estadio.id == id_equipo:
                estadio_partido=estadio
                break

        aux[6]=estadio_partido
        # aux = ["id","number","OBJ equipo_l","OBJ equipo_v","date","group","OBJ stadium"]

        #usamos la funcion map para crear un mapa para cada partido, se le pasan como parametros la capacidad 
        #del estadio entre las columnas y las columnas del mismo 
        mapa=crear_estadio(estadio.capacidad//10,10)
        nuevo_partido = Partido(aux[0],aux[1],aux[2],aux[3],aux[4],aux[5],aux[6],mapa)
        partidos.append(nuevo_partido)
        
    return partidos

def error():
    ''' Imprime error para que el usuario sepa que el dato ingresado no es valido '''
    print("\n\n\t*** ERROR! * DATO INGRESADO NO VALIDO ***\t\n\n")

######################################## GESTION DE PARTIDOS Y ESTADIOS ########################################

def opcion_1(equipos,partidos,estadios):
    ''' Muestra la opcion "Gestion de partidos y estadios" '''
    while True:
        
        
        opcion=input("\n\n\t\t--- GESTION DE PARTIDOS Y ESTADIOS ---\n\n 1- Buscar todos los partidos de un país\n 2- Buscar todos los partidos que se jugarán en un estadio específico\n 3- Buscar todos los partidos que se jugarán en una fecha determinada\n 4- Retroceder\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        while not opcion.isnumeric() or int(opcion) not in range(1,5):
            error()
            opcion=input("\t\t--- GESTION DE PARTIDOS Y ESTADIOS ---\n\n 1- Buscar todos los partidos de un país\n 2- Buscar todos los partidos que se jugarán en un estadio específico\n 3- Buscar todos los partidos que se jugarán en una fecha determinada\n 4- Retroceder\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")

        opcion=int(opcion)

        if opcion==1:
            opcion_1_1(equipos,partidos)
        
        elif opcion==2:
            opcion_1_2(estadios,partidos)

        elif opcion==3:
            opcion_1_3(partidos)

        else:
            break

def el_pais_existe(equipos,pais):
    ''' Verifica si el pais ingresado existe '''

    for equipo in equipos:
        if equipo.nombre==pais:
            return True
    
    return False

def opcion_1_1(equipos,partidos):
    ''' Muestra los partidos de un pais "Gestion de partidos y estadios" '''

    print("\n\n\t--- Busqueda de todos los partidos de un país ---\n")
    pais=input("\n - Ingrese el nombre (EN INGLES) del pais: ")
    pais=pais.title()
    existe=el_pais_existe(equipos,pais)
    
    while pais.isnumeric():
        error()
        pais=input(" - Ingrese el nombre (EN INGLES) del pais: ")
        pais=pais.title()
        existe=el_pais_existe(equipos,pais)

    if not existe:
        error()
        print("\t\t*** NO SE ENCONTRO AL PAIS INGRESADO ***\n\n")
    
    else:
        print("\n\n\t\t\t\t*** PARTIDOS ENCONTRADOS ***\n")
        for partido in partidos:
            if partido.equipo_l.nombre==pais or partido.equipo_v.nombre==pais:
                print(f"\n - ID:{partido.id} || L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' ||| Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}")

def el_estadio_existe(estadios,estadio):
    ''' Verifica si el estadio ingresado existe '''

    for estadio in estadios:
        if estadio.nombre==estadio:
            return True
    
    return False

def opcion_1_2(estadios,partidos):
    ''' Muestra la opcion 2 del menu "Gestion de partidos y estadios" '''

    print("\n\n\t--- Busqueda de todos los partidos de un estadio ---\n")
    estadio=input("\n - Ingrese el nombre del estadio: ")
    estadio=estadio.title()
    existe=el_estadio_existe(estadios,estadio)
    
    if not existe:
        error()
        print("\t*** NO SE ENCONTRARON PARTIDOS EN EL ESTADIO INGRESADO ***\n\n")

    else:
        print("\n\n\t\t\t\t*** PARTIDOS ENCONTRADOS ***\n")
        for partido in partidos:
            if partido.estadio.nombre==estadio:
                print(f"\n - ID:{partido.id} || L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' ||| Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}")

def la_fecha_existe(fecha_part,partidos):
    ''' Verifica si en la fecha ingresada existen partidos '''

    for partido in partidos:
        if fecha_part in partido.fecha:
            return True
    
    return False

def opcion_1_3(partidos):
    ''' Muestra la opcion 3 del menu "Gestion de partidos y estadios" '''

    while True:
        print("\n\n\t--- Busqueda de todos los partidos en una fecha determinada ---\n")
        dia=input("\n - Ingrese en numeros el dia: ")
        while not dia.isnumeric() or int(dia) not in range(1,32):
            error()
            dia=input(" - Ingrese en numeros el dia: ")
        
        mes=input("\n - Ingrese en numeros el mes: ")
        while not mes.isnumeric() or int(mes) not in range(1,13):
            error()
            mes=input(" - Ingrese en numeros el mes: ")

        fecha_part=f"2024-{mes}-{dia}"
        existe=la_fecha_existe(fecha_part,partidos)
 
        if existe:
            print("\n\n\t\t\t\t*** PARTIDOS ENCONTRADOS ***\n")
            for partido in partidos:
                if fecha_part in partido.fecha:
                    print(f"\n - ID:{partido.id} || L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' ||| Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}")

            break
        
        else:
            error()
            print("\t\t*** NO SE ENCONTRARON PARTIDOS EN LA FECHA ***\n\n")

            break
    
######################################## GESTION DE VENTAS Y ENTRADAS ########################################

def val_nombre():
    ''' Valida y recoleta el nombre '''

    nombre=input("\n - Ingrese el nombre del cliente: ")
    while not nombre.isalpha():
        error()
        nombre=input(" - Ingrese el nombre del cliente: ")
    nombre=nombre.capitalize()

    return nombre

def val_cedula():
    ''' Valida y recolecta la cedula '''

    cedula=input("\n - Ingrese la cedula del cliente: ")
    while not cedula.isnumeric() or len(cedula)<=7:
        error()
        cedula=input(" - Ingrese a cedula del cliente: ")

    return cedula

def val_edad():
    ''' Valida y recolecta la edad '''
    edad=input("\n - Ingrese la edad del cliente: ")
    while not edad.isnumeric() or int(edad) not in range(1,110):
        error()
        edad=input(" - Ingrese a edad del cliente: ")
    edad=int(edad)
    return edad

def numero_partido(partidos):
    ''' Recoleta e imprime los partidos '''

    print("\n\n\t\t\t\t========== PARTIDOS ==========\n\n")
    #inicializa un contador para enumerar los partidos
    cont=0
    for partido in partidos:
        cont+=1
        #imprime todos los partidos 
        print(f" {cont}- L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' ||| Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}\n")

    nro_partido=input(" ---> Ingrese el numero correspondiente al partido que desea asistir: ")

    while not nro_partido.isnumeric() or int(nro_partido) not in range(1,cont+1):
        error()
        cont=0
        for partido in partidos:
            cont+=1
            print(f" {cont}- L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' ||| Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}\n")

        nro_partido=input(" ---> Ingrese el numero correspondiente al partido que desea asistir: ")
    
    cont=0
    for partido in partidos:
        cont+=1
        if cont==int(nro_partido):
            return partido

def tipo_entrada(tipos_entradas):
    ''' Recoleta e imprime los tipos de entradas  '''

    print("\n\n\t\t--- TIPOS DE ENTRADA ---\n\n")
    cont=0
    # Itera sobre los tipos de entradas y los imprime con su número y precio
    for k,v in tipos_entradas.items():
        cont+=1
        print(f" {cont}- '{k}'    || Precio: ${v}")
    
    tipo=input("\n - Ingrese el numero correspondiente a la opcion que desea: ")
     # Valida la entrada del usuario
    while not tipo.isnumeric() or int(tipo) not in range(1,cont+1):
        # Si la entrada es inválida, llama a la función error() y vuelve a imprimir los tipos de entradas
        error()
        print("\n\t\t--- TIPOS DE ENTRADA ---\n\n")
        cont=0
        for k,v in tipos_entradas.items():
            cont+=1
            print(f" {cont}- '{k}'    || Precio: ${v}")
        
        tipo=input("\n - Ingrese el numero correspondiente a la opcion que desea: ")
    # Itera sobre los tipos de entradas nuevamente para encontrar el seleccionado por el usuario
    cont=0
    for k,v in tipos_entradas.items():
        cont+=1
        if cont==int(tipo):
            # Devuelve el tipo de entrada seleccionado y su precio
            return k,v

def val_existe(clientes,cedula):
    ''' Verifica si el cliente ya existe '''
    # Itera sobre los clientes registrados
    for k,v in clientes.items():
        # Verifica si la cédula del cliente actual coincide con la cédula proporcionada
        if k.cedula==cedula:
            # Si coincide, devuelve True y el objeto cliente que coincide
            return True,k
        # Si no se encontró un cliente que coincida, devuelve False y un mensaje de "no"
    return False,"no"

def val_partido(entradas,ticket):
    ''' Verifica si ya se han comprado entradas para ese partido '''

    for k,v in entradas.items():
            if ticket.partido==k:
                return True
    return False

def val_ocupado(mapa,fila,columna):
    f=0
    # Itera sobre las filas del mapa
    for x in mapa:
        # Incrementa el contador de filas
        f+=1
        # Verifica si se ha llegado a la fila especificada
        if f==(int(fila)):
            # Inicializa un contador para llevar la cuenta de las columnas
            c=0
            # Itera sobre las columnas de la fila actual
            for y in x:
                 # Incrementa el contador de columnas
                c+=1
                 # Verifica si se ha llegado a la columna especificada
                if c==(int(columna)):
                    # Verifica si la posición está ocupada (False significa que está disponible)
                    if y==False:
                        # Marca la posición como ocupada (True)
                        mapa[f-1][c-1]=True
                        return True
                     # Devuelve True para indicar que la posición se ha ocupado con éxito
                    else:
                        # Devuelve False para indicar que la posición ya está ocupada
                        return False

def imprimir_estadio(partido):
    ''' Imprime el estadio y permite seleccionar un asiento '''
    
    # Obtiene el mapa del estadio y su nombre
    mapa = partido.mapa
    nombre = partido.estadio.nombre
    
    # Calcula el número de filas y columnas del estadio
    filas = partido.estadio.capacidad // 10
    columnas = 10
    
    # Bucle infinito para seleccionar un asiento
    while True:
        # Imprime el título de selección de asiento
        print("\n\n\t\t--- SELECIONANDO ASIENTO ---\n\n")
        
        # Pide la fila al usuario
        fila = input(" - Seleccione la fila:  ")
        while not fila.isnumeric() or int(fila) not in range(1, filas + 1):
            # Si la entrada no es válida, muestra un error y pide de nuevo
            error()
            fila = input(" - Seleccione la fila:  ")
        
        # Pide la columna al usuario
        columna = input("\n - Seleccione la columna: ")
        while not columna.isnumeric() or int(columna) not in range(1, columnas + 1):
            # Si la entrada no es válida, muestra un error y pide de nuevo
            error()
            columna = input(" - Seleccione la columna: ")
        
        # Verifica si el asiento está disponible
        puede = val_ocupado(mapa, fila, columna)
        
        if puede:
            # Si el asiento está disponible, imprime un mensaje de éxito y sale del bucle
            print("\n\n\t\t\t\t*** ASIENTO GUARDADO CON EXITO ***\n\n")
            break
        else:
            # Si el asiento no está disponible, muestra un error y vuelve a imprimir el estadio
            error()
            print("\t\t*** EL ASIENTO ESCOGIDO YA ESTA OCUPADO ***\n\n")
            print("*" * (len(mapa[1]) - 5) + f" ESTADIO '{nombre}' " + "*" * (len(mapa[1]) - 5))
            print("\n")
            
            # Imprime el estadio con las filas y columnas numeradas
            nums = "    "
            for i, x in enumerate(mapa[1]):
                if i > 8:
                    nums += str(i + 1) + "| "
                else:
                    nums += str(i + 1) + " | "
            print(nums)
            for i, x in enumerate(mapa):
                if i > 8:
                    auxiliar = str(i + 1)
                else:
                    auxiliar = str(i + 1) + " "
                for y in x:
                    if y == True:
                        v = ("X")
                        auxiliar += f"| {v} "
                    else:
                        auxiliar += "|   "
                print("   " + "-" * len(mapa[1] * 4))
                print(auxiliar)
    
    # Imprime el estadio final con el asiento seleccionado
    print("*" * (len(mapa[1]) - 5) + f" ESTADIO '{nombre}' " + "*" * (len(mapa[1]) - 5))
    print("\n")
    
    nums = "    "
    for i, x in enumerate(mapa[1]):
        if i > 8:
            nums += str(i + 1) + "| "
        else:
            nums += str(i + 1) + " | "
    print(nums)
    for i, x in enumerate(mapa):
        if i > 8:
            auxiliar = str(i + 1)
        else:
            auxiliar = str(i + 1) + " "
        for y in x:
            if y == True:
                v = ("X")
                auxiliar += f"| {v} "
            else:
                auxiliar += "|   "
        print("   " + "-" * len(mapa[1] * 4))
        print(auxiliar)
    
    # Devuelve el asiento seleccionado y el mapa actualizado
    asiento = f" F: {fila} C: {columna}"
    return asiento, mapa, fila, columna

def es_vampiro(cedula):
    num_str = str(cedula)
    num_digits = len(num_str)
    half_digits = num_digits // 2

    #  Iteramos sobre todos los posibles pares de números con la misma cantidad de 
    # dígitos que la mitad del número original
    for i in range(10**(half_digits-1), 10**half_digits):
        for j in range(i, 10**half_digits):
            #  Verificamos si el producto de los dos números es igual al número original
            if i * j == cedula:
                #  Convertimos los dos números a cadenas para poder trabajar con sus dígitos
                i_str = str(i)
                j_str = str(j)
                
                #  Verificamos si todos los dígitos del número original están presentes en los dos números
                if set(i_str + j_str) == set(num_str):
                    return True

    return False

def opcion_2(partidos,clientes,entradas):
    ''' Ejecuta la opcion "Gestión de venta de entradas" '''

    tipos_entradas={"General":35,"VIP":75}
    opcion=input(f"\n\n\t\t--- GESTION DE VENTAS DE ENTRADAS ---\n\n 1- Registrar cliente\n 2- Retroceder\n\n ---> Ingrese el numero correspondiente al opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,3):
        error()
        opcion=input(f"\t\t--- GESTION DE VENTAS DE ENTRADAS ---\n\n 1- Registrar cliente\n 2- Retroceder\n\n ---> Ingrese el numero correspondiente al opcion que desea: ")

    if opcion=="1":
        print("\n\n\t\t--- REGISTRANDO CLIENTE ---\n")
        cedula=val_cedula()
        existe,c=val_existe(clientes,cedula)

        if not existe:
            nombre=val_nombre()
            edad=val_edad()

        else:
            comprador=c
            nombre=c.nombre

        partido=numero_partido(partidos)
        tipo,costo=tipo_entrada(tipos_entradas)
        # IMPRIMIR ESTADIO
        asiento,mapa,fila,columna=imprimir_estadio(partido)
        # Si cédula es un número vampiro su entrada tiene un 50% de descuento y se le notificara al cliente
        descuento=es_vampiro(int(cedula))
        if descuento:
            print("*** FELICIDADES! USTED ES UN VAMPIRO Y TIENE UN 50% DE DESCUENTO ***")
            descuento=0.5
                
        else:
            descuento=0
            
        subttl=costo-costo*descuento
        iva=subttl*0.16
        total=subttl+iva
        print(f'''
        ======================================= FACTURA ===================================

            - Nombre: {nombre} || - Cedula: {cedula}

            * Informacion de la compra *

            - Partido: 
                    L: '{partido.equipo_l.nombre}' vs V: '{partido.equipo_v.nombre}' 
                    Estadio: '{partido.estadio.nombre}' ||| Fecha: {partido.fecha}
            
            - Tipo de entrada: '{tipo}'  --- Costo: ${costo}
            - Asiento: {asiento}

                                        Descuento: ${descuento}
                                        SUBTTL: ${subttl}
                                        IVA: ${iva} (16%)

                                        TOTAL: ${total}
        ====================================================================================
        ''')

        continuar=input("\n - Desea proceder con el pago? (S: SI ó N: NO): ")
        continuar=continuar.capitalize()
        while not continuar.isalpha() or continuar!="N" and continuar!="S":
            error()
            continuar=input(" - Desea proceder con el pago? (S: SI ó N: NO): ")
            continuar=continuar.capitalize()

        if continuar=="S":
            
            letras="abcdehijklmnopqrstuvwxyz"
            numeros="0123456789"
            simbolos="!@#$%&*_-:;Æ?€€°·”/"
            codigo=""

            cont=0
            while cont<5:
                cont+=1
                x=random.randint(0, len(letras)-1)
                y=random.randint(0, len(numeros)-1)
                z=random.randint(0, len(simbolos)-1)
                letra=letras[x]
                numero=numeros[y]
                simbolo=simbolos[z]
                x=f"{letra}{simbolo}{numero}"
                codigo+=x
            print("\n\n\t *** PAGO REGISTRADO CON EXITO ***\n\n")
            asistencia=False
            ticket=Boleto(partido,tipo,total,codigo,asistencia)
            
            partido_regis=val_partido(entradas,ticket)
            if not partido_regis:
                entradas[ticket.partido]=[]
                entradas[ticket.partido].append(ticket)

            elif partido_regis:
                entradas[ticket.partido].append(ticket)


            if not existe:
                comprador=Cliente(nombre,cedula,edad)
                clientes[comprador]=[]

            clientes[comprador].append(ticket)
           
            print(f"  Su codigo de entrada es (RECUERDELO): {codigo} ")
        
        else:
            mapa[int(fila)-1][int(columna)-1]=False

        return clientes,entradas

    else:
        return clientes,entradas

######################################## GESTION DE ASISTENCIA Y PARTIDOS ########################################

def val_ticket(clientes,codigo):
    ''' Valida que el codigo ingresado pertenezca a una entrada '''

    for cliente,tickets in clientes.items():
        for ticket in tickets:
            if ticket.codigo==codigo:
                return True
    return False

def val_asistencia(clientes,codigo):
    ''' Verifica si ya el ticket fue utilizado '''

    for cliente,tickets in clientes.items():
            for ticket in tickets:
                if ticket.codigo==codigo and ticket.asistencia==True:
                    return True

def cambiar_asistencia(clientes, codigo, entradas):
    ''' Cambia el estado de asistencia de una entrada '''
    
    # Itera sobre los clientes y sus tickets
    for cliente, tickets in clientes.items():
        for ticket in tickets:
            # Verifica si el ticket coincide con el código proporcionado
            if ticket.codigo == codigo:
                # Cambia el estado de asistencia del ticket a True
                ticket.asistencia = True
    
    # Itera sobre las entradas y sus tickets
    for k, v in entradas.items():
        for x in v:
            # Verifica si el ticket coincide con el código proporcionado
            if ticket.codigo == codigo:
                # Cambia el estado de asistencia del ticket a True
                ticket.asistencia = True
                # Devuelve None (no es necesario, pero se agrega un return para claridad)
                return

def opcion_3(clientes,entradas):
    ''' Ejecuta la opcion "Gestión de asistencia y partidos" '''
    while True:
        opcion=input("\n\n\t\t--- MENU DE ASISTENCIA Y PARTIDOS ---\n\n 1- Ingresar al estadio \n 2- Retroceder\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        while not opcion.isnumeric() or int(opcion )not in range(1,3):
            error()
            opcion=input("\t\t--- MENU DE ASISTENCIA Y PARTIDOS ---\n\n 1- Ingresar al estadio \n 2- Retroceder\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")

        if opcion=="1":
            print("\n\n\t\t--- GESTION DE ASISTENCIA Y PARTIDOS ---\n\n")
            codigo=input(" - Ingrese el codigo de verificacion de su entrada: ")
            while len(codigo)!=15:
                error()
                codigo=input(" - Ingrese el codigo de verificacion de su entrada: ")

            existe=val_ticket(clientes,codigo)
            asistencia=val_asistencia(clientes,codigo)

            if existe and not asistencia:
                cambiar_asistencia(clientes,codigo,entradas)
                print("\n\n\t\t\t\t*** TICKET INGRESADO CON EXITO ***\n")
                return clientes

            else:
                error()
                print("\t\t*** EL TICKET YA INGRESÓ O CODIGO NO VALIDO ***\n\n")
                

        else:
            return clientes

######################################## GESTION DE RESTAURANTES ########################################

def val_nombre_prod():
    ''' Valida el nombre del producto ingresado'''

    nombre=input("\n - Ingrese el nombre del producto: ")
    while nombre.isnumeric():
        error()
        nombre=input("\n - Ingrese el nombre del producto: ")
    
    return nombre.title()

def existe_prod(nombre,restaurantes):
    ''' Valida que el producto ingresado exista '''

    for restaurante in restaurantes:
        for producto in restaurante.producto:
            if producto.nombre==nombre:
                return True

    return False

def busqueda_1(nombre, restaurantes):
    ''' Muestra los productos por el nombre ingresado '''
    
    # Imprime un título para indicar que se muestran los artículos encontrados
    print("\n\n\n\t\t\t--- ARTICULOS ENCONTRADOS ---\n")
    
    # Itera sobre los restaurantes y sus productos
    for restaurante in restaurantes:
        for producto in restaurante.producto:
            # Verifica si el nombre del producto coincide con el nombre ingresado
            if producto.nombre == nombre:
                # Verifica si el producto es de tipo Alimento
                if type(producto.nombre) == Alimento:
                    # Imprime la información del producto con formato específico para Alimento
                    print(f"\n - Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")
                else:
                    
                    print(f" \n- Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")
                # Devuelve None (no es necesario, pero se puede agregar un return para claridad)
                return

def busqueda_2(restaurantes):
    ''' Muestra los productos del tipo ingresado '''
    
    # Crea una lista de tipos de productos únicos
    tipos = []
    for restaurante in restaurantes:
        for producto in restaurante.productos:
            if producto.tipo not in tipos:
                tipos.append(producto.tipo)
    
    # Muestra la lista de tipos de productos
    cont = 0
    print("\n\n\t\t--- BUSQUEDA POR TIPO ---\n\n")
    for x in tipos:
        cont += 1
        print(f" {cont}- '{x}' ")
    
    # Pide al usuario que ingrese el número correspondiente al tipo de producto que desea buscar
    tipo = input("\n - Ingrese el numero correspondiente al tipo de que desea buscar: ")
    
    # Verifica que la entrada sea válida
    while not tipo.isnumeric() or int(tipo) not in range(1, cont + 1):
        error()  
        print("\t\t--- BUSQUEDA POR TIPO ---\n\n")
        cont = 0
        for x in tipos:
            cont += 1
            print(f" {cont}- '{x}' ")
        tipo = input("\n - Ingrese el numero correspondiente al tipo de que desea buscar: ")
    
    
    tipo = int(tipo)
    
    # Busca el tipo de producto correspondiente a la entrada del usuario
    cont = 0
    for x in tipos:
        cont += 1
        if cont == tipo:
            tipo = x
            break
    
    # Muestra los productos que coinciden con el tipo seleccionado
    print("\n\n\n\t\t\t--- ARTICULOS ENCONTRADOS ---\n")
    impresos = []
    for restaurante in restaurantes:
        for producto in restaurante.productos:
            if producto.tipo == tipo:
                if producto.nombre not in impresos:
                    impresos.append(producto.nombre)
                    if type(producto) == Alimento:
                        print(f"\n - Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")
                    else:
                        print(f"\n - Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")
    
    return

def val_numero():
    ''' Valida que el numero ingresado por el usuario sea entero'''

    numero=input("\n - Ingrese en numeros enteros el monto: ")
    while not numero.isnumeric() or int(numero)<=0:
        error()
        numero=input(" - Ingrese en numeros enteros el monto: ")
    return int(numero)

def busqueda_3(restaurantes):
    ''' Muestra los productos en el rango ingresado '''
    print("\n\n\t\t--- BUSQUEDA POR RANGO ---\n\n")
    print(" * Precio minino: ")
    p_min=val_numero()

    print("\n * Precio maximo: ")
    p_max=val_numero()
    
    impresos=[]
    for restaurante in restaurantes:
        for producto in restaurante.productos:
            if float(producto.precio)>=p_min and float(producto.precio)<=p_max:

                if producto.nombre not in impresos:
                    impresos.append(producto.nombre)

                    if len(impresos)==1:
                        print("\n\n\n\t\t\t--- ARTICULOS ENCONTRADOS ---\n")

                    if type(producto)==Alimento:
                        print(f"\n - Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")

                    else:
                        print(f"\n - Nombre: {producto.nombre} || Precio: ${producto.precio} || Tipo: {producto.tipo} || Stock: {producto.stock}")

    if len(impresos)==0:
        error()
        print("\t\t*** NO HAY PRODUCTOS EN ESE RANGO ***\n\n")

def opcion_4(partidos,clientes):
    ''' Ejecuta la opcion "Gestión de Restaurantes" '''
    while True:
        menu=input("--- GESTION DE RESTAURANTES PARA VIP---\n\n 1- Ingresar codigo de entrada\n 2- Retroceder\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")

        if menu=="1":
            cod=input("\n - Ingrese el codigo de entrada: ")
            existe=val_ticket(clientes,cod)

            if existe:
                vip=False
                for k,v in clientes.items():
                    for ticket in v:
                        if ticket.tipo_entrada=="VIP" and ticket.codigo==cod:
                            vip = True
                            restaurantes = ticket.partido.estadio.restaurantes

                if vip:
                    busqueda=input("\n\n\t\t--- BUSQUEDA DE PRODUCTOS ---\n\n 1- Busqueda por nombre\n 2- Busqueda por tipo\n 3- Busqueda por rango de precio\n 4- Retroceder\n\n ---> Ingrese el numero correspondiente al tipo de busqueda que desea realizar: ")
                    while not busqueda.isnumeric() or int(busqueda) not in range(1,5):
                        error()
                        busqueda=input("\t\t--- BUSQUEDA DE PRODUCTOS ---\n\n 1- Busqueda por nombre\n 2- Busqueda por tipo\n 3- Busqueda por rango de precio\n 4- Retroceder\n\n ---> Ingrese el numero correspondiente al tipo de busqueda que desea realizar: ")

                    if busqueda=="1":
                        print("\n\n\t\t--- BUSQUEDA POR NOMBRE ---\n\n")
                        nombre=val_nombre_prod()
                        existe=existe_prod(nombre,restaurantes)
                        
                        if not existe:
                            error()
                            print("\t*** EL PRODUCTO INGRESADO NO EXISTE O NO ES VALIDO ***\n\n")
                        
                        else:
                            busqueda_1(nombre,restaurantes)

                    elif busqueda=="2":
                        busqueda_2(restaurantes)

                    elif busqueda=="3":
                        busqueda_3(restaurantes)

                    else:
                        break
                else:
                    print("\n\n\t\t*** CODIGO NO VALIDO NO ERES VIP ***\n\n")
            
            else:
                print("\n\n\t\t*** CODIGO NO VALIDO ***\n\n")

        else:
            break

######################################## GESTION DE VENTAS DE RESTAURANTE ########################################

def sumar_cant(restaurante_seleccionado,compra):
    

    for producto in restaurante_seleccionado:
        for pedido in compra:
            if producto.nombre==pedido[0].nombre:
                #print(f"\n\n\nLa cantidad de stock era: {producto.stock}")
                #print(f"La cantidad de vendidos era: {producto.quantity}\n\n\n")
                producto.stock+=pedido[1]
                producto.quantity-=pedido[1]
                #print(f"\n\n\nLa cantidad de stock es: {producto.stock}")
                #print(f"La cantidad de vendidos es: {producto.quantity}\n\n\n")

def restar_cant(restaurante_seleccionado,compra):
   

    for producto in restaurante_seleccionado.productos:
        for pedido in compra:
            if producto.nombre==pedido[0].nombre:
                #print(f"\n\n\nLa cantidad de stock era: {producto.stock}")
                #print(f"La cantidad de vendidos era: {producto.quantity}\n\n\n")
                producto.stock-=pedido[1]
                producto.quantity+=pedido[1]
                #print(f"\n\n\nLa cantidad de stock es: {producto.stock}")
                #print(f"La cantidad de vendidos es: {producto.quantity}\n\n\n")

def es_numero_perfecto(cedula):
    cedula = int(cedula)
    divisores = []
    div = 0
    # Bucle para encontrar los divisores de cedula
    while div < cedula - 1:
        div += 1
        # Verificar si div es un divisor de cedula
        if cedula % div == 0:
            # Agregar div a la lista de divisores si es un divisor
            divisores.append(div)

    # Verificar si la suma de los divisores es igual a cedula
    if sum(divisores) == cedula:
        # Si es así, devuelve True (cedula es un número perfecto)
        return True

    else:
        # Si no es así, devuelve False (cedula no es un número perfecto)
        return False

def desea_comprar_mas():
    ''' Pregunta al usuario si desea comprar algun otro producto de ese restaurante '''

    continuar=input("\n - ¿Desea comprar algo mas? (S: SI ó N: NO): ")
    continuar=continuar.capitalize()
    while not continuar.isalpha() or continuar!="N" and continuar!="S":
        error()
        continuar=input(" - ¿Desea comprar algo mas? (S: SI ó N: NO): ")
        continuar=continuar.capitalize()

    if continuar=="S":
        return True

    else:
        return False

def val_cant():
    ''' Valida la cantidad del producto '''

    cant=input(" \n - Ingrese en numeros la cantidad que desea: ")
    while not cant.isnumeric() or int(cant)<=0:
        error()
        cant=input(" - Ingrese en numeros la cantidad que desea: ")

    return int(cant)

def opcion_5_1():
    opcion=input("\n\n\t\t--- MENU DE RESTAURANTE ---\n\n 1- Ingresar a un restaurante\n 2- Retroceder\n\n ---> Ingresar el numero correspondiente a la opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,3):
        error()
        opcion=input("\t\t--- MENU DE RESTAURANTE ---\n\n 1- Ingresar a un restaurante\n 2- Retroceder\n\n ---> Ingresar el numero correspondiente a la opcion que desea: ")

    return opcion

def opcion_5(clientes):
    ''' Ejecuta la opcion "Gestión de ventas de restaurante '''

    while True:
        opcion=opcion_5_1()

        if opcion=="1":
            cod=input("\n - Ingrese el codigo de entrada: ")
            existe=val_ticket(clientes,cod)

            if existe:
                vip=False
                # Verificar si el cliente es VIP
                for k,v in clientes.items():
                    if not vip:
                        for ticket in v:
                            if ticket.tipo_entrada=="VIP" and ticket.codigo==cod:
                                vip = True
                                ticket = ticket
                                cliente = k
                                break
                    else:
                        break
                    
                if vip:
                    # Obtener el estadio y los restaurantes asociados
                    estadio=ticket.partido.estadio
                    restaurantes_estadio=estadio.restaurantes

                    contador = 0
                    # Mostrar los restaurantes disponibles
                    for restaurante in restaurantes_estadio:
                        contador+=1
                        print(f" {contador}- *** RESTAURANTE '{restaurante.nombre}' ***\n")

                    n_restaurant=input("\n---> Ingrese el numero correspondiente al restaurante que desea: ")

                    while not n_restaurant.isnumeric() or int(n_restaurant) not in range(1,contador+1):
                        error()
                        n_restaurant=input("\n---> Ingrese el numero correspondiente al restaurante que desea: ")
                    
                    restaurante_seleccionado=restaurantes_estadio[int(n_restaurant)-1]
                    
                    compra=[]
                    while True:
                        # Mostrar los productos disponibles en el restaurante
                        pedido=[]
                        cont=0
                        for productos in restaurante_seleccionado.productos:
                            cont+=1
                            print(f" {cont}- * Nombre: {productos.nombre} || Precio: ${productos.precio} || Tipo: {productos.tipo} || Stock: {productos.stock} * Vendidos: {productos.quantity}\n")
                    
                        n_producto=input("\n---> Ingrese el numero correspondiente al producto que desea: ")
                        
                        while not n_producto.isnumeric() or int(n_producto) not in range(1,len(restaurante_seleccionado.productos)+1) or restaurante_seleccionado.productos[int(n_producto)-1].stock<=0:
                            if restaurante_seleccionado.productos[int(n_producto)-1].stock<=0:
                                print("\n\n\t\t*** PRODUCTO NO DISPONIBLE ***\n\n")

                            else:
                                error()

                            n_producto=input("\n---> Ingrese el numero correspondiente al producto que desea: ")
                        
                        cant=val_cant()

                        while cant>restaurante_seleccionado.productos[int(n_producto)-1].stock:
                            print("\n\n\t\t*** CANTIDAD NO PERMITIDA ***\n\n")
                            cant=val_cant()
                         # Calcular el subtotal del pedido
                        subttl=float(restaurante_seleccionado.productos[int(n_producto)-1].precio) * cant
                        
                        
                        # Agregar el pedido a la lista de compras
                        pedido.append(restaurante_seleccionado.productos[int(n_producto)-1])
                        pedido.append(cant)
                        pedido.append(subttl)
                        compra.append(pedido)

                        continuar=desea_comprar_mas()
                        if continuar:
                           continue

                        else:
                            break
                    
                    descuento=0
                    cont=0
                    subttl=0
                    print('''
            ======================================= FACTURA ===================================''')
                    for x in compra:
                        subttl+=(x[-1])
                        cont+=1
                        print(f'''
            - Pedido {cont}:

                        * {x[0].nombre} || Precio: ${x[0].precio}
                                        Cant.: {x[1]} ---> Subttl: ${x[-1]}''')
                    
                    perfecto=es_numero_perfecto(cliente.cedula)
                    if perfecto:
                        descuento+=0.15

                    descuento=subttl*descuento
                    total=subttl-descuento
                    print(f'''
                                        SUBTTL: ${subttl}
                                        Descuento: ${descuento}

                                        TOTAL: ${total}
            ====================================================================================''')
                    continuar=input("\n - Desea proceder con el pago? (S: SI ó N: NO): ")
                    continuar=continuar.capitalize()
                    while not continuar.isalpha() or continuar!="N" and continuar!="S":
                        error()
                        continuar=input(" - Desea proceder con el pago? (S: SI ó N: NO): ")
                        continuar=continuar.capitalize()

                    if continuar=="S":
                        ticket.total+=total
                        compra_aux = []
                        compra_aux.append(compra[-1])
                        restar_cant(restaurante_seleccionado,compra_aux)
                        print("**PAGO PROCESADO CON EXITO**")
                        
                    else:
                        compra.pop()
                        sumar_cant(restaurante_seleccionado,compra)

                    break 


                else:
                    print("\n\n\t\t*** CODIGO NO VALIDO NO ERES VIP ***\n\n")
        
                
                
            else:
                print("\n\n\t*** NO HAS HECHO EL INGRESO CON TU ENTRADA O NO ES VALIDA PARA ACCEDER A LOS RESTAURANTES ***")

        else:
            break

######################################## INDICADORES DE GESTION  ########################################

def estadistica_1(clientes):
    """ Calcula el promedio de gasto de un cliente VIP en un partido (ticket + restaurante) """
     # Inicializar variables para acumular el gasto total y contar clientes VIP
    total=0
    cant=0
    for cliente,tickets in clientes.items():
        cant+=1
        for ticket in tickets:
             # Filtrar tickets VIP con gasto mayor a 139.2
            if ticket.total>139.2 and ticket.tipo_entrada=="VIP":
                total+=ticket.total

    if cant==0:
        print("\n\n\t\t*** NO SE ENCONTRARON GASTOS DE CLIENTES VIP **")

    else:
        if total/cant==0:
            print("\n\n\t\t*** NO SE ENCONTRARON GASTOS DE CLIENTES VIP **")
         # Imprimir promedio de gasto
        else:
            print("\n\n\t\t\t--- PROMEDIO DE GASTO CLIENTE VIP ---\n\n")
            print(f"\t*** El promedio de gasto de un cliente VIP en un partido es: {total/cant} ***\n")

def estadistica_2(entradas):
    # Inicializa una lista vacía para almacenar la cantidad de entradas vendidas por partido
    quan=[]
    #inicializa un contador, par contar el numero de partidos 
    cont=0
    # Itera sobre los items del diccionario entradas (partidos y sus respectivas entradas vendidas)
    for k,v in entradas.items():
        cont+=1
        quan.append(len(v))
        
    if cont==0:
        print("\n\n\t\t*** NO SE HAN COMPRADO ENTRADAS ***")

    else:
        # Inicializa una lista vacía para almacenar la cantidad de asistentes por partido
        asis=[]
        # Itera sobre los items del diccionario entradas (partidos y sus respectivas entradas vendidas)
        for k,v in entradas.items():
            cont=0
            for x in v:
                if x.asistencia==True:
                    cont+=1
            asis.append(cont)
         # Ordena la lista asis en orden ascendente
        asis.sort()
        # Inicializa listas vacías para almacenar el tamaño de los campos de partido y estadio
        tamano_p=[]
        tamano_e=[]
        datos=[]
        impresos=[]
        # Itera sobre la lista asis (cantidad de asistentes por partido)
        for y in asis:
            for k,v in entradas.items():
                cont=0
                cant=0
                # Itera sobre las entradas vendidas por partido
                for x in v:
                    #incrementa la cantidad de entradas vendidas
                    cant+=1
                    if x.asistencia==True:
                        #si la entrada tiene asistecia, icrementa el cotador de asistencia 
                        cont+=1
                # Si la cantidad de asistentes coincide con la cantidad actual, imprime los datos
                if cont==y:
                    if k not in impresos:
                        impresos.append(k)
                        dato=[]
                        partido=f"|    '{k.equipo_l.nombre}' vs '{k.equipo_v.nombre}'    |"
                        estadio=f"|    {k.estadio.nombre}    |"
                        relacion=f"|    {cont}/{cant}    |"
                        asistentes=f"|    {cont}    |"
                        cantidad=f"|    {cant}    |"
                        # Agrega el tamaño de los campos de partido y estadio a las listas tamano_p y tamano_e
                        tamano_p.append(len(partido))
                        tamano_e.append(len(estadio))
                        
                        dato.append(partido)
                        dato.append(estadio)
                        dato.append(asistentes)
                        dato.append(cantidad)
                        dato.append(relacion)
                        datos.append(dato)
    
        if len(impresos)==0:
            print("...")
        
        else:
            tamano_p.sort()
            p_d=tamano_p[-1]/2
            p_d=int(p_d)
            p_d-=2
            tamano_e.sort()
            p_e=tamano_e[-1]/2
            p_e=int(p_e)
            p_e-=2
            print("\n\n\t\t\t--- ASISTENCIA A LOS PARTIDOS ---\n\n")
            print(" "*(p_d)+f"PARTIDO"+" "*(p_d)+" "*(p_e)+f"ESTADIO"+" "*(p_e)+"ASISTENCIA    VENDIDAS      RELACION")
            print(tabulate(datos))
def estadistica_3(entradas):
    '''Imprime el partido con mayor asistencia '''

    asistencia=[]
    
    for k,v in entradas.items():
        cont=0
        # Itera sobre la lista de entradas para cada partido
        for x in v:
            # Verifica si la entrada tiene asistencia
            if x.asistencia==True:
                cont+=1
                asistencia.append(cont)
    # Verifica si no hay asistencia registrada
    if len(asistencia)==0:
        print("\n\n\t\t*** NO SE HAN REGISTRADO ASISTENCIA A NINGUN PARTIDO ***")
    
    else:
        # Crea una copia de la lista de asistencia y la ordena
        asistencia_ordenada=asistencia
        asistencia_ordenada.sort()
        for v,k in entradas.items():
            cont=0
            for x in k:
                if x.asistencia==True:
                    cont+=1
            # Verifica si el partido tiene la mayor asistencia
            if cont==asistencia_ordenada[-1]:
                print("\n\n\t\t\t--- MAYOR ASISTENCIA ---\n\n")
                # Imprime la información del partido con mayor asistencia
                print(f" ---> 'L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}' ")
                break

def estadistica_4(entradas):
    '''Imprime el partido con mayor venta '''

    asistencia=[]
    for k,v in entradas.items():
        # Agrega la cantidad de entradas vendidas para cada partido a la lista
        asistencia.append(len(v))

    if len(asistencia)==0:
        print("\n\n\t\t*** NO SE HAN COMPRADO ENTRADAS ***")
    
    else:
        # Ordena la lista de asistencia en orden ascendente
        asistencia.sort()
        for v,k in entradas.items():
            # Verifica si el partido tiene la mayor asistencia
            if len(k)==asistencia[-1]:
                print("\n\n\t\t\t--- MAYOR VENTA ---\n\n")
                print(f"---> 'L: '{v.equipo_l.nombre}' vs V: '{v.equipo_v.nombre}' ||| Estadio: '{v.estadio.nombre}' ||| Fecha: {v.fecha}' ")
                break

def estadistica_5(partidos):
    ''' Top 3 productos más vendidos en el restaurante. '''
    estadios=[]
    for partido in partidos:
        if partido.estadio not in estadios:
            estadios.append(partido.estadio)

    final=[]
    for estadio in estadios:
        #Obtiene la lista de restaurantes asociados al estadio
        restaurantes=estadio.restaurantes

        for restaurante in restaurantes:
            cantidades=[]
            for producto in restaurante.productos:
                # Crea una lista auxiliar para almacenar la información del producto
                aux=[]
                aux.append(restaurante.nombre)
                aux.append(producto.nombre)
                aux.append(producto.quantity)
                cantidades.append(aux)

            # Ordena la lista de cantidades por la cantidad vendida en orden descendente
            lista_ordenada = sorted(cantidades, key=lambda x: x[2])
            
            #Agrega los 3 productos más vendidos del restaurante a la lista final
            final.append(lista_ordenada[-1])
            final.append(lista_ordenada[-2])
            final.append(lista_ordenada[-3])

    print("\n\n\t\t--- TOP PRODUCTOS VENDIDOS POR RESTAURANT ---\n\n")
    # Inicializa un contador y una lista para almacenar los restaurantes impresos
    cont=0
    impresos = []
    for product in final:
        cont+=1
         # Verifica si el restaurante no ha sido impresionado antes
        if product[0] not in impresos:
            print(f"Restaurante {product[0]}\n")
            # Imprime el nombre del restaurante
            impresos.append(product[0])
            # Imprime la información del producto
        print(f" - Nombre: {product[1]} || Cantidad vendida: {product[2]}\n")

def estadistica_6(clientes):
    ''' Top 3 de clientes (clientes que más compraron boletos) '''

    cantidad=[]
    for k,v in clientes.items():
        cantidad.append(len(v))

    if len(cantidad)==0:
        print("\n\n\t\t*** NO SE HAN COMPRADO ENTRADAS ***")

    else:
        #y define al tamaño de la lista de tickets que esta en clientes
        y=[]
        #x define a los nombres de lo clientes 
        x=[]
         # Ordena la lista de cantidades en orden ascendente
        cantidad.sort()
        print("\n\n\n\t\t--- TOP CLIENTES CON MAYOR CANTIDAD DE ENTRADAS ---\n")
        for k,v in clientes.items():
            print()
             
             # Verifica si el cliente tiene la mayor, segunda mayor o tercera mayor cantidad de entradas
            if cantidad[-1]==len(v) or cantidad[-2]==len(v) or cantidad[-3]==len(v):
                
                # Agrega el nombre del cliente a la lista x
                x.append(k.nombre)

                # Agrega la cantidad de entradas del cliente a la lista y
                y.append(len(v))

        # Crea un gráfico de barras con los nombres de los clientes en el eje x y la cantidad de entradas en el eje y
        plt.bar(x,y)
        plt.ylabel("CANTIDAD DE ENTRADAS")
        plt.xlabel("CLIENTES")
        plt.show()

def opcion_6(clientes,entradas,restaurantes):
    ''' Ejecuta la opcion "Indicadores de gestión" '''
    

    while True:
        opcion=input("\n\n\t\t--- MENU DE INDICADORES DE GESTION ---\n\n 1- Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)\n 2- Mostrar tabla con la asistencia a los partidos\n 3- Partido con mayor asistencia\n 4- Partido con mayor boletos vendidos\n 5- Top 3 productos más vendidos en el restaurante\n 6- Top 3 de clientes (clientes que más compraron boletos) \n 7- Retroceder \n\n ---> Ingrese el numero correpondiente al opcion que desea: ")
        while not opcion.isnumeric() or int(opcion) not in range(1,8):
            error()
            opcion=input("\n\n\t\t--- MENU DE INDICADORES DE GESTION ---\n\n 1- Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)\n 2- Mostrar tabla con la asistencia a los partidos\n 3- Partido con mayor asistencia\n 4- Partido con mayor boletos vendidos\n 5- Top 3 productos más vendidos en el restaurante\n 6- Top 3 de clientes (clientes que más compraron boletos)\n 7- Retroceder \n\n ---> Ingrese el numero correpondiente al opcion que desea: ")

        if opcion=="1":
            estadistica_1(clientes)

        elif opcion=="2":
            estadistica_2(entradas)
            
        elif opcion=="3":
            estadistica_3(entradas)

        elif opcion=="4":
            estadistica_4(entradas)

        elif opcion=="5":
            estadistica_5(restaurantes)

        elif opcion=="6":
            estadistica_6(clientes)

        else:
            break
