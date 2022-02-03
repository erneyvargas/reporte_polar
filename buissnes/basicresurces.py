from util.util import Util as Ut


class Basicresources:
    parameter_basicresorces = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_basicresorces = {
            "get": {
                "field": "*",
                "table": "basicresources",
                "where": " ",
            },
        }

    def get_basicresources(self, df_pivote):
        lista_tercero = list(df_pivote["id_responsible_id"].drop_duplicates().fillna(0))
        where_tercero = Ut.configure_field(lista_tercero).replace("'", "")
        self.parameter_basicresorces["get"]["where"] = "id IN ( " + where_tercero + ")"
        df_basicresorces = Ut.get_dataframe(self.parameter_basicresorces, self.conexion)

        return df_basicresorces