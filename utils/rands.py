import string
from random import SystemRandom

from django.utils.text import slugify

def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=k
    ))

def new_slugify(string,k=5):
    return slugify(string) + '-' + random_letters(k)