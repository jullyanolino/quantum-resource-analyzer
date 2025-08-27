# Quantum Algorithm Analyzer

![Quantum Analyzer Banner](https://via.placeholder.com/1200x300?text=Quantum+Algorithm+Analyzer) <!-- Replace with actual banner if available -->

A professional Streamlit application for end-to-end analysis of quantum algorithm resource requirements. This tool is based on the AWS Center for Quantum Computing's framework, as detailed in the survey "Quantum algorithms: A survey of applications and end-to-end complexities."

This is a Python/Streamlit port of the original React application, preserving all functionalities including interactive parameter adjustments, resource calculations, and tabbed navigation for overview, calculator, primitives, and fault-tolerance analysis.

## Features

- **Interactive Resource Calculator**: Adjust parameters like system size, precision, and error rates to estimate logical/physical qubits, gates, runtime, and more.
- **Application Domains**: Support for key quantum applications including Fermi-Hubbard Model, Quantum Chemistry, Optimization, and Machine Learning.
- **Algorithmic Primitives**: Detailed views of building blocks like Quantum Phase Estimation, Hamiltonian Simulation, and others.
- **Fault-Tolerance Insights**: Analysis of surface code requirements, overheads, and hardware considerations.
- **Modular Tabs**: Easy navigation between overview, calculator, primitives, and fault-tolerance sections.
- **Realistic Estimates**: Accounts for fault-tolerant overheads and provides formatted, readable outputs.

## Installation

1. Clone the repository:
``` bash
git clone https://github.com/your-repo/quantum-algorithm-analyzer-streamlit.git
cd quantum-algorithm-analyzer-streamlit
```
2. Install dependencies:
``` bash
pip install -r requirements.txt
```
## Usage

Run the application locally:
``` bash
streamlit run app.py
```

- Open your browser at `http://localhost:8501`.
- Select an application domain and adjust sliders to see real-time resource estimates.
- Navigate tabs for in-depth information on quantum primitives and fault tolerance.

## Screenshots

### Overview Tab
![Overview Screenshot](https://via.placeholder.com/800x400?text=Overview+Tab) <!-- Replace with actual screenshot -->

### Resource Calculator
![Calculator Screenshot](https://via.placeholder.com/800x400?text=Resource+Calculator) <!-- Replace with actual screenshot -->

## Technical Details

- **Framework**: Built with Streamlit for rapid web app development.
- **Calculations**: Implements quantum resource estimation formulas for logical gates, qubits, runtime, and error correction overheads.
- **State Management**: Uses Streamlit's session state to persist user inputs and results.
- **Compatibility**: Tested on Python 3.8+.

## Credits

- Original React implementation: [QuantumAlgorithmAnalyzer.tsx](original-source-link) <!-- Link to original if available -->
- Inspired by AWS Center for Quantum Computing's research.

## License

MIT License. See [LICENSE](LICENSE) for details.

For questions or contributions, open an issue or pull request!
