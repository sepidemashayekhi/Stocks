python -m venv venv
call .\venv\Scripts\activate.bat
python -m pip install -r requirements.txt

python models.py


python SQLFunction.py
python data.py
python -m uvicorn services.api:app --reload
