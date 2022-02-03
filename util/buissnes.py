from util.util import Util as Ut
import re


class Bussines:
    conexion = None
    dataframe_pivote = None

    def __init__(self, conexion):
        self.conexion = conexion

    def get_codigo_impreso(self, dataframe_pivote):
        self.dataframe_pivote = dataframe_pivote
        nombre_columnas = list(self.dataframe_pivote.columns.values)

        regex = ".*cencoscodigo|.*numerodocumento"
        r = re.compile(regex)
        columna_centrocosto_filtrada = list(filter(r.match, nombre_columnas))[0]
        entidad = columna_centrocosto_filtrada.split("_")[0]
        self.dataframe_pivote = self.get_dataframe_centrocosto()
        self.dataframe_pivote = self.get_dataframe_empresa()
        columna_consecutivo_centrocosto = entidad + "_codigo_impreso"
        self.dataframe_pivote[columna_consecutivo_centrocosto] = self.dataframe_pivote[
            "empresa_codigocontable"].str.zfill(2)
        self.dataframe_pivote[columna_consecutivo_centrocosto] = self.dataframe_pivote[
                                                                     columna_consecutivo_centrocosto] + \
                                                                 self.dataframe_pivote[
                                                                     "cencos_digito"].str.strip().str.zfill(3)
        self.dataframe_pivote[columna_consecutivo_centrocosto] = self.dataframe_pivote[
                                                                     columna_consecutivo_centrocosto] + "-" + \
                                                                 self.dataframe_pivote[
                                                                     columna_centrocosto_filtrada].astype(str)
        self.dataframe_pivote = self.clean_dataframe()
        return self.dataframe_pivote

    def get_dataframe_empresa(self):
        parameter_empresa = {
            "get": {
                "field": ["empresa_codigo", "empresa_codigocontable"],
                "table": "tb_empresa",
                "where": " "
            },
            "merge": {
                "on": ["empresa_codigo"],
                "how-inner": "inner"
            }
        }
        df_tb_empresa = Ut.get_dataframe(parameter_empresa, self.conexion)
        df_codigo_impreso = Ut.merge_dataframe(self.dataframe_pivote, df_tb_empresa, parameter_empresa["merge"]["how-inner"],
                                               parameter_empresa["merge"]["on"])
        return df_codigo_impreso

    def get_dataframe_centrocosto(self):
        parameter_centrocosto = {
            "get": {
                "field": ["cencos_codigo", "cencos_digito"],
                "table": "tb_centrocosto",
                "where": "estado_codigo = 160"
            },
            "merge": {
                "on": ["cencos_codigo"],
                "how-inner": "inner",
            }
        }
        # INNER entre tb_remesa y tb_centrocosto
        df_tb_centrocosto = Ut.get_dataframe(parameter_centrocosto, self.conexion)
        df_codigo_impreso = Ut.merge_dataframe(self.dataframe_pivote, df_tb_centrocosto,
                                               parameter_centrocosto["merge"]["how-inner"],
                                               parameter_centrocosto["merge"]["on"])
        return df_codigo_impreso

    def clean_dataframe(self):
        dataframe_pivote = self.dataframe_pivote.drop(self.dataframe_pivote.iloc[:, 1:-1], axis=1)
        return dataframe_pivote
