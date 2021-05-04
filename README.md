# chrome-forensics
Python scripts to interact with and extract data from Google Chrome's SQLite databases


### sqlacodegen
```
sudo sqlacodegen "sqlite:////home/kali/.config/google-chrome/Default/History" > db_tables.py
```

### Location of Google Chrome history

Linux

```
/home/<username>/.config/google-chrome/Default/History
```

Mac
```
/Users/<username>/Library/Application Support/Google/Chrome/Default/History
```

Windows
```
C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\History```