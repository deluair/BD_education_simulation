#!/usr/bin/env python
"""
Run script for Bangladesh Education Simulation
"""

from config.sample_config import SAMPLE_CONFIG
from simulation.main import BangladeshEducationSimulation
import os
import time

def main():
    try:
        start_time = time.time()
        
        # Create simulation instance with sample configuration
        print("Initializing Bangladesh Education Simulation (2025-2050)...")
        simulation = BangladeshEducationSimulation(SAMPLE_CONFIG)
        
        # Set output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "simulation_report.html")
        
        # Run simulation and get results
        print("Running simulation...")
        results = simulation.run_simulation()
        
        # Analyze results
        print("Analyzing results...")
        analysis = simulation.analyze_results(results)
        
        # Generate report
        print("Generating report...")
        simulation.generate_report(results, analysis, output_path)
        
        end_time = time.time()
        
        print(f"Simulation completed in {end_time - start_time:.2f} seconds.")
        print(f"Report saved to: {output_path}")
        
        # Print a summary of key metrics
        print("\n===== SIMULATION SUMMARY =====")
        print(f"Average Teacher Quality Index: {analysis.get('Average Teacher Quality', 'N/A'):.3f}")
        print(f"Average Curriculum Relevance: {analysis.get('Average Curriculum Relevance', 'N/A'):.3f}")
        print(f"Average Digital Infrastructure: {analysis.get('Average Digital Infrastructure', 'N/A'):.3f}")
        print(f"Average Funding Adequacy: {analysis.get('Average Funding Adequacy', 'N/A'):.3f}")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 