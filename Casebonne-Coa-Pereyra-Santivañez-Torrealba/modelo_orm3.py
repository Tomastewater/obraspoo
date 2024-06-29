#ACA AGREGUE LAS TABLAS LOOKUP Y MODIFIQUE LA CANTIDAD DE ATRIBUTOS DE OBRA PARA QUE SALGAN MENOS COLUMNAS EN LA TABLA

from peewee import  *

# Define la conexión a la base de datos SQLite
db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})

# Define la clase BaseModel
class BaseModel(Model):
    class Meta:
        database = db

# Definimos las tablas lookup

class Etapa(BaseModel):
    nombre = CharField(unique = True)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'etapas'

class Tipo_obra(BaseModel):
    nombre = CharField(unique = True)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipos_obra'

class Tipo_contratacion(BaseModel):
    nombre = CharField(unique = True)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipos_contratacion'

class Comuna(BaseModel):
    nombre = CharField(unique = True)
    def __str__(self):
        return self.nombre    
    class Meta:
        db_table = 'comunas'

class Barrio(BaseModel):
    nombre = CharField(unique = True)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'barrios'        

# Define la clase del modelo de datos
class Obra(BaseModel):
    ID = IntegerField(primary_key=True)
    nombre = CharField()
    etapa = ForeignKeyField(Etapa, backref='etapas')
    tipo = ForeignKeyField(Tipo_obra, backref='tipos_obra')
    area_responsable = CharField()
    monto_contrato = FloatField()
    comuna = ForeignKeyField(Comuna, backref='comunas')
    barrio = ForeignKeyField(Barrio, backref='barrios')
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    porcentaje_avance = FloatField()
    contratacion_tipo = ForeignKeyField(Tipo_contratacion, backref='tipos_contratacion')
    nro_contratacion = CharField()
    cuit_contratista = CharField()
    mano_obra = IntegerField()
    compromiso = CharField()
    destacada = BooleanField()
    financiamiento = CharField()

    def nuevo_proyecto(self):
        self.etapa = "Nuevo Proyecto"
        self.save()

    def iniciar_contratacion(self):
        self.etapa = "Contratación Iniciada"
        self.save()

    def adjudicar_obra(self):
        self.etapa = "Obra Adjudicada"
        self.save()

    def iniciar_obra(self):
        self.etapa = "Obra Iniciada"
        self.save()

    def actualizar_porcentaje_avance(self, porcentaje):
        if 0 <= porcentaje <= 100:
            self.porcentaje_avance = porcentaje
            self.save()
        else:
            raise ValueError("El porcentaje debe estar entre 0 y 100.")

    def incrementar_plazo(self, meses):
        if meses > 0:
            self.plazo_meses += meses
            self.save()
        else:
            raise ValueError("La cantidad de meses debe ser mayor que 0.")

    def incrementar_mano_obra(self, cantidad):
        if cantidad > 0:
            self.mano_obra += cantidad
            self.save()
        else:
            raise ValueError("La cantidad de mano de obra debe ser mayor que 0.")

    def finalizar_obra(self):
        self.etapa = "Obra Finalizada"
        self.save()

    def rescindir_obra(self):
        self.etapa = "Obra Rescindida"
        self.save()

def inicializar_base_de_datos():
    # Conectar a la base de datos antes de realizar operaciones
    db.connect()

    # Crear las tablas si no existen
    db.create_tables([Obra])

    # Cerrar la conexión después de realizar operaciones
    db.close()

inicializar_base_de_datos()