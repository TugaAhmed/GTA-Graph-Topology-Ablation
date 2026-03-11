import sys
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

load_dotenv()

def decrypt_file_content(encrypted_file_path):
    """Decrypts the content of an encrypted file and returns bytes"""
    private_key_pem = os.environ.get("SUBMISSION_PRIVATE_KEY")
    
    if not private_key_pem:
        raise ValueError("Error: 'SUBMISSION_PRIVATE_KEY' is missing from environment variables.")

    # Convert \n to actual newlines if needed
    private_key_pem = private_key_pem.replace('\\n', '\n').strip()

    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
        )
    except Exception as e:
        print(f"DEBUG: Key starts with: {private_key_pem[:30]}...")
        raise ValueError(f"Invalid Private Key format: {e}")

    try:
        with open(encrypted_file_path, "rb") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {encrypted_file_path}")

    rsa_segment_size = 256
    if len(file_content) < rsa_segment_size:
        raise ValueError("File is too short to contain a valid encrypted header.")

    encrypted_session_key = file_content[:rsa_segment_size]
    encrypted_data = file_content[rsa_segment_size:]

    try:
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise ValueError(f"RSA Decryption failed: {e}")

    try:
        cipher_suite = Fernet(session_key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        raise ValueError(f"Data decryption failed: {e}")


def decrypt_file(encrypted_file_path, output_file_path=None):
    """
    Decrypts a file and saves it to disk. Returns the output file path.
    This is the function importable by update_leaderboard.py
    """
    decrypted_bytes = decrypt_file_content(encrypted_file_path)
    if output_file_path is None:
        output_file_path = str(encrypted_file_path).replace(".enc", "")
    with open(output_file_path, "wb") as f:
        f.write(decrypted_bytes)
    return output_file_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <filename>")
    else:
        try:
            out_file = decrypt_file(sys.argv[1])
            print(f"Decryption successful! Saved to '{out_file}'")
        except Exception as e:
            print(f"FAILED: {e}")
