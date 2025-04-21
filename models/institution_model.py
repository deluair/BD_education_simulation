from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class InstitutionParameters:
    """Parameters for the institution model"""
    governance_structures: Dict[str, float]
    management_practices: Dict[str, float]
    resource_allocation: Dict[str, float]
    institutional_culture: Dict[str, float]
    # Growth/change factors - read from config dict
    annual_leadership_improvement_factor: float = 0.0
    annual_engagement_improvement_factor: float = 0.0
    annual_resource_util_improvement_factor: float = 0.0
    annual_culture_improvement_factor: float = 0.0

class InstitutionModel:
    """Model educational institution evolution and management"""
    
    def __init__(self, parameters: InstitutionParameters):
        self.parameters = parameters
        # Initialize state variables
        self.current_leadership_effectiveness = 0.0
        self.current_community_engagement = 0.0
        self.current_resource_utilization = 0.0
        self.current_institutional_culture = 0.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        # Leadership Effectiveness
        base_effectiveness = self.parameters.governance_structures.get('leadership_quality', 0.0)
        mgmt_factor_lead = self.parameters.management_practices.get('strategic_planning', 0.0)
        res_factor_lead = self.parameters.resource_allocation.get('budget_management', 0.0)
        self.current_leadership_effectiveness = min(base_effectiveness * (1 + mgmt_factor_lead * 0.2) * (1 + res_factor_lead * 0.1), 1.0)
    
        # Community Engagement
        base_engagement = self.parameters.governance_structures.get('community_participation', 0.0)
        culture_factor_eng = self.parameters.institutional_culture.get('parent_involvement', 0.0)
        mgmt_factor_eng = self.parameters.management_practices.get('community_outreach', 0.0)
        self.current_community_engagement = min(base_engagement * (1 + culture_factor_eng * 0.1) * (1 + mgmt_factor_eng * 0.1), 1.0)
    
        # Resource Utilization
        base_efficiency = self.parameters.resource_allocation.get('resource_efficiency', 0.0)
        mgmt_factor_res = self.parameters.management_practices.get('financial_management', 0.0)
        gov_factor_res = self.parameters.governance_structures.get('accountability', 0.0)
        self.current_resource_utilization = min(base_efficiency * (1 + mgmt_factor_res * 0.1) * (1 + gov_factor_res * 0.1), 1.0)
    
        # Institutional Culture
        base_culture = self.parameters.institutional_culture.get('school_climate', 0.0)
        lead_factor_cult = self.parameters.governance_structures.get('vision_alignment', 0.0)
        mgmt_factor_cult = self.parameters.management_practices.get('staff_morale', 0.0)
        self.current_institutional_culture = min(base_culture * (1 + lead_factor_cult * 0.1) * (1 + mgmt_factor_cult * 0.1), 1.0)
    
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        lead_factor = self.parameters.annual_leadership_improvement_factor
        eng_factor = self.parameters.annual_engagement_improvement_factor
        res_factor = self.parameters.annual_resource_util_improvement_factor
        cult_factor = self.parameters.annual_culture_improvement_factor

        # Apply improvement factors with diminishing returns
        self.current_leadership_effectiveness = min(self.current_leadership_effectiveness * (1 + lead_factor * (1 - self.current_leadership_effectiveness)), 1.0)
        self.current_community_engagement = min(self.current_community_engagement * (1 + eng_factor * (1 - self.current_community_engagement)), 1.0)
        self.current_resource_utilization = min(self.current_resource_utilization * (1 + res_factor * (1 - self.current_resource_utilization)), 1.0)
        self.current_institutional_culture = min(self.current_institutional_culture * (1 + cult_factor * (1 - self.current_institutional_culture)), 1.0)
    
    def simulate_institutional_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate institutional dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'leadership_effectiveness': self.current_leadership_effectiveness,
            'community_engagement': self.current_community_engagement,
            'resource_utilization': self.current_resource_utilization,
            'institutional_culture': self.current_institutional_culture
        })
        
        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'leadership_effectiveness': self.current_leadership_effectiveness,
                'community_engagement': self.current_community_engagement,
                'resource_utilization': self.current_resource_utilization,
                'institutional_culture': self.current_institutional_culture
            })
        
        return pd.DataFrame(results) 