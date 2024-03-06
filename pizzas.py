class Guardar:
    @staticmethod
    
    def unapizza(tamaño, ingredientes, numero):
         try:
            # Verificar el tamaño y asignar el costo correspondiente
            if tamaño == 'chica':
                costo_tamaño = 40
            elif tamaño == 'mediana':
                costo_tamaño = 80
            elif tamaño == 'grande':
                costo_tamaño = 120
            else:
                raise ValueError("Tamaño de pizza no válido")

            subtotal = costo_tamaño * numero

            # Añadir costos de ingredientes si están seleccionados
            if ingredientes.get('jamon', False):
                subtotal += 10*numero
            if ingredientes.get('piña', False):
                subtotal += 10*numero
            if ingredientes.get('champiñones', False):
                subtotal += 10*numero
            
            

            ingredientes_seleccionados = [ingrediente for ingrediente, seleccionado in ingredientes.items() if seleccionado]
            with open('pizzas.txt', 'a') as archivo_texto:
                cadena_ingredientes = ', '.join(ingredientes_seleccionados)
                archivo_texto.write(f'\n{tamaño}-{cadena_ingredientes }-{numero}-{subtotal}')
            datos_archivo = Guardar.leer_datos_archivo()
            return "¡Muy bien insertado correctamente!"
         except Exception as e:
            return f"Error al insertar la palabra: {e}"

    @staticmethod
    def leer_datos_archivo():
     datos = []
     try:
        with open('pizzas.txt', 'r') as archivo_texto:
            lineas = archivo_texto.readlines()
            for idx, linea in enumerate(lineas):
                try:
                    partes = linea.strip().split('-')
                    if len(partes) == 4:
                        tamaño, ingredientes, numero, subtotal = partes[0], partes[1], int(partes[2]), int(partes[3])
                        datos.append({'tamaño': tamaño, 'ingredientes': ingredientes, 'numero': numero, 'subtotal': subtotal})
                    else:
                        print(f"Advertencia: Ignorando línea con formato incorrecto en la línea {idx + 1}: {linea}")
                except Exception as e:
                    print(f"Error al procesar línea {idx + 1}: {e}")
     except Exception as e:
        print(f"Error al leer el archivo: {e}")
     return datos

    @staticmethod
    def sumar_subtotales():
        try:
            with open('pizzas.txt', 'r') as archivo_texto:
                lineas = archivo_texto.readlines()

            total_subtotales = sum(int(linea.strip().split('-')[3]) for linea in lineas if len(linea.strip().split('-')) == 4)

            return total_subtotales
        except Exception as e:
            return f"Error al sumar los subtotales: {e}"

if __name__ == "__main__":
    # Insertar una pizza
    tamaño_pizza = 'mediana'
    ingredientes_pizza = {'jamon': True, 'piña': True, 'champiñones': False}
    numero_pizza = 2


    resultado = Guardar.unapizza(tamaño_pizza, ingredientes_pizza, numero_pizza)
    print(resultado)

    