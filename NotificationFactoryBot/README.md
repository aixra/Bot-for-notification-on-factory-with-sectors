1) Код написан с использованием библиотек
pip install -U aiogram
pip install -U google-api-python-client
pip install -U google-auth
pip install -U openpyxl

2)Рекомендуеться использование виртуальной среды venv, во избежания конфликтов библиотек.

3)Бот может быть создан через @BotFather в тг (токен бота можно получить в нем же, 
и вставить в строку TOKEN в файле main.py)

Код написан на python 3.12.3 (для работы aiogram подходит версия python 3.9+)

Настройка отображения:
Все управление происходит через config.py
Файл config.py содержит все параметры используемые в названиях, через изменгения содержимого
его переменных, можно менять название кнопок в боте и т.п. 
ID админа следует вписывать в него же.


-----------------------------------КАК ИСПОЛЬЗОВАТЬ ГУГЛ ТАБЛИЦЫ---------------------------------------------------------------------------
---------------------------------Шаг 1: Создание проекта в Google Cloud--------------------------------------------------------------------
Перейдите в https://console.cloud.google.com/apis/dashboard.
Нажмите "Select a project" (Выбрать проект) -> "New Project" (Новый проект).
Введите название проекта и нажмите "Create"

---------------------------------Шаг 2: Включение Google Sheets API------------------------------------------------------------------------
В меню слева выберите "APIs & Services" -> "Dashboard" (Панель управления).
Нажмите "+ ENABLE APIS AND SERVICES" (Включить API и сервисы).
В строке поиска введите "Google Sheets API", выберите его и нажмите "Enable" (Включить).
Рекомендуется также включить "Google Drive API" (для работы с файлами)

---------------------------------Шаг 3: Создание сервисного аккаунта и ключа (JSON)-------------------------------------------------------
Перейдите в раздел "APIs & Services" -> "Credentials" (Учетные данные).
Нажмите "+ CREATE CREDENTIALS" (Создать учетные данные) и выберите "Service account".
Введите имя сервисного аккаунта (например, sheets-bot), нажмите "Create and Continue".
Нажмите "Done" (Роли назначать не обязательно).
В списке "Service Accounts" нажмите на только что созданный аккаунт.
Перейдите во вкладку "KEYS" (Ключи).
Нажмите "ADD KEY" -> "Create new key".
Выберите тип JSON и нажмите "Create".

---------------------------------Шаг 4: Предоставление доступа к таблице-------------------------------------------------------------------
Сервисный аккаунт — это как новый пользователь Google. Чтобы он мог читать/писать в вашу таблицу, нужно дать ему права.
Откройте нужную Google Таблицу.
Нажмите кнопку "Share" (Настройки доступа).
В скачанном JSON-файле найдите поле client_email (выглядит как "sheets-bot@project-id.iam.gserviceaccount.com").

Вставьте этот email в поле общего доступа к таблице, выбрав роль "Editor" (Редактор), и нажмите "Отправить".

-----------------------------------------------------------ENGLISH-------------------------------------------------------------------------
1) The code is written using the following libraries:
pip install -U aiogram
pip install -U google-api-python-client
pip install -U google-auth
pip install -U openpyxl

2) Using the venv virtual environment is recommended to avoid library conflicts.

3) The bot can be created via @BotFather in Telegram (the bot token can be obtained there,
and inserted into the TOKEN line in the main.py file).

The code is written in Python 3.12.3 (Python 3.9+ is suitable for aiogram).

Display settings:
All control is handled through config.py.
The config.py file contains all the parameters used in the names. By changing the contents of its variables, you can change the names of buttons in the bot, etc.
The admin ID should also be entered in it.

-----------------------------------HOW TO USE GOOGLE SHEETS---------------------------------------------------------------------------
---------------------------------Step 1: Create a project in Google Cloud--------------------------------------------------------------------
Go to https://console.cloud.google.com/apis/dashboard.
Click "Select a project" -> "New Project".
Enter a project name and click "Create".

---------------------------------Step 2: Enable the Google Sheets API------------------------------------------------------------------------
In the left menu, select "APIs & Services" -> "Dashboard".
Click "+ ENABLE APIS AND SERVICES".
In the search bar, type "Google Sheets API", select it, and click "Enable".
It is also recommended to enable the Google Drive API (for working with files).

---------------------------------Step 3: Create a service account and key (JSON)-------------------------------------------------------
Go to "APIs & Services" -> "Credentials".
Click "+ CREATE CREDENTIALS" and select "Service account".
Enter a name for the service account (e.g., sheets-bot), click "Create and Continue".
Click "Done" (assigning roles is optional).
In the "Service Accounts" list, click the newly created account.
Go to the "KEYS" tab.
Click "ADD KEY" -> "Create new key".
Select the JSON type and click "Create".

---------------------------------Step 4: Grant access to the spreadsheet-------------------------------------------------------------------
A service account is like a new Google user. To allow them to read and write to your spreadsheet, you need to grant them permissions.
Open the desired Google Sheet.
Click the "Share" button.
In the downloaded JSON file, find the client_email field (looks like "sheets-bot@project-id.iam.gserviceaccount.com").
Paste this email into the spreadsheet sharing field, selecting the "Editor" role, and click "Submit."

