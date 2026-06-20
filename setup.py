from setuptools import setup, find_packages

setup(
    name="sayanox-one",
    version="1.0.0",
    author="Sayanox Team",
    description="All‑in‑One Autonomous Penetration Testing Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR‑USERNAME/Sayanox‑One",
    license="MIT",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "sayanox=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Android :: Termux",
        "Topic :: Security",
        "Intended Audience :: Security Professionals",
    ],
    python_requires=">=3.8",
)
