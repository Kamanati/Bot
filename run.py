import requests

# Your PythonAnywhere credentials and host
username = 'Opsridhar'
token = '186ee03ce3ad37d28e357cde8a774db51dd40e30'
host = 'www.pythonanywhere.com'  # or 'eu.pythonanywhere.com' for EU-based accounts

# Function to delete all consoles
def delete_all_consoles():
    response = requests.get(
        f'https://{host}/api/v0/user/{username}/consoles/',
        headers={'Authorization': f'Token {token}'}
    )
    
    if response.status_code == 200:
        consoles = response.json()
        for console in consoles:
            console_id = console['id']
            requests.delete(
                f'https://{host}/api/v0/user/{username}/consoles/{console_id}/',
                headers={'Authorization': f'Token {token}'}
            )
        print("All consoles deleted.")
    else:
        print(f'Error deleting consoles. Status code: {response.status_code}')

# Function to create a new console and run main.py
def create_and_run_console():
    payload = {
        'executable': 'python',
        'arguments': 'main.py',
        'working_directory': ''
    }
    
    response = requests.post(
        f'https://{host}/api/v0/user/{username}/consoles/',
        headers={'Authorization': f'Token {token}'},
        json=payload
    )
    
    if response.status_code == 201:
        print("New console created and main.py started.")
    else:
        print(f'Error creating console. Status code: {response.status_code}')

# Delete existing consoles and create a new one
delete_all_consoles()
create_and_run_console()
