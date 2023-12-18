# README

## Descripción del Programa

### a. Gráfico de Precio de Bitcoin Filtrable por Periodo Típico

Este programa logra mostrar un gráfico interactivo del precio de Bitcoin con la capacidad de filtrar por períodos típicos comúnmente utilizados en gráficos de acciones. Esta funcionalidad se ha implementado gracias a la biblioteca Plotly.

### b. Formularios Adicionales

Se han incorporado dos formularios adicionales para ampliar la funcionalidad del programa:

1. **Consulta de Precio en Fecha Específica:** Permite visualizar el precio de Bitcoin en una fecha específica.

2. **Consulta de Precio Promedio entre Dos Fechas:** Permite la visualización del precio promedio de Bitcoin en el intervalo seleccionado.

El primer formulario interactúa con la base de datos, registrando cada consulta realizada. Esto se ha implementado con el propósito de demostrar la interacción con la base de datos creada para el proyecto.

### c. Base de Datos en PostgreSQL

Se crea una base de datos llamada mywacc. configurada en PostgreSQL, y las credenciales de acceso se encuentran en el archivo `settings.py`.

## Instrucciones para Ejecutar el Programa

1. **Crear Migraciones:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Correr el Servidor:**

   ```bash
   python manage.py runserver
   ```

3. **Acceder al Programa:**

   Ingresa al siguiente enlace en tu navegador web:

   ```bash
   http://127.0.0.1:8000/app/
   ```

### d. Consideraciones

Se ha implementado el manejo de errores con la API externa para evitar la interrupción del programa. Es importante destacar que realizar múltiples llamadas consecutivas a la API puede provocar la caída de los gráficos o valores mostrados debido a la falta de respuestas de la API.
