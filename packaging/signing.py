"""Create a dedicated Android publishing identity; never print private material."""
import base64,datetime,secrets,subprocess
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
root=Path(__file__).resolve().parents[1];folder=root/'.signing';folder.mkdir(exist_ok=True)
keyfile=folder/'marco-video.p12';passwordfile=folder/'password.txt'
if not keyfile.exists():
    password=secrets.token_urlsafe(40);key=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Marco Vídeo - Marco Pescador')]);now=datetime.datetime.now(datetime.timezone.utc)
    cert=x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(days=1)).not_valid_after(now+datetime.timedelta(days=365*30)).sign(key,hashes.SHA256())
    keyfile.write_bytes(pkcs12.serialize_key_and_certificates(b'marco-video',key,cert,None,serialization.BestAvailableEncryption(password.encode())))
    passwordfile.write_text(password,encoding='utf-8')
gh='D:/PROGRAMAS/tools/gh/bin/gh.exe'
for name,data in [('ANDROID_KEYSTORE',base64.b64encode(keyfile.read_bytes())),('ANDROID_KEY_PASSWORD',passwordfile.read_bytes())]:
    subprocess.run([gh,'secret','set',name,'--repo','Peskysa/marco-video'],input=data,check=True)
print('Firma propia de Marco Vídeo preparada; copia privada excluida de Git y secretos guardados.')
