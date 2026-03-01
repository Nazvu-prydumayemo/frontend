# TUI Frontend (Textual + FastAPI Backend)

## 1. Create virtual environment

### 1. Windows

```bash
py -m venv .venv
```

### 2. Linux/MacOS

```bash
python3 -m venv .venv
```

## 2. Start virtual environment

### 1. Windows

```bash
.venv\Scripts\activate
```

### 2. Linux/MacOS

```bash
source .venv/bin/activate
```

## 3. Install dependencies

### 1. Windows

```bash
py -m pip install -e ".[dev]"
```

### 2. Linux/MacOS

```bash
pip3 install -e ".[dev]"
```

## 4. Run the app

### 1. Windows

```powershell
./tasks.ps1 run
```

### 2. Linux/MacOS

```bash
python3 -m tuiapp.main
```

## 5. Lint and format

### 1. Windows

```powershell
./tasks.ps1 lint
./tasks.ps1 format
```

### 2. Linux/MacOS

```bash
ruff check .
ruff format .
```
