'''
Created on 28/01/2013
Paramatros del Sistema
@author: diego
'''

'''
Lista de pares (servidor, port) que responde a los mensaje
'''
REQUESTSERVER = [('127.0.0.1',61613)]

'''
Cola donde se envian las requests (consultas)
'''
REQUESTQUEUENAME = '/queue/predictions.requests'

'''
Cola de respuesta
'''
RESPONSEQUEUENAME = '/temp-queue/responseQueue'

'''
Cantidad de Predicciones enviadas en la response (respuesta)
'''
PREDICTIONSNUMBERS = 6

'''
Cantidad de Predicciones enviadas en la wap response (respuesta)
'''
MOBILEPREDICTIONSNUMBERS = 2

'''
Cantidad de Predicciones enviadas en la wap response (respuesta)
'''
SPHONEPREDICTIONSNUMBERS = 3
 
'''
Tiempo limite de respuesta para las consultas
'''
REQUESTTIMEOUT = 15