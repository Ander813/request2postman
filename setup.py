from distutils.core import setup


with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()


setup(
    name="request2postman",
    packages=["request2postman"],
    version="0.1.1",
    license="MIT",
    description="Lib that generates postman collections out of requests",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Egor Gondurov",
    author_email="ander_the_wood@mail.ru",
    url="https://github.com/Ander813",
    download_url="https://github.com/Ander813/request2postman/archive/refs/tags/0.1.0.tar.gz",
    keywords=["requests", "postman", "generate postman collections"],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
