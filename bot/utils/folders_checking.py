import os

def create_directories():
    current_directory = os.getcwd()

    # Поднимаемся на одну директорию вверх
    parent_directory = os.path.dirname(current_directory)

    logs_directory = os.path.join(parent_directory, 'logs')
    media_directory = os.path.join(parent_directory, 'media')

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

if __name__ == "__main__":
    create_directories()
