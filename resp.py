import inspect
import os
from enum import Enum
from app.service.logging_service import setup_logger

logger = setup_logger()


class ResponseStatus(str, Enum):
    """
    Object enum untuk standarisasi Response Status dengan inherit type str agar dapat di serialize saat di jsonify
    """
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


def resp(status: ResponseStatus, message: str = '', data: any = None):
    """
    standarisasi response fungsi

    :param status: (ResponseStatus) Status eksekusi
    :param message: (str) Pesan eksekusi
    :param data: (any) Data hasil eksekusi

    :return: (dict) kumpulan objek dari parameter
    """
    resp = {}
    resp['status'] = status
    resp['message'] = message
    resp['data'] = data

    file, func = __get_file_n_func()
    extra_info = {"file": file, "func": func}

    if status == ResponseStatus.SUCCESS:
        logger.info(message, extra=extra_info)
    elif status == ResponseStatus.WARNING:
        logger.warning(message, exc_info=True, extra=extra_info)
    elif status == ResponseStatus.ERROR:
        logger.error(message, exc_info=True, extra=extra_info)
    elif status == ResponseStatus.CRITICAL:
        logger.critical(message, exc_info=True, extra=extra_info)
    return resp


def __get_file_n_func():
    """
    Digunakan untuk mendapatkan file dan fungsi pemanggil resp

    :return: (str) filename pemanggil, (str) fungsi pemanggil
    """

    caller_frame = inspect.stack()[2] # 2 berarti 2 level pemanggil sebelumnya
    caller_file = os.path.basename(caller_frame.filename)  # Nama file pemanggil
    caller_function = caller_frame.function  # Nama fungsi pemanggil
    return caller_file, caller_function
