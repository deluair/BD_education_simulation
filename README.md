# Bangladesh Education Simulation (2025-2035)

This project implements a comprehensive computational simulation model of the education ecosystem in Bangladesh, projecting trends and outcomes from 2025 to 2035. It integrates various factors influencing education access, quality, and equity.

## Overview

The simulation aims to provide insights into the potential evolution of the Bangladeshi education system under different assumptions and potential policy interventions. It models key components of the system and their interactions over a 10-year period, creating a holistic view of how multiple factors influence educational outcomes.

![Bangladesh Education Simulation](https://raw.githubusercontent.com/deluair/BD_education_simulation/main/docs/images/simulation_banner.png)

## Components / Models

The simulation is built upon several interconnected modules:

1. **Access Model (`models/access_model.py`):** Simulates enrollment rates and transition between education levels (primary, secondary, tertiary) based on demographics, geography, socioeconomic factors, institutional capacity, incentives, and infrastructure.

2. **Quality Model (`models/quality_model.py`):** Models educational quality indicators like proficiency in reading and numeracy, influenced by teaching practices, learning environments, assessment systems, and curriculum implementation.

3. **Teacher Model (`models/teacher_model.py`):** Simulates the dynamics of the teacher workforce, including quality, effectiveness, and motivation, based on qualification distribution, experience levels, professional development, workload factors, and motivation indicators.

4. **Institution Model (`models/institution_model.py`):** Models the development and effectiveness of educational institutions based on governance structures, management practices, resource allocation, and institutional culture.

5. **Curriculum Model (`models/curriculum_model.py`):** Simulates the evolution of the curriculum, considering relevance, integration of 21st-century skills, quality of learning materials, and pedagogical innovation.

6. **EdTech Model (`models/edtech_model.py`):** Models the adoption and impact of educational technology, considering digital infrastructure, technology access, digital capacity, and pedagogical integration.

7. **Finance Model (`models/finance_model.py`):** Simulates education financing, including funding adequacy, allocation efficiency, financial management, and the role of alternative financing mechanisms.

## Interactive Visualization

The simulation generates an interactive HTML report with visualizations powered by Plotly:

- **Trend Analysis:** Line charts with markers showing progression of key metrics over time
- **Component Comparison:** Bar charts comparing different aspects of the education system
- **Correlation Heatmap:** Visual representation of relationships between different educational factors
- **Detailed Metrics:** Comprehensive breakdown of means and standard deviations for all tracked indicators

The report uses Bangladesh's national colors (green and red) in its design for a culturally appropriate presentation.

## Configuration

The simulation uses a configuration file (`config/sample_config.py`) to set initial parameters for all models. The current configuration attempts to use realistic baseline data for Bangladesh around the year 2023/2024, sourced from organizations like:

* UNESCO Institute for Statistics (UIS)
* World Bank DataBank
* TheGlobalEconomy.com (often citing UNESCO)
* UNICEF (specifically the "Survey on Children's Education in Bangladesh 2021")
* GPE (Global Partnership for Education)
* Local news reports (e.g., The Daily Star citing BANBEIS)

Where direct data was unavailable, particularly for qualitative aspects or very specific metrics, reasonable placeholders or estimations based on related data points were used. Comments within `config/sample_config.py` indicate the source or basis for many parameters.

**Note:** For high-fidelity results, this configuration should be further refined with more granular and up-to-date data specific to the Bangladeshi context.

## Technical Architecture

The simulation follows a modular, object-oriented design:

- **Parameter Classes:** Each model has an associated dataclass for configuration parameters
- **State Management:** Models maintain internal state that evolves over time
- **Dynamic Calculations:** Composite metrics calculated from multiple underlying factors
- **Annual Updates:** State variables updated with improvement factors and diminishing returns
- **DataFrame Output:** Results provided as pandas DataFrames for flexible analysis
- **Visualization Engine:** Custom report generator using Plotly for interactive charts

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/deluair/BD_education_simulation.git
   cd BD_education_simulation
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

To run the simulation with the default configuration and generate the report:

```bash
python run_simulation.py
```

This will:

1. Initialize all models with parameters from `config/sample_config.py`.
2. Run the simulation for the specified number of years (default: 10).
3. Analyze the results, calculating mean and standard deviation for key metrics.
4. Generate an interactive HTML report.

## Output

The primary output is an interactive HTML report file located at:

* `output/simulation_report.html`

This report contains:

* An executive summary with key metrics displayed as cards.
* Interactive trend plots for key metrics within each model component over the simulation period.
* A bar chart comparing key metrics across components in the final simulation year.
* A correlation heatmap showing relationships between components based on time series data.
* A detailed analysis section with summary statistics for key metrics.

## Research Applications

This simulation framework can be used for:

- Projecting long-term educational outcomes based on current conditions
- Testing hypothetical policy interventions before implementation
- Understanding complex interactions between different aspects of the education system
- Identifying high-leverage factors that may have outsized impacts on outcomes
- Building evidence-based arguments for educational investments

## Future Work

* Integrate more granular, validated data for Bangladesh.
* Implement policy intervention scenarios with UI controls.
* Refine model interactions and feedback loops.
* Add geospatial visualization for regional disparities.
* Develop machine learning components to improve predictive accuracy.
* Add unit tests and further validation.
* Create a web-based interface for non-technical users.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* University of Tennessee research initiative
* Bangladeshi education experts who provided domain knowledge
* Open-source data providers including UNESCO, World Bank, and UNICEF 