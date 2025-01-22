import os
import csv
import xml.etree.ElementTree as ET
import grpc
import csv_to_xml_service_pb2
import csv_to_xml_service_pb2_grpc
from settings import MEDIA_PATH

class CsvToXmlService(csv_to_xml_service_pb2_grpc.CsvToXmlServiceServicer):
    def ConvertCsvToXmlAndSave(self, request, context):
        # Caminho completo do arquivo CSV
        csv_file_path = os.path.join(MEDIA_PATH, request.file_name)
        if not os.path.exists(csv_file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("CSV file not found.")
            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(success=False, message="CSV file not found.")

        try:
            # Nome do arquivo XML
            xml_file_name = request.file_name.replace(".csv", ".xml")
            xml_file_path = os.path.join(MEDIA_PATH, xml_file_name)

            # Processamento em streaming
            with open(csv_file_path, "r") as csv_file, open(xml_file_path, "wb") as xml_file:
                reader = csv.DictReader(csv_file)
                
                # Criar o elemento raiz e gravar o cabeçalho do XML
                root = ET.Element("root")
                xml_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<root>\n')
                
                # Escrever linhas do CSV como elementos XML
                for row in reader:
                    row_element = ET.Element("row")
                    for key, value in row.items():
                        child = ET.SubElement(row_element, key)
                        child.text = value
                    
                    # Gravando a linha diretamente no arquivo para evitar sobrecarga na memória
                    xml_file.write(ET.tostring(row_element, encoding="utf-8") + b'\n')
                
                # Fechar o elemento raiz
                xml_file.write(b'</root>\n')

            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(
                success=True,
                message=f"XML file saved at {xml_file_path}."
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to convert CSV to XML: {str(e)}")
            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(success=False, message=str(e))
