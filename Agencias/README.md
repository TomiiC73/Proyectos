# Sistema de Gestión de Agencias de Vehículos

Sistema backend para gestión de pruebas de vehículos en agencias automotrices. Implementa una arquitectura de microservicios con Spring Boot y Spring Cloud.

## 📋 Descripción

Aplicación que permite a las agencias de vehículos gestionar y realizar pruebas de diferentes modelos. El sistema incluye endpoints para todas las operaciones necesarias y cuenta con un sistema completo de autenticación y autorización.

## 🏗️ Arquitectura

El proyecto está dividido en tres microservicios:

- **Api-Gateway**: Puerta de enlace que gestiona el enrutamiento a los diferentes servicios
- **Pruebas**: Servicio principal que gestiona las pruebas de vehículos, posiciones, configuraciones de APIs externas, etc.
- **Notificaciones**: Servicio dedicado a la gestión y envío de notificaciones

## 🔧 Tecnologías

- **Framework:** Spring Boot
- **Gateway:** Spring Cloud Gateway
- **Seguridad:** OAuth2 Resource Server
- **Base de Datos:** JPA/Hibernate
- **Build Tool:** Maven

## 🚀 Uso

Se incluye una colección de Postman (`TP BACK.postman_collection.json`) con todos los endpoints disponibles para facilitar las pruebas del sistema. La colección incluye las configuraciones necesarias para la autenticación.

## 📁 Estructura

```
Api-Gateway/     - Servicio de gateway
Notificaciones/  - Servicio de notificaciones
Pruebas/         - Servicio principal de gestión de pruebas
```

## 🔐 Seguridad

El sistema implementa OAuth2 para asegurar todos los endpoints y gestionar la autenticación y autorización de usuarios.

---

## 📝 Notas del Proyecto

El trabajo consta de una agencia que quiere llevar a cabo una serie de acciones con las pruebas de cada vehículo. Se puede observar que posee endpoints para realizar cada tarea. Se adjunta el enunciado del trabajo para tener más claridad sobre la resolución. También el archivo "TP BACK.postman_collection" es un archivo de Postman para probar todos y cada uno de los endpoints, y posee todo lo necesario para llevar a cabo el aspecto de la seguridad de la aplicación.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
