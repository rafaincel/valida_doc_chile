import aiohttp

from .consulta import API_URL, _parse_response


async def async_query(run: str, doc_num: str, doc_type: str, api_key: str = None) -> str:
    """Consulta asíncrona del estado de vigencia de un documento de identidad."""
    data = {
        "run": run,
        "serial_number": doc_num,
        "doc_type": doc_type,
    }
    headers = {}
    if api_key is not None:
        headers["X-Token"] = api_key

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=data, headers=headers) as response:
            body = await response.text()
            return _parse_response(body, response.status)
