format: 
	poetry run black . && poetry run isort .

mypy:
	poetry run mypy . 

.venv:
	mkdir .venv
	poetry install

clean:
	rm -rf .venv
