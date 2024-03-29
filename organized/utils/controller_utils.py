from hashlib import sha256

def generate_firebase():
    return {
        "firebase": {
            "uri": "INSERT_FIREBASE_URI",
            "bucket": "INSERT_FIREBASE_BUCKET",
            #TODO: Autentification
        }
    }

def generate_hash(email, title, language):

    input = str(email + title + language)
    print("controller_utils ->\tHashing input: ", str(input))

    hash = sha256(input.encode()).hexdigest()
    print("controller_utils ->\tGenerated hash: ", str(hash))

    return hash

def translate_video():
    pass