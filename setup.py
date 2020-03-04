from setuptools import setup, find_packages

setup(
    name="tsd",
    version="0.1a1",
    description="Terminal Smart Display",
    url="https://github.com/hjalves/tsd",
    author="Humberto Alves",
    author_email="hjalves@live.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["tsd = tsd.app:main",]},
    install_requires=["hbmqtt==0.9.6", "urwid==2.1.0", "emoji==0.5.4", "toml==0.10.0"],
    # include_package_data=True,
    zip_safe=False,
)
