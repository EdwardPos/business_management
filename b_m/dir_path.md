cd d:\PythonProjects\business_management\b_m\

dir
uvicorn db_create:app --reload
uvicorn main:app --reload
uvicorn auth:app --reload --port 9000