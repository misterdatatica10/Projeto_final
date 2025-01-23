from concurrent import futures
import grpc
import send_file_service
import file_conversion_service
import csv_to_xml_service
import file_upload_service
import pesquisa_texto_service
import filtros_service  # Importa o novo serviço de filtros
import server_services_pb2_grpc
import file_conversion_service_pb2_grpc
import csv_to_xml_service_pb2_grpc
import file_upload_service_pb2_grpc
import pesquisa_texto_service_pb2_grpc
import filtros_service_pb2_grpc  # Importa os stubs gRPC gerados
import validate_schema_service  # Importa o novo serviço de validação
import validate_schema_service_pb2_grpc  # Importa os stubs gRPC gerados para o serviço de validação
from settings import GRPC_SERVER_PORT, MAX_WORKERS

def serve():
    # Cria o servidor gRPC
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAX_WORKERS),
        options=[
            ('grpc.max_receive_message_length', 200 * 1024 * 1024),  # 200 MB
            ('grpc.max_send_message_length', 200 * 1024 * 1024)      # 200 MB
        ]
    )

    # Registra os serviços
    server_services_pb2_grpc.add_SendFileServiceServicer_to_server(
        send_file_service.SendFileService(), server
    )
    file_conversion_service_pb2_grpc.add_FileConversionServiceServicer_to_server(
        file_conversion_service.FileConversionService(), server
    )
    csv_to_xml_service_pb2_grpc.add_CsvToXmlServiceServicer_to_server(
        csv_to_xml_service.CsvToXmlService(), server
    )
    file_upload_service_pb2_grpc.add_FileUploadServiceServicer_to_server(
        file_upload_service.FileUploadService(), server
    )
    pesquisa_texto_service_pb2_grpc.add_PesquisaTextoServiceServicer_to_server(
        pesquisa_texto_service.PesquisaTextoService(), server
    )
    filtros_service_pb2_grpc.add_FiltrosServiceServicer_to_server(
        filtros_service.FiltrosService(), server
    )

    # Registra o ValidateSchemaService
    validate_schema_service_pb2_grpc.add_ValidateSchemaServiceServicer_to_server(
        validate_schema_service.ValidateSchemaService(), server
    )

    # Inicia o servidor
    server.add_insecure_port(f'[::]:{GRPC_SERVER_PORT}')
    print(f"gRPC server running on port {GRPC_SERVER_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
