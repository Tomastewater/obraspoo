#ABAJO ESTA LO QUE QUISE MODIFICAR PERO NO ME TERMINA DE SALIR. LOGRO CREAR DF PARA CADA TABLA LOOKUP PERO NO LOGRO PASARLE LOS DATOS DEL DF LIMPIADO

from modelo_orm3 import *
from gestionar_obras3 import *

def cargarTabla():

    # Extraer datos para Data Frame limpio
    archivo_csv = './archivo_csv.csv'
    df = GestionarObra.extraer_datos(archivo_csv)
    print(df)
    df_con_columnas_eliminadas = GestionarObra.eliminar_columnas(df)
    df_limpiado = GestionarObra.limpiar_datos(df_con_columnas_eliminadas)
    print(df_limpiado)

    # Conecta a la base de datos
    GestionarObra.conectar_db()


    print("Datos cargados exitosamente.")


    GestionarObra.db.close()

def crearInstancias():
    # Conecta a la base de datos
    GestionarObra.conectar_db()

    # Crear dos nuevas instancias de Obra con valores específicos
    nueva_obra_1 = GestionarObra.nueva_obra()

    # Guardar las instancias en la base de datos
    nueva_obra_1.save()

    # Cerrar la conexión a la base de datos
    GestionarObra.db.close()

cargarTabla()

if __name__ == '__main__':


   eleccion = (int)(input("""
                           
                           ___Eliga una opcion (en numero)___
                     
                     1. Crear nueva obra
                     2. Iniciar contratacion
                     3. Adjudicar obra
                     4. 
                           
                     """))
    
    #if eleccion == 1:
    #    crearInstancias()
    
"""    # Crea estructura de la BD (tablas y relaciones)
    GestionarObra.mapear_orm([Obra, Etapa, Tipo_obra, Tipo_contratacion, Comuna, Barrio])

   # GestionarObra.cargar_datos(df_limpiado, Obra)

    df_etapas = df_limpiado[['etapa']]
    df_tiposObra = df_limpiado[['tipo']]
    df_comunas = df_limpiado[['comuna']]
    df_barrios = df_limpiado[['barrio']]
    df_tiposContratacion = df_limpiado[['contratacion_tipo']]
        
    dfs = {
            Obra: df_limpiado,
            Etapa: df_etapas,
            Tipo_obra: df_tiposObra,
            Tipo_contratacion: df_tiposContratacion,
            Comuna: df_comunas,
            Barrio: df_barrios,
        }
    print(dfs)

    GestionarObra.cargar_datos(dfs)"""
