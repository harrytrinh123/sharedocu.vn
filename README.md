# Share do cu

  Chia sẻ đồ không dùng nữa cho mọi người
 
### Installing

- Open CMD

```
- cd sharedocu.vn/
```
```
- python -m venv venv
```
```
- activate
```
```
- pip install --upgrade pip
```
```
- pip install -r requirements.txt
```
```
- export FLASK_APP=crudapp.py
```
```
- flask db init
```
```
- flask db migrate -m "entries table"
```
```
- flask db upgrade
```
```
- flask run
```