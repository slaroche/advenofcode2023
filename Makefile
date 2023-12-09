format: 
	poetry run black . && poetry run isort .

mypy:
	poetry run mypy . 
