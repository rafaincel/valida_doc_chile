# requisitos
- python >= 3.2

# dependencias
este proyecto no tiene ninguna dependencia externa.

# como usar
`consulta.py` contiene la función que consulta la vigencia de la cédula o del pasaporte. si se ejecuta este por si mismo, tambien es posible validar documentos directamente desde la consola.

## validar por codigo python
se importa la función `query` de tal manera : `from consulta import query`. luego, se puede llamar la función de la siguiente manera: `query(run, doc_number, doc_type)` donde
- run: string, rol unico nacional sin puntos, con guión.
- doc_number: string, número del documento / numero de serie.
- doc_type: string, `CEDULA` o `PASAPORTE`.
- api_key: opcional, string. para chequeos mas frecuentes y agresivos.

### retorno
la función retorna el string `VALID` si el documento está vigente. si no, se retorna `NO_MATCH` o `NOT_VALID`.

### ejemplo de consulta por codigo
existe un [codigo ejemplo](ejemplo.py) practico que hace implementa esta función rapidamente.
    
## validar por consola
al ejecutar `python consulta.py --help` o `chmod +x consulta.py && ./consulta.py --help` se explica el funcionamiento:

```
$ python consulta.py --help
usage: Verificador de RUN [-h] run doc_num {CEDULA,PASAPORTE}

positional arguments:
  run                 16273463-6
  doc_num             106879378
  {CEDULA,PASAPORTE}  Tipo de documento

options:
  -h, --help          show this help message and exit
```

### codigos de salida (exit codes)


| respuesta api | texto impreso | exit code |
| ---------------- | ------------------------------------------------------ | --------- |
| `VALID`          | El documento está vigente.                             | `0`       |
| `NOT_VALID`      | El documento existe, pero no está vigente.             | `1`       |
| `NO_MATCH`       | No se encuentra coincidencia / el documento no existe. | `2`       |

    
### ejemplo de consulta por comando de linea
```
$ python consulta.py 16273463-6 106879378 CEDULA
El documento existe, pero no está vigente.
$ echo $?
1
```

# más informacion
esta api hace uso de la api gratuita de consulta de documentos [regcivil.impish.top](https://regcivil.impish.top/)
