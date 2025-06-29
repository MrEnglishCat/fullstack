import csv
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union, Optional
from zipfile import ZipFile

logger = logging.getLogger(f"__main__.{__name__}")
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    '[{asctime}] #{levelname:8} {filename}::{lineno}::{funcName} ===> {name} ===> {message}',
    style="{",
    datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler = RotatingFileHandler(
    __name__,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class FilesHandler:
    @classmethod
    def checking_folder(cls, folder_path: Union[str, Path]) -> None:
        """Создаёт папку, если её нет."""
        path = Path(folder_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Папка создана: {path}")

    @classmethod
    def ensure_directories(cls, dirs: list[Union[str, Path]]) -> None:
        """
        Создаёт список каталогов, если они не существуют.
        Использует уже реализованный метод `checking_folder`.
        """
        for path in dirs:
            cls.checking_folder(path)

    @classmethod
    def ensure_directories_with_log(cls, dirs: list[Union[str, Path]], context: str = "") -> None:
        """
        Создаёт список каталогов с логированием контекста.
        Например: создаются директории для определённой задачи или модуля.
        """
        logger.info(f"[{context}] Начинаю проверку и создание директорий...")
        cls.ensure_directories(dirs)
        logger.info(f"[{context}] Все директории проверены и созданы при необходимости.")

    @classmethod
    def check_file(cls, file_path: Union[str, Path]) -> bool:
        """Проверяет существование файла."""
        return Path(file_path).exists()

    @classmethod
    def read_json(cls, full_path: Union[str, Path]) -> Optional[dict]:
        """Читает JSON-файл и возвращает данные."""
        path = Path(full_path)
        if not cls.check_file(path):
            logger.warning(f"Файл не найден: {path}")
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Файл прочитан: {path}")
                return data
        except Exception as e:
            logger.error(f"Ошибка чтения файла {path}: {e}")
            return None

    @classmethod
    def write_json(cls, full_path: Union[str, Path], data: Union[dict, list]) -> bool:
        """Записывает данные в JSON-файл."""
        path = Path(full_path)
        if not data:
            logger.warning("Нет данных для записи.")
            return False
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                logger.info(f"Файл сохранён: {path}")
                return True
        except Exception as e:
            logger.error(f"Ошибка записи файла {path}: {e}")
            return False

    @classmethod
    def update_json_file(cls, full_path: Union[str, Path], data: Union[dict, list]) -> bool:
        """Дополняет существующий JSON-файл новыми данными."""
        path = Path(full_path)
        existing_data = cls.read_json(path) or []
        if isinstance(existing_data, list) and isinstance(data, list):
            existing_data.extend(data)
        elif isinstance(existing_data, dict) and isinstance(data, dict):
            existing_data.update(data)
        else:
            logger.warning("Тип данных не совпадает для обновления.")
            return False

        return cls.write_json(path, existing_data)

    @classmethod
    def get_zip(cls, result_path: Union[str, Path], from_path: Union[str, Path]) -> None:
        """Архивирует содержимое директории."""
        result_path = Path(result_path)
        from_path = Path(from_path)

        logger.info("Начато формирование архива с логами...")
        try:
            with ZipFile(result_path, 'w') as zip_file:
                for root, _, files in os.walk(from_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(from_path)
                        zip_file.write(file_path, arcname)
            logger.info("Архив сформирован.")
        except Exception as e:
            logger.error(f"Ошибка при формировании архива: {e}")

    @classmethod
    def remove_result_zip(cls, folder_path: Union[str, Path], extension: str = '.zip') -> None:
        """Удаляет все ZIP-файлы в указанной папке."""
        folder_path = Path(folder_path)
        if not folder_path.exists():
            logger.warning(f"Папка не существует: {folder_path}")
            return

        logger.info("Удаление всех .zip архивов...")
        for file in folder_path.iterdir():
            if file.suffix == extension:
                file.unlink()
                logger.info(f"Файл удалён: {file}")

    @classmethod
    def remove_file(cls, file_path: Union[str, Path]) -> None:
        """Удаляет файл, если он существует."""
        file_path = Path(file_path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Файл удалён: {file_path}")
        else:
            logger.warning(f"Файл не найден: {file_path}")

    @classmethod
    def write_file(cls, file_path: Union[str, Path], filename: str, data: str) -> bool:
        """Сохраняет текстовые данные в файл."""
        file_path = Path(file_path)
        cls.checking_folder(file_path)

        full_path = file_path / filename
        try:
            with full_path.open("w", encoding="utf-8") as f:
                f.writelines(data)
            logger.info(f"Файл сохранён: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка записи файла {full_path}: {e}")
            return False

    @classmethod
    def write_csv_file(
            cls,
            file_path: Union[str, Path],
            filename: str,
            data: list[dict],
            fieldnames: tuple,
            first_time: bool = True
    ) -> bool:
        """Записывает данные в CSV-файл."""
        file_path = Path(file_path)
        cls.checking_folder(file_path)

        full_path = file_path / filename
        try:
            with full_path.open("w", encoding="utf-8-sig", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", quoting=csv.QUOTE_STRINGS)
                if first_time:
                    writer.writeheader()
                writer.writerows(data)
            logger.info(f"CSV-файл сохранён: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка записи CSV-файла {full_path}: {e}")
            return False
