clean:
	@rm -rf .coverage coverage.xml htmlcov report.xml
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

format:
	@pre-commit run --all-files

generate_requirements:
	@poetry export --without-hashes -f requirements.txt > app/requirements.txt

check_requirements: generate_requirements
	@git diff --quiet app/requirements.txt

test:
	@pytest app -s --cov=app --cov-config=app/.coveragerc

migrate:
	@yc serverless function invoke keepintouch-bot -d '{"command_name": "migrate"}'

set_up_commands:
	@yc serverless function invoke keepintouch-bot -d '{"command_name": "set_up_commands"}'

notify_keepintouch:
	@yc serverless function invoke keepintouch-bot -d '{"command_name": "notify_keepintouch"}'
