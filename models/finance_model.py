from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

@dataclass
class FinanceParameters:
    """Parameters for the finance model"""
    revenue_generation: Dict[str, float]
    allocation_mechanisms: Dict[str, float]
    expenditure_patterns: Dict[str, float]
    efficiency_measures: Dict[str, float]
    # Growth/change factors - read from config dict
    annual_funding_change_factor: float = 0.0
    annual_efficiency_improvement_factor: float = 0.0
    annual_management_improvement_factor: float = 0.0
    annual_alternative_financing_growth_factor: float = 0.0

class FinanceModel:
    """Model education financing and resource utilization"""
    
    def __init__(self, parameters: FinanceParameters):
        self.parameters = parameters
        # Initialize state variables
        self.current_funding_adequacy = 0.0
        self.current_allocation_efficiency = 0.0
        self.current_financial_management = 0.0
        self.current_alternative_financing = 0.0
        
    def _calculate_initial_state(self):
        """Calculate the state for year 0 based on initial parameters."""
        # Funding Adequacy
        base_funding = self.parameters.revenue_generation.get('budget_share', 0.0)
        alloc_factor_fund = self.parameters.allocation_mechanisms.get('equitable_distribution', 0.0)
        effic_factor_fund = self.parameters.efficiency_measures.get('resource_utilization', 0.0)
        # Using budget_share directly as it's a key driver, less sensitive to others initially
        self.current_funding_adequacy = min(base_funding * (1 + alloc_factor_fund * 0.05) * (1 + effic_factor_fund * 0.05), 1.0)
    
        # Allocation Efficiency
        base_effic = self.parameters.allocation_mechanisms.get('targeting_accuracy', 0.0)
        exp_factor_effic = self.parameters.expenditure_patterns.get('priority_alignment', 0.0)
        rev_factor_effic = self.parameters.revenue_generation.get('funding_stability', 0.0)
        self.current_allocation_efficiency = min(base_effic * (1 + exp_factor_effic * 0.1) * (1 + rev_factor_effic * 0.1), 1.0)
    
        # Financial Management
        base_mgmt = self.parameters.efficiency_measures.get('budget_execution', 0.0)
        alloc_factor_mgmt = self.parameters.allocation_mechanisms.get('transparency', 0.0)
        exp_factor_mgmt = self.parameters.expenditure_patterns.get('accountability', 0.0)
        self.current_financial_management = min(base_mgmt * (1 + alloc_factor_mgmt * 0.1) * (1 + exp_factor_mgmt * 0.1), 1.0)
    
        # Alternative Financing
        base_alt = self.parameters.revenue_generation.get('private_sector', 0.0)
        alloc_factor_alt = self.parameters.allocation_mechanisms.get('partnership_effectiveness', 0.0)
        effic_factor_alt = self.parameters.efficiency_measures.get('cost_recovery', 0.0)
        self.current_alternative_financing = min(base_alt * (1 + alloc_factor_alt * 0.1) * (1 + effic_factor_alt * 0.1), 1.0)
    
    def update_state(self, year: int):
        """Update the state for the next year based on current state and factors."""
        fund_factor = self.parameters.annual_funding_change_factor
        effic_factor = self.parameters.annual_efficiency_improvement_factor
        mgmt_factor = self.parameters.annual_management_improvement_factor
        alt_factor = self.parameters.annual_alternative_financing_growth_factor

        # Funding adequacy can increase or decrease
        self.current_funding_adequacy = min(max(self.current_funding_adequacy + fund_factor, 0.0), 1.0)
        
        # Others improve with diminishing returns
        self.current_allocation_efficiency = min(self.current_allocation_efficiency * (1 + effic_factor * (1 - self.current_allocation_efficiency)), 1.0)
        self.current_financial_management = min(self.current_financial_management * (1 + mgmt_factor * (1 - self.current_financial_management)), 1.0)
        self.current_alternative_financing = min(self.current_alternative_financing * (1 + alt_factor * (1 - self.current_alternative_financing)), 1.0)
    
    def simulate_finance_dynamics(self, years: int) -> pd.DataFrame:
        """Simulate finance dynamics over multiple years"""
        self._calculate_initial_state() # Set state for year 0
        results = []
        
        # Record initial state for year 0
        results.append({
            'year': 0,
            'funding_adequacy': self.current_funding_adequacy,
            'allocation_efficiency': self.current_allocation_efficiency,
            'financial_management': self.current_financial_management,
            'alternative_financing': self.current_alternative_financing
        })
        
        # Simulate for subsequent years
        for year in range(1, years):
            self.update_state(year) # Update state based on previous year
            
            results.append({
                'year': year,
                'funding_adequacy': self.current_funding_adequacy,
                'allocation_efficiency': self.current_allocation_efficiency,
                'financial_management': self.current_financial_management,
                'alternative_financing': self.current_alternative_financing
            })
        
        return pd.DataFrame(results) 