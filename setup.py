import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='agendamentos',
    version='1.0.0',
    url='https://github.com/ceb10n/agendamentos',
    license='MIT',
    maintainer='Rafael Marques',
    maintainer_email='rafaelomarques@gmail.com',
    description='Projeto simples para gerenciamento de agendamento de salas.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'bcrypt',
        'flasgger',
        'flask-sqlalchemy',
        'marshmallow',
        'passlib',
        'python-dotenv'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)