import os

from invoke import task

VERSION = None
with open("setup.py") as fh:
    for line in fh:
        if line.startswith("__version__"):
            VERSION = eval(line.partition(" = ")[2])
            break
assert VERSION is not None


@task
def build(c):
    print(f"Building source distribution...")
    c.run("python setup.py sdist")


@task
def build_linux(c):
    print(f"Building v{VERSION} for Linux, using Docker...")
    basedir = os.path.dirname(os.path.realpath(__file__))
    c.run(
        f"docker run --rm -v {basedir}:/io -w /io quay.io/pypa/manylinux2014_x86_64 /io/travis/build-wheels.sh"
    )


@task
def build_windows(c):
    print(f"Building v{VERSION} for Windows...")
    c.run("python setup.py bdist_wheel --plat-name win_amd64")


@task
def build_macos(c):
    print(f"Building v{VERSION} for macOS...")
    c.run("python3 setup.py bdist_wheel --plat-name macosx_10_11_x86_64")


@task
def tag(c):
    print(f"Tagging v{VERSION}...")
    c.run(f"git tag v{VERSION}")
    c.run("git push --tags")


@task
def upload(c):
    print("Uploading wheels from dist/* to PyPI...")
    c.run("twine upload dist/*")
