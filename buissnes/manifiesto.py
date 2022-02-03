import pandas as pd

from util.util import Util as Ut
from util.buissnes import Bussines
from buissnes.vehiculo import Vehiculo

class Manifiesto:
    conexion = None
    parameter_manifiesto = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_manifiesto = {
            "get": {
                "field": ["manifiesto_codigo", "manifiesto_numero", "manifiesto_cencoscodigo", "empresa_codigo",
                          "cencos_codigo", "manifiesto_fechacreacion", "ciudad_codigo_origen", "ciudad_codigo_destino",
                          "tercero_codigo_propietario", "tercero_codigo_conductor", "vehiculo_codigo", "manifiesto_fletepactado",
                          "manifiesto_flete", "manifiesto_cargue", "manifiesto_descargue",],
                "table": "tb_manifiesto",
                "where": " ",
            },
            "merge": {
                "on": ["manifiesto_codigo"],
                "how-inner": "inner",
                "how-left": "left",
                "how-right": "right",
            }
        }

    def get_manifiesto(self, dataframe_pivote):
        lista_manifiestos = list(dataframe_pivote["document"].fillna(0))
        where_manifiesto = Ut.configure_field(lista_manifiestos).replace("'", "")
        self.parameter_manifiesto["get"]["where"] = "manifiesto_codigo IN ( " + where_manifiesto + ")"

        df_manifiesto = Ut.get_dataframe(self.parameter_manifiesto, self.conexion)
        df_list_codigo_impreso = df_manifiesto[["manifiesto_codigo", "manifiesto_cencoscodigo", "cencos_codigo", "empresa_codigo"]]
        df_codigo_impreso = Bussines(self.conexion).get_codigo_impreso(df_list_codigo_impreso)
        df_manifiesto = Ut.merge_dataframe(df_codigo_impreso, df_manifiesto,
                                           self.parameter_manifiesto["merge"]["how-right"],
                                           self.parameter_manifiesto["merge"]["on"])

        df_vehiculo = Vehiculo(self.conexion).get_vehiculo(df_manifiesto)

        df_manifiesto = pd.merge(df_manifiesto, df_vehiculo,how="left", on="vehiculo_codigo")

        return df_manifiesto

