from cryptography.fernet import Fernet

# Génère une nouvelle clé Fernet
key = Fernet.generate_key()

# Affiche la clé générée en texte lisible
print(key.decode())
