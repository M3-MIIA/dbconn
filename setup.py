from setuptools import setup, find_packages

setup(
    name='dbconn',
    version='2.0',
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary',
        'SQLAlchemy',
        'boto3',
        'botocore'
    ],
)