import logging
import configparser


def read_parameters(file_path):
    """
    Function to read the .ini configuration file
    
    :param file_path: configuration (.ini) file path
    :return: config._sections: Dictionary with all the sections and options of a configuration file.
    """

    parameter_file = check_file(file_path)
    config = configparser.ConfigParser()
    config.read(parameter_file)  # Leer el archivo de configuración
    return config._sections


def check_file(file_path):
    """
    Function to check if the file exists

    :param file_path: path to file to check
    :return file_path: returns the file path.
    :raises Exception e:General exception if file doesn't exist.
    """

    try:
        with open(file_path):
            return file_path
    except Exception as e:
        logging.error("Error in check_file(%s). Error: %s " % (file_path, str(e)))  # El mensaje de error contiene la ruta del archivo y la descripción del error obtenido.
        raise Exception("Error in check_file(%s). Error: %s " % (file_path, str(e)))
