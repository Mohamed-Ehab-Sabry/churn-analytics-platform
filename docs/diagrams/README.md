# Diagrams Directory

This directory contains all visual diagrams for the Customer Churn Analytics Platform.

## Required Diagrams

### 1. System Architecture Diagram
**File**: `system_architecture.png` (and source file)

Shows the complete end-to-end system architecture including:
- Data sources (MySQL, MongoDB, CSV files)
- Ingestion layer (Python scripts)
- Analytical warehouse (DuckDB)
- Transformation layer (dbt)
- Orchestration (Airflow)
- Visualization (Dash)
- End users

**Status**: ⏳ Pending creation

See [../DIAGRAMS.md](../DIAGRAMS.md) for detailed requirements and templates.

---

### 2. Data Flow Diagram
**File**: `data_flow_diagram.png` (and source file)

Illustrates data movement through the pipeline with transformations at each stage.

**Status**: ⏳ Pending creation

See [../DIAGRAMS.md](../DIAGRAMS.md) for detailed requirements and templates.

---

### 3. Entity Relationship Diagram (ERD)
**File**: `erd_star_schema.png` (and source file)

Shows the star schema with dimension and fact tables, including:
- fact_churn (center)
- dim_customer
- dim_geography  
- dim_service
- Relationships and cardinality

**Status**: ⏳ Pending creation

See [../DIAGRAMS.md](../DIAGRAMS.md) for detailed requirements and templates.

---

### 4. dbt Model Lineage Graph
**File**: `dbt_lineage_graph.png`

Auto-generated from dbt documentation showing model dependencies.

**Status**: ⏳ Pending generation

To generate:
```bash
cd dbt/churn_analytics
dbt docs generate
dbt docs serve
# Then take screenshot of lineage graph
```

---

## How to Create Diagrams

1. **Read the guide**: Review [../DIAGRAMS.md](../DIAGRAMS.md) for detailed instructions
2. **Choose a tool**: Use Draw.io, Lucidchart, or other diagramming tool
3. **Create diagram**: Follow the templates and guidelines
4. **Export**: Save as PNG (high resolution) and keep source file
5. **Commit**: Add both PNG and source files to this directory

## File Naming Convention

- Use lowercase with underscores: `system_architecture.png`
- Include source files: `system_architecture.drawio`
- Keep versions if needed: `system_architecture_v2.png`

## Quality Standards

- **Resolution**: Minimum 1920x1080 for PNG
- **Format**: PNG for viewing, source format for editing
- **Readability**: Text must be legible at 100% zoom
- **Consistency**: Use consistent colors and styling across diagrams
- **Labels**: All components clearly labeled

## Additional Resources

- ASCII diagrams in [../TECHNICAL.md](../TECHNICAL.md) can serve as reference
- Mermaid code templates in [../DIAGRAMS.md](../DIAGRAMS.md)
- ERD schema definitions in [../TECHNICAL.md](../TECHNICAL.md)

---

*When diagrams are created, update this README to mark them as complete and add preview images if desired.*
