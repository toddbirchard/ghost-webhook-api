SRCPATH := pwd

if [ -d ".venv" ] then;
    source .venv/bin/activate
    python3 -m pip install -r requirements.txt
    exit
fi