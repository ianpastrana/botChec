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

#import zeep
import requests
from rasa_sdk import Action, Tracker # Esto está definico en el archivo interfaces.py
#from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#from rasa_sdk.forms import formAction
#from rasa.core.actions.action actions

#import pandas as pd
import sys

import requests
from requests.auth import HTTPDigestAuth
import json
#import jwt
from datetime import timezone
import time
import datetime
from calendar import timegm


class WebService:
    """Crea un objeto que Consulra el WebService de Comercial"""
    
    def __init__(self):
        self.credenciales = {"Username": "admin", "Password": "123456"}
        self.getCuenta = ""
        self.urlAutenticacion = "https://checaliadoscomerciales.chec.com.co/api/login/authenticate"
        self.completarurl = "/GetId?id="
        self.urlConsulta = "https://checaliadoscomerciales.chec.com.co/api/CupoTarjeta" #/GetId?id=107558968"
        
    def autenticacion(self):
        """ solicita token de autenticacion para futuras transacciones 
        
        Args:
            split (str): one of "train", "val", or "test"
        """
        solicitudAutenticacion = requests.post(self.urlAutenticacion, json = self.credenciales)
        self.token = solicitudAutenticacion.json()
            
    def obtener_autenticacion(self):
        """ retorna el token de autenticacion 
            
        Args: Ninguno
        """
        return self.token
        
    def solicitud(self, cuenta, tipoTransaccion):
        """ Consulta la API con el fin de obtener un tipo de consulta 
            
        Args: 
            cuenta (str): la cuenta a consultar
            tipoTransaccion (str): el tipo de consulta a realizar
        """
        cuenta = cuenta.replace(" ", "")
        print(cuenta)
        sys.stdout.write(cuenta)
        urlSolicitud =  "https://checaliadoscomerciales.chec.com.co/api/" + tipoTransaccion + "/GetId?id=" + cuenta
        headers = {'Authorization' : self.token}
        respuesta = requests.get(urlSolicitud, headers=headers)
        return json.loads(respuesta.text)            
             #= "https://checaliadoscomerciales.chec.com.co/api/CupoTarjeta/GetId?id=107558968"
        
 # from conexionWebService import  WebService

class SolicitudFactura(Action):
    
        
    def name(self):
        return "accion_solicitud_factura"
    
    def run(self, dispatcher, tracker, domain):
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta')
        urlCadena = "https://adminchecweb.cadenaportalgestion.com/PDF/Show?Id=" + str(numero_cuenta_usuario)
        #https://adminchecweb.cadenaportalgestion.com/PDF/Show?Id=396789018
        respuesta = requests.get(urlCadena)
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]


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
        respuesta = "Los datos de Alto Costo asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
        dispatcher.utter_message(respuesta)
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)] 
        
def detalleUltimaFactura(consulta, descripcionConcepto, cuenta = False, conexion = False):
    conceptosSimilares = []
    for i in range(len(consulta)):
        if consulta[i]['DescripcionConcepto'] == descripcionConcepto: 
            conceptosSimilares.append((consulta[i]["Valor"], consulta[i]["SaldoAnterior"]))
    return conceptosSimilares
    

    
      
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
        conexion = WebService()
        conexion.autenticacion()
        consulta = conexion.solicitud(numero_cuenta_usuario, "DetalleUltFactura")
        if consulta["IsOk"]:
            respuestaGeneral = ("A continuación se describen los conceptos facturados sobre la Cuenta de Energía {} " + 
                        "para el último periodo facturado.\n\n").format(numero_cuenta_usuario)
            
            conceptoEnergia = detalleUltimaFactura(consulta['Data'], "CONSUMO ACTIVA")
            #sys.stdout.write(str(type(valorEnergia)))
            respuestaEnergia = ("CONCEPTO DE ENERGIA:\n" + 
                                "- Valor por Consumo de Energía en el periodo anterior: ${}\n" + 
                                "- Saldo anterior por energía: ${}\n").format(conceptoEnergia[0][0], conceptoEnergia[0][1])
            respuestaSubsidio = ("- Valor Subsidiado por el Estado: ${}\n").format(detalleUltimaFactura(consulta['Data'], "SUBSIDIO")[0][0])
            respuestaInteresMoraEnergia = ("- Mora sobre el Saldo de Energía de ${}: ${}\n\n").format(conceptoEnergia[0][1],
                                                                                              detalleUltimaFactura(consulta['Data'], "INTERESES DE MORA")[0][0])
            
            respuesta = respuestaGeneral + respuestaEnergia + respuestaSubsidio + respuestaInteresMoraEnergia
            dispatcher.utter_message(respuesta)
            
            # Productos Adicionales
            conceptoCreditos = detalleUltimaFactura(consulta['Data'], "CUOTA PFS - TARJETA")
            conceptoCreditosIntereses = detalleUltimaFactura(consulta['Data'], "INTERES FINANC PFS - TARJETA")
            if conceptoCreditos:
                if len(conceptoCreditos) == 1:
                    pluralidadCreditos = "Cŕedito Activo"
                else:
                    pluralidadCreditos = "Cŕeditos Activos" 
                cantidadCreditos = len(conceptoCreditos)
                respuesta = ("CONCEPTO DE PRODUCTOS ADICIONALES A ENERGIA.\n" +
                                "La Cuenta actualmente tiene {} " + pluralidadCreditos + 
                                " con la CHEC. Los siguientes son los valores facturados: \n\n").format(cantidadCreditos)
                for i in range(cantidadCreditos):
                    respuesta = respuesta + ("Credito {} :\n" + 
                                             "- Valor Cuota del Crédito : ${}\n" + 
                                             "- Saldo anterior del Crédito: ${}\n" +  
                                             "- Valor Intereses de Crédito: ${}\n" + 
                                             "- Saldo Anterior de Intereses: ${}\n"
                                            ).format(i+1, conceptoCreditos[i][0], 
                                                     conceptoCreditos[i][1],
                                                    conceptoCreditosIntereses[i][0],
                                                    conceptoCreditosIntereses[i][0])
            #respuesta = respuestaGeneral + respuestaEnergia
        #sys.stdout.write(consulta['Data'][0])
            #respuesta = "Los datos de Valor a Pagar asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, respuesta)
            dispatcher.utter_message(respuesta)
        else:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
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
        conexion = WebService()
        conexion.autenticacion()
        consulta = conexion.solicitud(numero_cuenta_usuario, "Credito")
        if consulta["IsOk"]:
            cantidadCreditosActivos = 0
            for credito in consulta['Data']:
                if credito['Estado'] == 'Activo':
                    cantidadCreditosActivos += 1
            if cantidadCreditosActivos:
                if cantidadCreditosActivos == 1:
                    pluralidadCreditos = "Cŕedito Activo"
                else:
                    pluralidadCreditos = "Cŕeditos Activos"
                respuesta = ("La cuenta de Energía {} tiene {} " + pluralidadCreditos).format(numero_cuenta_usuario, cantidadCreditosActivos)
                dispatcher.utter_message(respuesta)
                creditosActivos = 0
                for credito in consulta['Data']:
                    if credito['Estado'] == 'Activo':
                        creditosActivos += 1
                        respuesta = ("Crédito Número {} :\n\t" +
                            "- Fecha del Crédito: {}\n\t" +  
                            "- Valor del Crédito: {}\n\t" +
                            "- Número de Cuotas: {}\n").format(creditosActivos, 
                                                     credito['Fecha'],
                                                     int(credito['Valor']),
                                                     int(credito['NumeroCuotas'])
                        )
                        #sys.stdout.write(json.loads(credito))
                        print(credito)
                        dispatcher.utter_message(respuesta)
                    else:
                        respuesta = "No hay Créditos activos Asociados su cuenta {}".format(numero_cuenta_usuario)
        else:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
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
        
        respuesta = "Los datos de Informacion de Pagos asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
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
        
        respuesta = "Los datos de PQRs asociados a la cuenta {} son:\n{}".format(numero_cuenta_usuario, consulta['Data'])
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
    
    
