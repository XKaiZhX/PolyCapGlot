from hashlib import sha256
import os
import random
from config.app_config import tmp_folder_path, hashing_base

def generate_video_hash(email, title, language):
    """Genera un hash SHA-256 para un video basado en el email, título y lenguaje."""
    input_str = f"{email}{title}{language}"
    hash_str = sha256(input_str.encode()).hexdigest()
    return hash_str

def generate_translation_hash(video_hash, sub_lang):
    """Genera un hash SHA-256 para una traducción basada en el hash del video y el lenguaje de los subtítulos."""
    input_str = f"{video_hash}{sub_lang}"
    hash_str = sha256(input_str.encode()).hexdigest()
    return hash_str

def generate_password_salt():
    """Genera una sal aleatoria para el hashing de contraseñas."""
    base = hashing_base
    base_len = len(base)
    max_extra_len = 15
    min_len = 10
    length = random.randint(min_len, min_len + max_extra_len)
    
    salt = ''.join(
        random.choice(base).upper() if random.random() > 0.5 else random.choice(base)
        for _ in range(length)
    )
    
    return salt

def generate_password_hash(password: str, salt: str):
    """Genera un hash SHA-256 para una contraseña combinada con una sal."""
    input_str = f"{salt}{password}"
    hash_str = sha256(input_str.encode()).hexdigest()
    return hash_str

def generate_temp_folder(video_id: str, og_lang: str, target_lang: str):
    """Genera un directorio temporal basado en el ID del video y los lenguajes original y de destino."""
    folder_path = os.path.join(tmp_folder_path, f'{video_id}_{og_lang}_{target_lang}')
    
    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Created directory: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")
        raise Exception("Folder already exists")
    
    return folder_path

def check_file_exists(filepath: str):
    """Verifica si un archivo existe en el sistema de archivos."""
    return os.path.exists(filepath)


'''
from hashlib import sha256
import os
import random

from config.app_config import tmp_folder_path, hashing_base

def generate_video_hash(email, title, language):

    input = str(email + title + language)
    #print("service_utils - generate_video_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    #print("service_utils - generate_video_hash ->\tGenerated hash: ", str(hash))

    return hash

def generate_translation_hash(video_hash, sub_lang):

    input = str(video_hash + sub_lang)
    #print("service_utils - generate_translation_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    #print("service_utils - generate_translation_hash ->\tGenerated hash: ", str(hash))

    return hash

def generate_password_salt():
    base = hashing_base
    base_len = len(base)

    max_extra_len = 15
    min_len = 10

    salt = ""
    lenght = int(random.random() * max_extra_len + min_len)

    for i in range(lenght):
        letter = base[int(random.random() * base_len)]
        if(random.random() > 0.5):
            letter = letter.upper()
        salt += letter

    return salt


def generate_password_hash(password: str, salt: str):
    input = salt + password
    #print("service_utils - generate_password_hash: input=" + input)

    hash = sha256(input.encode()).hexdigest()
    #print("service_utils - generate_password_hash: hash=" + hash)

    return hash

def generate_temp_folder(video_id: str, og_lang: str, target_lang: str):
    
    folder_path = os.path.join(tmp_folder_path, f'{video_id}_{og_lang}_{target_lang}')
    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    # Create the id_lang directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Created directory: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")
        raise Exception("Folder already exists")
    
    return folder_path

def check_file_exists(filepath: str):
    return os.path.exists(filepath)     
'''