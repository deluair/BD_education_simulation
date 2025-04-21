from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class CurriculumParameters:
    """Parameters for the curriculum model"""
    content_development: Dict[str, float]
    competency_frameworks: Dict[str, float]
    instructional_methods: Dict[str, float]
    learning_materials: Dict[str, float]
    # Growth/change factors - read from config dict
    annual_relevance_improvement_factor: float = 0.0
    annual_skills_improvement_factor: float = 0.0
    annual_materials_improvement_factor: float = 0.0
    annual_innovation_improvement_factor: float = 0.0

class CurriculumModel:
    """Model curriculum evolution and instructional approaches"""
    
    def __init__(self, parameters: CurriculumParameters):
        self.parameters = parameters
        # Initialize state variables
        self.current_curriculum_relevance = 0.0
        self.current_21st_century_skills = 0.0
        self.current_learning_materials = 0.0
        self.current_pedagogical_innovation = 0.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        # Curriculum Relevance
        base_relevance = self.parameters.content_development.get('content_quality', 0.0)
        comp_factor_rel = self.parameters.competency_frameworks.get('skill_alignment', 0.0)
        method_factor_rel = self.parameters.instructional_methods.get('pedagogical_effectiveness', 0.0)
        self.current_curriculum_relevance = min(base_relevance * (1 + comp_factor_rel * 0.1) * (1 + method_factor_rel * 0.1), 1.0)
    
        # 21st Century Skills
        base_integration = self.parameters.competency_frameworks.get('critical_thinking', 0.0)
        content_factor_skills = self.parameters.content_development.get('digital_literacy', 0.0)
        method_factor_skills = self.parameters.instructional_methods.get('collaborative_learning', 0.0)
        self.current_21st_century_skills = min(base_integration * (1 + content_factor_skills * 0.1) * (1 + method_factor_skills * 0.1), 1.0)
    
        # Learning Materials
        base_quality_mat = self.parameters.learning_materials.get('textbook_quality', 0.0)
        content_factor_mat = self.parameters.content_development.get('supplementary_materials', 0.0)
        method_factor_mat = self.parameters.instructional_methods.get('resource_utilization', 0.0)
        self.current_learning_materials = min(base_quality_mat * (1 + content_factor_mat * 0.1) * (1 + method_factor_mat * 0.1), 1.0)
    
        # Pedagogical Innovation
        base_innovation = self.parameters.instructional_methods.get('active_learning', 0.0)
        content_factor_innov = self.parameters.content_development.get('digital_content', 0.0)
        comp_factor_innov = self.parameters.competency_frameworks.get('assessment_innovation', 0.0)
        self.current_pedagogical_innovation = min(base_innovation * (1 + content_factor_innov * 0.1) * (1 + comp_factor_innov * 0.1), 1.0)
    
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        rel_factor = self.parameters.annual_relevance_improvement_factor
        skills_factor = self.parameters.annual_skills_improvement_factor
        mat_factor = self.parameters.annual_materials_improvement_factor
        innov_factor = self.parameters.annual_innovation_improvement_factor

        # Apply improvement factors with diminishing returns
        self.current_curriculum_relevance = min(self.current_curriculum_relevance * (1 + rel_factor * (1 - self.current_curriculum_relevance)), 1.0)
        self.current_21st_century_skills = min(self.current_21st_century_skills * (1 + skills_factor * (1 - self.current_21st_century_skills)), 1.0)
        self.current_learning_materials = min(self.current_learning_materials * (1 + mat_factor * (1 - self.current_learning_materials)), 1.0)
        self.current_pedagogical_innovation = min(self.current_pedagogical_innovation * (1 + innov_factor * (1 - self.current_pedagogical_innovation)), 1.0)
    
    def simulate_curriculum_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate curriculum dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'curriculum_relevance': self.current_curriculum_relevance,
            '21st_century_skills': self.current_21st_century_skills,
            'learning_materials': self.current_learning_materials,
            'pedagogical_innovation': self.current_pedagogical_innovation
        })
        
        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'curriculum_relevance': self.current_curriculum_relevance,
                '21st_century_skills': self.current_21st_century_skills,
                'learning_materials': self.current_learning_materials,
                'pedagogical_innovation': self.current_pedagogical_innovation
            })
        
        return pd.DataFrame(results) 