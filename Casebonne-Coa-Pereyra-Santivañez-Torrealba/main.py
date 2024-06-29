from modelo_orm import *
from gestionar_obras import GestionarObra as go

def main():
    eleccion = (int)(input("""
                           
                           ___Eliga una opcion (en numero)___
                     
                     1. Crear nueva obra
                     2. Nuevo Proyecto
                     3. Adjudicar obra
                     4. Cargar datos
                           
                     """))
    
    if eleccion == 1:
        crearInstancias()
    elif eleccion == 2:
        GestionarObra.conectar_db
        obra = Obra.get_by_id(1)
        setattr(obra, "etapa", 'Nuevo')
        obra.save()

        GestionarObra.db.close()
    elif eleccion == 3:
        mostrar_nombre_obra(1)
    elif eleccion == 4:
        GestionarObra.extraer_datos()

if __name__ == '__main__':
    
    
    # Probando el codigo
    """go.mapear_orm(modelo_orm)
    df = go.extraer_datos()
    print(df)
    go.limpiar_datos(df)
    print(df)

    go.cargar_datos(df)
    """

    #go.nueva_obra()

    print(go.obtener_indicadores())

    obra = Obra.get(Obra.nombre == 2)
    print(obra)

    obra.iniciar_contratacion()
    print(obra)

    obra.adjudicar_obra()
    print(obra)

    obra.iniciar_obra()
    print(obra)

    obra.actualizar_porcentaje_avance(80)
    print(obra)

    obra.incrementar_mano_obra(15)
    print(obra)

    obra.finalizar_obra()
    print(obra)

    obra.rescindir_obra()
    print(obra)