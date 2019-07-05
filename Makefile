VERSION=$(shell python -c "print(open('setup.py').readlines()[18].split('\"')[1])")

# https://packaging.python.org/distributing/#id72
upload_win: setup.py
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	rm -f dist/*
	python setup.py sdist
	python setup.py bdist_wheel --plat-name win_amd64
	python -m twine upload dist/*

upload_linux: setup.py
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	rm -f dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel --plat-name manylinux1_x86_64
	python3 -m twine upload dist/*

tag:
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags
