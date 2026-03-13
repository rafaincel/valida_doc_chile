#!/usr/bin/env python3
from argparse import ArgumentParser
from html import parser
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

def query(run: str, doc_num: str, doc_type: str, api_key: str = None) -> str:
    """
    Consulta el estado de vigencia de un documento de identidad.

    :param run: Identificador de la persona (ej. "98765432-K")
    :type run: str
    :param doc_num: Número del documento (ej. "12345678")
    :type doc_num: str
    :param doc_type: Tipo de documento: CEDULA o PASAPORTE
    :type doc_type: str
    :param api_key: Clave de acceso a la API
    :type api_key: str, optional
    :return: Estado del documento.
            Valores posibles:
            - VALID: el documento está vigente.
            - NOT_VALID: el documento existe, pero no está vigente
            (vencido, bloqueado, perdido, etc.).
            - NO_MATCH: no se encuentra coincidencia o el documento no existe.
    :rtype: str
    """
        
    data = {
        "run": run,
        "doc_num": doc_num,
        "doc_type": doc_type
    }
    form_data = urlencode(data).encode("utf-8")

    req = Request("https://regcivil.impish.top/query", data=form_data, method="POST")
    if api_key is not None:
        req.add_header("X-api-key", api_key)

    try:
        with urlopen(req) as response:
            res = response.read().decode("utf-8")
    except HTTPError as e:
        res = e.read().decode("utf-8")

    json_data = json.loads(res)

    if json_data["error"]:
        raise RuntimeError(f"api falló: {json_data['error_code']}: {json_data['desc']}")

    return json_data["state"]


def main():
    parser = ArgumentParser('Verificador de RUN')
    parser.add_argument('run', help='16273463-6', type=str)
    parser.add_argument('doc_num', help='106879378', type=str)
    parser.add_argument('doc_type', help='Tipo de documento', type=str, choices=["CEDULA", "PASAPORTE"])
    args = parser.parse_args()

    state = query(args.run, args.doc_num, args.doc_type)

    state_messages = {
        "VALID": ("El documento está vigente.", 0),
        "NOT_VALID": ("El documento existe, pero no está vigente.", 1),
        "NO_MATCH": ("No se encuentra coincidencia / el documento no existe.", 2)
    }

    msg, ec = state_messages[state]

    print(msg)
    exit(ec)

if __name__ == '__main__':
    main
