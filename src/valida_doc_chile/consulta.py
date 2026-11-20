import json
from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.request import Request, urlopen


API_URL = "https://regcivil.impish.top/v1/query"
VALID_STATES = {"VALID", "NOT_VALID", "NO_MATCH"}


def _parse_response(body: str, status_code: int = 200) -> str:
    json_data = json.loads(body)
    if not isinstance(json_data, dict):
        raise RuntimeError("API returned an invalid response")

    if not 200 <= status_code < 300 or json_data.get("error"):
        message = json_data.get("message") or json_data.get("detail")
        if not isinstance(message, str):
            message = json.dumps(message) if message is not None else "Unknown API error"
        raise RuntimeError(f"API request failed (HTTP {status_code}): {message}")

    state = json_data.get("status")
    if not isinstance(state, str) or state not in VALID_STATES:
        raise RuntimeError("API returned an unknown document status")
    return state


def query(run: str, doc_num: str, doc_type: str, api_key: str = None) -> str:
    """Consulta el estado de vigencia de un documento de identidad.

    :param run: Identificador de la persona (ej. "98765432-K")
    :type run: str
    :param doc_num: Número del documento (ej. "12345678")
    :type doc_num: str
    :param doc_type: Tipo de documento: CEDULA o PASAPORTE
    :type doc_type: str
    :param api_key: Token de acceso enviado en el encabezado X-Token
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
        "serial_number": doc_num,
        "doc_type": doc_type,
    }
    req = Request(
        API_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if api_key is not None:
        req.add_header("X-Token", api_key)

    try:
        with urlopen(req) as response:
            res = response.read().decode("utf-8")
    except HTTPError as e:
        res = e.read().decode("utf-8")
        return _parse_response(res, e.code)

    return _parse_response(res)


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
        "NO_MATCH": ("No se encuentra coincidencia / el documento no existe.", 2),
    }

    msg, ec = state_messages[state]

    print(msg)
    exit(ec)


if __name__ == '__main__':
    main()
