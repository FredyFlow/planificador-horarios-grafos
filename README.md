# Planificador de Horarios y Asignación de Recursos sin Conflictos mediante Coloración de Grafos
### *Conflict-Free Academic Timetable & Resource Scheduler via Graph Coloring*

[![Tests - Fase 3](https://img.shields.io/badge/tests-passing%20(Fase%203)-brightgreen)](#4-ejecución-de-pruebas-automatizadas--running-automated-tests)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Matemáticas Discretas](https://img.shields.io/badge/ESPOCH-Matem%C3%A1ticas%20Discretas%20PAO%203-red)](#1-descripción-del-proyecto-y-base-matemática-discreta--project-description)

> **Institución / Institution:** Escuela Superior Politécnica de Chimborazo (ESPOCH)  
> **Facultad / Faculty:** Facultad de Informática y Electrónica — Carrera de Ingeniería de Software  
> **Asignatura / Course:** Matemáticas Discretas para Ingeniería de Software (PAO 3)  
> **Docente / Instructor:** Mg. Miriam Ávila  
> **Grupo / Team:** Grupo 3  
> **Estado Actual / Current Status:** Fase 3 — Investigación Formativa (Prototipo Preliminar)

---

## 🇪🇸 Versión en Español

### 1. Descripción del Proyecto y Base Matemática Discreta

En los sistemas de gestión académica universitaria (como la planificación semestral de asignaturas en la ESPOCH), la asignación de franjas horarias y aulas/laboratorios a materias que comparten **docente**, **nivel curricular (PAO)**, **grupos de estudiantes** o **infraestructura física** suele generar colisiones críticas de simultaneidad.

Este proyecto resuelve el problema modelando las restricciones como un **Grafo Simple No Dirigido de Conflictos** $G = (V, E)$:
- **Conjunto de vértices ($V$):** Representa las asignaturas o eventos académicos $V = \{v_1, v_2, \dots, v_n\}$.
- **Conjunto de aristas ($E$):** Pares no ordenados $\{u, v\} \in E$ inducidos por el predicado lógico simétrico e irreflexivo de conflicto $P(u, v)$, el cual es verdadero si y solo si $u \neq v$ y comparten docente, nivel/PAO, aula o grupo estudiantil.
- **$k$-Coloración Propia y Número Cromático $\chi(G)$:** Una función $c: V \to \{1, 2, \dots, k\}$ tal que $\forall \{u, v\} \in E, c(u) \neq c(v)$. Cada clase de color $C_i = c^{-1}(\{i\})$ constituye un **conjunto independiente** libre de choques y equivale a una **franja horaria válida**. El mínimo número de franjas horarias necesarias es el número cromático $\chi(G)$, acotado teóricamente por:
  $$\omega(G) \le \chi(G) \le \Delta(G) + 1$$
  donde $\omega(G)$ es el tamaño del clique máximo y $\Delta(G) = \max_{v \in V} \deg_G(v)$ es el grado máximo del grafo.
- **Algoritmos del Núcleo Discreto:** Se desarrolla desde cero (sin librerías de grafos de caja negra) el algoritmo voraz de **Welsh-Powell** (implementado en esta Fase 3 por ordenamiento decreciente de grado $\deg_G(v)$) y el algoritmo dinámico **DSatur de Brélaz** basado en el grado de saturación $d_{\text{sat}}(v) = |\{c(u) \mid u \in N_G(v) \setminus U\}|$ (donde $U$ es el conjunto de vértices no coloreados; planificado para el Sprint 2).

---

### 2. Estructura del Repositorio y Estado por Fases

```text
planificador-horarios-grafos/
├── .github/
│   ├── workflows/ci.yml              # Pipeline CI/CD (GitHub Actions + pruebas automatizadas)
│   └── PULL_REQUEST_TEMPLATE.md      # Plantilla de Pull Requests por rol
├── data/
│   ├── dataset_espoch_6_asignaturas.json  # Ejemplo mínimo trabajado (6 asignaturas ESPOCH)
│   └── dataset_espoch_6_asignaturas.csv   # Versión CSV equivalente
├── docs/
│   └── investigacion_formativa/
│       ├── main.tex                  # Documento en LaTeX para Overleaf (Fase 3)
│       ├── logo_espoch.png           # Escudo institucional ESPOCH
│       └── logo_fie.png              # Escudo de la Facultad (FIE)
├── src/
│   ├── models/course.py              # [Implementado Fase 3] Entidades y predicado P(u, v)
│   ├── core/
│   │   ├── graph.py                  # [Implementado Fase 3] Grafo G=(V,E) y matriz A_G (Clique en Sprint 2)
│   │   ├── coloring.py               # [Implementado Fase 3] Prototipo Welsh-Powell (DSatur en Sprint 2)
│   │   └── verifier.py               # [Implementado Fase 3] Verificador de coloración propia y cota superior
│   ├── utils/loader.py               # [Implementado Fase 3] Parsers de archivos JSON y CSV
│   ├── api/app.py                    # [Esqueleto Fase 3] API FastAPI (Endpoints de carga en Sprint 3)
│   └── ui/templates/index.html       # [Esqueleto Fase 3] Plantilla base UI (Renderizado SVG en Sprint 3)
├── tests/                            # Suite de pruebas automatizadas (unittest / pytest)
│   ├── test_graph.py
│   ├── test_coloring_algorithms.py
│   └── test_mathematical_properties.py
├── CONTRIBUTING.md                   # Guía de ramas y commits para los 6 integrantes
├── pyproject.toml                    # Configuración del paquete y pytest
├── requirements.txt                  # Dependencias de Python
└── README.md                         # Documentación bilingüe (Español / Inglés)
```

---

### 3. Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio y crear el entorno virtual:**
   ```bash
   git clone https://github.com/FredyFlow/planificador-horarios-grafos.git
   cd planificador-horarios-grafos
   python -m venv .venv
   # En Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # En Linux / macOS:
   source .venv/bin/activate
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor preliminar (Fase 3):**
   ```bash
   uvicorn src.api.app:app --reload --port 8000
   ```
   Consultar `http://127.0.0.1:8000/api/example` para inspeccionar la salida JSON del ejemplo trabajado de 6 asignaturas resuelto por `WelshPowellColoring`.

---

### 4. Ejecución de Pruebas Automatizadas

La suite de pruebas en `/tests` puede ejecutarse con `pytest` o directamente con la librería estándar `unittest`:

```bash
python -m unittest discover -s tests -v
# O con pytest y reporte de cobertura:
pytest --cov=src --cov-report=term-missing
```

---

### 5. Equipo de Trabajo y Roles — Grupo 3 (Sección 3 del Instructivo)

| N.º | Rol en el Equipo | Especialidad Técnica | Integrante | Correo Institucional |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Líder / Product Owner** | Gestión ágil (Scrum) y coordinación | **Fredy Jamphier Cárdenas Peñafiel** | `fredy.cardenas@espoch.edu.ec` |
| 2 | **Matemático / Modelador Formal** | Formalización matemático-discreta | **Giovanni Isarel Gavilanes Gavilanes** | `giovanni.gavilanes@espoch.edu.ec` |
| 3 | **QA Engineer / Verificador** | Pruebas y validación formal | **Danixa Juleydi Rodas Riofrío** | `danixa.rodas@espoch.edu.ec` |
| 4 | **Desarrollador de Algoritmos** | Implementación de Welsh-Powell y DSatur | **Joseph Isaías Cuñas Guilcapi** | `darwin.cunias@espoch.edu.ec` |
| 5 | **Documentador / DevOps** | Informe LaTeX, Git y pipeline CI/CD | **William Mauricio Tigasi Toaquiza** | `willia.tigasi@espoch.edu.ec` |
| 6 | **Desarrollador Full Stack / UI** | Integración FastAPI y visualización web | **Geomayra Alexandra Vilca Vilca** | `geomayra.vilca@espoch.edu.ec` |

---
---

## 🇬🇧 English Version

### 1. Project Description & Discrete Mathematics Foundation

In university academic management systems, scheduling courses into time slots and classrooms without collisions is a combinatorial challenge known as the *University Course Timetabling Problem (UCTP)*. Whenever two courses share the same **professor**, **academic semester (PAO)**, **student group**, or **specialized laboratory**, they cannot be scheduled simultaneously.

This project formalizes and solves the problem using **Graph Theory and Vertex Coloring**:
- **Conflict Graph $G = (V, E)$:** Courses are modeled as vertices $V = \{v_1, \dots, v_n\}$, and pairwise incompatibilities determined by the symmetric, irreflexive predicate $P(u, v)$ are modeled as undirected edges $\{u, v\} \in E$.
- **Proper $k$-Coloring & Chromatic Number $\chi(G)$:** A mapping $c: V \to \{1, \dots, k\}$ such that $\forall \{u, v\} \in E, c(u) \neq c(v)$. Each color class $C_i = \{v \in V \mid c(v) = i\}$ forms an **independent set** representing a conflict-free time slot. The minimum number of required time slots is the chromatic number $\chi(G)$, bounded by $\omega(G) \le \chi(G) \le \Delta(G) + 1$.
- **From-Scratch Algorithmic Core:** Phase 3 implements the data structures for $G=(V,E)$, the adjacency matrix $A_G$, the **Welsh-Powell** greedy coloring prototype, and the formal property verifier (`verifier.py`). **Brélaz's DSatur** ($d_{\text{sat}}(v) = |\{c(u) \mid u \in N_G(v) \setminus U\}|$), exact clique bound computation ($\omega(G)$), and the interactive SVG web visualizer are scheduled for Sprints 2 and 3.

### 2. Running Automated Tests

```bash
python -m unittest discover -s tests -v
```
