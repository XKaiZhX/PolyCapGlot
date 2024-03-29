from hashlib import sha256

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

def translate_video():
    pass