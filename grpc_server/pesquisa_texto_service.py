import grpc
import pesquisa_texto_service_pb2
import pesquisa_texto_service_pb2_grpc
from lxml import etree
from settings import MEDIA_PATH

class PesquisaTextoService(pesquisa_texto_service_pb2_grpc.PesquisaTextoServiceServicer):
    def __init__(self):
        self.xml_file_path = f"{MEDIA_PATH}/uploaded_file.xml"

    def BuscarTexto(self, request, context):
        termo = request.termo
        resultados = self.pesquisar_xml(termo)
        return pesquisa_texto_service_pb2.BuscaResponse(resultados=resultados)

    def pesquisar_xml(self, termo):
        resultados = []
        try:
            # Use iterparse para processar o XML de forma eficiente
            context = etree.iterparse(self.xml_file_path, events=("start", "end"))
            for event, elem in context:
                if event == "end":  # Apenas processa os elementos completos
                    if elem.text and termo.lower() in elem.text.lower():
                        resultados.append(elem.tag)
                    # Libera memória do elemento após o processamento
                    elem.clear()

        except etree.XMLSyntaxError as e:
            print(f"Erro ao processar o XML: {e}")
        except FileNotFoundError:
            print(f"Arquivo XML não encontrado: {self.xml_file_path}")

        return resultados
