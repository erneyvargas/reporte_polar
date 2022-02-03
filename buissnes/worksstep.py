from util.util import Util as Ut
from buissnes.reports import Reports
import pandas as pd



class Worksstep:
    parameter_worksstep = {}

    def __init__(self, conexion):
        self.conexion = conexion
        self.parameter_worksstep = {
            "get": {
                "field": "*",
                "table": "worksstep",
                "where": " ",
            },
        }

    def get_worksstep(self, df_pivote):
        lista_work = list(df_pivote["id"].drop_duplicates().fillna(0))
        where_work = Ut.configure_field(lista_work).replace("'", "")
        self.parameter_worksstep["get"]["where"] = "id_work_id IN ( " + where_work + ")"
        df_worksstep = Ut.get_dataframe(self.parameter_worksstep, self.conexion)

        df_reports = Reports(self.conexion).get_reports(df_worksstep)
        df_reports["reportdate"] = df_reports["reportdate"].apply(lambda x: pd.to_datetime(x))
        df_reports["reportdate"] = df_reports["reportdate"].dt.tz_localize(None)

        # Merge para traer la fecha del reporte
        df_reports.rename(columns={'id': 'report'}, inplace=True)
        df_merge_result = pd.merge(df_worksstep, df_reports[["report", "reportdate", "send_date"]],
                                      how="left", on="report")

        return df_merge_result