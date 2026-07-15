import os
import hashlib
import subprocess
import platform
import time
import urllib.request

# URL of the update hash file
zip_hash_url = "DRIVE URL REPLACED FOR PRIVACY"

# URL of the file to download
zip_url = "DRIVE URL REPLACED FOR PRIVACY"

# URL of script updater
script_url = "DRIVE URL REPLACED FOR PRIVACY"

# URL of script hash
script_hash_url = "DRIVE URL REPLACED FOR PRIVACY"

# Path where the file will be saved
zip_download_path = "SCRIPT URL REPLACED FOR PRIVACY"

# Path where the file will be saved
script_download_path = "SCRIPT URL REPLACED FOR PRIVACY"

# Path where the hash will be stored
zip_hash_path = "SCRIPT URL REPLACED FOR PRIVACY"

# Hash of script
script_hash_path = "SCRIPT URL REPLACED FOR PRIVACY"

from urllib.request import build_opener, install_opener, _opener

if _opener is None:
    opener = build_opener()
    install_opener(opener)
else:
    opener = _opener

opener.addheaders = [('User-agent', 'Mozilla/5.0')]




def check_update(update_hash_url, file_url, stored_hash_path, download_path, isScript):

    
    # Fetch the update hash content
    response = urllib.request.urlopen(update_hash_url)
    update_hash = response.read().decode().strip()

    # Check if the update hash is the same as the stored hash
    if os.path.exists(stored_hash_path):
        with open(stored_hash_path, "r") as file:
            stored_hash = file.read()
        if update_hash == stored_hash:
            print("Update hash is the same. Skipping update.")
            return 0
    else:
        print("No stored hash found. Proceeding with downloading the update.")

    # Download the file
    response = urllib.request.urlopen(file_url)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    print("Downloading update...")
    start_time = time.time()
    with open(download_path, "wb") as file:
        downloaded_size = 0
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            file.write(buffer)
            downloaded_size += len(buffer)
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                download_speed = (downloaded_size * 8) / (1024 * 1024 * elapsed_time)  # Mbps
                print(f"Progress: {downloaded_size / total_size * 100:.2f}% Speed: {download_speed:.2f} Mbps", end="\r")

    print("\nDownload of the update completed.")

    # Calculate the hash of the downloaded file
    hasher = hashlib.sha256()
    with open(download_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    file_hash = hasher.hexdigest()
    with open(stored_hash_path, "w") as file:
        file.write(update_hash)
    if isScript:
        try:
            print("Lord willing this shall work")
            os.rename("extractor.py","extractor_old.py")
            print("uno")
            os.rename("extractor_new.py","extractor.py")
            print("dos")
            os.remove("extractor_old.py")
            print("tres")
            processe = subprocess.Popen(["python","extractor.py"])
            processe.wait()
            print("Script will be updated and them start new script")
        except Exception as e:
            print("It didn't")
            print("Exception:", e)
            print("error in the script update subprocess call. Exiting")
            exit()
    else:
        # Path where the file will be extracted
        extract_path = "FILEPATH HAS BEEN CHANGED FOR PRIVACY REASONS"
        # Extract the file using 7zip
        extraction_command = f'7z x "{download_path}" -o"{extract_path}" -y'
        subprocess.run(extraction_command, shell=True)
        os.remove(download_path)

    print("Extracting update completed successfully.")
    #exit()
#Check Script
check_update(script_hash_url,script_url,script_hash_path,script_download_path,True)
#check zip
check_update(zip_hash_url,zip_url,zip_hash_path,zip_download_path,False)

print("It is done")
