from util.util import Util as Ut

class Reports:
    parameter_ = {}
    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_reports= {
            "get": {
                "field": "*",
                "table": "reports",
                "where": ""
            },
        }

    def get_reports(self, filter):
        list_reports = list(filter["report"])
        where = Ut.configure_field(list_reports).replace("'", "")
        self.parameter_reports["get"]["where"] = " id IN ( " + where + ")"

        df_reports = Ut.get_dataframe(self.parameter_reports, self.conexion)

        return df_reports