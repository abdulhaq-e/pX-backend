from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


def get_public_key():
    f = open('cert.cer', 'rb')
    cert_obj = load_pem_x509_certificate(f.read(), default_backend())
    public_key = cert_obj.public_key()

    return public_key


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    print "hi"
    print payload.get('upn')
    return payload.get('upn')