import pandas as pd
from peewee import *
from modelo_ormPrueba import *

#Creo la clase abstracta (?) Gestionar Obra, con sus métodos de clase
class GestionarObra():
    
    @classmethod
    def extraer_datos(cls, archivo_csv):
        archivo_csv = "./observatorio-de-obras-urbanas.csv"
        try:
            df = pd.read_csv(archivo_csv, sep=",")
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False
    
    @classmethod
    def conectar_db(cls):
        # Conecta a la base de datos
        try:
            sqlite_db.connect()
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()

    @classmethod
    def mapear_orm(cls, model_classes):
        # Crea las tablas si no existen
        sqlite_db.create_tables(model_classes)

    @classmethod
    def limpiar_datos(cls, df):
        # Limpia los datos nulos en el DataFrame
        df_cleaned = df.dropna()
        return df_cleaned

    @classmethod
    def cargar_datos(cls, df_cleaned, model_class):
        # Persiste los datos en la base de datos
        for _, row in df_cleaned.iterrows():
            model_class.create(**row.to_dict())

    @classmethod
    def nueva_obra(cls, model_class, foreign_key_model_class):
        # Crea una nueva instancia de Obra ingresando los valores por teclado
        nueva_obra = model_class()

        for field in model_class._meta.fields:
            if field.name != 'ID':
                value = input(f"Ingrese el valor para '{field.name}': ")
                setattr(nueva_obra, field.name, value)

                # Si es una clave foránea, busca el valor en la tabla correspondiente
                if isinstance(field, model_class._meta.fields.ForeignKeyField):
                    foreign_key_value = value
                    foreign_key_instance = foreign_key_model_class.select().where(
                        foreign_key_model_class.ID == foreign_key_value
                    ).first()

                    # Si no encuentra la instancia, informa al usuario y pide un nuevo ingreso
                    if not foreign_key_instance:
                        print(f"No se encontró la instancia con ID {foreign_key_value} en la tabla {foreign_key_model_class.__name__}.")
                        return None

                    setattr(nueva_obra, field.name, foreign_key_instance)

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
    


GestionarObra.conectar_db()

#GestionarObra.mapear_orm([Obra, Etapa, Tipo_obra, Tipo_contratacion, Comuna, Barrio])

#df_cleaned=NO PUDE USAR EL METODO LIMPIAR DATOS PORQUE DEJA EL DF VACIO --- GestionarObra.limpiar_datos(GestionarObra.extraer_datos("./observatorio-de-obras-urbanas.csv"))

#Encontre esta manera de limpiar las columnas del dataframe para persistir solo los datos que yo deje en Obra y las otras clases creadas

df_a_limpiar = GestionarObra.extraer_datos("./observatorio-de-obras-urbanas.csv")
columnas_a_eliminar = ["entorno", "descripcion", "direccion", "lat", "lng", "imagen_1", "imagen_2", "imagen_3", "imagen_4",
                    "licitacion_oferta_empresa", "licitacion_anio", "beneficiarios", "ba_elige", "link_interno", 
                    "pliego_descarga", "expediente-numero", "estudio_ambiental_descarga"]
df_columnas_limpias = df_a_limpiar.drop(columnas_a_eliminar, axis = 1)
#print(df_a_limpiar)
#print(df_columnas_limpias)

#Este método reemplaza los datos nulos o NaN por el valor 0
df_columnas_limpias.fillna(0, inplace=True)

#Ahora paso los datos del dataframe con menos columnas a las clases/tablas creadas en la BD (falta evitar valores repetidos)

GestionarObra.cargar_datos(df_columnas_limpias, Obra)
GestionarObra.cargar_datos(df_columnas_limpias, Barrio)
GestionarObra.cargar_datos(df_columnas_limpias, Comuna)
GestionarObra.cargar_datos(df_columnas_limpias, Etapa)
GestionarObra.cargar_datos(df_columnas_limpias, Tipo_contratacion)
GestionarObra.cargar_datos(df_columnas_limpias, Tipo_obra)



