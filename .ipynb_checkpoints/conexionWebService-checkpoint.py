import requests
from requests.auth import HTTPDigestAuth
import json
import jwt
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
        urlSolicitud =  "https://checaliadoscomerciales.chec.com.co/api/" + tipoTransaccion + "/GetId?id=" + cuenta
        headers = {'Authorization' : self.token}
        respuesta = requests.get(urlSolicitud, headers=headers)
        return json.loads(respuesta.text)            
             #= "https://checaliadoscomerciales.chec.com.co/api/CupoTarjeta/GetId?id=107558968"
        
    def datosCliente(self, cuenta):
        """ Consulta información general del Cliente 
            
        Args: 
                cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'Cliente'
        return json.loads(self.solicitud(cuenta, transaccion))
        
    def consumos(self, cuenta):
        """ Consulta información de Consumo del Cliente 
            
        Args: 
            cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'Consumo'
        return json.loads(self.solicitud(cuenta, transaccion))
        
    def creditos(self, cuenta):
        """ Consulta información de Creditos del Cliente 
            
        Args: 
            cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'Credito'
        return self.solicitud(cuenta, transaccion)
        
    def cupoTarjeta(self, cuenta):
        """ Consulta el Cupo PFS de Cliente 
            
        Args: 
            cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'CupoTarjeta'
        return self.solicitud(cuenta, transaccion)
        
    def DatosTransformador(self, cuenta):
        """ Consulta el Cupo PFS de Cliente 
            
        Args: 
            cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'DatosTransformador'
        return self.solicitud(cuenta, transaccion)
        
    def DetalleUltFactura(self, cuenta):
        """ Consulta el Cupo PFS de Cliente 
            
        Args: 
            cuenta (str): la cuenta a consultar
        """
        self.cuenta = cuenta
        transaccion = 'DetalleUltFactura'
        return self.solicitud(cuenta, transaccion)