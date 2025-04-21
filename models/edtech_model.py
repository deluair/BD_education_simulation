from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class EdTechParameters:
    """Parameters for the edtech model"""
    infrastructure_development: Dict[str, float]
    technology_access: Dict[str, float]
    digital_capacity: Dict[str, float]
    pedagogical_integration: Dict[str, float]
    # Growth/change factors - read from config dict
    annual_infra_improvement_factor: float = 0.0
    annual_competency_improvement_factor: float = 0.0
    annual_content_improvement_factor: float = 0.0
    annual_adoption_improvement_factor: float = 0.0

class EdTechModel:
    """Model educational technology adoption and impact"""
    
    def __init__(self, parameters: EdTechParameters):
        self.parameters = parameters
        # Initialize state variables
        self.current_digital_infrastructure = 0.0
        self.current_teacher_digital_competency = 0.0
        self.current_digital_content = 0.0
        self.current_emerging_tech_adoption = 0.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        # Digital Infrastructure
        base_infra = self.parameters.infrastructure_development.get('connectivity', 0.0)
        access_factor_infra = self.parameters.technology_access.get('device_availability', 0.0)
        capacity_factor_infra = self.parameters.digital_capacity.get('technical_support', 0.0)
        self.current_digital_infrastructure = min(base_infra * (1 + access_factor_infra * 0.2) * (1 + capacity_factor_infra * 0.1), 1.0)
    
        # Teacher Digital Competency
        base_comp = self.parameters.digital_capacity.get('teacher_training', 0.0)
        int_factor_comp = self.parameters.pedagogical_integration.get('tech_integration', 0.0)
        access_factor_comp = self.parameters.technology_access.get('resource_availability', 0.0)
        self.current_teacher_digital_competency = min(base_comp * (1 + int_factor_comp * 0.1) * (1 + access_factor_comp * 0.1), 1.0)
    
        # Digital Content
        base_content = self.parameters.infrastructure_development.get('content_platforms', 0.0)
        access_factor_cont = self.parameters.technology_access.get('content_access', 0.0)
        int_factor_cont = self.parameters.pedagogical_integration.get('content_utilization', 0.0)
        self.current_digital_content = min(base_content * (1 + access_factor_cont * 0.1) * (1 + int_factor_cont * 0.1), 1.0)
    
        # Emerging Tech Adoption
        base_adoption = self.parameters.infrastructure_development.get('innovation_readiness', 0.0)
        capacity_factor_adopt = self.parameters.digital_capacity.get('technical_expertise', 0.0)
        int_factor_adopt = self.parameters.pedagogical_integration.get('innovative_practices', 0.0)
        self.current_emerging_tech_adoption = min(base_adoption * (1 + capacity_factor_adopt * 0.1) * (1 + int_factor_adopt * 0.1), 1.0)
    
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        infra_factor = self.parameters.annual_infra_improvement_factor
        comp_factor = self.parameters.annual_competency_improvement_factor
        cont_factor = self.parameters.annual_content_improvement_factor
        adopt_factor = self.parameters.annual_adoption_improvement_factor

        # Apply improvement factors with diminishing returns
        self.current_digital_infrastructure = min(self.current_digital_infrastructure * (1 + infra_factor * (1 - self.current_digital_infrastructure)), 1.0)
        self.current_teacher_digital_competency = min(self.current_teacher_digital_competency * (1 + comp_factor * (1 - self.current_teacher_digital_competency)), 1.0)
        self.current_digital_content = min(self.current_digital_content * (1 + cont_factor * (1 - self.current_digital_content)), 1.0)
        self.current_emerging_tech_adoption = min(self.current_emerging_tech_adoption * (1 + adopt_factor * (1 - self.current_emerging_tech_adoption)), 1.0)
    
    def simulate_edtech_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate edtech dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'digital_infrastructure': self.current_digital_infrastructure,
            'teacher_digital_competency': self.current_teacher_digital_competency,
            'digital_content': self.current_digital_content,
            'emerging_tech_adoption': self.current_emerging_tech_adoption
        })
        
        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'digital_infrastructure': self.current_digital_infrastructure,
                'teacher_digital_competency': self.current_teacher_digital_competency,
                'digital_content': self.current_digital_content,
                'emerging_tech_adoption': self.current_emerging_tech_adoption
            })
        
        return pd.DataFrame(results) 