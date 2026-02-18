from flask import session

translations = {
    'en': {
        'hello_world': 'Hello, World!',
        'app_running': 'Your Python web app is running.',
        'login': 'Login',
        'logout': 'Logout',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email',
        'language': 'Language',
        'new_user': 'New user?',
        'register_here': 'Register here',
        'already_account': 'Already have an account?',
        'invalid_credentials': 'Invalid credentials',
        'user_exists': 'User already exists',
        'settings': 'Settings',
        'server': 'Server',
        'port': 'Port',
        'protocol': 'Protocol',
        'add_server': 'Add Server',
        'test_connection': 'Test Connection',
        'connection_success': 'Connection successful',
        'connection_failed': 'Connection failed',
        'no_servers': 'No email servers configured',
        'imap': 'IMAP',
        'pop3': 'POP3',
    },
    'it': {
        'hello_world': 'Ciao, Mondo!',
        'app_running': 'La tua app Python è in esecuzione.',
        'login': 'Accedi',
        'logout': 'Disconnetti',
        'register': 'Registrati',
        'username': 'Nome utente',
        'password': 'Password',
        'first_name': 'Nome',
        'last_name': 'Cognome',
        'email': 'Email',
        'language': 'Lingua',
        'new_user': 'Nuovo utente?',
        'register_here': 'Registrati qui',
        'already_account': 'Hai già un account?',
        'invalid_credentials': 'Credenziali non valide',
        'user_exists': 'Utente già esistente',
        'settings': 'Impostazioni',
        'server': 'Server',
        'port': 'Porta',
        'protocol': 'Protocollo',
        'add_server': 'Aggiungi server',
        'test_connection': 'Test collegamento',
        'connection_success': 'Collegamento riuscito',
        'connection_failed': 'Collegamento fallito',
        'no_servers': 'Nessun server di posta configurato',
        'imap': 'IMAP',
        'pop3': 'POP3',
    },
}

def get_locale() -> str:
    return session.get('lang', 'en')

def translate(key: str) -> str:
    lang = get_locale()
    return translations.get(lang, translations['en']).get(key, key)
