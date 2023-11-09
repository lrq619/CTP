PACKAGE_NAME = cthenp
VERSION = $(shell hatch version)
WHL_FILE = dist/$(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl

all : build

generate_proto:
	@cd ctp/ctp_grpc/ && ./build.sh


build: generate_proto freeze
	@python -m build

install: build
	@pip uninstall -y cthenp
	@pip install $(WHL_FILE) 

test: install
	@pytest

upload: test
	@python -m twine upload --repository testpypi $(WHL_FILE)


freeze:
	@pip freeze > requirements.txt

install_dependency:
	@pip install -r requirements.txt

clean:
	@rm dist/*