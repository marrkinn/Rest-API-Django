# brmed-rate

### Linux
```bash
python3 -m venv myvenv
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Windows
```bash
python -m venv myvenv
myvenv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### OBS: no Windows precisa ajustar os static files, path dos statics inicialmente configurado para Linux

### URL: http://localhost:8000/
