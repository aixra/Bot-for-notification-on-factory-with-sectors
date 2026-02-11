BOT_TOKEN = "" #TOKEN OF BOT

SECTOR_PREFIX = "Участок"
DEVICE_PREFIC = "Device"
BACK_BUTTON1 = "Назад"
BACK_BUTTON2 = "Назад к сектору"

ADMIN_CHAT_ID = -5228109324

# Fallback sections/devices if Excel file is unavailable /Если эксель не работает - данные беруться от сюда
DEFAULT_SECTORS = ["Участок 1", "Участок 2", "Участок 3", "Участок 4"]
DEFAULT_DEVICES = {
    "Участок 1": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 2": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 3": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 4": ["Device 1", "Device 2", "Device 3", "Device 4"],
}

# External Excel source with sectors/devices
EQUIPMENT_EXCEL_FILE = "equipment_catalog.xlsx" #Указать путь к файлу с оборудовнаием
EQUIPMENT_SHEET_NAME = "Catalog"                 #лист в файле

# Google Tables (Google Sheets API) settings
GOOGLE_TABLES_SPREADSHEET_ID = "1g_3ON8XvoIw1-DWmy9FCgLSmNnx-Lthzqi9QWbxdw3I"
GOOGLE_TABLES_CREDENTIALS_FILE = "zavod-487108-c22adbd6d551.json"
GOOGLE_TABLES_SHEET_NAME = "Sheet1"


# Incremental request id storage
REQUEST_ID_COUNTER_FILE = "request_id_counter.txt" #Файл где храниться последней номер заявки

# SMTP / e-mail notification settings
EMAIL_ENABLED = False      # Включить ли отправку писем (True / False)
SMTP_HOST = ""             # Адрес SMTP-сервера
SMTP_PORT = 587            # Порт SMTP
SMTP_USERNAME = ""         # Логин (обычно полный e-mail)
SMTP_PASSWORD = ""         # Пароль (или app-password)
SMTP_FROM = ""             # От кого отправляется письмо ("My App <myemail@gmail.com>")
EMAIL_TO = ""              # Кому отправлять (если один адрес)
SMTP_USE_TLS = True        # Использовать TLS
