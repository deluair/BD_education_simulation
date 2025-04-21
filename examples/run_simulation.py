import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.main import BangladeshEducationSimulation
from config.sample_config import SAMPLE_CONFIG

def main():
    # Initialize the simulation
    simulation = BangladeshEducationSimulation(SAMPLE_CONFIG)
    
    # Run the simulation
    print("Running Bangladesh Education Simulation (2025-2050)...")
    results = simulation.run_simulation()
    
    # Analyze the results
    analysis = simulation.analyze_results(results)
    
    # Generate and print the report
    report = simulation.generate_report(results, analysis)
    print("\n" + report)
    
    # Save results to CSV files
    for component, df in results.items():
        filename = f"results_{component}.csv"
        df.to_csv(filename, index=False)
        print(f"\nSaved {component} results to {filename}")

if __name__ == "__main__":
    main() 