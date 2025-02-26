



### para añadir

1. crea agente con su logica translator.py
2. regitrar agante en Main.py -agente y tarea

3. Añadir nueva tarea utils/weather.py.
4. añade tarea a agente main.py



Flujo de Ejecución
1. Inicialización
Secuencia : En serie.
Descripción :
Se cargan las configuraciones desde config.json.
Se inicializa el cliente Ollama.
Se crean instancias de los agentes (agente1, agente2, agente3, agente4 y supervisor).
Se definen las tareas y se asignan a los agentes correspondientes.
2. Ejecución de Tareas
Esquema : Paralelo.
Descripción :
Las tareas se ejecutan en paralelo utilizando ThreadPoolExecutor.
Cada tarea se asigna a un agente específico.
Si la tarea está registrada en task_registry, se utiliza la función correspondiente (por ejemplo, obtener temperatura, hora, traducción, etc.).
Si no está registrada, se usa el modelo de lenguaje de Ollama para generar una respuesta.
3. Supervisión
Secuencia : En serie.
Descripción :
Una vez que todas las tareas han sido completadas, el supervisor evalúa cada respuesta de manera secuencial.
El supervisor genera una evaluación para cada resultado y registra su veredicto.
Diagrama del Flujo de Ejecución
Aquí tienes un diagrama visual que representa el flujo:

Copiar
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
[Inicio]
    |
    v
[Cargar Configuración]
    |
    v
[Inicializar Clientes y Agentes]
    |
    v
[Definir Tareas]
    |
    v
[Ejecución de Tareas]
    |
    v
+-------------------------------------------------------------+
|                                                             |
|                     [Paralelismo]                           |
|                                                             |
|  +-------------------+      +-------------------+          |
|  | Agente 1 (Tarea 1) | ---> | Agente 2 (Tarea 2) |          |
|  +-------------------+      +-------------------+          |
|                                                             |
|  +-------------------+      +-------------------+          |
|  | Agente 3 (Tarea 3) | ---> | Agente 4 (Tarea 4) |          |
|  +-------------------+      +-------------------+          |
|                                                             |
+-------------------------------------------------------------+
    |
    v
[Recopilar Resultados]
    |
    v
[Supervisión Secuencial]
    |
    v
+-------------------------------------------------------------+
|                                                             |
|  [Serie]                                                    |
|                                                             |
|  Supervisor evalúa respuesta de Agente 1                    |
|  --> Supervisor evalúa respuesta de Agente 2                |
|  --> Supervisor evalúa respuesta de Agente 3                |
|  --> Supervisor evalúa respuesta de Agente 4                |
|                                                             |
+-------------------------------------------------------------+
    |
    v
[Muestra Resultados Finales]
    |
    v
[Fin]
Esquema: Mixto (Paralelo + Serie)
Parte Paralela :
La ejecución de las tareas se realiza en paralelo gracias a ThreadPoolExecutor. Esto permite que varias tareas se procesen simultáneamente, lo cual mejora significativamente el rendimiento cuando las tareas son independientes entre sí.
Parte Serial :
La supervisión de las respuestas se realiza de forma secuencial. El supervisor evalúa una respuesta después de otra, asegurando que cada evaluación sea completa antes de pasar a la siguiente.
Resumen del Esquema
Ejecución de Tareas : Paralelo (optimiza el tiempo de procesamiento).
Supervisión : En Serie (garantiza que cada evaluación sea precisa y ordenada).
Flujo General : Mixto (combinación de paralelismo para tareas y secuencia para supervisión).
Este diseño es eficiente porque aprovecha el paralelismo donde es posible (ejecución de tareas) y mantiene la secuencia donde es necesario (evaluación por el supervisor).