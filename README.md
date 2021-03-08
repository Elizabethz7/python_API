# first_api_python
 API con Flask

Primero ver si se tiene instalado:
    python --version
    pip --version

Instalar Flask
    pip install flask

Puerto por default -> 5000

Para utilizar servicios de AWS

AWS CLI
Herramienta unificada para administrar los productos de AWS, administrar desde la línea de comandos
    pip install awscli
https://aws.amazon.com/es/cli/

    pip install  boto3
documentacion: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation
 boto3 necesita aws cli para poner las credenciales, o se puede hacer un documento tu mismo en la carpeta aws
import boto3
from botocore.config import Config

Configuracion
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration
my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

client = boto3.client('kinesis', config=my_config)

RDS
https://docs.aws.amazon.com/es_es/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html

Requisitos
 * Autentucacion, Modificar el RDS con:
  Password and IAM database authentication (Autenticación de bases de datos con 
 * Creación y uso de una política de IAM para el acceso a bases de datos de IAM
 * Configurar las credenciales
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html, se puede hacer por un file, consola o por parametros

 import sys
import boto3
             
                

