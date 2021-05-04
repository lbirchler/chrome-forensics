# chrome-forensics
Python scripts to interact with and extract data from Google Chrome's SQLite databases


## Installation

```
pip3 install -r requirements.txt
```

## Usage

```shell
usage: chrome_history.py [-h] [-l] [-s] [-o] [-op OUTFILEPATH] CHROME_HISTORY_DB

positional arguments:
  CHROME_HISTORY_DB     path of Chrome History database

optional arguments:
  -h, --help            show this help message and exit
  -l, --logs            gather historical webpage visits stored in History database
  -s, --summary         gather summary metrics for every url in History database
  -o, --outfile         output data to csv file (saved in cwd)
  -op OUTFILEPATH, --outfilepath OUTFILEPATH
                        output data to csv file (saved in specified path)
```
### Location of Google Chrome history database

- **Linux**: /home/USERNAME/.config/google-chrome/Default/History

- **Mac**: /Users/USERNAME/Library/Application Support/Google/Chrome/Default/History

- **Windows**: C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data\Default\History




## Examples

```bash
$ python3 chrome-forensics/chrome_history.py '/home/kali/.config/google-chrome/Default/History' -l

[+] Chrome History Logs:

|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|
|visit_time_utc            |visit_duration_min|title                                |url                                  |url_id|transition|transition_desc|from_url                             |
|=================================================================================================================================================================================================|
|2021-05-04 10:41:55.436107|0.06              |Functional Programming HOWTO — Python|https://docs.python.org/3/howto/funct|13    |0         |LINK           |https://docs.python.org/3/howto/index|
|                          |                  | 3.9.5 documentation                 |ional.html                           |      |          |               |.html                                |
|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|
|2021-05-04 10:41:53.161687|0.04              |Python HOWTOs — Python 3.9.5 document|https://docs.python.org/3/howto/index|12    |0         |LINK           |https://www.python.org/              |
|                          |                  |ation                                |.html                                |      |          |               |                                     |
|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|
|2021-05-04 10:41:38.503598|0.0               |Our Documentation | Python.org       |https://www.python.org/doc/          |11    |0         |LINK           |https://www.python.org/blogs/        |
|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|
|2021-05-04 10:41:29.570902|0.15              |Our Blogs | Python.org               |https://www.python.org/blogs/        |10    |0         |LINK           |https://www.python.org/              |
|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|
|2021-05-04 10:41:24.789719|0.47              |Welcome to Python.org                |https://www.python.org/              |9     |0         |LINK           |None                                 |
|--------------------------|------------------|-------------------------------------|-------------------------------------|------|----------|---------------|-------------------------------------|

...




### References















### sqlacodegen
```
sudo sqlacodegen "sqlite:////home/kali/.config/google-chrome/Default/History" > db_tables.py
```

