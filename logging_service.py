import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_dir = 'log'
initial_log_name = 'Today.log'
log_file_path = os.path.join(log_dir, initial_log_name)


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Custom class TimedRotatingFileHandler
    """

    def __init__(self, *args, **kwargs):
        # Menginisiasi backup_count dari induk
        self.backup_count = kwargs.get('backupCount', 0) 
        super().__init__(*args, **kwargs)

    @staticmethod
    def __rename_log():
        """
        Static method untuk melakukan rename file setelah dilakukan rotate
        """

        # Mengambil nama file yang telah di rotate dan 'log' telah dihilangkan
        file_to_rename = [file for file in os.listdir(log_dir) if 'log' not in file.lower()]

        # Merename file yang telah di rotate ke formate 'date.log'
        for file in file_to_rename:
            new_file = file.replace('.', '') + '.log'
            os.rename(os.path.join(log_dir, file), os.path.join(log_dir, new_file))

    def __delete_log(self):
        """
        Menghapus file log yang melebihi backup_count
        """
        if self.backup_count > 0:

            # Mengambil nama semua nama file di log yang bukan initial_log_name
            files = sorted([file for file in os.listdir(log_dir) if initial_log_name not in file])

            # Menghapus file yang melebihi backup_count
            if len(files) > self.backup_count:
                if os.path.exists(os.path.join(log_dir, files[0])):
                    os.remove(os.path.join(log_dir, files[0]))

    def doRollover(self):
        """
        Override fungsi doRollover dengan menambahkan fungsi rename_log() untuk mengubah nama file setelah di rotate
        """
        super().doRollover()
        self.__rename_log()
        self.__delete_log()


def setup_logger():
    """
    Melakukan konfigurasi logging system

    :return: (Logger) logger object
    """

    # Cek ketersediaan logger
    if logging.getLogger("app").hasHandlers():
        return logging.getLogger("app")

    # Membuat logger
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Formatting log
    log_format = "%(asctime)s - %(levelname)s - %(file)s - %(func)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Pastikan folder logs ada
    os.makedirs(log_dir, exist_ok=True)

    # Handler rotasi berdasarkan waktu
    file_handler = CustomTimedRotatingFileHandler(
        filename=log_file_path,  # Nama file awal
        when="midnight",  # Rotasi setiap tengah malam
        interval=1,  # Interval harian
        backupCount=7,  # Simpan 7 hari log
        encoding="utf-8",  # Encoding UTF-8
        delay=True  # Menghindari tabrakan saat rotate (File dibuat ketika dibutuhkan)
    )

    # Ubah nama file setelah rotasi agar filename mudah di format
    file_handler.namer = lambda name: name.replace(initial_log_name, "")

    # Set format untuk log
    file_handler.setFormatter(formatter)

    # Tambahkan handler ke logger
    logger.addHandler(file_handler)

    return logger
