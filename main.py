import App as a
import pickle

def menu():
    
    print("\n")
    print("\t\t--- MENU PRINCIPAL ---")
    opcion=input("\n 1- Gestión de partidos y estadios\n 2- Gestión de venta de entradas\n 3- Gestión de asistencia a partidos\n 4- Gestión de restaurantes\n 5- Gestión de venta de restaurantes\n 6- Indicadores de gestión (estadísticas)\n 7-Salir \n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
    while not opcion.isnumeric() or int(opcion) not in range(1,8):
        a.error()
        print("\t\t--- MENU PRINCIPAL ---")
        opcion=input("\n 1- Gestión de partidos y estadios\n 2- Gestión de venta de entradas\n 3- Gestión de asistencia a partidos\n 4- Gestión de restaurantes\n 5- Gestión de venta de restaurantes\n 6- Indicadores de gestión (estadísticas)\n 7- Salir\n\n ---> Ingrese el numero correspondiente a la opcion que desea: ")
        
    return int(opcion)

def main():
    try:
        with open("entradas.txt","rb") as f:
            entradas=pickle.load(f)

    except:
        entradas=dict()

    try:
        with open("clientes.txt","rb") as f:
            clientes=pickle.load(f)

    except:
        clientes=dict()
    
    try:
        with open("partidos.txt","rb") as f:
            partidos=pickle.load(f)
    
    except:
        equipos=a.registrar_equipos()
        restaurantes=a.registrar_restaurantes()
        estadios=a.registrar_estadios(restaurantes)
        partidos=a.registrar_partidos(equipos,estadios)
    
    print("\n\n")
    print("\t--- BIENVENIDO AL SISTEMA DE 'EUROCOPA 2024' ---")
    

    while True:
        opcion=menu()

        if opcion==1:
            a.opcion_1(equipos,partidos,estadios)

        elif opcion==2:
            clientes,entradas=a.opcion_2(partidos,clientes,entradas)

        elif opcion==3:
            clientes=a.opcion_3(clientes,entradas)

        elif opcion==4:
            a.opcion_4(partidos,clientes)

        elif opcion==5:
            restaurantes=a.opcion_5(clientes)

        elif opcion==6:
            a.opcion_6(clientes,entradas,partidos)

        else:
            print("GRACIAS POR PARTCIPAR EN LA EUROCOPA 2024")
            pickle.dump(clientes,open("clientes.txt","wb"))
            pickle.dump(entradas,open("entradas.txt","wb"))
            pickle.dump(partidos,open("partidos.txt","wb"))
            break
main()