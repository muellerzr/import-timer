from setuptools import find_packages, setup


extras = {}
extras["quality"] = ["black ~= 23.1", "ruff ~= 0.2.1"]
extras["test"] = ["pytest"]


setup(
    name="import-timer",
    version="0.0.1",
    description="A pragmatic approach to interpreting `importtime` import profiles.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="tuna",
    license="Apache",
    author="Zach Mueller",
    author_email="muellerzr@gmail.com",
    url="https://github.com/muellerzr/import-timer",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.8.0",
    install_requires=[],
    extras_require=extras,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
