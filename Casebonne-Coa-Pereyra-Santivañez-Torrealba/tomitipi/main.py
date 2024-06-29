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
        pass
    elif eleccion == 2:
        pass
    elif eleccion == 3:
        pass
    elif eleccion == 4:
        pass

if __name__ == '__main__':
    
    
    # Probando el codigo
    
    go.mapear_orm(modelo_orm)     #Aqui se mapea
    df = go.extraer_datos()       # Se extrae el dataframe del archivo
    print(df)           
    go.limpiar_datos(df)          # Limpiamos, se ponen en 0 los datos nulos, falto quitarle los espacios en blancos
    print(df)

    go.cargar_datos(df)           # Lo cargamos a la base de datos
    

    #go.nueva_obra()              # Se agrega una nueva obra, aguantate porque son 36 campos

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