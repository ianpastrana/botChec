# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

# *********************************************************************************

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import zeep
import requests
from rasa_sdk import Action, Tracker # Esto está definico en el archivo interfaces.py
#from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#from rasa_sdk.forms import formAction

import pandas as pd
import sys


from conexionWebService import  WebService


class ObtenerDatosUsuario(Action):
        
    def name(self):
        #return "get_todays_horoscope"
        return "accion_obtener_datos_usuario" # nombre de accion definido en el archivo domain
    
    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        """user_horoscope_sign = tracker.get_slot('horoscope_sign')
        base_url = http://horoscope-api.herokuapp.com/horoscope/{day}/{sign}
        url = base_url.format(**{'day': "today", 'sign': user_horoscope_sign})
        #http://horoscope-api.herokuapp.com/horoscope/today/capricorn
        res = requests.get(url)
        todays_horoscope = res.json()['horoscope']
        response = "Your today's horoscope:\n{}".format(todays_horoscope)
        """
        # rastreador de estado para el usuario actual. Accesamos valores slot.
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta') #pasamos el nombre del slot que estamos accesando
        
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        #print(conexion.token)
        #conexion.datosClientes(str(107558968))
                
        
        #wsdl = 'https://checomnicanalidad.chec.com.co/WS_SIEC_Omni.SSiec.svc?wsdl'
        #client = zeep.Client(wsdl=wsdl)
        #print('-1', numero_cuenta_usuario)
        #consulta = client.service.GetDatos(numero_cuenta_usuario)
        consulta = conexion.solicitud(numero_cuenta_usuario, "Cliente")
        if not consulta["IsOk"]:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario) 
            
        #print('0', consulta)
        #consulta = consulta.split('\r\n')[:-1]
        #print('1', consulta)
        #consulta = [linea.split('|') for linea in consulta]
        #print('2', consulta)
        #consulta = dict(zip(*consulta))
        #print('3', consulta)
        #consulta = consulta['nombre']
        #print('4', consulta)
              
        respuesta = "Los datos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]

class AltoCosto(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "accion_alto_costo" # nombre de accion definido en el archivo domain
    
    #@consulta
    def consulta(self, consultaRx):
        print(consultaRx)
        consultaRx = consultaRx.split('\r\n')[:-1]
        consultaRx = [linea.split('|') for linea in consultaRx]
        dfConsulta = pd.DataFrame(consultaRx[1:],columns =consultaRx[0])
        return dfConsulta
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        #sys.stdout.write(numero_cuenta_usuario)
        #print(numero_cuenta_usuario)
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        consulta = conexion.solicitud(numero_cuenta_usuario, "Consumo")
        if not consulta["IsOk"]:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        '''
        
        # rastreador de estado para el usuario actual. Accesamos valores slot.
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta') #pasamos el nombre del slot que estamos accesando
        print('-1', numero_cuenta_usuario)
        periodo = tracker.get_slot('fecha_factura')
        valor_factura = tracker.get_slot('obtener_valor_factura')
        print(periodo)
        #wsdl = 'https://checomnicanalidad.chec.com.co/WS_SIEC_Omni.SSiec.svc?wsdl'
        cliente = zeep.Client(wsdl='https://checomnicanalidad.chec.com.co/WS_SIEC_Omni.SSiec.svc?wsdl')
        consumos = cliente.service.GetConsumos(numero_cuenta_usuario)
        print(consumos)
        
        dfConsumos = self.consulta(consumos)  
        dfConsumos['Periodo'] = pd.to_datetime(dfConsumos.Mes + '/' + dfConsumos.Ano,format='%m/%Y')
        dfConsumos.sort_values('Periodo', ascending=False).reset_index(drop=True)
        #dfConsumos['Periodo'] = (dfConsulta.Mes + '/' + dfConsulta.Ano).astype('datetime64[ns]')
        ultimoConsumo = int(dfConsumos.loc[0,'consumo_KWH'])
        ultimos6Consumos = dfConsumos.loc[1:7,'consumo_KWH'].astype(int)
        consumoPromedio = round(ultimos6Consumos.mean())
        if(ultimoConsumo / consumoPromedio >= 1.35):
            respuestaConsumo = "Su Último consumo fue de {} kWh. Los consumos en los anteriores 6 meses fue de {} kWh".format(ultimoConsumo, 
                                                                                                                              list(ultimos6Consumos))
        else:
            ProductosActivos = cliente.service.GetProductosActivos(numero_cuenta_usuario)
            dfProductosActivos = self.consulta(ProductosActivos)
            print(dfProductosActivos)
            respuestaConsumo = "No tenemos problemas con su consumo de energia. El consumo promedio de los últimos 6 meses fue de {} kHw, y el actual es de {}. Actualmente tiene {} productos activos:\n {}".format(ultimoConsumo, consumoPromedio, dfProductosActivos.shape[0], dfProductosActivos)
        #dfRespuesta = dfConsumos.loc[dfConsumos.Periodo == periodo]
        respuesta = respuestaConsumo
        #if valor_factura:
        #    respuesta = "El valor facturado para el {} es de: {}".format(periodo, dfRespuesta['valor_$'].values)
        '''
        respuesta = "Los datos de Costos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)] 
        

        
class ValorAPagar(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "accion_valor_a_pagar" # nombre de accion definido en el archivo domain
    
    #@consulta
    def consulta(self, consultaRx):
        print(consultaRx)
        consultaRx = consultaRx.split('\r\n')[:-1]
        consultaRx = [linea.split('|') for linea in consultaRx]
        dfConsulta = pd.DataFrame(consultaRx[1:],columns =consultaRx[0])
        return dfConsulta
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        #sys.stdout.write(numero_cuenta_usuario)
        #print(numero_cuenta_usuario)
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        consulta = conexion.solicitud(numero_cuenta_usuario, "DetalleUltFactura")
        if not consulta["IsOk"]:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        
        respuesta = "Los datos de Costos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)] 
        
        
class FinanciacionProductos(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "accion_financiacion_productos" # nombre de accion definido en el archivo domain
    
    #@consulta
    def consulta(self, consultaRx):
        print(consultaRx)
        consultaRx = consultaRx.split('\r\n')[:-1]
        consultaRx = [linea.split('|') for linea in consultaRx]
        dfConsulta = pd.DataFrame(consultaRx[1:],columns =consultaRx[0])
        return dfConsulta
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        #sys.stdout.write(numero_cuenta_usuario)
        #print(numero_cuenta_usuario)
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        consulta = conexion.solicitud(numero_cuenta_usuario, "Credito")
        #sys.stdout.write(consulta)
        #if not consulta["IsOk"]:
         #   respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        
        respuesta = "Los datos de Costos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]   

class InformacionPagos(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "accion_informacion_pagos" # nombre de accion definido en el archivo domain
    
    #@consulta
    def consulta(self, consultaRx):
        print(consultaRx)
        consultaRx = consultaRx.split('\r\n')[:-1]
        consultaRx = [linea.split('|') for linea in consultaRx]
        dfConsulta = pd.DataFrame(consultaRx[1:],columns =consultaRx[0])
        return dfConsulta
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        #sys.stdout.write(numero_cuenta_usuario)
        #print(numero_cuenta_usuario)
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        consulta = conexion.solicitud(numero_cuenta_usuario, "Pagos")
        #sys.stdout.write(consulta)
        #if not consulta["IsOk"]:
         #   respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        
        respuesta = "Los datos de Costos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]    
    
class InformacionPqrs(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "accion_informacion_pqrs" # nombre de accion definido en el archivo domain
    
    #@consulta
    def consulta(self, consultaRx):
        print(consultaRx)
        consultaRx = consultaRx.split('\r\n')[:-1]
        consultaRx = [linea.split('|') for linea in consultaRx]
        dfConsulta = pd.DataFrame(consultaRx[1:],columns =consultaRx[0])
        return dfConsulta
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        #sys.stdout.write(numero_cuenta_usuario)
        #print(numero_cuenta_usuario)
        conexion = WebService()
        #print(conexion)
        conexion.autenticacion()
        #sys.stdout.write(conexion.token)
        consulta = conexion.solicitud(numero_cuenta_usuario, "PqrPqt")
        #sys.stdout.write(consulta)
        #if not consulta["IsOk"]:
         #   respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        
        respuesta = "Los datos de Costos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)] 
    
 

 
class SubscribeUser(Action):
                
    def name(self):
        return "subscribir_usuario"
    
    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        subscribir = tracker.get_slot('subscribir').lower()
        if subscribir == "si":
            respuesta = "You're successfully subscribed"
        if subscribir == "no":
            respuesta = "You're successfully unsubscribed"
        dispatcher.utter_message(respuesta)
        return [SlotSet("subscribir", subscribir)]
    
class Consumos(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "obtener_consumo" # nombre de accion definido en el archivo domain
    
    def run(self, dispatcher, tracker, domain): 
        consumo_KWH = None; valor_factura = None; Valor_tarifa = None; valor_a_CU = None
        
        # rastreador de estado para el usuario actual. Accesamos valores slot.
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta') #pasamos el nombre del slot que estamos accesando
        periodo = tracker.get_slot('fecha_factura')
        valor_factura = tracker.get_slot('obtener_valor_factura')
        print(periodo)
        wsdl = 'https://checomnicanalidad.chec.com.co/WS_SIEC_Omni.SSiec.svc?wsdl'
        client = zeep.Client(wsdl=wsdl)
        print('-1', numero_cuenta_usuario)
        consulta = client.service.GetConsumos(numero_cuenta_usuario)
        print(consulta)
        consulta = consulta.split('\r\n')[:-1]
        print(consulta)
        consulta = [linea.split('|') for linea in consulta]
        dfConsulta = pd.DataFrame(consulta[1:],columns =consulta[0])  
        dfConsulta['Periodo'] = (dfConsulta.Mes + '/' + dfConsulta.Ano)#.astype('datetime64[ns]')
        dfRespuesta = dfConsulta.loc[dfConsulta.Periodo == periodo]
        if valor_factura:
            respuesta = "El valor facturado para el {} es de: {}".format(periodo, dfRespuesta['valor_$'].values)
              
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]
        
class Financiaciones(Action):    
    
    def name(self):
        #return "get_todays_horoscope"
        return "obtener_financiaciones" # nombre de accion definido en el archivo domain
    
    def run(self, dispatcher, tracker, domain): 
        valor_financiado = None; estado = None; numero_cuotas = None
        
        # rastreador de estado para el usuario actual. Accesamos valores slot.
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta') #pasamos el nombre del slot que estamos accesando
        fecha_financiacion = tracker.get_slot('fecha_factura')
        #valor_financiado = tracker.get_slot('valor_total_financiado')
        tiempo_financiacion = tracker.get_slot('tiempo')
        print(fecha_financiacion)
        wsdl = 'https://checomnicanalidad.chec.com.co/WS_SIEC_Omni.SSiec.svc?wsdl'
        client = zeep.Client(wsdl=wsdl)
        print('-1', numero_cuenta_usuario)
        consulta = client.service.GetFinanciaciones(numero_cuenta_usuario)
        print(consulta)
        consulta = consulta.split('\r\n')[:-1]
        print(consulta)
        consulta = [linea.split('|') for linea in consulta]
        dfConsulta = pd.DataFrame(consulta[1:],columns =consulta[0])  
        #dfConsulta['Periodo'] = (dfConsulta.Mes + '/' + dfConsulta.Ano)#.astype('datetime64[ns]')
        dfRespuesta = dfConsulta.loc[dfConsulta.Fecha == fecha_financiacion]
        print(fecha_financiacion)
        if fecha_financiacion:
            respuesta = "El valor financiado a {} cuotas el {} es de: {}. Su estado es {}.".format(dfRespuesta['numero_cuotas'].values, 
                                                                                                   fecha_financiacion, 
                                                                                                   dfRespuesta['valor_total_financiado'].values, 
                                                                                                   dfRespuesta['estado'].values)
        
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]
    
    
