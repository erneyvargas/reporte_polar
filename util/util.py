import pandas as pd
class Util:

    @staticmethod
    def get_dataframe(configuration, conn=None):
        fields = Util.configure_field(configuration["get"]["field"])
        table = configuration["get"]["table"]
        where = configuration["get"]["where"]
        if where.isspace():
            where = where.replace(" ", "")
        if len(where) > 0:
            query_tb_remesa = f"""SELECT {fields} FROM {table} WHERE  {where}"""
        else:
            query_tb_remesa = f"""SELECT {fields} FROM {table} """
        df_tb_remesa = pd.read_sql(query_tb_remesa, conn)
        return df_tb_remesa

    @staticmethod
    def configure_field(field):
        return ", ".join(str(f) for f in field)

    @staticmethod
    def merge_dataframe(dataframe, dataframe_pivote, tipo, primary):
        df_resultado = pd.merge(dataframe, dataframe_pivote, how=tipo,
                                on=primary)
        return df_resultado