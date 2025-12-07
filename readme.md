using python venv
1 create
python -m venv .venv
2 activate
.\.venv\Scripts\Activate.ps1
3 install from req
pip install -r requirements.txt

4 capture packages
pip freeze > requirements.txt

5 generate grpc code
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greet.proto

cert
1 create cert.pem and key.pem
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "//CN=localhost" -addext "subjectAltName=DNS:localhost"

2 pfx
openssl pkcs12 -export -out certificate.pfx -inkey key.pem -in cert.pem

3 pfx for c#, cert for py