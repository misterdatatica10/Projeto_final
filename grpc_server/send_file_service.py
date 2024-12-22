import os
import server_services_pb2
import server_services_pb2_grpc
from settings import MEDIA_PATH

class SendFileService(server_services_pb2_grpc.SendFileServiceServicer):
    def __init__(self, *args, **kwargs):
        pass

    def SendFile(self, request, context):
        # Cria o diretório de armazenamento se não existir
        os.makedirs(MEDIA_PATH, exist_ok=True)
        
        # Define o caminho do arquivo com base no nome do arquivo e MIME
        file_path = os.path.join(MEDIA_PATH, request.file_name + request.file_mime)

        # Salva o arquivo recebido no diretório
        ficheiro_em_bytes = request.file
        with open(file_path, 'wb') as f:
            f.write(ficheiro_em_bytes)

        # Retorna a resposta conforme o definido no proto
        return server_services_pb2.SendFileResponseBody(success=True)