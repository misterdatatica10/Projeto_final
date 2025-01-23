import grpc
from lxml import etree
import validate_schema_service_pb2
import validate_schema_service_pb2_grpc
from settings import MEDIA_PATH  # Caminho configurado para o XML armazenado

class ValidateSchemaService(validate_schema_service_pb2_grpc.ValidateSchemaServiceServicer):
    def __init__(self):
        # Define o caminho completo do arquivo XML no volume configurado
        self.xml_file_path = f"{MEDIA_PATH}/uploaded_file.xml"

    def Validate(self, request, context):
        try:
            # Verifica se o arquivo XML existe
            with open(self.xml_file_path, 'rb') as xml_file:  # Leitura em modo binário
                xml_content = xml_file.read()  # Lê o conteúdo do arquivo XML como bytes

            # Parseia o XSD fornecido pelo cliente
            try:
                # Certifique-se de que o XSD está em bytes
                xsd_content = request.xsd_content.encode('utf-8') if isinstance(request.xsd_content, str) else request.xsd_content
                xsd_root = etree.XML(xsd_content)
                schema = etree.XMLSchema(xsd_root)  # Cria o objeto schema a partir do XSD fornecido
            except etree.XMLSyntaxError as e:
                return validate_schema_service_pb2.ValidateSchemaResponse(
                    is_valid=False,
                    error_message=f"Erro ao processar o schema XSD: {e}"
                )

            # Remover a declaração XML se estiver presente
            if xml_content.startswith(b"<?xml"):
                xml_content = xml_content.split(b"\n", 1)[1]  # Remove a primeira linha (declaracao XML)

            # Parseia o XML carregado
            try:
                xml_doc = etree.XML(xml_content)  # Passa os bytes do XML para o parser
            except etree.XMLSyntaxError as e:
                return validate_schema_service_pb2.ValidateSchemaResponse(
                    is_valid=False,
                    error_message=f"Erro ao processar o XML: {e}"
                )

            # Valida o XML contra o schema
            if schema.validate(xml_doc):  # Se o XML for válido
                return validate_schema_service_pb2.ValidateSchemaResponse(
                    is_valid=True,
                    error_message=""
                )

            # Caso o XML não seja válido, retorna os erros de validação
            error_messages = "\n".join(str(error) for error in schema.error_log)
            return validate_schema_service_pb2.ValidateSchemaResponse(
                is_valid=False,
                error_message=error_messages
            )

        except FileNotFoundError:
            return validate_schema_service_pb2.ValidateSchemaResponse(
                is_valid=False,
                error_message=f"Arquivo XML não encontrado: {self.xml_file_path}"
            )
        except Exception as e:
            return validate_schema_service_pb2.ValidateSchemaResponse(
                is_valid=False,
                error_message=f"Erro desconhecido: {e}"
            )
