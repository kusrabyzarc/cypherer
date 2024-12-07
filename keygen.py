from russian_crypto import RussianCrypto
import platform
import subprocess
import logger_module

logger = logger_module.create_logger('keygen')

def run_command(command):
    try:
        logger.debug(f"Выполнение команды: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        logger.debug(f"Результат выполнения команды: {result.stdout.strip()}")
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды {' '.join(command)}: {str(e)}")
        return "Unknown"

def get_motherboard_serial():
    if platform.system() == "Windows":
        return run_command(["wmic", "baseboard", "get", "serialnumber"])
    elif platform.system() == "Linux":
        return run_command(["sudo", "dmidecode", "-s", "baseboard-serial-number"])
    return "UnknownMotherboardSerial"

def get_cpu_id():
    if platform.system() == "Windows":
        return run_command(["wmic", "cpu", "get", "ProcessorId"])
    elif platform.system() == "Linux":
        return run_command(["lscpu"])
    return "UnknownCPU"

def get_bios_info():
    if platform.system() == "Windows":
        return run_command(["wmic", "bios", "get", "Manufacturer,SMBIOSBIOSVersion"])
    elif platform.system() == "Linux":
        return run_command(["sudo", "dmidecode", "-s", "bios-version"])
    return "UnknownBIOS"

def generate_unique_key(external_data: str = ""):
    try:
        logger.info("Начата генерация уникального ключа")
        motherboard_serial = get_motherboard_serial()
        cpu_id = get_cpu_id()
        bios_info = get_bios_info()
        os_version = platform.version()  # Версия ОС
        logger.debug("Собранные данные:")
        logger.debug(f"Материнская плата={motherboard_serial}")
        logger.debug(f"Процессор={cpu_id}")
        logger.debug(f"BIOS={bios_info}")
        logger.debug(f"ОС={os_version}")

        # Собираем все данные в строку
        data_string = f"{motherboard_serial}|{cpu_id}|{bios_info}|{os_version}|{external_data}"

        # Генерируем хэш Стрибог
        key = RussianCrypto.hash(bytearray(data_string.encode('utf-8')))
        logger.info("Уникальный ключ успешно сгенерирован")
        logger.debug(f"Сгенерированный ключ: {key}")
        return key
    except Exception as e:
        logger.critical(f"Ошибка при генерации ключа: {str(e)}")
        return f"Error generating key: {str(e)}"

if __name__ == "__main__":
    external_data = "MyExternalData123"
    unique_key = generate_unique_key(external_data)
