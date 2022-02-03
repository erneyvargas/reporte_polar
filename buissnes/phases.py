from util.util import Util as Ut

class Phases:
    parameter_phases = {}
    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_phases= {
            "get": {
                "field": "*",
                "table": "phases",
                "where": ""
            },
        }

    def get_phases(self, filter):
        self.parameter_phases["get"]["where"] = "id_type_id = " + str(filter)
        df_phases = Ut.get_dataframe(self.parameter_phases, self.conexion)
        return df_phases