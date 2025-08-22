from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati


DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

BACKEND_HOST = env.str("BACKEND_HOST", "http://localhost:8000")


API_ID = env.str("api_id")
API_HASH = env.str("api_hash")

BASE_URL=env.str("BACKEND_HOST")
API_TOKEN=env.str("API_TOKEN")