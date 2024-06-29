from peewee import *

#Creando la base de datos SQLite donde vamos a persistir los datos importados del dataset
sqlite_db = SqliteDatabase('./obras_urbanas.db', pragmas={'journal_mode': 'wal'})

class BaseModel(Model):
    class Meta:
        database = sqlite_db #Este modelo va a usar la base de datos "obras_urbanas.db"

class Etapa(BaseModel):
    etapa = CharField()
    class Meta:
        db_table = 'etapa'

class Tipo_obra(BaseModel):
    tipo = CharField()
    class Meta:
        db_table = 'tipo_obra'

class Tipo_contratacion(BaseModel):
    contratacion_tipo = CharField()
    class Meta:
        db_table = 'tipo_contratacion'

class Comuna(BaseModel):
    comuna = CharField()
    class Meta:
        db_table = 'comuna'

class Barrio(BaseModel):
    barrio = CharField()
    class Meta:
        db_table = 'barrio'

class Obra(BaseModel):
    ID = IntegerField(primary_key=True)
    nombre = CharField()
    etapa = ForeignKeyField(Etapa, backref='etapa')
    tipo = ForeignKeyField(Tipo_obra, backref='tipo_obra')
    area_responsable = CharField()
    monto_contrato = FloatField()
    comuna = ForeignKeyField(Comuna, backref='comuna')
    barrio = ForeignKeyField(Barrio, backref='barrio')
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    porcentaje_avance = FloatField()
    contratacion_tipo = CharField()
    nro_contratacion = ForeignKeyField(Tipo_contratacion, backref='tipo_contratacion')
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

class Etapa(BaseModel):
    etapa = CharField()
    class Meta:
        db_table = 'etapa'

class Tipo_obra(BaseModel):
    tipo = CharField()
    class Meta:
        db_table = 'tipo_obra'

class Tipo_contratacion(BaseModel):
    contratacion_tipo = CharField()
    class Meta:
        db_table = 'tipo_contratacion'

class Comuna(BaseModel):
    comuna = CharField()
    class Meta:
        db_table = 'comuna'

class Barrio(BaseModel):
    barrio = CharField()
    class Meta:
        db_table = 'barrio'



