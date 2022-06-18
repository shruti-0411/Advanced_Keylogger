# Advanced_Keylogger
The purpose of this application is to keep tracks on every key that is typed through the keyboard and send it to the admin through the mail server in the time set or given. 

## Features
- KeyLogging
- Mail the log file
- Screenshot 
- Audio capture
- Clipboard Logging
- Gather System Information
- Encrypting all the log files


## Methodology
1. Creating files different text files that we will need in ordr to log different details like key log , system log etc .
2. To log keys using python, we will be using the pynput module where using the key listener function we can record all the keys and log them into the text file
3. To add an email functionality, we created a send email function where using the email module we can set all the email module details like title , subj , body of the mail etc.And later using SMTP module we can create SMTP sessions to send the mails
4. To gather computer information, we have used  socket and platform modules. Using which we log all the system information like IP address and model name into a text file
5. To get the clipboard information, we have used the win32clipboard module, which is a submodule of pywin .
6. We used the sound device module To record with a microphone, and we are writing the recorded audio to a .wav file using the scipy.io.wavfile module.
7. We implemented the screenshot function which takes the image of the current window and stores it in png format and it is done using ImageGrabTo take a screenshot, from the Pillow Module.
8. Then we encrypt all the text file using fernet module, which basically generates a key and convert or encrypts the data according to the key generated and stores it in a different text file
9. Atlast we send all the files as mail to the administrator whose email address we had already set in the code
10. Finally cleaning up the session by deleting all the recorded files so there is no proof of the logging done
