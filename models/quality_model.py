from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class QualityParameters:
    """Parameters for the quality model"""
    teaching_practices: Dict[str, float]
    learning_environments: Dict[str, float]
    assessment_systems: Dict[str, float]
    curricular_implementation: Dict[str, float]
    # Growth/change factors - now read from config dict
    annual_quality_improvement_factor: float = 0.0

class QualityModel:
    """Model educational quality dimensions and learning achievement"""
    
    def __init__(self, parameters: QualityParameters):
        self.parameters = parameters
        # Initialize state variables
        self.current_reading_proficiency = 0.0
        self.current_numeracy_skills = 0.0
        self.current_critical_thinking = 0.0
        self.current_science_literacy = 0.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        # Reading Proficiency
        base_reading = self.parameters.teaching_practices.get('reading_instruction_quality', 0.0)
        env_factor_read = self.parameters.learning_environments.get('classroom_quality', 0.0)
        assess_factor_read = self.parameters.assessment_systems.get('reading_assessment_frequency', 0.0)
        self.current_reading_proficiency = min(base_reading * (1 + env_factor_read * 0.1) * (1 + assess_factor_read * 0.1), 1.0)
        
        # Numeracy Skills
        base_numeracy = self.parameters.teaching_practices.get('math_instruction_quality', 0.0)
        curr_factor_num = self.parameters.curricular_implementation.get('math_curriculum_quality', 0.0)
        assess_factor_num = self.parameters.assessment_systems.get('math_assessment_frequency', 0.0)
        self.current_numeracy_skills = min(base_numeracy * (1 + curr_factor_num * 0.1) * (1 + assess_factor_num * 0.1), 1.0)
        
        # Critical Thinking
        base_crit = self.parameters.teaching_practices.get('critical_thinking_emphasis', 0.0)
        env_factor_crit = self.parameters.learning_environments.get('student_engagement', 0.0)
        curr_factor_crit = self.parameters.curricular_implementation.get('critical_thinking_integration', 0.0)
        self.current_critical_thinking = min(base_crit * (1 + env_factor_crit * 0.1) * (1 + curr_factor_crit * 0.1), 1.0)
        
        # Science Literacy
        base_science = self.parameters.teaching_practices.get('science_instruction_quality', 0.0)
        env_factor_sci = self.parameters.learning_environments.get('lab_facilities', 0.0)
        curr_factor_sci = self.parameters.curricular_implementation.get('science_curriculum_quality', 0.0)
        self.current_science_literacy = min(base_science * (1 + env_factor_sci * 0.1) * (1 + curr_factor_sci * 0.1), 1.0)
        
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        improvement_factor = self.parameters.annual_quality_improvement_factor
        
        # Apply improvement factor with diminishing returns
        self.current_reading_proficiency = min(self.current_reading_proficiency * (1 + improvement_factor * (1 - self.current_reading_proficiency)), 1.0)
        self.current_numeracy_skills = min(self.current_numeracy_skills * (1 + improvement_factor * (1 - self.current_numeracy_skills)), 1.0)
        self.current_critical_thinking = min(self.current_critical_thinking * (1 + improvement_factor * (1 - self.current_critical_thinking)), 1.0)
        self.current_science_literacy = min(self.current_science_literacy * (1 + improvement_factor * (1 - self.current_science_literacy)), 1.0)

    def simulate_quality_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate quality dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'reading_proficiency': self.current_reading_proficiency,
            'numeracy_skills': self.current_numeracy_skills,
            'critical_thinking': self.current_critical_thinking,
            'science_literacy': self.current_science_literacy
        })

        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'reading_proficiency': self.current_reading_proficiency,
                'numeracy_skills': self.current_numeracy_skills,
                'critical_thinking': self.current_critical_thinking,
                'science_literacy': self.current_science_literacy
            })
        
        return pd.DataFrame(results) 