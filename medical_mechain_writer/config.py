from getpass import getuser
from loguru import logger

logger.info('current system user is {}', getuser())

if getuser() == 'zj':
    STATIC_URL = 'http://127.0.0.1:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
    PROJECT_DIR = '~/local-rag'
elif getuser() == 'ubuntu':
    STATIC_URL = 'http://125.69.16.175:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
elif getuser() == 'gx':
    STATIC_URL = 'http://127.0.0.1:8501/app/static/'
    OLLAMA_BASE_URL = 'http://125.69.16.175:11434'
else:
    STATIC_URL = 'http://192.168.1.159:8501/app/static/'
    OLLAMA_BASE_URL = 'http://192.168.1.159:11434'


# BASE_VECTOR_DB_DIR = 'vector_db'
BASE_VECTOR_DB_DIR = 'vector_db202411011216'
