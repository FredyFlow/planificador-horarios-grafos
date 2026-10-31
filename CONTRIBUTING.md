# Guía de Contribución y Flujo de Trabajo Git (ESPOCH)

Este documento regula el flujo de trabajo colaborativo en Git para los **6 integrantes del equipo**, cumpliendo estrictamente la **Sección 7.3 y 9.3 del Instructivo**:
- Mínimo **20 commits descriptivos** distribuidos equitativamente entre los 6 integrantes antes de la entrega final.
- Uso obligatorio de **ramas (`branches`)** por funcionalidad o rol y **Pull Requests (PRs)** documentados antes de fusionar a `main`.

---

## 1. Estructura de Ramas (Gitflow Ligero)
- `main`: Rama principal estable (entregables verificados de cada Fase).
- `develop`: Rama de integración continua del Sprint.
- Ramas de trabajo por integrante/funcionalidad (Grupo 3):
  - `chore/gestion-backlog-y-ejemplos` (**Fredy Jamphier Cárdenas Peñafiel** — Líder / Product Owner)
  - `feature/modelo-matematico-formal` (**Giovanni Isarel Gavilanes Gavilanes** — Matemático / Modelador Formal)
  - `feature/pruebas-y-verificacion-formal` (**Danixa Juleydi Rodas Riofrío** — QA Engineer / Verificador)
  - `feature/algoritmos-welsh-powell-dsatur` (**Joseph Isaías Cuñas Guilcapi** — Desarrollador de Algoritmos)
  - `docs/informe-latex-y-devops` (**William Mauricio Tigasi Toaquiza** — Documentador / DevOps)
  - `feature/interfaz-web-visualizador` (**Geomayra Alexandra Vilca Vilca** — Desarrollador Full Stack / UI)

---

## 2. Convención de Mensajes de Commit
Utilizamos **Conventional Commits** en español o inglés para que el historial sea claro y auditable por la docente:
- `feat(core): implementar selección por grado de saturación en DSatur`
- `math(docs): añadir demostración por inducción de la cota Delta(G) + 1`
- `test(verifier): agregar prueba de grafo completo K_5 y ciclo impar C_5`
- `feat(ui): renderizar grafo coloreado en SVG e historial de pasos`
- `docs(readme): actualizar tabla de correspondencia formalismo-software`

---

## 3. Comandos Paso a Paso para cada Integrante
1. Clonar el repositorio y ubicarse en la rama `develop`:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd planificador-horarios-grafos
   git checkout -b feature/nombre-de-tu-tarea
   ```
2. Realizar tus cambios, ejecutar las pruebas (`pytest`) y registrar commits descriptivos:
   ```bash
   pytest
   git add .
   git commit -m "feat(modulo): descripción clara del aporte"
   git push -u origin feature/nombre-de-tu-tarea
   ```
3. Abrir un **Pull Request** en GitHub hacia `develop` o `main`, completando la plantilla automática y solicitando revisión de otro compañero.
