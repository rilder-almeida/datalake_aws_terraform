import zipfile
import requests
from io import BytesIO
import os

base_path = "/opt/ml/processing/output"
censo_path = f"{base_path}/censoescolar"

if __name__ == "__main__":

    os.makedirs(censo_path, exist_ok=True)

    url = "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2020.zip"
    filebytes = BytesIO(requests.get(url, stream=True).content)

    myzip = zipfile.ZipFile(filebytes)
    myzip.extractall(censo_path)
