import grpc
import pesquisa_texto_service_pb2
import pesquisa_texto_service_pb2_grpc
import xml.etree.ElementTree as ET
from settings import MEDIA_PATH  # Importa o caminho do diretório MEDIA_PATH

class PesquisaTextoService(pesquisa_texto_service_pb2_grpc.PesquisaTextoServiceServicer):
    def __init__(self):
        # Define o caminho completo do arquivo XML no volume configurado
        self.xml_file_path = f"{MEDIA_PATH}/uploaded_file.xml"

    def BuscarTexto(self, request, context):
        termo = request.termo
        resultados = self.pesquisar_xml(termo)
        return pesquisa_texto_service_pb2.BuscaResponse(resultados=resultados)

    def pesquisar_xml(self, termo):
        resultados = []
        try:
            # Faz o parsing do XML usando o caminho dinâmico configurado
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()

            # Pesquisa no XML por elementos contendo o texto especificado
            for elem in root.iter():
                if termo.lower() in elem.text.lower() if elem.text else "":
                    resultados.append(elem.tag)

        except ET.ParseError as e:
            print(f"Erro ao processar o XML: {e}")
        except FileNotFoundError:
            print(f"Arquivo XML não encontrado: {self.xml_file_path}")

        return resultados
