import os
import json
from datetime import datetime

# Указываем пути к директориям
lib_directory = 'amaterasudir/var/lib'
os.makedirs(lib_directory, exist_ok=True)

# Файл конфигурации
config_file = 'amaterasudir/etc/mail.json'

def load_config():
    """Загрузка конфигурации из файла."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # Если файл не существует, создаем его с пустой конфигурацией
        return {"accounts": []}

def save_config(config):
    """Сохранение конфигурации в файл."""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def create_account(email):
    """Создание нового аккаунта."""
    config = load_config()
    if email in [account['email'] for account in config['accounts']]:
        print("Аккаунт с таким адресом уже существует.")
        return

    config['accounts'].append({"email": email, "sent_emails": []})
    save_config(config)
    print(f"Аккаунт {email} успешно создан.")

def send_email(from_email, to_email, subject, body):
    """Отправка письма."""
    config = load_config()
    account = next((acc for acc in config['accounts'] if acc['email'] == from_email), None)

    if account is None:
        print("Аккаунт отправителя не найден.")
        return

    email_data = {
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "body": body,
        "timestamp": datetime.now().isoformat()
    }

    # Сохраняем письмо в аккаунте
    account['sent_emails'].append(email_data)
    save_config(config)

    # Сохраняем письмо в файл
    email_filename = os.path.join(lib_directory, f"{from_email}_{to_email}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(email_filename, 'w') as f:
        f.write(f"From: {from_email}\n")
        f.write(f"To: {to_email}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Body:\n{body}\n")
        f.write(f"Timestamp: {email_data['timestamp']}\n")

    print(f"Письмо отправлено от {from_email} к {to_email}.")

if __name__ == "__main__":
    while True:
        print("Добро пожаловать в LibreMail Client")
        print("\n1. Создать аккаунт")
        print("2. Отправить письмо")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            email = input("Введите адрес электронной почты (с доменом): ")
            create_account(email)
        elif choice == '2':
            from_email = input("Введите адрес отправителя: ")
            to_email = input("Введите адрес получателя: ")
            subject = input("Введите тему письма: ")
            body = input("Введите текст письма: ")
            send_email(from_email, to_email, subject, body)
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
