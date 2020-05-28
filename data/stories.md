## busqueda solicitud datos cuenta
* saludo
  - utter_saludo
* solicitud_datos_cuenta{"numero_cuenta": 101177447}
  - accion_obtener_datos_usuario
* despedida
  - utter_despedida

## busqueda solicitud datos cuenta + pedir cuenta
* saludo
  - utter_saludo
* solicitud_datos_cuenta
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_obtener_datos_usuario
* despedida
  - utter_despedida

## Reclamos + pedir cuenta
* saludo
  - utter_saludo
* reclamo_valor_factura{"costo": false}
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_alto_costo
* despedida
  - utter_despedida

## Reclamos
* saludo
  - utter_saludo
* reclamo_valor_factura{"numero_cuenta": 101177242, "costo": false}
  - accion_alto_costo
* despedida
  - utter_despedida

## informacion factura + valor a pagar + pedir cuenta
* saludo
  - utter_saludo
* explicacion_factura
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_valor_a_pagar
* despedida
  - utter_despedida

## informacion factura + valor a pagar
* saludo
  - utter_saludo
* explicacion_factura{"numero_cuenta": 101177242}
  - accion_valor_a_pagar
* despedida
  - utter_despedida

## informacion financiaciones Productos + pedir cuenta
* saludo
  - utter_saludo
* explicacion_financiaciones{"financiacion": "credito"}
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_financiacion_productos
* despedida
  - utter_despedida

## informacion financiaciones Productos
* saludo
  - utter_saludo
* explicacion_financiaciones{"numero_cuenta": 101177242, "financiacion": "credito"}
  - accion_financiacion_productos
* despedida
  - utter_despedida

## informacion de pagos + pedir cuenta
* saludo
  - utter_saludo
* pagos_realizados{"pago": "cancelado"} 
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_informacion_pagos
* despedida
  - utter_despedida

## informacion de pagos
* saludo
  - utter_saludo
* pagos_realizados{"numero_cuenta": 101177242, "pago": "cancelado"}
  - accion_informacion_pagos
* despedida
  - utter_despedida

## informacion de pqrs + pedir cuenta
* saludo
  - utter_saludo
* informacion_pqrs_interpuestos{"pqr": "queja"} 
  - utter_pedir_cuenta
* cuenta{"numero_cuenta": 101177242}
  - accion_informacion_pqrs
* despedida
  - utter_despedida

## informacion de pqrs
* saludo
  - utter_saludo
* informacion_pqrs_interpuestos{"numero_cuenta": 101177242, "pqr": "queja"}
  - accion_informacion_pqrs
* despedida
  - utter_despedida
