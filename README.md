pip install -r requirements.txt
pytest -m smoke

pytest -m smoke --browser chromium
pytest -m "ui and regression" --browser chromium
pytest -m readonly --browser chromium
pytest tests/ui --browser chromium
