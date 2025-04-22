"""
A partir d'une clé encodée en base 64 :
$ cat API_TOKEN_FILE | base64 -d > service_account_credentials.json

Modifier dans ce fichier les variables d'environnement
avec les valeurs corespondant à l'application

Puis gérérer un token avec :
$ python gen_jwt_from_service_account.py

Pour voir le contenu d'un token :
Aller voir sur https://jwt.io
"""

import io
import json
import os
import time

from google.auth import crypt
from google.auth import jwt

## Chemin du fichier contenant les credentials GCP
GCP_CREDENTIALS_FILE_PATH = "folder/service_account.json"

# AUDIENCE = URL de l'API
# If you use cloud endpoints for you API, you can take the x-google-audiences value in your security definitions.
AUDIENCE = "https://app_name.api.host.com"

# Expiry time for your JWT token
DUREE_VALIDITE_TOKEN_SEC = 1 * 3600


def get_jwt_params():
    # Service account key path
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_CREDENTIALS_FILE_PATH

    # Get service account email and load the json data from the service account key file.
    with io.open(GCP_CREDENTIALS_FILE_PATH, "r", encoding="utf-8") as json_file:
        data = json.loads(json_file.read())
        sa_email = data['client_email']

    return {
        "sa_keyfile": GCP_CREDENTIALS_FILE_PATH,
        "sa_email": sa_email,
        "audience": AUDIENCE,
        "expiry_length": DUREE_VALIDITE_TOKEN_SEC,
    }


def generate_jwt(sa_keyfile, sa_email, audience, expiry_length=1000):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud': audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt_token = jwt.encode(signer, payload)
    return jwt_token


if __name__ == '__main__':
    jwt_params = get_jwt_params()
    signed_jwt = generate_jwt(**jwt_params)
    print(signed_jwt)
