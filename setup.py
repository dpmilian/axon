import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axon-dpmilian",
    version="0.0.5",
    author="Daniel Perez",
    author_email="dperez@scrobotics.es",
    description="hub with zmq suscriber broker with influxdb time logging backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpmilian/scrubb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['zmq', 'tornado', 'influxdb'],
)


