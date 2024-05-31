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
    
    folder_path = os.path.join(tmp_folder_path, f'{id}_{og_lang}_{target_lang}')
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
        
