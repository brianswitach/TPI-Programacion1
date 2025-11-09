
import csv

def cargar_csv(ruta):
    datos=[]
    with open(ruta, newline='', encoding='utf-8') as f:
        lector=csv.DictReader(f)
        for fila in lector:
            try:
                nombre=str(fila["nombre"]).strip()
                poblacion=int(str(fila["poblacion"]).strip())
                superficie=int(str(fila["superficie"]).strip())
                continente=str(fila["continente"]).strip()
                if not nombre or not continente or poblacion<0 or superficie<0:
                    continue
                datos.append({"nombre":nombre,"poblacion":poblacion,"superficie":superficie,"continente":continente})
            except Exception:
                continue
    return datos

def guardar_csv(ruta, datos):
    campos=["nombre","poblacion","superficie","continente"]
    with open(ruta,"w",newline="",encoding="utf-8") as f:
        escritor=csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for d in datos:
            escritor.writerow(d)

def normalizar_nombre(x):
    return str(x).strip()

def encontrar_indices_por_nombre(datos, nombre):
    n=normalizar_nombre(nombre).lower()
    res=[]
    for i,d in enumerate(datos):
        if n in d["nombre"].lower():
            res.append(i)
    return res

def agregar_pais(datos, nombre, poblacion, superficie, continente):
    nombre=normalizar_nombre(nombre)
    if not nombre or not continente: 
        return False
    try:
        poblacion=int(poblacion)
        superficie=int(superficie)
    except:
        return False
    if poblacion<0 or superficie<0:
        return False
    datos.append({"nombre":nombre,"poblacion":poblacion,"superficie":superficie,"continente":continente})
    return True

def actualizar_pais(datos, nombre, nueva_poblacion, nueva_superficie):
    idxs=encontrar_indices_por_nombre(datos, nombre)
    if not idxs:
        return False
    try:
        np=int(nueva_poblacion)
        ns=int(nueva_superficie)
    except:
        return False
    if np<0 or ns<0:
        return False
    for i in idxs:
        datos[i]["poblacion"]=np
        datos[i]["superficie"]=ns
    return True

def buscar_paises(datos, nombre):
    idxs=encontrar_indices_por_nombre(datos, nombre)
    return [datos[i] for i in idxs]

def filtrar_por_continente(datos, continente):
    c=str(continente).strip().lower()
    return [d for d in datos if d["continente"].lower()==c]

def filtrar_por_rango_poblacion(datos, minimo, maximo):
    try:
        minimo=int(minimo); maximo=int(maximo)
    except:
        return []
    if minimo>maximo:
        minimo,maximo=maximo,minimo
    return [d for d in datos if minimo<=d["poblacion"]<=maximo]

def filtrar_por_rango_superficie(datos, minimo, maximo):
    try:
        minimo=int(minimo); maximo=int(maximo)
    except:
        return []
    if minimo>maximo:
        minimo,maximo=maximo,minimo
    return [d for d in datos if minimo<=d["superficie"]<=maximo]

def ordenar_paises(datos, clave, descendente=False):
    claves={"nombre","poblacion","superficie"}
    if clave not in claves:
        return datos[:]
    return sorted(datos, key=lambda d: d[clave], reverse=descendente)

def estadisticas(datos):
    if not datos:
        return None
    mayor=max(datos, key=lambda d:d["poblacion"])
    menor=min(datos, key=lambda d:d["poblacion"])
    prom_p=sum(d["poblacion"] for d in datos)/len(datos)
    prom_s=sum(d["superficie"] for d in datos)/len(datos)
    por_continente={}
    for d in datos:
        c=d["continente"]
        por_continente[c]=por_continente.get(c,0)+1
    return {"mayor_poblacion":mayor,"menor_poblacion":menor,"promedio_poblacion":prom_p,"promedio_superficie":prom_s,"cantidad_por_continente":por_continente}

def pedir_entero(mensaje):
    while True:
        x=input(mensaje).strip()
        try:
            return int(x)
        except:
            print("Entrada inválida. Intente nuevamente.")

def mostrar(d):
    print(f'{d["nombre"]} | Población: {d["poblacion"]} | Superficie: {d["superficie"]} | Continente: {d["continente"]}')

def menu():
    print("1) Cargar CSV")
    print("2) Agregar país")
    print("3) Actualizar país")
    print("4) Buscar país por nombre")
    print("5) Filtrar por continente")
    print("6) Filtrar por rango de población")
    print("7) Filtrar por rango de superficie")
    print("8) Ordenar países")
    print("9) Mostrar estadísticas")
    print("10) Guardar CSV")
    print("0) Salir")

def main():
    ruta_csv="dataset.csv"
    datos=[]
    while True:
        menu()
        opcion=input("Opción: ").strip()
        if opcion=="1":
            try:
                datos=cargar_csv(ruta_csv)
                print(f"Registros cargados: {len(datos)}")
            except Exception as e:
                print("Error al cargar CSV.")
        elif opcion=="2":
            n=input("Nombre: ").strip()
            p=pedir_entero("Población: ")
            s=pedir_entero("Superficie: ")
            c=input("Continente: ").strip()
            if agregar_pais(datos,n,p,s,c):
                print("País agregado.")
            else:
                print("No se pudo agregar.")
        elif opcion=="3":
            n=input("Nombre a actualizar (parcial o exacto): ").strip()
            p=pedir_entero("Nueva población: ")
            s=pedir_entero("Nueva superficie: ")
            if actualizar_pais(datos,n,p,s):
                print("Actualización realizada.")
            else:
                print("No se pudo actualizar.")
        elif opcion=="4":
            n=input("Nombre a buscar: ").strip()
            res=buscar_paises(datos,n)
            if res:
                for d in res: mostrar(d)
            else:
                print("Sin resultados.")
        elif opcion=="5":
            c=input("Continente: ").strip()
            res=filtrar_por_continente(datos,c)
            if res:
                for d in res: mostrar(d)
            else:
                print("Sin resultados.")
        elif opcion=="6":
            a=pedir_entero("Mínimo población: ")
            b=pedir_entero("Máximo población: ")
            res=filtrar_por_rango_poblacion(datos,a,b)
            if res:
                for d in res: mostrar(d)
            else:
                print("Sin resultados.")
        elif opcion=="7":
            a=pedir_entero("Mínimo superficie: ")
            b=pedir_entero("Máximo superficie: ")
            res=filtrar_por_rango_superficie(datos,a,b)
            if res:
                for d in res: mostrar(d)
            else:
                print("Sin resultados.")
        elif opcion=="8":
            c=input("Clave (nombre/poblacion/superficie): ").strip()
            d=input("Descendente? (s/n): ").strip().lower()=="s"
            res=ordenar_paises(datos,c,d)
            for r in res: mostrar(r)
        elif opcion=="9":
            est=estadisticas(datos)
            if not est:
                print("Sin datos.")
            else:
                print("Mayor población:"); mostrar(est["mayor_poblacion"])
                print("Menor población:"); mostrar(est["menor_poblacion"])
                print(f'Promedio población: {est["promedio_poblacion"]:.2f}')
                print(f'Promedio superficie: {est["promedio_superficie"]:.2f}')
                print("Cantidad por continente:")
                for k,v in est["cantidad_por_continente"].items():
                    print(f'{k}: {v}')
        elif opcion=="10":
            try:
                guardar_csv(ruta_csv, datos)
                print("CSV guardado.")
            except:
                print("Error al guardar CSV.")
        elif opcion=="0":
            break
        else:
            print("Opción inválida.")

if __name__=="__main__":
    main()
