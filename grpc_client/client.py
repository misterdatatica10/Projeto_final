import grpc
import send_file_service_pb2
import send_file_service_pb2_grpc

def generate_chunks(file_path, chunk_size=1024):
    """Função geradora que lê o arquivo em chunks."""
    with open(file_path, 'rb') as f:
        while True:
            content = f.read(chunk_size)
            if not content:  # Quando acabar o arquivo, encerra
                break
            yield send_file_service_pb2.FileChunk(
                file_name=file_path.split('/')[-1],  # Envia o nome do arquivo no primeiro chunk
                content=content
            )

def main():
    # Conecta ao servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')  # Altere o endereço conforme necessário
    stub = send_file_service_pb2_grpc.FileUploadServiceStub(channel)

    # Caminho do arquivo CSV que será enviado
    file_path = 'car_prices.csv'

    # Envia o arquivo como streaming
    try:
        response = stub.UploadFile(generate_chunks(file_path))
        print(f"Response from server: {response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.details()} (code: {e.code()})")

if __name__ == '__main__':
    main()