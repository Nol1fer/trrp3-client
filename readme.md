using python venv
1 create
python -m venv .venv
2 activate
.\.venv\Scripts\Activate.ps1
3 install from req
pip install -r requirements.txt

4 capture packages
pip freeze > requirements.txt

generate grpc code

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greet.proto