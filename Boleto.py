class Boleto:
    def __init__(self,partido,tipo_entrada,total,codigo,asistencia):
        self.partido=partido
        self.tipo_entrada=tipo_entrada
        self.total=total
        self.codigo=codigo
        self.asistencia=asistencia

    def hacer_gol(self):
        self.score+=1