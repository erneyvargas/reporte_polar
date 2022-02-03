from util.util import Util as Ut


class Vehiculo:
    parameter_vehiculo = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_vehiculo = {
            "get": {
                "field": ["vehiculo_codigo", "vehiculo_placa", "claveh_codigo"],
                "table": "tb_vehiculo",
                "where": " ",
            },
        }


    def get_vehiculo(self, df_pivote):
        lista_vehiculos = list(df_pivote["vehiculo_codigo"])
        where_vehiculos = Ut.configure_field(lista_vehiculos)
        self.parameter_vehiculo["get"]["where"] = "vehiculo_codigo IN ( " + where_vehiculos.replace("'", "") + ")"
        df_vehiculo = Ut.get_dataframe(self.parameter_vehiculo, self.conexion)
        return df_vehiculo