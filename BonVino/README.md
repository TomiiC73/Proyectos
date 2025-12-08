# BonVino - Sistema de Ranking de Vinos

Aplicación web para gestión de bodegas de vino que permite generar rankings de los mejores vinos basados en reseñas de sommeliers.

## 📋 Descripción

Sistema desarrollado como trabajo práctico integrador de Diseño de Sistemas de Información. Permite a las bodegas consultar un ranking de los 10 mejores vinos filtrados por reseñas de sommeliers dentro de un período específico de fechas.

## 🎯 Funcionalidad Principal

- Generación de ranking de vinos según reseñas de sommeliers
- Filtrado por rango de fechas
- Búsqueda y navegación de vinos y reseñas mediante patrón Iterator

## 🏗️ Arquitectura

El proyecto implementa el **Patrón Iterator** para realizar búsquedas eficientes de vinos y reseñas, demostrando la aplicación práctica de patrones de diseño.

### Estructura del Proyecto

- **Backend**: API REST desarrollada en Spring Boot con JPA/Hibernate
- **Frontend**: Interfaz de usuario desarrollada en React

## 🔧 Tecnologías

**Backend:**
- Spring Boot
- JPA/Hibernate
- Maven
- MySQL (configurado en persistence.xml)

**Frontend:**
- React 18
- JavaScript

## 📁 Componentes Principales

### Backend
- `Entidades`: Bodega, Vino, Reseña, Varietal, Región Vitivinícola, Provincia, País
- `Gestor`: GestorRankingVinos (lógica de negocio)
- `Patrón Iterator`: IteradorVinos, IteradorReseñas
- `Controllers`: ReporteController
- `Interfaces`: InterfazExcel, InterfazPDF para exportación de reportes

### Frontend
- `ReporteForm.js`: Formulario para generar reportes de ranking

## 🚀 Ejecución

**Backend:**
```bash
cd Backend
./mvnw spring-boot:run
```

**Frontend:**
```bash
cd Frontend
npm install
npm start
```

---

## 📝 Notas del Proyecto

Este fue un trabajo práctico integrador de la materia Diseño de Sistemas de Información, en la que el dominio era unas bodegas de vinos que necesitaban realizar un ranking de los 10 mejores vinos según ciertos requisitos (que sea de sommelier y que esté dentro de unas fechas determinadas la reseña), en la que se aplicó el patrón iterador para realizar la búsqueda de vinos y reseñas.
