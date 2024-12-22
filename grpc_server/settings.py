import os

# Server Configuration
# Default value '50051'
GRPC_SERVER_PORT = os.getenv('GRPC_SERVER_PORT', '50051')
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '10'))

# Media Files
MEDIA_PATH = os.getenv('MEDIA_PATH', f'{os.getcwd()}/app/csv')

# PostgreSQL Database Configuration (Adicione as variáveis de configuração)
DBNAME = os.getenv('DBNAME', 'mydatabase')
DBUSERNAME = os.getenv('DBUSERNAME', 'myuser')
DBPASSWORD = os.getenv('DBPASSWORD', 'mypassword')
DBHOST = os.getenv('DBHOST', 'db')  # ou o nome do serviço se estiver em Docker
DBPORT = os.getenv('DBPORT', '5432')  # Porta padrão do PostgreSQL