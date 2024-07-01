class Bebida:

    def __init__(self,nombre,quantity,precio,stock,tipo):
        self.nombre=nombre
        self.quantity=quantity
        self.precio=precio
        self.stock=stock
        self.tipo=tipo
        

    def mostrar(self):
        print(f" - Nombre: {self.nombre} || Precio: ${self.precio} || Tipo: {self.tipo} || Alcoholica: {self.alcoholica} \n")

