from concurrent import futures
import grpc
import send_file_service
import file_conversion_service
import csv_to_xml_service
import csv_to_xml_service_pb2_grpc
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

    # Registra o CsvToXmlService
    csv_to_xml_service_pb2_grpc.add_CsvToXmlServiceServicer_to_server(
        csv_to_xml_service.CsvToXmlService(), server
    )

    # Inicia o servidor
    server.add_insecure_port(f'[::]:{GRPC_SERVER_PORT}')
    print(f"gRPC server running on port {GRPC_SERVER_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
