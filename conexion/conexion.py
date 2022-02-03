import psycopg2


class Conexion:

    def conectarAPP(self):
        # Conexion a Base de datos APP
        try:
            conexion = psycopg2.connect("host=192.168.102.211 dbname='tms' user='tmsadmin' password='20tms.admin15'")
            print(
                '########################################\n# Conexion a base de datos establecida #\n########################################\n')
            return conexion
        except psycopg2.Error as e:
            print('Unable connect to the database!')
            print(e.pgerror)
            print(e.diag.message_detail)
        #cursor = conexion.cursor()

    def conectarSW(self):
        # Conexion a Base de datos Switrans
        try:
            conexion = psycopg2.connect("host=192.168.102.29 dbname='switrans' user='admin' password='lITOMUvb7k'")
            print('########################################\n# Conexion a base de datos establecida #\n########################################\n')
            return conexion
        except psycopg2.Error as e:
            print('Unable connect to the database!')
            print(e.pgerror)
            print(e.diag.message_detail)