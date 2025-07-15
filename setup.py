import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

setuptools.setup(
    name="SuperClaude",
    version=version,
    author="Mithun Gowda B, NomenAK",
    author_email="contact@superclaude.dev",
    description="SuperClaude Framework Management Hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NomenAK/SuperClaude",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": [
            "SuperClaude=SuperClaude.__main__:main",
        ],
    },
    python_requires=">=3.6",
    project_urls={
        "GitHub": "https://github.com/NomenAK/SuperClaude",
        "Mithun Gowda B": "https://github.com/mithun50",
        "NomenAK": "https://github.com/NomenAK",
        "Bug Tracker": "https://github.com/NomenAK/SuperClaude/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
)
