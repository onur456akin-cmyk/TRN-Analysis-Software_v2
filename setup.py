from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="trn-analysis-software",
    version="0.1.0",
    author="Onur Akin",
    author_email="onur456akin-cmyk@example.com",
    description="Professional acoustic analysis software for Target Radiated Noise calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onur456akin-cmyk/TRN-Analysis-Software_v2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "trn-analysis=src.main:main",
        ],
    },
    include_package_data=True,
)
