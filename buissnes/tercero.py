from util.util import Util as Ut


class Tercero:
    parameter_tercero = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_tercero = {
            "get": {
                "field": ["tercero_codigo", "tercero_documento", "tercero_nombre1", "tercero_nombre2",
                          "tercero_apellido1", "tercero_apellido2"],
                "table": "tb_tercero",
                "where": " ",
            },
            "merge": {
                "on": ["tercero_codigo"],
                "how-left": "left"
            }
        }

    def get_tercero(self, df_pivote):
        lista_tercero = list(df_pivote["id_sw1"].drop_duplicates().fillna(0))
        where_tercero = Ut.configure_field(lista_tercero).replace("'", "")
        self.parameter_tercero["get"]["where"] = "tercero_codigo IN ( " + where_tercero + ")"
        df_tercero = Ut.get_dataframe(self.parameter_tercero, self.conexion)

        # Crea una nueva columna concatenando los nombres y apellidos.
        nombres_completos = ["tercero_nombre1", "tercero_nombre2", "tercero_apellido1", "tercero_apellido2"]
        df_tercero["nombre_completo"] = df_tercero[nombres_completos].apply(' '.join, axis=1)
        return df_tercero