import grpc
import time
import threading
from concurrent import futures
import greet_pb2
import greet_pb2_grpc
import sqlite3

class PythonGrpcClient:
    def __init__(self, server_address='100.125.170.91:7031'):
        # Create insecure channel (for HTTP) or secure channel
        self.channel = grpc.insecure_channel(server_address)
        self.stub = greet_pb2_grpc.GreeterStub(self.channel)
    
    def secure_stream_example(self, cert_path=None):
        """Example with SSL/TLS (if server uses HTTPS)"""
        print("\n=== Secure Streaming (TLS) ===\n")
        
        # For HTTPS/SSL, you need to create a secure channel
        if cert_path:
            # Read certificate file
            with open(cert_path, 'rb') as f:
                trusted_certs = f.read()
            
            credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs
            )
            channel = grpc.secure_channel(
                '100.125.170.91:7031',
                credentials
            )
        else:
            # For testing with self-signed certs (insecure)
            channel = grpc.insecure_channel('100.125.170.91:5106')
        
        stub = greet_pb2_grpc.GreeterStub(channel)

        def message_generator():
            data = test()
            messages = [create_protobuf_message(dict) for dict in data]
            
            for message in messages:
                print(f"Sending: {message}")
                yield message
                time.sleep(0.5)  # Optional delay
        
        response = stub.StreamFromClientSayHello(message_generator())
        
        print(f"\nServer response: {response.message}")
        return response

def test():
    conn = sqlite3.connect('tv-shows.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv_show_episodes")
    episodes = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return episodes

def create_protobuf_message(data_dict):
    request = greet_pb2.HelloRequest1()
    
    # Map and set fields
    request.tv_show_name = data_dict.get('t_name', '')
    request.tv_show_year = data_dict.get('t_year', 0)
    request.episode_name = data_dict.get('e_name', '')
    request.episode_season = data_dict.get('e_season', 0)
    request.episode_number = data_dict.get('e_number', 0)
    request.character_name = data_dict.get('c_name', '')
    request.actor_name = data_dict.get('a_name', '')
    
    return request

def main():
    client = PythonGrpcClient('100.125.170.91:7031')
    client.secure_stream_example('cert.pem') # 'C:\\certs\\certificate.crt'

if __name__ == "__main__":
    main()