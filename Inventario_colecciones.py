import os
import json
from tabulate import tabulate  # Librería para darle formato a las tablas

# Obtener la ruta del directorio actual de trabajo

# Nombre de los archivos JSON donde se almacenará la información
ARCHIVO_INVENTARIO = "inventario.json"
ARCHIVO_ELIMINADOS = "productos_fuera_de_stock.json"

class Inventario:
    # Clase para gestionar el inventario de artículos.
    def __init__(self):
        self.inventario = self.cargar_datos(ARCHIVO_INVENTARIO)
        self.eliminados = self.cargar_datos(ARCHIVO_ELIMINADOS, lista=True)

    def cargar_datos(self, archivo, lista=False):
        # Carga los datos desde un archivo JSON.
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as file:
                return json.load(file)
        return {} if not lista else []

    def guardar_datos(self, archivo, datos):
        # Guarda los datos en un archivo JSON.
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)

    def agregar_articulo(self):
        # Agrega un nuevo artículo al inventario.
        id_unico = input("Ingrese ID único del artículo: ")
        if id_unico in self.inventario:
            print("Error: ID ya existe en el inventario.")
            return

        nombre = input("Ingrese nombre del artículo: ")
        cantidad = int(input("Ingrese cantidad: "))
        precio = float(input("Ingrese precio: ").replace(",", "."))

        self.inventario[id_unico] = {"ID Artículo": id_unico, "Nombre": nombre, "Cantidad": cantidad, "Precio": precio}
        self.guardar_datos(ARCHIVO_INVENTARIO, self.inventario)
        print("Artículo añadido con éxito.")

    def eliminar_articulo(self):
        # Elimina un artículo del inventario y lo mueve a la lista de eliminados.
        id_unico = input("Ingrese ID del artículo a eliminar: ")
        if id_unico in self.inventario:
            self.eliminados.append(self.inventario.pop(id_unico))
            self.guardar_datos(ARCHIVO_INVENTARIO, self.inventario)
            self.guardar_datos(ARCHIVO_ELIMINADOS, self.eliminados)
            print("Artículo eliminado con éxito.")
        else:
            print("Error: ID no encontrado.")

    def actualizar_articulo(self):
        # Actualiza los datos de un artículo en el inventario.
        id_unico = input("Ingrese ID del artículo a actualizar: ")
        if id_unico in self.inventario:
            print("Datos actuales del artículo:")
            self.mostrar_tabla([self.inventario[id_unico]])

            nombre = input("Nuevo nombre (Enter para mantener actual): ") or self.inventario[id_unico]["nombre"]
            cantidad = input("Nueva cantidad (Enter para mantener actual): ")
            cantidad = int(cantidad) if cantidad else self.inventario[id_unico]["cantidad"]
            precio = input("Nuevo precio (Enter para mantener actual): ")
            precio = float(precio.replace(",", ".")) if precio else self.inventario[id_unico]["precio"]

            self.inventario[id_unico] = {"ID Artículo": id_unico, "Nombre": nombre, "Cantidad": cantidad,
                                         "Precio": precio}
            self.guardar_datos(ARCHIVO_INVENTARIO, self.inventario)
            print("Artículo actualizado con éxito.")
        else:
            print("Error: ID no encontrado.")

    def buscar_articulos(self):
        # Busca artículos en el inventario por nombre o parte del nombre.
        busqueda = input("Ingrese nombre o parte del nombre a buscar: ").lower()
        encontrados = [articulo for articulo in self.inventario.values() if busqueda in articulo["nombre"].lower()]
        self.mostrar_tabla(encontrados)

    def mostrar_tabla(self, articulos):
        # Muestra los artículos en formato de tabla.
        if articulos:
            print(tabulate(articulos, headers="keys", tablefmt="fancy_grid"))
        else:
            print("No hay artículos disponibles.")


def mostrar_menu():
    # Función que muestra el menú de opciones y gestiona la interacción con el usuario.
    inventario = Inventario()

    while True:
        print("\n" + "=" * 50)
        print("║    Papelería Compu Click Tena - Inventario     ║")
        print("=" * 50)
        print("1. Añadir nuevo artículo")
        print("2. Eliminar artículo")
        print("3. Actualizar artículo")
        print("4. Buscar artículos")
        print("5. Mostrar todos los artículos")
        print("6. Mostrar artículos eliminados")
        print("7. Salir")
        print("=" * 50)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inventario.agregar_articulo()
        elif opcion == "2":
            inventario.eliminar_articulo()
        elif opcion == "3":
            inventario.actualizar_articulo()
        elif opcion == "4":
            inventario.buscar_articulos()
        elif opcion == "5":
            print("*********** Artículos disponibles en Inventario ***********")
            inventario.mostrar_tabla(list(inventario.inventario.values()))
        elif opcion == "6":
            print("************* Artículos eliminados del Inventario *************")
            inventario.mostrar_tabla(inventario.eliminados)
        elif opcion == "7":
            print("******* Gracias por usar el sistema de Inventario de Compu Click. ¡Hasta luego! *******")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")

mostrar_menu()