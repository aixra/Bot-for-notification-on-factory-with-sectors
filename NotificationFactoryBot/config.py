SECTOR_PREFIX = "Участок"
DEVICE_PREFIC = "Device"
BACK_BUTTON1 = "Назад"
BACK_BUTTON2 = "Назад к сектору"

ADMIN_CHAT_ID = -5228109324

# Fallback sections/devices if Excel file is unavailable
DEFAULT_SECTORS = ["Участок 1", "Участок 2", "Участок 3", "Участок 4"]
DEFAULT_DEVICES = {
    "Участок 1": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 2": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 3": ["Device 1", "Device 2", "Device 3", "Device 4"],
    "Участок 4": ["Device 1", "Device 2", "Device 3", "Device 4"],
}

# External Excel source with sectors/devices
EQUIPMENT_EXCEL_FILE = "equipment_catalog.xlsx"
EQUIPMENT_SHEET_NAME = "Catalog"

# Google Tables (Google Sheets API) settings
GOOGLE_TABLES_SPREADSHEET_ID = ""
GOOGLE_TABLES_CREDENTIALS_FILE = "service_account.json"
GOOGLE_TABLES_SHEET_NAME = "Sheet1"

# Incremental request id storage
REQUEST_ID_COUNTER_FILE = "request_id_counter.txt"

# SMTP / e-mail notification settings
EMAIL_ENABLED = False
SMTP_HOST = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
SMTP_FROM = ""
EMAIL_TO = ""
SMTP_USE_TLS = True


# External Excel source for allowed Telegram logins (one row = one user)
USERS_EXCEL_FILE = "allowed_users.xlsx"
USERS_SHEET_NAME = "Users"
