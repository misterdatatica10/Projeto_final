import grpc
import filtros_service_pb2
import filtros_service_pb2_grpc
from lxml import etree
from settings import MEDIA_PATH  # Caminho configurado no projeto

class FiltrosService(filtros_service_pb2_grpc.FiltrosServiceServicer):
    def __init__(self):
        # Define o caminho completo do arquivo XML no volume configurado
        self.xml_file_path = f"{MEDIA_PATH}/uploaded_file.xml"

    def ConsultarComFiltros(self, request, context):
        query = request.xpath_query
        resultados = self.consultar_com_xpath(query)
        return filtros_service_pb2.FiltrosResponse(resultados=resultados)

    def consultar_com_xpath(self, query):
        resultados = []
        try:
            # Abre e processa o XML com etree.iterparse
            context = etree.iterparse(
                self.xml_file_path, events=('end',), tag='row', recover=True
            )

            for event, elem in context:
                try:
                    # Aplica a query diretamente no elemento `elem` e verifica se ele corresponde
                    if elem.xpath(query):
                        resultados.append(
                            etree.tostring(elem, pretty_print=True, encoding='unicode').strip()
                        )
                except etree.XPathError as e:
                    print(f"Erro na consulta XPath: {e}")

                # Libera memória ao limpar elementos já processados
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

        except FileNotFoundError:
            print(f"Arquivo XML não encontrado: {self.xml_file_path}")
        except etree.XMLSyntaxError as e:
            print(f"Erro de sintaxe no XML: {e}")

        return resultados