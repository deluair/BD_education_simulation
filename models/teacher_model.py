from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

@dataclass
class TeacherParameters:
    qualification_distribution: Dict[str, float]
    experience_levels: Dict[str, float]
    professional_development: Dict[str, float]
    workload_factors: Dict[str, float]
    motivation_indicators: Dict[str, float]
    # Dynamic parameters (annual change factors)
    annual_qualification_improvement_factor: float = 0.01 # e.g., 1% annual improvement
    annual_experience_shift_factor: float = 0.02 # e.g., 2% shift towards more experienced
    annual_pd_effectiveness_increase: float = 0.015 # e.g., 1.5% annual increase in PD effectiveness
    annual_workload_change_factor: float = 0.0 # e.g., 0% change initially
    annual_motivation_increase_factor: float = 0.005 # e.g., 0.5% annual increase

class TeacherModel:
    def __init__(self, params: TeacherParameters):
        self.params = params
        # Initialize with empty state first
        self.current_state = {}
        # Then calculate the initial state
        self.current_state = self._calculate_initial_state()

    def _calculate_initial_state(self) -> Dict[str, float]:
        """Calculate the initial state based on parameters."""
        # Calculate the initial values for basic metrics
        pd_effectiveness = self.params.professional_development.get('effectiveness', 0.5)
        workload_score = self.params.workload_factors.get('average_hours', 40) / 50  # Normalize
        motivation_score = self.params.motivation_indicators.get('satisfaction_index', 0.6)
        qualification_score = sum(self.params.qualification_distribution.values()) / len(self.params.qualification_distribution) if self.params.qualification_distribution else 0
        experience_score = sum(self.params.experience_levels.values()) / len(self.params.experience_levels) if self.params.experience_levels else 0
        
        # Store these in a temporary state dictionary
        state = {
            "pd_effectiveness": pd_effectiveness,
            "workload_score": workload_score,
            "motivation_score": motivation_score,
            "qualification_score": qualification_score,
            "experience_score": experience_score,
        }
        
        # Calculate composite metrics using the temporary state
        state["Teacher Quality"] = self._calculate_teacher_quality(state)
        state["Teaching Effectiveness"] = self._calculate_teaching_effectiveness(state)
        state["Teacher Motivation"] = self._calculate_teacher_motivation(state)
        
        return state

    def _calculate_teacher_quality(self, state: Optional[Dict] = None) -> float:
        """Calculates the overall teacher quality index."""
        current_state = state if state else self.current_state
        qualification_score = current_state['qualification_score']
        experience_score = current_state['experience_score']
        pd_effectiveness = current_state['pd_effectiveness']

        # Weights can be adjusted based on research/expert opinion
        quality_index = (0.4 * qualification_score +
                         0.3 * experience_score +
                         0.3 * pd_effectiveness)
        return np.clip(quality_index, 0, 1)

    def _calculate_teaching_effectiveness(self, state: Optional[Dict] = None) -> float:
        """Calculates the teaching effectiveness score."""
        current_state = state if state else self.current_state
        teacher_quality = current_state["Teacher Quality"] if "Teacher Quality" in current_state else 0.5
        workload_score = current_state['workload_score'] # Higher score means higher workload (negative impact)
        motivation_score = current_state['motivation_score']

        # Effectiveness is influenced by quality, motivation, and negatively by high workload
        effectiveness_score = (0.5 * teacher_quality +
                               0.3 * motivation_score -
                               0.2 * workload_score)
        return np.clip(effectiveness_score, 0, 1)

    def _calculate_teacher_motivation(self, state: Optional[Dict] = None) -> float:
        """Calculates the teacher motivation score."""
        current_state = state if state else self.current_state
        workload_score = current_state['workload_score'] # Higher workload decreases motivation
        pd_effectiveness = current_state['pd_effectiveness'] # Effective PD can boost motivation
        satisfaction_index = current_state['motivation_score'] # Base satisfaction

        motivation_score = (0.6 * satisfaction_index +
                            0.2 * pd_effectiveness -
                            0.2 * workload_score)
        return np.clip(motivation_score, 0, 1)

    def update_state(self):
        """Update the state for the next simulation year."""
        # Apply annual changes
        self.current_state['qualification_score'] *= (1 + self.params.annual_qualification_improvement_factor)
        self.current_state['experience_score'] *= (1 + self.params.annual_experience_shift_factor)
        self.current_state['pd_effectiveness'] *= (1 + self.params.annual_pd_effectiveness_increase)
        self.current_state['workload_score'] *= (1 + self.params.annual_workload_change_factor)
        self.current_state['motivation_score'] *= (1 + self.params.annual_motivation_increase_factor)

        # Clip values to ensure they stay within reasonable bounds (e.g., 0 to 1 or higher if normalization changes)
        self.current_state['qualification_score'] = np.clip(self.current_state['qualification_score'], 0, 1) # Assuming scores are normalized 0-1
        self.current_state['experience_score'] = np.clip(self.current_state['experience_score'], 0, 1)
        self.current_state['pd_effectiveness'] = np.clip(self.current_state['pd_effectiveness'], 0, 1)
        self.current_state['workload_score'] = np.clip(self.current_state['workload_score'], 0, 2) # Workload might exceed normalized 1
        self.current_state['motivation_score'] = np.clip(self.current_state['motivation_score'], 0, 1)

        # Recalculate composite metrics based on updated state variables
        self.current_state["Teacher Quality"] = self._calculate_teacher_quality()
        self.current_state["Teaching Effectiveness"] = self._calculate_teaching_effectiveness()
        self.current_state["Teacher Motivation"] = self._calculate_teacher_motivation()


    def simulate_teacher_dynamics(self, start_year: int, end_year: int) -> pd.DataFrame:
        """Simulates the dynamics of the teacher workforce over the specified period."""
        years = list(range(start_year, end_year + 1))
        results = [] # List to store results for each year

        # Reset to initial state for a new simulation run
        self.current_state = self._calculate_initial_state()

        for year in years:
            # Store current state for the year
            year_results = {
                "Year": year,
                "Teacher Quality": self.current_state["Teacher Quality"],
                "Teaching Effectiveness": self.current_state["Teaching Effectiveness"],
                "Teacher Motivation": self.current_state["Teacher Motivation"],
                # Include underlying factors if needed for detailed analysis
                "Qualification Score": self.current_state['qualification_score'],
                "Experience Score": self.current_state['experience_score'],
                "PD Effectiveness": self.current_state['pd_effectiveness'],
                "Workload Score": self.current_state['workload_score'],
                "Motivation Score": self.current_state['motivation_score']
            }
            results.append(year_results)

            # Update state for the next year
            self.update_state()

        return pd.DataFrame(results).set_index("Year") 