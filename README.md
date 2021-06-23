# chrome-forensics
Python scripts to interact with and extract data from Google Chrome's SQLite databases

---

## Installation

```
pip3 install -r requirements.txt
```

---

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

- **Linux**: /home/<username>/.config/google-chrome/Default/History

- **Mac**: /Users/<username>/Library/Application Support/Google/Chrome/Default/History

- **Windows**: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\History

---

## Examples

**To Note:** 
- If no output flag is provided the results will be displayed in the console - every 5 lines (press enter to display next 5 lines, any other character to escape)
- Make sure Chrome is closed before executing the script. You'll receive the following error if its still running, `sqlite3.OperationalError: database is locked`


### History Logs

```bash
$ python3 chrome_history.py /home/$USER/.config/google-chrome/Default/History -l

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

```


### History Summary

```bash
$ python3 chrome_history.py /home/$USER/.config/google-chrome/Default/History -s

[+] Chrome History Summary:

|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|
|url_id|title                                              |url                                                |visit_count|typed_count|hidden|first_visit_time          |last_visit_time           |
|===================================================================================================================================================================================================|
|6     |GitHub - psf/requests: A simple, yet elegant HTTP l|https://github.com/psf/requests                    |2          |0          |0     |2021-05-04 10:40:49.350410|2021-05-04 10:41:03.979415|
|      |ibrary.                                            |                                                   |           |           |      |                          |                          |
|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|
|7     |Issues · psf/requests · GitHub                     |https://github.com/psf/requests/issues             |2          |0          |0     |2021-05-04 10:41:04.021337|2021-05-04 10:41:04.467752|
|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|
|8     |python - Google Search                             |https://www.google.com/search?q=python&oq=python&aq|2          |0          |0     |2021-05-04 10:41:22.615857|2021-05-04 10:41:23.529702|
|      |                                                   |s=chrome..69i57j46i433j0i433l3j0j0i433l3j0.1332j0j7|           |           |      |                          |                          |
|      |                                                   |&sourceid=chrome&ie=UTF-8                          |           |           |      |                          |                          |
|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|
|13    |Functional Programming HOWTO — Python 3.9.5 documen|https://docs.python.org/3/howto/functional.html    |1          |0          |0     |2021-05-04 10:41:55.436107|2021-05-04 10:41:55.436107|
|      |tation                                             |                                                   |           |           |      |                          |                          |
|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|
|12    |Python HOWTOs — Python 3.9.5 documentation         |https://docs.python.org/3/howto/index.html         |1          |0          |0     |2021-05-04 10:41:53.161687|2021-05-04 10:41:53.161687|
|------|---------------------------------------------------|---------------------------------------------------|-----------|-----------|------|--------------------------|--------------------------|

...

```

### Output File

```bash
$ python3 chrome_history.py /home/$USER/.config/google-chrome/Default/History -l -op ~/Desktop/chrome_history_out.csv

[+] CSV saved to: /home/$USER/Desktop/chrome_history_out.csv

```

---

### References

- https://www.sans.org/blog/google-chrome-forensics/
- https://chromium.googlesource.com/chromium/+/trunk/content/public/common/page_transition_types.h
- https://www.dfir.training/infographics-cheats/210-evolution-of-chrome-databases-v35/file

















<!-- ### sqlacodegen
```
sudo sqlacodegen "sqlite:////home/kali/.config/google-chrome/Default/History" > db_tables.py
``` -->

