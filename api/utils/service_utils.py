from hashlib import sha256
import random

def generate_video_hash(email, title, language):

    input = str(email + title + language)
    print("controller_utils - generate_video_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    print("controller_utils - generate_video_hash ->\tGenerated hash: ", str(hash))

    return hash

def generate_translation_hash(video_hash, sub_lang):

    input = str(video_hash + sub_lang)
    print("controller_utils - generate_translation_hash ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    print("controller_utils - generate_translation_hash ->\tGenerated hash: ", str(hash))

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


def generate_password_hash(password, salt):
    password
