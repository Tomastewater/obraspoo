#OJO QUE MODIFIQUE LOS METODOS DE LIMPIAR DATOS Y CARGAR DATOS, DEL ARCHIVO DE TOMAS. Y AGREGUE UNO QUE SE LLAMA ELIMINAR COLUMNAS

import pandas as pd
from peewee import *
from modelo_orm3 import *

# Define la conexión a la base de datos SQLite
db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})

# Clase abstracta GestionarObra
class GestionarObra:

    db = db

    @classmethod
    def extraer_datos(cls, archivo_csv):
        # Lee el archivo CSV en un DataFrame
        df = pd.read_csv(archivo_csv)
        return df

    @classmethod
    def conectar_db(cls):
        # Conecta a la base de datos
        db.connect()

    @classmethod
    def mapear_orm(cls, model_classes, safe=True):
        # Crea las tablas si no existen
        db.create_tables(model_classes, safe=True)

    @classmethod
    def eliminar_columnas(cls, df):
        df_con_colum_eliminadas = df.drop(["entorno", "descripcion", "direccion", "lat", "lng", "imagen_1", "imagen_2", "imagen_3", "imagen_4",
                    "licitacion_oferta_empresa", "licitacion_anio", "beneficiarios", "ba_elige", "link_interno", "pliego_descarga", "expediente-numero", "estudio_ambiental_descarga"], axis = 1)
        return df_con_colum_eliminadas

    @classmethod
    def limpiar_datos(cls, df_con_colum_eliminadas):
        df_cleaned = df_con_colum_eliminadas.fillna(0, inplace=False)
        return df_cleaned

    @classmethod
    def cargar_datos(cls, dfs):
        # dfs es un diccionario que mapea las clases de los modelos a los DataFrames
        for model_class, df in dfs.items():
        # Persiste los datos en la base de datos
            for _, row in df.iterrows():
                model_class.create(**row.to_dict())       

    @classmethod
    def nueva_obra(cls):
        # Crea una nueva instancia de Obra ingresando los valores por teclado
        nueva_obra = Obra()

        for field in Obra._meta.fields:
            if field != 'ID':
                value = input(f"Ingrese el valor para '{field}': ")

                setattr(nueva_obra, field, value)

                # ESTA MIERDA NO FUNCIONA DESPUES  VEMOS QUE PASA 
                """# Si es una clave foránea, busca el valor en la tabla correspondiente
                if isinstance(field, Obra._meta.fields.ForeignKeyField):
                    foreign_key_value = value
                    foreign_key_model_class = field.rel_model
                    foreign_key_instance = foreign_key_model_class.select().where(
                        foreign_key_model_class.ID == foreign_key_value
                    ).first()

                    # Si no encuentra la instancia, informa al usuario y pide un nuevo ingreso
                    if not foreign_key_instance:
                        print(f"No se encontró la instancia con ID {foreign_key_value} en la tabla {foreign_key_model_class.__name__}.")
                        return None

                    setattr(nueva_obra, field, foreign_key_instance)
                else:
                    setattr(nueva_obra, field, value)"""

        # Guarda la nueva instancia en la base de datos
        nueva_obra.save()
        return nueva_obra

    @classmethod
    def obtener_indicadores(cls, model_class):
        # Obtiene información de las obras existentes en la base de datos
        indicadores = {
            'total_obras': model_class.select().count(),
            'costo_total': model_class.select().aggregate_total(model_class.monto_contrato),
            # Otros indicadores que desees obtener
        }

        return indicadores