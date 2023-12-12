import pyodbc
from data.clsDatos import clsDatos


class clsConexion():
    # Declara las variables para la conexion
    _servidor = ' 192.168.18.8'  # Recuerde cambiar la dirección y contraseña
    _basedatos = 'datos'
    _usuario = 'sa'
    _contra = 'Utn123**'

    def __init__(self):
        pass

    def _conectar(self):
        try:
            _conex = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                    'SERVER=' + self._servidor +
                                    ';DATABASE=' + self._basedatos +
                                    ';UID=' + self._usuario +
                                    ';PWD=' + self._contra)
        except Exception as err:
            print(err)
        return _conex

    def agregar(self, dato):
        estado = False
        AuxSql = "insert into datos(texto, descripcion) values('{0}','{1}')".format(dato.Texto, dato.Descripcion)
        try:
            _conex = self._conectar()
            with _conex.cursor() as cursor:
                cursor.execute(AuxSql)

            _conex.close()
            estado = True
        except Exception as err:
            print(err)
        return estado

    def editar(self, dato):
        estado = False
        AuxSql = "update datos set texto = '{1}', descripcion = '{2}' where id = {0}".format(dato.ID, dato.Texto,
                                                                                             dato.Descripcion)
        try:
            _conex = self._conectar()
            with _conex.cursor() as cursor:
                cursor.execute(AuxSql)

            _conex.close()
            estado = True
        except Exception as err:
            print(err)
        return estado

    def borrar(self, ide):
        estado = False
        AuxSql = "delete datos where id = {0}".format(ide)
        try:
            _conex = self._conectar()
            with _conex.cursor() as cursor:
                cursor.execute(AuxSql)

            _conex.close()
            estado = True
        except Exception as err:
            print(err)
        return estado

    def consultar(self, ide=None):
        data = ''
        salida = []

        try:
            _conex = self._conectar()
            with _conex.cursor() as cursor:
                if ide is None:
                    cursor.execute("Select * from datos")
                else:
                    cursor.execute("Select * from datos where id = {0}".format(ide))
                data = cursor.fetchall()

            _conex.close()
        except Exception as err:
            print(err)

        for tupla in data:
            salida.append(clsDatos(tupla[0], tupla[1], tupla[2]))

        return salida
