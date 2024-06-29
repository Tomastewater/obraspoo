from peewee import  *

db = SqliteDatabase('./Casebonne-Coa-Pereyra-Santivañez-Torrealba/obras_urbanas.db', pragmas={'journal_mode': 'wal'})

try:
    db.connect()
except OperationalError as e:
    print("Se ha generado un error en la conexión a la BD.", e)
    exit()

# Define la clase BaseModel
class BaseModel(Model):
    class Meta:
        database = db

# Clase para la ubicación
class Ubicacion(BaseModel):
    ID = IntegerField(primary_key=True)
    lat = FloatField()
    lng = FloatField()
    comuna = CharField()
    barrio = CharField()
    direccion = CharField()

    class Meta:
        db_table = 'ubicaciones'

    def __str__(self):
        return f"Comuna: {self.comuna}, Barrio: {self.barrio}, Direccion: {self.direccion}"

# Clase para las fechas
class Fechas(BaseModel):
    ID = IntegerField(primary_key=True)
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()

    class Meta:
        db_table = 'fechas'

    def incrementar_plazo(self, meses):
        if meses > 0:
            self.plazo_meses += meses
            self.save()
        else:
            raise ValueError("La cantidad de meses debe ser mayor que 0.")

    def __str__(self):
        return f"Fecha de inicio: {self.fecha_inicio}, Fecha fin inicial: {self.fecha_fin_inicial}, Plazos mensuales: {self.plazo_meses}"

# Clase para la contratación
class Contratacion(BaseModel):
    ID = IntegerField(primary_key=True)
    licitacion_oferta_empresa = CharField()
    licitacion_anio = IntegerField()
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()

    class Meta:
        db_table = 'contrataciones'

    def __str__(self):
        return f"Licitacion - Oferta de la empresa: {self.licitacion_oferta_empresa}, Cuit Contratista: {self.cuit_contratista}"

class Imagen(BaseModel):

    ID = IntegerField(primary_key=True) 
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()

    def __str__(self):
        return f"Imagen 1: {self.imagen_1}, Imagen 2: {self.imagen_2}, Imagen 3: {self.imagen_3}, Imagen 4: {self.imagen_4}"
    
    class Meta:
        db_table = 'imagenes'

# Define la clase del modelo de datos
class Obra(BaseModel):
    ID = IntegerField(primary_key=True)
    ubicacion = ForeignKeyField(Ubicacion, backref='obras')
    fechas = ForeignKeyField(Fechas, backref='obras')
    contratacion = ForeignKeyField(Contratacion, backref='obras')
    imagenes = ForeignKeyField(Imagen, backref='obras')
    entorno = CharField()
    nombre = CharField()
    etapa = CharField()
    tipo = CharField()
    area_responsable = CharField()
    descripcion = CharField()
    monto_contrato = FloatField()
    porcentaje_avance = FloatField()
    beneficiarios = IntegerField()
    mano_obra = IntegerField()
    compromiso = CharField()
    destacada = BooleanField()
    ba_elige = BooleanField()
    link_interno = CharField()
    pliego_descarga = CharField()
    expediente_numero = CharField()
    estudio_ambiental_descarga = CharField()
    financiamiento = CharField()

    class Meta:
        db_table = 'obras'

    def __str__(self):
        return f"ID: {self.ID}, Nombre: {self.nombre}, Etapa: {self.etapa}, Porcentaje Avancee: {self.porcentaje_avance}, Mano de Obra: {self.mano_obra}"

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
    

if __name__ == '__main__':

    pass