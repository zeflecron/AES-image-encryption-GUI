# AES-image-encryption-GUI
AES image encryption using cryptography library with tkinter as the GUI

Purpose of this is to practice tkinter and file management

# How to run app.py (windows)
1. Put all the folders and files into a directory
2. Create a virtual environment in that directory using cmd: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate.bat`
4. Download the dependencies: `pip install -r requirements.txt`
5. Run app.py in the cmd, or use an IDE
6. Another window should appear with the app running

# How to use it
1. Generate a key and iv (if needed)
2. Select key, iv, and the mode to encrypt/decrypt
3. Add images, encrypt
4. Make sure that the mode, key, and iv are the same when decrypting

# Extra notes
test_image_2 in the dec_images cannot be opened because it was decrypted incorrectly (on purpose)
everything was encrypted and decrypted using CTR mode (except test_image_2 using CFB)

[Link for some of the test images](https://unsplash.com/@simonppt)
