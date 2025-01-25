# Family Tree Visualization Tool

This project is a Python-based tool for visualizing family relationships as an interactive family tree. It processes input data from a CSV file and generates a web-accessible HTML file showing the family tree with detailed information for each individual.

## Features

- **Interactive Family Tree Visualization**: Nodes represent family members, and edges represent parent-child relationships.
- **Level and Overall Numbering**:
  - Each individual is assigned a level in the family hierarchy (e.g., Parent, Child, Grandchild).
  - Level-based numbering (e.g., Grandchild 1, Grandchild 2).
  - Overall numbering based on date of birth (oldest to youngest, with alphabetical tie-breaking).
- **HTML Output**: Generates an interactive family tree viewable in any web browser.
- **CSV Export**: Outputs an enriched CSV file with level and numbering information for easy reference.

## Requirements

- Python 3.7+
- Libraries: Install the dependencies using the provided `requirements.txt`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/esola-thomas/family-tree-visualization.git
   cd family-tree-visualization

## Run instructions

`make` or `make all`