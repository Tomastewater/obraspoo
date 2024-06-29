import pandas as pd
from peewee import *
import modelo_orm as mo
from datetime import datetime

# Define la conexión a la base de datos SQLite
db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})

# Clase abstracta GestionarObra
class GestionarObra:
    # ESTO LO COMENTO PORQUE NO ENTIENDO QUE ESTARIA HACIENDO Y NO ME FUNCIONABA ADEMAS 
    #db = db

    @classmethod
    def extraer_datos(cls):

        # Extrae los datos del archivo_csv
        
        archivo_csv = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv"

        try:
            df = pd.read_csv(archivo_csv, sep=",")
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False

    @classmethod

    # COnecta a la base de datos
    def conectar_db(cls):
        try:
            db.connect()
        except OperationalError as e:
            print("Se ha generado un error en la conexión a la BD.", e)
            exit()

    @classmethod
    def mapear_orm(cls, modelo_orm):

        #Recibe como parametro el modulo modelo_orm donse se encuentran las clases a mapear

        try:
            db.create_tables([modelo_orm.Ubicacion, modelo_orm.Fechas, modelo_orm.Contratacion, modelo_orm.Imagen, modelo_orm.Obra])
            print("Se ha mapeado con exito")
        except OperationalError as e:
            print("Se ha generado un error al crear las tablas de la BD.")
            exit()

    @classmethod
    def limpiar_datos(cls, df):

        try:
            
            df.fillna(0, inplace = True)
            df.rename(columns={'expediente-numero': 'expediente_numero'}, inplace=True)   # Se esta tomando el dataframe directamente desde la pagina principal, por eso el cambio de en el campo
            print("Se limpiaron los datos correctamente")
            return df

        except OperationalError as e:
            print("No se han podido limpiar los datos")
            return False


    @classmethod
    def cargar_datos(cls, df):

        try:
            for _, row in df.iterrows():
                # Crea instancias de las clases del modelo
                ubicacion = mo.Ubicacion.create(lat=row['lat'], lng=row['lng'], comuna=row['comuna'], barrio=row['barrio'], direccion=row['direccion'])
                fechas = mo.Fechas.create(fecha_inicio=row['fecha_inicio'], fecha_fin_inicial=row['fecha_fin_inicial'], plazo_meses=row['plazo_meses'])
                contratacion = mo.Contratacion.create(licitacion_oferta_empresa=row['licitacion_oferta_empresa'], licitacion_anio=row['licitacion_anio'], contratacion_tipo=row['contratacion_tipo'], nro_contratacion=row['nro_contratacion'], cuit_contratista=row['cuit_contratista'])
                imagenes = mo.Imagen.create(imagen_1=row['imagen_1'], imagen_2=row['imagen_2'], imagen_3=row['imagen_3'], imagen_4=row['imagen_4'])

                # Crea la instancia de la clase Obra relacionando las instancias anteriores
                mo.Obra.create(
                    ubicacion=ubicacion,
                    fechas=fechas,
                    contratacion=contratacion,
                    imagenes=imagenes,
                    entorno=row['entorno'],
                    nombre=row['nombre'],
                    etapa=row['etapa'],
                    tipo=row['tipo'],
                    area_responsable=row['area_responsable'],
                    descripcion=row['descripcion'],
                    monto_contrato=row['monto_contrato'],
                    comuna=row['comuna'],
                    barrio=row['barrio'],
                    direccion=row['direccion'],
                    lat=row['lat'],
                    lng=row['lng'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin_inicial=row['fecha_fin_inicial'],
                    plazo_meses=row['plazo_meses'],
                    porcentaje_avance=row['porcentaje_avance'],
                    licitacion_oferta_empresa=row['licitacion_oferta_empresa'],
                    licitacion_anio=row['licitacion_anio'],
                    contratacion_tipo=row['contratacion_tipo'],
                    nro_contratacion=row['nro_contratacion'],
                    cuit_contratista=row['cuit_contratista'],
                    beneficiarios=row['beneficiarios'],
                    mano_obra=row['mano_obra'],
                    compromiso=row['compromiso'],
                    destacada=row['destacada'],
                    ba_elige=row['ba_elige'],
                    link_interno=row['link_interno'],
                    pliego_descarga=row['pliego_descarga'],
                    expediente_numero=row['expediente_numero'],
                    estudio_ambiental_descarga=row['estudio_ambiental_descarga'],
                    financiamiento=row['financiamiento']
                )
            print("Datos cargados exitosamente")
            return True
        except OperationalError as e:
            print("No se han podido cargar los datos")
            return False
            
    @classmethod
    def nueva_obra(cls):
        # Solicitar al usuario los datos para crear una nueva obra
        entorno = input("Ingrese el entorno: ")
        nombre = input("Ingrese el nombre: ")
        etapa = input("Ingrese la etapa: ")
        tipo = input("Ingrese el tipo: ")
        area_responsable = input("Ingrese el área responsable: ")
        descripcion = input("Ingrese la descripción: ")
        monto_contrato = float(input("Ingrese el monto del contrato: "))
        comuna = input("Ingrese la comuna: ")
        barrio = input("Ingrese el barrio: ")
        direccion = input("Ingrese la dirección: ")
        lat = float(input("Ingrese la latitud: "))
        lng = float(input("Ingrese la longitud: "))
        fecha_inicio = input("Ingrese la fecha de inicio (DD-MM-YYYY): ")
        fecha_fin_inicial = input("Ingrese la fecha fin inicial (DD-MM-YYYY): ")
        plazo_meses = int(input("Ingrese el plazo en meses: "))
        porcentaje_avance = float(input("Ingrese el porcentaje de avance: "))
        licitacion_oferta_empresa = input("Ingrese la licitación/oferta/empresa: ")
        licitacion_anio = int(input("Ingrese el año de la licitación: "))
        contratacion_tipo = input("Ingrese el tipo de contratación: ")
        nro_contratacion = input("Ingrese el número de contratación: ")
        cuit_contratista = input("Ingrese el CUIT del contratista: ")
        beneficiarios = int(input("Ingrese el número de beneficiarios: "))
        mano_obra = int(input("Ingrese la cantidad de mano de obra: "))
        compromiso = input("Ingrese el compromiso: ")
        destacada = input("¿Es destacada? (True/False): ")
        ba_elige = input("¿Es de BA Elige? (True/False): ")
        link_interno = input("Ingrese el enlace interno: ")
        pliego_descarga = input("Ingrese el pliego de descarga: ")
        expediente_numero = input("Ingrese el expediente número: ")
        estudio_ambiental_descarga = input("Ingrese el enlace de descarga del estudio ambiental: ")
        financiamiento = input("Ingrese el financiamiento: ")

        # Crea instancias de las clases del modelo
        ubicacion = mo.Ubicacion.create(lat=lat, lng=lng, comuna=comuna, barrio=barrio, direccion=direccion)
        fechas = mo.Fechas.create(fecha_inicio=fecha_inicio, fecha_fin_inicial=fecha_fin_inicial, plazo_meses=plazo_meses)
        contratacion = mo.Contratacion.create(licitacion_oferta_empresa=licitacion_oferta_empresa, licitacion_anio=licitacion_anio, contratacion_tipo=contratacion_tipo, nro_contratacion=nro_contratacion, cuit_contratista=cuit_contratista)
        imagenes = mo.Imagen.create(imagen_1="", imagen_2="", imagen_3="", imagen_4="")

        # Crea la instancia de la clase Obra relacionando las instancias anteriores
        nueva_obra = mo.Obra.create(
            ubicacion=ubicacion,
            fechas=fechas,
            contratacion=contratacion,
            imagenes=imagenes,
            entorno=entorno,
            nombre=nombre,
            etapa=etapa,
            tipo=tipo,
            area_responsable=area_responsable,
            descripcion=descripcion,
            monto_contrato=monto_contrato,
            porcentaje_avance=porcentaje_avance,
            beneficiarios=beneficiarios,
            mano_obra=mano_obra,
            compromiso=compromiso,
            destacada=destacada,
            ba_elige=ba_elige,
            link_interno=link_interno,
            pliego_descarga=pliego_descarga,
            expediente_numero=expediente_numero,
            estudio_ambiental_descarga=estudio_ambiental_descarga,
            financiamiento=financiamiento
        )

        print("Nueva obra agregada con éxito.")
        return nueva_obra

    @classmethod
    def obtener_indicadores(cls):
        Obra = mo.Obra

        # Indicador 1: Total de Obras
        total_obras = Obra.select().count()

        # Indicador 2: Promedio de Porcentaje de Avance
        promedio_avance = Obra.select().group_by(Obra.porcentaje_avance).scalar()

        # Indicador 3: Obras Destacadas
        obras_destacadas = Obra.select().where(Obra.destacada == True).count()

        # Indicador 4 Obras en una Etapa Específica (Ejemplo: "En ejecucion")
        etapa_en_ejecucion = "En ejecución"
        obras_en_ejecucion = Obra.select().where(Obra.etapa == etapa_en_ejecucion).count()

        # Indicador 5 Obras en una Etapa Específica (Ejemplo: "Finalizada")
        etapa_finalizada = "Finalizada"
        obras_finalizadas = Obra.select().where(Obra.etapa == etapa_finalizada).count()

        # Indicador 6
        etapa_desestimada = "Desestimada"
        obras_desestimada = Obra.select().where(Obra.etapa == etapa_desestimada).count()

        # Puedes agregar más indicadores según tus necesidades

        indicadores = {
            'total_obras': total_obras,
            'promedio_avance': promedio_avance,
            'obras_destacadas': obras_destacadas,
            'obras en Proceso': obras_en_ejecucion,
            'obras Finalizadas': obras_finalizadas,
            'obras Desestimadas': obras_desestimada
            # Puedes agregar más indicadores aquí
        }

        return indicadores
    
"""
# agrego codigo con esto se carga la base de datos 

# Lee el archivo CSV en un DataFrame
df = GestionarObra.extraer_datos(archivo_csv)

# Conectar a la base de datos
GestionarObra.conectar_db()

# Crear las tablas si no existen
GestionarObra.mapear_orm([Obra])

# Rellenar los valores nulos en el DataFrame con cero
df_filled = df.fillna(0)

# Reemplazar los valores nulos para poder cargarlos
df['beneficiarios'].fillna(0, inplace=True)
df['mano_obra'].fillna(0, inplace=True)
df['plazo_meses'].fillna(0, inplace=True)
df['expediente-numero'].fillna("", inplace=True)
df['licitacion_anio'].fillna(0, inplace=True)
df['monto_contrato'].fillna(0, inplace=True)
df['fecha_inicio'].fillna(pd.to_datetime('today'), inplace=True)
df['fecha_fin_inicial'].fillna(pd.to_datetime('today'), inplace=True)
df['lat'].fillna(0, inplace=True)
df['lng'].fillna(0, inplace=True)
df['porcentaje_avance'].fillna(0, inplace=True)
# Rellenar los valores nulos en la columna con una cadena vacía
df['imagen_3'].fillna("", inplace=True)
df['imagen_1'].fillna("", inplace=True)
df['imagen_4'].fillna("", inplace=True)
df['imagen_2'].fillna("", inplace=True)
df['compromiso'].fillna("", inplace=True)
df['ba_elige'].fillna("", inplace=True)
df['estudio_ambiental_descarga'].fillna("", inplace=True)
df['financiamiento'].fillna("", inplace=True)
df['link_interno'].fillna("", inplace=True)
df['pliego_descarga'].fillna("", inplace=True)
df['contratacion_tipo'].fillna("", inplace=True)
df['nro_contratacion'].fillna("", inplace=True)
df['cuit_contratista'].fillna("", inplace=True)
df['descripcion'].fillna("", inplace=True)
df['licitacion_oferta_empresa'].fillna("", inplace=True)
df['direccion'].fillna("", inplace=True)
df['comuna'].fillna("", inplace=True)
df['tipo'].fillna("", inplace=True)
# Rellenar los valores nulos en la columna 'destacada' con False
df['destacada'].fillna(False, inplace=True)

# Se elimina la columna ID antes de cargar los datos ya que el ID se genera automáticamente, ver modificación de la clase Obra en modelo_orm
df = df.drop(columns=['ID'])  

# Cargar los datos en la base de datos sin eliminar los valores nulos
GestionarObra.cargar_datos(df, Obra)

"""