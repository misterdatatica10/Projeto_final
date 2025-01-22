import grpc
import send_file_service_pb2
import send_file_service_pb2_grpc

def stream_csv(file_path):
    """Função geradora que lê o arquivo linha por linha e envia como chunks."""
    # Envia o nome do arquivo no primeiro chunk, sem conteúdo
    yield send_file_service_pb2.FileChunk(
        file_name=file_path.split('/')[-1],  # Nome do arquivo extraído do caminho
        content=b''  # Sem conteúdo no primeiro chunk
    )

    # Envia o conteúdo do arquivo linha por linha
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove a quebra de linha e codifica a linha
            yield send_file_service_pb2.FileChunk(
                file_name='',  # Nome do arquivo já enviado no primeiro chunk
                content=line.rstrip('\n').encode('utf-8')  # Remove quebra de linha antes de enviar
            )

def main():
    # Conecta ao servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')  # Altere o endereço conforme necessário
    stub = send_file_service_pb2_grpc.FileUploadServiceStub(channel)

    # Caminho do arquivo CSV que será enviado
    file_path = 'car_prices.csv'

    # Envia o arquivo como streaming
    try:
        response = stub.UploadFile(stream_csv(file_path))
        print(f"Response from server: {response.message}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e.details()} (code: {e.code()})")

if __name__ == '__main__':
    main()
