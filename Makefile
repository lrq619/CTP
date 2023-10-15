all : build

generate_proto:
	@cd ctp/ctp_grpc/ && ./build.sh

test: generate_proto
	@pytest

build: test
	@python -m build

upload: build
	@python -m twine upload --repository testpypi dist/*

freeze:
	@pip freeze > requirements.txt

install_dependency:
	@pip install -r requirements.txt

clean:
	@rm dist/*