import os

for filename in os.listdir('.'):
    if ' ' in filename:
        new_name = filename.replace(' ', '-')
        os.rename(filename, new_name)
        print(f'Renamed: "{filename}" -> "{new_name}"')