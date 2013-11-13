import os.path

def handle_uploaded_file(f, path, new_name=None):
    if new_name:
        file_name = new_name
    else:
        file_name = f.name
    destination = open(os.path.join(path, file_name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()