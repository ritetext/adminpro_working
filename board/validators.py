from django.core.exceptions import ValidationError

def vaidate_file_size(file):
    max_size = 100

    if file.size > max_size * 1024:
        raise ValidationError(f'file cannot be larger than {max_size}kb')