import os
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom  # Adicionado para formatar o XML
import grpc
import csv_to_xml_service_pb2
import csv_to_xml_service_pb2_grpc
from settings import MEDIA_PATH

class CsvToXmlService(csv_to_xml_service_pb2_grpc.CsvToXmlServiceServicer):
    def ConvertCsvToXmlAndSave(self, request, context):
        # Caminho completo do arquivo CSV no volume
        csv_file_path = os.path.join(MEDIA_PATH, request.file_name)
        if not os.path.exists(csv_file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("CSV file not found.")
            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(success=False, message="CSV file not found.")

        try:
            # Converte o CSV para XML
            root = ET.Element("root")
            with open(csv_file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    row_element = ET.SubElement(root, "row")
                    for key, value in row.items():
                        child = ET.SubElement(row_element, key)
                        child.text = value

            # Nome do arquivo XML
            xml_file_name = request.file_name.replace(".csv", ".xml")
            xml_file_path = os.path.join(MEDIA_PATH, xml_file_name)

            # Formata o XML para uma estrutura bem indentada
            rough_string = ET.tostring(root, encoding="utf-8")
            reparsed = minidom.parseString(rough_string)
            pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

            # Salva o XML no volume
            with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                xml_file.write(pretty_xml_as_string)

            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(
                success=True,
                message=f"XML file saved at {xml_file_path}."
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to convert CSV to XML: {str(e)}")
            return csv_to_xml_service_pb2.ConvertCsvToXmlAndSaveResponse(success=False, message=str(e))
