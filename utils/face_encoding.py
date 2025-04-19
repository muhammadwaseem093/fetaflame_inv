import os
import numpy as np
import face_recognition
from django.conf import settings

def encode_face(image_path):
    """Encode face from image and return a Numpy Array."""
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]
    except Exception as e:
        print(f"Error encoding face: {e}")
    return None