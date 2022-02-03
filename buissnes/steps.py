from util.util import Util as Ut

class Steps:
    parameter_ = {}
    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_steps= {
            "get": {
                "field": "*",
                "table": "steps",
                "where": ""
            },
        }

    def get_steps(self, filter):
        list_steps = list(filter["id"])
        where = Ut.configure_field(list_steps).replace("'", "")
        self.parameter_steps["get"]["where"] = " id IN ( " + where + ")"

        df_steps = Ut.get_dataframe(self.parameter_steps, self.conexion)
        return df_steps