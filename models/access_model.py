from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class AccessParameters:
    """Parameters for the access model"""
    population_demographics: Dict[str, float]
    geographic_distribution: Dict[str, float]
    socioeconomic_factors: Dict[str, float]
    institutional_capacity: Dict[str, float]
    incentive_programs: Dict[str, float]
    physical_infrastructure: Dict[str, float]
    # Growth/change factors - now read from config dict
    annual_enrollment_growth_factor: float = 0.0
    annual_transition_improvement_factor: float = 0.0 
    annual_dropout_reduction_factor: float = 0.0


class AccessModel:
    """Model educational access patterns and enrollment dynamics"""
    
    def __init__(self, parameters: AccessParameters):
        self.parameters = parameters
        # Initialize state variables (will hold the *current* year's value)
        self.current_primary_enrollment = 0.0
        self.current_secondary_transition = 0.0
        self.current_primary_dropout = 1.0
        self.current_secondary_dropout = 1.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        base_primary_enrollment = self.parameters.population_demographics.get('primary_age_population', 0.0)
        infrastructure_factor = self.parameters.physical_infrastructure.get('school_density', 0.0)
        incentive_factor = self.parameters.incentive_programs.get('stipend_coverage', 0.0)
        # Adjusted sensitivity for initial calculation
        self.current_primary_enrollment = min(base_primary_enrollment * (1 + infrastructure_factor * 0.1) * (1 + incentive_factor * 0.1), 1.0)
        
        base_transition_rate = self.parameters.institutional_capacity.get('secondary_schools', 0.0)
        economic_factor = self.parameters.socioeconomic_factors.get('household_income', 0.0)
        geographic_factor = self.parameters.geographic_distribution.get('transportation_access', 0.0) 
        # Adjusted sensitivity for initial calculation
        self.current_secondary_transition = min(base_transition_rate * (1 + economic_factor * 0.1) * (1 + geographic_factor * 0.1), 1.0)
        
        base_dropout_risk = self.parameters.socioeconomic_factors.get('poverty_rate', 0.0)
        infrastructure_risk = 1 - self.parameters.physical_infrastructure.get('school_quality', 0.0)
        incentive_mitigation = self.parameters.incentive_programs.get('dropout_prevention', 0.0)
        # Adjusted sensitivity for initial calculation
        initial_dropout_risk = min(base_dropout_risk * (1 + infrastructure_risk * 0.5) * (1 - incentive_mitigation * 0.5), 1.0)
        self.current_primary_dropout = min(initial_dropout_risk * 0.8, 1.0)
        self.current_secondary_dropout = min(initial_dropout_risk * 1.2, 1.0)
        
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        # Apply growth/improvement factors from parameters
        enrollment_improvement = self.parameters.annual_enrollment_growth_factor * (1 - self.current_primary_enrollment)
        self.current_primary_enrollment = min(self.current_primary_enrollment * (1 + enrollment_improvement) , 1.0)

        transition_improvement = self.parameters.annual_transition_improvement_factor * (1 - self.current_secondary_transition)
        self.current_secondary_transition = min(self.current_secondary_transition * (1 + transition_improvement), 1.0)
        
        dropout_reduction = self.parameters.annual_dropout_reduction_factor
        self.current_primary_dropout = max(self.current_primary_dropout * (1 - dropout_reduction), 0.0) 
        self.current_secondary_dropout = max(self.current_secondary_dropout * (1 - dropout_reduction * 0.8), 0.0)

    def simulate_access_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate access dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'primary_enrollment': self.current_primary_enrollment,
            'secondary_transition': self.current_secondary_transition,
            'primary_dropout': self.current_primary_dropout,
            'secondary_dropout': self.current_secondary_dropout
        })

        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'primary_enrollment': self.current_primary_enrollment,
                'secondary_transition': self.current_secondary_transition,
                'primary_dropout': self.current_primary_dropout,
                'secondary_dropout': self.current_secondary_dropout
            })
        
        return pd.DataFrame(results) 