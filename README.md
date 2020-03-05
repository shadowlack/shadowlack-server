# Shadowlack MU*

Shadowlack Python MUD/MUX/MUSH/MU* development.

```bash

# If you are using a standard command prompt, you can use the following:
evenv\scripts\activate.bat

# If you are using a PS Shell, Git Bash, or other, you can use the following:
.\evenv\scripts\activate

cd shadowlack
# server controls
evennia start
evennia reload
evennia stop
```

## Installation
```
pip install -e evennia
pip install mysqlclient
```


## Development
```
evennia makemigrations
evennia migrate
```
