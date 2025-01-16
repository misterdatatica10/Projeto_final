import os
import file_upload_service_pb2_grpc
from file_upload_service_pb2 import UploadStatus
from settings import MEDIA_PATH  # Importe a variável MEDIA_PATH

class FileUploadService(file_upload_service_pb2_grpc.FileUploadServiceServicer):
    def __init__(self):
        # Cria o diretório se não existir
        os.makedirs(MEDIA_PATH, exist_ok=True)

    def UploadFile(self, request_iterator, context):
        try:
            file_name = None
            file_path = None

            # Abrir o arquivo para escrita imediatamente
            with open(os.path.join(MEDIA_PATH, "uploaded_file.csv"), 'wb') as f:
                first_chunk = True  # Flag para garantir que processamos o primeiro chunk

                for chunk in request_iterator:
                    # No primeiro chunk, defina o nome do arquivo
                    if first_chunk:
                        if chunk.file_name:
                            file_name = chunk.file_name  # Atribui o nome do arquivo
                            file_path = os.path.join(MEDIA_PATH, file_name)  # Define o caminho completo
                        else:
                            file_name = "uploaded_file.csv"  # Caso não tenha nome no primeiro chunk
                            file_path = os.path.join(MEDIA_PATH, file_name)
                        first_chunk = False  # Marca que o primeiro chunk foi processado

                    # Agora, escreva os dados no arquivo, incluindo quebras de linha (se necessário)
                    f.write(chunk.content + b'\n')

            # Retorna sucesso e o caminho do arquivo
            if not file_path:
                file_path = os.path.join(MEDIA_PATH, "uploaded_file.csv")

            print(f"File uploaded successfully to {file_path}")  # Log para depuração
            return UploadStatus(success=True, message=f"File uploaded successfully to {file_path}")

        except Exception as e:
            print(f"Error during file upload: {str(e)}")  # Log para depuração de erro
            return UploadStatus(success=False, message=f"Failed to upload file: {str(e)}")
