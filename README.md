
# valida_doc_chile

Librería en Python para validar la vigencia de documentos de identidad chilenos (cédula y pasaporte) usando la API pública de [regcivil.impish.top](https://regcivil.impish.top/).

## Instalación

```bash
pip install valida-doc-chile
```

## Requisitos

- Python >= 3.2

## Uso desde Python

```python
from valida_doc_chile import query

estado = query("16273463-6", "106879378", "CEDULA")
print(estado)  # "VALID", "NOT_VALID" o "NO_MATCH"
```

### Parámetros

- `run`: string, RUT con guión (ej. "16273463-6").
- `doc_num`: string, número de documento o número de serie.
- `doc_type`: string, `CEDULA` o `PASAPORTE`.
- `api_key` (opcional): string para usar la API con mayor frecuencia.

### Retorno

La función `query(...)` retorna un string con uno de los siguientes valores:

- `VALID`: el documento está vigente.
- `NOT_VALID`: el documento existe, pero no está vigente (vencido, bloqueado, perdido, etc.).
- `NO_MATCH`: no se encuentra coincidencia o el documento no existe.

## Uso desde la línea de comandos

Al instalar el paquete, se agrega el comando `valcl` al entorno.
```bash
$ valcl --help
usage: Verificador de RUN [-h] run doc_num {CEDULA,PASAPORTE}

positional arguments:
  run                 16273463-6
  doc_num             106879378
  {CEDULA,PASAPORTE}  Tipo de documento

options:
  -h, --help          show this help message and exit
```

```bash
$ valcl 16273463-6 106879378 CEDULA
El documento existe, pero no está vigente.
$ echo $?
1
```

### Mensajes y códigos de salida

| respuesta API | mensaje impreso                                     | exit code |
| ------------- | -------------------------------------------------- | --------- |
| `VALID`       | El documento está vigente.                          | `0`       |
| `NOT_VALID`   | El documento existe, pero no está vigente.          | `1`       |
| `NO_MATCH`    | No se encuentra coincidencia / el documento no existe. | `2`       |

## Más información

Esta librería usa la API gratuita de consulta de documentos proporcionada por [regcivil.impish.top](https://regcivil.impish.top/).
