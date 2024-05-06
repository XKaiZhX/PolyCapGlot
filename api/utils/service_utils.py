from hashlib import sha256
import os
import random
import time

#print(storage.child(f"raw_videos/{id}.mp4").get_url(config["apiKey"])) Conservar para conseguir las urls
def generate_video_hash(email, title, language):

    input = str(email + title + language)
    print("service_utils - generate_video_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    print("service_utils - generate_video_hash ->\tGenerated hash: ", str(hash))

    return hash

def generate_translation_hash(video_hash, sub_lang):

    input = str(video_hash + sub_lang)
    print("service_utils - generate_translation_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    print("service_utils - generate_translation_hash ->\tGenerated hash: ", str(hash))

    return hash

def generate_password_salt():
    base = "enunlugardelamanchadecuyonombrenoquieroacordarmenohacemuchotiempoqueviviaunhidalgoconellobosennuestrospaises"
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
    print("service_utils - generate_password_hash: input=" + input)

    hash = sha256(input.encode()).hexdigest()
    print("service_utils - generate_password_hash: hash=" + hash)

    return hash

def generate_temp_folder():
    temp_filepath = "./temp"
    if(os.path.exists(temp_filepath) is False):
        os.makedirs(temp_filepath)

def check_file_exists(filepath: str):
    while(os.path.exists(filepath) is False):
        print("waiting on file")
        time.sleep(5)
