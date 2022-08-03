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
	pytest app -s

deploy: clean generate_requirements
	@yc serverless function version create --function-name=keepintouch-bot --service-account-id=ajesbmo4lf82ltn2oc0j --runtime python39 --entrypoint manage.handler --memory 128m --execution-timeout 20s --source-path app

run:
	@yc serverless function invoke keepintouch-bot
