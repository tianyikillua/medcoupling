import os
import shutil

from invoke import task

VERSION = open("setup.py").readlines()[18].split("\"")[1]


@task
def build_linux(c):
    print(f"Building v{VERSION} for Linux, using Docker")
    basedir = os.path.dirname(os.path.realpath(__file__))
    c.run(f"docker run --rm -v {basedir}:/io -w /io quay.io/pypa/manylinux2010_x86_64 /io/travis/build-wheels.sh")


@task
def build_windows(c):
    print(f"Building v{VERSION} for Windows...")
    shutil.rmtree("dist", ignore_errors=True)
    c.run("python setup.py sdist")
    c.run("python setup.py bdist_wheel --plat-name win_amd64")


@task
def tag(c):
    print(f"Tagging v{VERSION}...")
    c.run(f"git tag v{VERSION}")
    c.run("git push --tags")


@task
def upload(c):
    print("Uploading wheels from dist/* to PyPI...")
    c.run("twine upload dist/*")
