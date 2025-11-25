# Device Info Collector

This script python get info computer on Windows (CPU, Mainboard, RAM, Disk, GPU) and save to folder share by "computer name/username"

---

## Create env and active
```python
python -m env env
.\venv\Scripts\activate.bat
```

## Install lib

```python
pip install pyinstaller
```

---

## Build to exe file

```python
pyinstaller --onefile main.py
```