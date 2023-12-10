format: 
	poetry run black . 
	poetry run autoflake .
	poetry run isort .

mypy:
	poetry run mypy . 

.venv: pyproject.toml
	mkdir .venv
	poetry install

clean:
	rm -rf .venv
