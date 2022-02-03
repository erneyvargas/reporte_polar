from datetime import datetime
from datetime import timedelta

from util.util import Util as Ut

class Works:
    parameter_works = {}
    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_works= {
            "get": {
                "field": "*",
                "table": "works",
                "where": ""
            },
        }

    def get_works(self, filter):
        fecha_actual = datetime.now().date()
        ultimos_cuatro_dias = (fecha_actual - timedelta(days=4))
        self.parameter_works["get"]["where"] = "id_type_id = " + str(filter) + " AND created_date > '" + str(ultimos_cuatro_dias) + "'"
        df_works = Ut.get_dataframe(self.parameter_works, self.conexion)
        return df_works