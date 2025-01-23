import os
import grpc
import csv
import psycopg2
import file_conversion_service_pb2
import file_conversion_service_pb2_grpc
from settings import MEDIA_PATH, DBNAME, DBUSERNAME, DBPASSWORD, DBHOST, DBPORT
from datetime import datetime
import re

class FileConversionService(file_conversion_service_pb2_grpc.FileConversionServiceServicer):
    def __init__(self):
        # Inicializa a conexão com o banco de dados PostgreSQL
        self.connection = psycopg2.connect(
            dbname=DBNAME,
            user=DBUSERNAME,
            password=DBPASSWORD,
            host=DBHOST,
            port=DBPORT
        )
        self.cursor = self.connection.cursor()

        # Cria a tabela 'ficheiro_csv' no PostgreSQL com os tipos corretos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ficheiro_csv (
                id SERIAL PRIMARY KEY,
                year INTEGER,
                make VARCHAR(50),
                model VARCHAR(50),
                trim VARCHAR(50),
                body VARCHAR(50),
                transmission VARCHAR(20),
                vin VARCHAR(20),
                state VARCHAR(50),
                condition INTEGER,
                odometer INTEGER,
                color VARCHAR(30),
                interior VARCHAR(30),
                seller VARCHAR(100),
                mmr NUMERIC(10, 2),
                selling_price NUMERIC(10, 2),
                sale_date TEXT  -- Alterado de TIMESTAMP para TEXT
            );
        """)
        self.connection.commit()

    def parse_sale_date(self, sale_date):
        """
        Converte a data no formato do CSV para um objeto datetime.
        Se a data for inválida, retorna o valor como uma string.
        """
        if sale_date:
            try:
                # Remove a parte "(PST)" ou similar
                sale_date = re.sub(r'\s+\(.*\)$', '', sale_date)
                # Converte para datetime
                parsed_date = datetime.strptime(sale_date, '%a %b %d %Y %H:%M:%S GMT%z')
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')  # Retorna a data como string no formato esperado
            except ValueError:
                # Se a data for inválida, retorna a data original como texto
                return sale_date  # Pode ser armazenado como string original
        return None  # Se a data não estiver presente

    def ConvertCsvToDbAndSave(self, request, context):
        # Caminho completo do arquivo CSV no volume
        csv_file_path = os.path.join(MEDIA_PATH, request.file_name)

        if not os.path.exists(csv_file_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("CSV file not found.")
            return file_conversion_service_pb2.ConvertCsvToDbAndSaveResponse(success=False, message="CSV file not found.")

        try:
            # Abre o CSV e insere os dados na tabela 'ficheiro_csv'
            with open(csv_file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)  # Lê o CSV como um dicionário
                
                for row in reader:
                    # Converte os dados para os tipos apropriados
                    year = int(row.get('year', 0)) if row.get('year') else None
                    make = row.get('make', None)
                    model = row.get('model', None)
                    trim = row.get('trim', None)
                    body = row.get('body', None)
                    transmission = row.get('transmission', None)
                    vin = row.get('vin', None)
                    state = row.get('state', None)
                    condition = int(row.get('condition', 0)) if row.get('condition') else None
                    odometer = int(row.get('odometer', 0)) if row.get('odometer') else None
                    color = row.get('color', None)
                    interior = row.get('interior', None)
                    seller = row.get('seller', None)
                    mmr = float(row.get('mmr', 0)) if row.get('mmr') else None
                    selling_price = float(row.get('sellingprice', 0)) if row.get('sellingprice') else None
                    sale_date = self.parse_sale_date(row.get('saledate', None))

                    # Insere os dados na tabela
                    self.cursor.execute("""
                        INSERT INTO ficheiro_csv (
                            year, make, model, trim, body, transmission, vin, 
                            state, condition, odometer, color, interior, seller, 
                            mmr, selling_price, sale_date
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        year, make, model, trim, body, transmission, vin, 
                        state, condition, odometer, color, interior, seller, 
                        mmr, selling_price, sale_date
                    ))

            # Confirma a transação no banco de dados
            self.connection.commit()

            # Retorna a resposta indicando sucesso
            return file_conversion_service_pb2.ConvertCsvToDbAndSaveResponse(
                success=True,
                message="CSV data saved to database."
            )
        except Exception as e:
            # Tratamento de erro
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to convert CSV to database: {str(e)}")
            return file_conversion_service_pb2.ConvertCsvToDbAndSaveResponse(success=False, message=str(e))
