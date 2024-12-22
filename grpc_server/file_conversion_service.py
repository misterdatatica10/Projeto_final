import os
import grpc
import csv
import psycopg2
import file_conversion_service_pb2
import file_conversion_service_pb2_grpc
from settings import MEDIA_PATH, DBNAME, DBUSERNAME, DBPASSWORD, DBHOST, DBPORT

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

        # Cria a tabela 'ficheiro_csv' no PostgreSQL, se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ficheiro_csv (
                id SERIAL PRIMARY KEY,
                year TEXT,
                make TEXT,
                model TEXT,
                trim TEXT,
                body TEXT,
                transmission TEXT,
                vin TEXT,
                state TEXT,
                condition TEXT,
                odometer TEXT,
                color TEXT,
                interior TEXT,
                seller TEXT,
                mmr TEXT,
                selling_price TEXT,
                sale_date TEXT
            );
        """)
        self.connection.commit()

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
                    # Insere os dados do CSV na tabela 'ficheiro_csv', mantendo tudo como texto
                    self.cursor.execute("""
                        INSERT INTO ficheiro_csv (
                            year, make, model, trim, body, transmission, vin, 
                            state, condition, odometer, color, interior, seller, 
                            mmr, selling_price, sale_date
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        row.get('year', ''),
                        row.get('make', ''),
                        row.get('model', ''),
                        row.get('trim', ''),
                        row.get('body', ''),
                        row.get('transmission', ''),
                        row.get('vin', ''),
                        row.get('state', ''),
                        row.get('condition', ''),
                        row.get('odometer', ''),
                        row.get('color', ''),
                        row.get('interior', ''),
                        row.get('seller', ''),
                        row.get('mmr', ''),
                        row.get('sellingprice', ''),
                        row.get('saledate', '')
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
