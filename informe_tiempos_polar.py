from conexion import conexion
import pandas as pd
from buissnes.phases import Phases
from buissnes.steps import Steps
from buissnes.works import Works
from buissnes.tercero import Tercero
from buissnes.basicresurces import Basicresources
from buissnes.worksstep import Worksstep
from buissnes.manifiesto import Manifiesto
from buissnes.reports import Reports
from util.correo import Correo
from util.style_excel import ExcelStyle


conn = conexion.Conexion()
conexion_app = conn.conectarAPP()
# Transformacion de la data a utf-8
conexion_app.set_client_encoding('UTF-8')

conexion_sw = conn.conectarSW()

#Operacion Polar = 16
operation_type = 16

df_phases = Phases(conexion_app).get_phases(operation_type)
df_steps = Steps(conexion_app).get_steps(df_phases)
df_works = Works(conexion_app).get_works(operation_type)
df_basicresources = Basicresources(conexion_app).get_basicresources(df_works)
df_workssteps = Worksstep(conexion_app).get_worksstep(df_works)
df_reports = Reports(conexion_app).get_reports(df_workssteps)

df_manifiesto = Manifiesto(conexion_sw).get_manifiesto(df_works)
df_tercero = Tercero(conexion_sw).get_tercero(df_basicresources)



# Merge para obtener el nombre y documento del tercero
df_basicresources.rename(columns={'id_sw1':'tercero_codigo', 'id': 'id_responsible_id'},inplace=True)
df_merge_basicresources = pd.merge(df_basicresources, df_tercero, how="left", on="tercero_codigo")

# Merge para vincular el trabajo con el tercero
df_merge_works = pd.merge(df_works, df_merge_basicresources[["id_responsible_id", "tercero_documento", "nombre_completo"]],
                        how="left", on="id_responsible_id")

# Merge para vincular el Manifiesto con El trabajo
df_manifiesto.rename(columns={'manifiesto_codigo':'document'},inplace=True)
# Se pasan los manifiestos a tipo Numerico
df_merge_works['document'] = pd.to_numeric(df_merge_works['document'])

df_merge_manifiesto = pd.merge(df_merge_works, df_manifiesto[["document", "manifiesto_codigo_impreso", "vehiculo_placa"]],
                        how="left", on="document")

df_workssteps_pivote = df_workssteps.pivot(index="id_work_id", columns="tittle", values="reportdate").reset_index()


df_reports.rename(columns={'id':'report'},inplace=True)
df_merge_reports = pd.merge(df_workssteps, df_reports[["report", "message_wrote"]],
                        how="left", on="report")
df_reports_pivote = df_merge_reports.pivot(index="id_work_id", columns="tittle", values=["message_wrote"]).reset_index()
dicc_reports = df_reports_pivote.set_index('id_work_id').to_dict('index')



# Inicia Filtrado de Columnas
df_result = df_merge_manifiesto["id"].to_frame()
df_result["FECHA"] = df_merge_manifiesto["created_date"].apply(lambda x: pd.to_datetime(x).date())
df_result["ESTADO"] = df_merge_manifiesto["state"]
df_result["RESPONSABLE"] = df_merge_manifiesto["nombre_completo"]
df_result["DOCUMENTO"] = df_merge_manifiesto["tercero_documento"]
df_result["MANIFIESTO"] = df_merge_manifiesto["manifiesto_codigo_impreso"]
df_result["PLACA"] = df_merge_manifiesto["vehiculo_placa"]

# Merge para trater los campos de las tareas
df_workssteps_pivote.rename(columns={'id_work_id':'id' },inplace=True)

#Reordenar las columnas de acuerdo al informe necesario
df_workssteps_pivote = df_workssteps_pivote[["id","LLEGADA A PLANTA","INGRESO A PLANTA", "INICIO DEL CARGUE", "FIN DEL CARGUE", "SALIDA DE PLANTA",
                                             "LLEGADA A DESCARGUE", "INGRESO A DESCARGUE", "INICIO DEL DESCARGUE", "FIN DEL DESCARGUE", "SALIDA DE DESCARGUE",
                                             "VEHICULO RETORNADO A PLANTA POLAR"]]
df_result = pd.merge(df_result, df_workssteps_pivote, how="left", on="id")


# Inicia  calculos:

df_result["INICIO Round Trip"] = (df_result["INICIO DEL CARGUE"].sub(df_result["LLEGADA A PLANTA"]))
df_result["TIEMPO DE CARGUE"] = (df_result["FIN DEL CARGUE"].sub(df_result["INICIO DEL CARGUE"]))
df_result["TIEMPO DE SALIDA"] = (df_result["SALIDA DE PLANTA"].sub(df_result["FIN DEL CARGUE"]))
df_result["TIEMPO EN RUTA"] = (df_result["LLEGADA A DESCARGUE"].sub(df_result["SALIDA DE PLANTA"]))
df_result["INICIO LLEGADA A DESCARGAR"] = (df_result["INICIO DEL DESCARGUE"].sub(df_result["LLEGADA A DESCARGUE"]))
df_result["TIEMPO DE DESCARGUE"] = (df_result["FIN DEL DESCARGUE"].sub(df_result["INICIO DEL DESCARGUE"]))
df_result["TIEMPO DE SALIDA"] = (df_result["SALIDA DE DESCARGUE"].sub(df_result["FIN DEL DESCARGUE"]))
df_result["TIEMPO EN RUTA"] = (df_result["VEHICULO RETORNADO A PLANTA POLAR"].sub(df_result["SALIDA DE DESCARGUE"]))
df_result["TIEMPO TOTAL X VIAJE"] = df_result["VEHICULO RETORNADO A PLANTA POLAR"].sub(df_result["LLEGADA A PLANTA"])

save_route = 'assets/informe_polar.xlsx'
recipients = ["erney.vargas@mct.com.co", "nancy.medina@mct.com.co"]
title = "Informe Tiempos APP Operacion Polar"
df_result.to_excel(save_route)
print("Termina construciion de DataFrame con Pandas")
ExcelStyle().format_excel(save_route, dicc_reports)

#Enviar_correo("ruta del archivo, "destinatarios", "titulo")
Correo().send_mail(save_route, recipients, title)

