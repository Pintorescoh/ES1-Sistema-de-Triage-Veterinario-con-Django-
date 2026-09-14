# Uso de Inteligencia Artificial (EVA 2)

Durante este proyecto, utilicé IA (Gemini) como un asistente de aprendizaje para entender la sintaxis de Python y la estructura base de Django.

* La IA me propuso utilizar MongoDB Atlas en la nube, pero rechacé y corregí esta sugerencia basándome en el documento de migración, obligando a la IA a reestructurar el modelo para utilizar SQLite localmente".

* La IA me entregó el código inicial para el archivo `views.py` intentando importar una función inventada por ella llamada `evaluar_triage`. Al levantar el servidor, el sistema arrojó error. Le mostré la evidencia a la IA y le exigí que corrigiera el código, así respetar el documento de instrucciones que indicaba explícitamente que la función original debía mantenerse intacta bajo el nombre `decidir()`. La IA tuvo que reescribir las vistas para importar correctamente el motor lógico.