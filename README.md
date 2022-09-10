# No más accidentes
> Sistema de gestión empresarial de prevención de riesgos.
> Repositorio [Github](https://github.com/Portafolio-001D-Caso-4/no-mas-accidentes)

## Tecnologías usadas
- Python 3.9.13
- PostgreSQL 14.5
- Mailhog 1.1.0
- Redis 6.0
- Docker 20.10
- Django

## Requerimientos de instalación
**Ambiente Windows:**
- Docker 20.10 o similar (Recomendamos usar Docker Desktop 4.12.0). Puedes chequearlo con `docker version`
- Docker compose. Puedes chequearlo con `docker-compose --version`
- Git. Puedes chequearlo con `git --version`
- Python 3.6 o superior. Puedes chequearlo con `python -- version`



## Instalación
- Hacer un git clone del proyecto en la rama `main`
	```bash
	git clone https://github.com/Portafolio-001D-Caso-4/no-mas-accidentes.git
	```
- Iniciar servicio de Docker. Si usa Docker Desktop, solo debe iniciar el programa.
- En el root del proyecto, realizar la build del programa utilizando `docker-compose`
	```bash
	docker-compose -f local.yml build
	```
- Iniciar el programa utilizando `docker-compose`
	```bash
	docker-compose -f local.yml up
	```

## Uso

- **Aplicación principal**: `localhost:8000`
	Aplicación en Django, principal producto a utilizar.
	Debes crear un usuario con el siguiente comando:
TODO: Generar script para creación de usuario
- **Base de datos**: `localhost:5432`
	Puedes conectarte a la base de datos utilizando las credenciales ubicadas en `.envs/.local/.postgres` Recomendamos utilizar `PGadmin` como cliente
- **Mailhog**: `localhost:8025`
	 Para ver los correos electrónicos enviados
- **Redis**: `localhost:6379`
	Para conectarse al servicio de storage y cache. Recomendamos utilizar `RedisInsightv-2` como cliente
- **Flower**: `localhost:5555`
	Para conocer el estado de las tareas asíncronas

Si alguno de estos puertos colisiona con algún servicio que estés usando, puedes cambiarlos en las variables de `ports` expuestos en el archivo `local.yml`


## Testing
Para correr los tests, debes utilizar
```bash
docker-compose -f local.yml run --rm django pytest
```
## Estado del proyecto
En progreso, actualmente en la iteración 1 de 3.
