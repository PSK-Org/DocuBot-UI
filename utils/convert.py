import requests
import asyncio
from pdfrw import PdfReader, PdfWriter
from io import BytesIO

async def convert(filePath, format, file):
    """
    Send a PDF to the Windows server to be converted to a different format.
    :param filePath: The path to the file to convert.
    :param format: The format to convert the file to. (iml | kml | tex | mathml | hrtex)
    :return: The converted file as a bytestring.
    """

    if format not in ("iml", "kml", "tex", "mathml", "hrtex"):
        raise ValueError("Invalid format.")

    url = "https://windows.samiyousef.ca"

    headers = {"authorization": "1dfdd271-159a-414c-a947-a5d31dd6ffac"}

    if file is None:
        file = open(filePath, "rb").read()

    response = requests.post(f"{url}/uploadPDF/{format}",
                             data=file,
                             headers={"authorization": "1dfdd271-159a-414c-a947-a5d31dd6ffac", "Content-Type": "application/octet-stream"})

    if response.status_code != 200:
        print(response.text)
        raise ValueError("Invalid response from server.")

    id = response.text

    print("Conversion started. Received ID:", id)

    print("Checking for completion")
    while True:
        success_check = requests.get(f"{url}/files/{id}/{id}.{format}", headers=headers)
        failure_check = requests.get(f"{url}/files/{id}/error", headers=headers)

        if success_check.status_code == 200:
            print(success_check)
            return success_check.content
        elif failure_check.status_code == 200:
            raise ValueError(f"❌ Conversion failed: {failure_check.text}.")

        print(".", end="", flush=True)
        await asyncio.sleep(2)
