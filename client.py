import configparser
import grpc
import time
import greet_pb2
import greet_pb2_grpc
import sqlite3

class PythonGrpcClient:
    def secure_stream_example(self, cert_path=None):
        """Example with SSL/TLS (if server uses HTTPS)"""
        print("\n=== Secure Streaming (TLS) ===\n")
        config = configparser.ConfigParser()
        config.read("settings.ini")
        
        # For HTTPS/SSL, you need to create a secure channel
        if cert_path:
            # Read certificate file
            with open(cert_path, 'rb') as f:
                trusted_certs = f.read()
            
            credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs
            )
            channel = grpc.secure_channel(
                config["service"]["target"],
                credentials
            )
        else:
            # For testing with self-signed certs (insecure)
            channel = grpc.insecure_channel(config["service"]["insecure_target"])
        
        stub = greet_pb2_grpc.GreeterStub(channel)

        def message_generator():
            data = test()
            messages = [create_protobuf_message(dict) for dict in data]
            
            for message in messages:
                print(f"Sending: {message}")
                yield message
                time.sleep(2)  # Optional delay
        
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
    client = PythonGrpcClient()
    client.secure_stream_example('cert.pem') # 'cert.pem'

if __name__ == "__main__":
    main()