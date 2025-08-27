import streamlit as st
import math

# Application domains from the survey
applications = {
    'fermi-hubbard': {
        'name': 'Fermi-Hubbard Model',
        'description': 'Quantum simulation of electronic materials and superconductors',
        'primitives': ['Quantum Phase Estimation', 'Qubitization', 'Block Encoding', 'State Preparation'],
        'complexity': 'O(N log N / ε)',
        'classicalChallenge': 'Exponential scaling for 2D systems'
    },
    'quantum-chemistry': {
        'name': 'Quantum Chemistry',
        'description': 'Molecular ground state energy calculation',
        'primitives': ['Hamiltonian Simulation', 'Variational Quantum Eigensolver', 'Amplitude Amplification'],
        'complexity': 'O(N^3 / ε)',
        'classicalChallenge': 'Exponential scaling with system size'
    },
    'optimization': {
        'name': 'Quantum Optimization',
        'description': 'Solving combinatorial optimization problems',
        'primitives': ['Grover\'s Algorithm', 'Quantum Approximate Optimization', 'Amplitude Amplification'],
        'complexity': 'O(√N)',
        'classicalChallenge': 'NP-hard problems'
    },
    'machine-learning': {
        'name': 'Quantum Machine Learning',
        'description': 'Quantum-enhanced learning algorithms',
        'primitives': ['Quantum Linear Algebra', 'Quantum Principal Component Analysis', 'Quantum Support Vector Machines'],
        'complexity': 'O(log N)',
        'classicalChallenge': 'Feature space dimensionality'
    }
}

def calculate_resources(selected_application, parameters):
    system_size = parameters['systemSize']
    precision = parameters['precision']
    physical_error_rate = parameters['physicalErrorRate']
    hopping_parameter = parameters['hoppingParameter']
    interaction_strength = parameters['interactionStrength']
    
    # Different calculations based on selected application
    if selected_application == 'fermi-hubbard':
        alpha = (2 * hopping_parameter + interaction_strength / 8) * system_size
        logical_gates = alpha * 5 * system_size * math.log2(system_size) / precision
        logical_qubits = system_size + math.log2(system_size)
    elif selected_application == 'quantum-chemistry':
        alpha = system_size * 2
        logical_gates = math.pow(system_size, 3) / precision
        logical_qubits = system_size
    elif selected_application == 'optimization':
        alpha = math.sqrt(system_size)
        logical_gates = math.sqrt(system_size) / precision
        logical_qubits = math.log2(system_size)
    elif selected_application == 'machine-learning':
        alpha = math.log2(system_size)
        logical_gates = math.log2(system_size) * system_size / precision
        logical_qubits = math.log2(system_size)
    else:
        alpha = system_size
        logical_gates = system_size / precision
        logical_qubits = system_size
    
    # Surface code distance calculation
    target_logical_error_rate = 1e-10  # Typical requirement
    surface_code_distance = max(3, math.ceil(math.log(target_logical_error_rate) / math.log(physical_error_rate)))
    
    physical_qubits = 4 * logical_qubits * math.pow(surface_code_distance, 2)
    syndrome_time = 1e-6  # 1 microsecond for superconducting qubits
    total_runtime = logical_gates * surface_code_distance * syndrome_time
    
    # Fault-tolerant overhead
    fault_tolerant_overhead = math.pow(surface_code_distance, 2)
    
    return {
        'logicalGates': round(logical_gates),
        'logicalQubits': round(logical_qubits),
        'physicalQubits': round(physical_qubits),
        'surfaceCodeDistance': surface_code_distance,
        'runtimeHours': total_runtime / 3600,
        'faultTolerantOverhead': fault_tolerant_overhead,
        'alpha': alpha
    }

def format_number(num):
    if num >= 1e9:
        return f"{num / 1e9:.1f}B"
    if num >= 1e6:
        return f"{num / 1e6:.1f}M"
    if num >= 1e3:
        return f"{num / 1e3:.1f}K"
    return f"{num:,.0f}"

# Streamlit app
st.set_page_config(page_title="Quantum Algorithm Analyzer", layout="wide")

st.title("End-to-End Quantum Algorithm Resource Analyzer")
st.markdown("A comprehensive tool for analyzing quantum algorithm resource requirements based on AWS's quantum computing framework")

# Initialize session state
if 'selected_application' not in st.session_state:
    st.session_state.selected_application = 'fermi-hubbard'
if 'parameters' not in st.session_state:
    st.session_state.parameters = {
        'systemSize': 800,
        'precision': 0.0001,
        'physicalErrorRate': 0.001,
        'hoppingParameter': 1.0,  # Ensure float
        'interactionStrength': 8
    }
if 'results' not in st.session_state:
    st.session_state.results = calculate_resources(st.session_state.selected_application, st.session_state.parameters)
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'overview'

# Tabs
tab_overview, tab_calculator, tab_primitives, tab_fault_tolerance = st.tabs(["Overview", "Resource Calculator", "Algorithmic Primitives", "Fault Tolerance"])

with tab_overview:
    st.header("Quantum Algorithm Framework")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("The End-to-End Process")
        st.markdown("""
        1. **Define Customer Problem**: Identify the specific computational task  
        2. **Design Quantum Algorithm**: Build from algorithmic primitives  
        3. **Fault-Tolerant Implementation**: Apply quantum error correction  
        4. **Resource Estimation**: Calculate end-to-end requirements
        """)
    with col2:
        st.subheader("Key Applications")
        for key, app in applications.items():
            st.markdown(f"**{app['name']}**: {app['description']}")

    st.header("Why End-to-End Analysis Matters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("📈 **Realistic Estimates**  \nAccount for all overheads including fault tolerance")
    with col2:
        st.markdown("🧮 **Modular Analysis**  \nUnderstand how primitives combine")
    with col3:
        st.markdown("⚡ **Optimization Insights**  \nIdentify bottlenecks and improvement opportunities")

with tab_calculator:
    st.header("Resource Calculator")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Algorithm Parameters")
        selected_application = st.selectbox(
            "Application Domain",
            options=list(applications.keys()),
            format_func=lambda x: applications[x]['name'],
            index=list(applications.keys()).index(st.session_state.selected_application)
        )
        
        # Update selected application
        if st.session_state.selected_application != selected_application:
            st.session_state.selected_application = selected_application

        system_size = st.slider("System Size (N)", 100, 2000, st.session_state.parameters['systemSize'], step=100)
        precision = st.slider("Required Precision (ε)", 0.00001, 0.01, st.session_state.parameters['precision'], step=0.00001, format="%.5f")
        physical_error_rate = st.slider("Physical Error Rate", 0.0001, 0.01, st.session_state.parameters['physicalErrorRate'], step=0.0001, format="%.4f")

        # Conditionally show sliders for Fermi-Hubbard parameters
        if selected_application == 'fermi-hubbard':
            hopping_parameter = st.slider("Hopping Parameter", 0.1, 10.0, float(st.session_state.parameters['hoppingParameter']), step=0.1)
            interaction_strength = st.slider("Interaction Strength", 1, 20, int(st.session_state.parameters['interactionStrength']))
        else:
            hopping_parameter = float(st.session_state.parameters['hoppingParameter'])
            interaction_strength = int(st.session_state.parameters['interactionStrength'])

        # Update parameters
        new_parameters = {
            'systemSize': system_size,
            'precision': precision,
            'physicalErrorRate': physical_error_rate,
            'hoppingParameter': hopping_parameter,
            'interactionStrength': interaction_strength
        }

        # Check if parameters have changed
        if st.session_state.parameters != new_parameters:
            st.session_state.parameters = new_parameters
            # Automatically recalculate resources
            st.session_state.results = calculate_resources(selected_application, st.session_state.parameters)

        # Manual recalculation button (optional, for user control)
        if st.button("Recalculate Resources"):
            st.session_state.results = calculate_resources(selected_application, st.session_state.parameters)

    with col2:
        st.subheader("Selected Application")
        app = applications[selected_application]
        st.markdown(f"**{app['name']}**  \n{app['description']}  \n**Complexity:** {app['complexity']}  \n**Classical Challenge:** {app['classicalChallenge']}")

    # Display results if available
    if st.session_state.results:
        results = st.session_state.results
        st.subheader("Resource Estimates")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Logical Gates", format_number(results['logicalGates']), "gates")
        col2.metric("Logical Qubits", format_number(results['logicalQubits']), "qubits")
        col3.metric("Physical Qubits", format_number(results['physicalQubits']), "qubits")
        col4.metric("Runtime", f"{results['runtimeHours']:.2f}", "hours")

        st.subheader("Detailed Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fault Tolerance Details**  \n- **Surface Code Distance:** {0}  \n- **Fault-Tolerant Overhead:** {1}x  \n- **Block Encoding Parameter (α):** {2}".format(
                results['surfaceCodeDistance'], format_number(results['faultTolerantOverhead']), results['alpha']))
        with col2:
            st.markdown("**Performance Metrics**  \n- **Logical Error Rate:** ~10⁻¹⁰  \n- **Physical-to-Logical Ratio:** {0}:1  \n- **Gate-to-Time Ratio:** {1} gates/hour".format(
                format_number(results['physicalQubits'] / results['logicalQubits']), format_number(results['logicalGates'] / results['runtimeHours'])))

with tab_primitives:
    st.header("Algorithmic Primitives")
    st.markdown("Building blocks that provide quantum advantage across multiple applications")
    
    col1, col2, col3 = st.columns(3)
    primitives = [
        {"name": "Quantum Phase Estimation", "description": "Estimates eigenvalues of unitary operators with high precision", "complexity": "O(1/ε)"},
        {"name": "Hamiltonian Simulation", "description": "Simulates time evolution under quantum Hamiltonians", "complexity": "O(t²/ε)"},
        {"name": "Amplitude Amplification", "description": "Generalizes Grover's algorithm for amplitude enhancement", "complexity": "O(√N)"},
        {"name": "Quantum Linear Algebra", "description": "Solves linear systems and performs matrix operations", "complexity": "O(log N)"},
        {"name": "Block Encoding", "description": "Encodes matrices into quantum circuits efficiently", "complexity": "O(||A||)"},
        {"name": "Qubitization", "description": "Implements Hamiltonian evolution with optimal scaling", "complexity": "O(||H||)"}
    ]
    for i, prim in enumerate(primitives):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"**{prim['name']}**  \n{prim['description']}  \n*{prim['complexity']}*")

    st.subheader("Primitive Interactions")
    st.markdown("**Modular Design:** Primitives can be combined in plug-and-play fashion")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Common Combinations**  \n- Phase Estimation + Qubitization → Ground State Energy  \n- Amplitude Amplification + Linear Algebra → Quantum ML  \n- Block Encoding + Hamiltonian Simulation → Chemistry")
    with col2:
        st.markdown("**Key Considerations**  \n- Success probabilities compound  \n- Error rates accumulate  \n- Resource requirements multiply")

with tab_fault_tolerance:
    st.header("Fault-Tolerant Implementation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Surface Code Architecture")
        st.markdown("""
        The most widely studied quantum error correction scheme for fault-tolerant quantum computing.  
        - **2D Layout:** Compatible with hardware constraints  
        - **High Threshold:** Tolerates ~1% physical error rates  
        - **Scalable:** Distance scales with required precision  
        - **Overhead:** ~d² physical qubits per logical qubit
        """)
    with col2:
        st.subheader("Resource Scaling")
        st.markdown("""
        Fault tolerance introduces significant but predictable overheads.  
        - **Space:** 4Qd² physical qubits  
        - **Time:** Gd syndrome cycles  
        - **Distance:** d ∝ log(1/ε_target)  
        - **Threshold:** p_phys < p_threshold ≈ 1%
        """)

    if st.session_state.results:
        results = st.session_state.results
        st.subheader("Current Calculation Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Code Distance", results['surfaceCodeDistance'], "Required for target error rate")
        col2.metric("Space Overhead", f"{format_number(results['faultTolerantOverhead'])}x", "Physical to logical qubits")
        col3.metric("Time Overhead", f"{results['surfaceCodeDistance']}x", "Logical to physical operations")

    st.subheader("Hardware Considerations")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Superconducting Qubits**  \n- Fast gate times (~10-100 ns)  \n- Syndrome extraction ~1 μs  \n- 2D connectivity matches surface code  \n- Cryogenic requirements")
    with col2:
        st.markdown("**Trapped Ion Systems**  \n- High-fidelity gates  \n- All-to-all connectivity  \n- Slower gate times (~10-100 μs)  \n- Room temperature operation")

st.markdown("---")
st.markdown("""
Based on "Quantum algorithms: A survey of applications and end-to-end complexities" 
by the AWS Center for Quantum Computing
""", unsafe_allow_html=True)
