# Proyecto Invertir Pinamar

[![Python Version](https://img.shields.io/badge/python-3.9.6-brightgreen.svg)](https://www.python.org/downloads/release/python-396/)
[![Django Version](https://img.shields.io/badge/django-3.2-brightgreen.svg)](https://www.djangoproject.com/)
[![Build Status](https://travis-ci.org/yourname/projectname.svg?branch=master)](https://travis-ci.org/yourname/projectname)

Proyecto  Invertir Pinamar es una aplicación web basada en Django para administrar y gestionar el stock ...

## Table of Contents

- [Instaladores](#instaladores)
- [Instalación](#instalación)
- [Uso](#uso)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Instaladores

#### Compilador

- [Python3](https://www.python.org/downloads/release/python-396/ "Python3")

#### IDE

- [Visual Studio Code](https://code.visualstudio.com/ "Visual Studio Code")
- [Sublime Text](https://www.sublimetext.com/ "Sublime Text")
- [Pycharm](https://www.jetbrains.com/es-es/pycharm/download/#section=windows "Pycharm")

#### Motor de base de datos

- [Sqlite Studio](https://github.com/pawelsalawa/sqlitestudio/releases "Sqlite Studio")
- [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads "PostgreSQL")
- [MySQL](https://www.apachefriends.org/es/index.html "MySQL")

## Instalación

#### Clonar repositorio 

#### Crear un entorno virtual para posteriormente instalar las librerias del proyecto

- `python3 -m venv venv` (Linux o Windows)

#### Instalar el complemento de [weasyprint](https://weasyprint.org/ "weasyprint")

- Si estas usando Windows debe descargar el complemento de [GTK3 installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases "GTK3 installer"). En algunas ocasiones se debe colocar en las variables de entorno como primera para que funcione y se debe reiniciar el computador.
- Si estas usando Linux debes instalar las [librerias](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux "librerias") correspondientes a la distribución que tengas instalado en tu computador.

#### Activar el entorno virtual de nuestro proyecto

- `cd venv\Scripts\activate.bat` (Windows)
- `source venv/bin/active` (Linux)

#### Instalar todas las librerias del proyecto que se encuentran en la carpeta deploy

- `pip install -r deploy/requirements.txt`

#### Crear la base de datos con las migraciones y el superuser para iniciar sesión

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`

#### Insertar información inicial en la base de datos

- `python manage.py shell`
- `from core.utilities import *`

## Uso

Descripción de como usar el proyecto...

## Contribuir

Si quieres contribuir a este proyecto...


