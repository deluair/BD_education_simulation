from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from models.access_model import AccessModel, AccessParameters
from models.quality_model import QualityModel, QualityParameters
from models.teacher_model import TeacherModel, TeacherParameters
from models.institution_model import InstitutionModel, InstitutionParameters
from models.curriculum_model import CurriculumModel, CurriculumParameters
from models.edtech_model import EdTechModel, EdTechParameters
from models.finance_model import FinanceModel, FinanceParameters
from simulation.report_generator import ReportGenerator

class BangladeshEducationSimulation:
    """Main simulation environment integrating all components"""
    
    def __init__(self, config: Dict):
        """Initialize simulation with configuration parameters"""
        self.config = config
        self.years = config.get('simulation_years', 25)
        
        # Extract access-specific parameters
        access_params_dict = config.get('access_params', {})
        # Extract quality-specific parameters
        quality_params_dict = config.get('quality_params', {})
        # Extract teacher-specific parameters
        teacher_params_dict = config.get('teacher_params', {})
        # Extract institution-specific parameters
        institution_params_dict = config.get('institution_params', {})
        # Extract curriculum-specific parameters
        curriculum_params_dict = config.get('curriculum_params', {})
        # Extract edtech-specific parameters
        edtech_params_dict = config.get('edtech_params', {})
        # Extract finance-specific parameters
        finance_params_dict = config.get('finance_params', {})

        # Initialize component models
        self.access = AccessModel(
            AccessParameters(
                population_demographics=config.get('population_demographics', {}),
                geographic_distribution=config.get('geographic_distribution', {}),
                socioeconomic_factors=config.get('socioeconomic_factors', {}),
                institutional_capacity=config.get('institutional_capacity', {}),
                incentive_programs=config.get('incentive_programs', {}),
                physical_infrastructure=config.get('physical_infrastructure', {}),
                annual_enrollment_growth_factor=access_params_dict.get('annual_enrollment_growth_factor', 0.005),
                annual_transition_improvement_factor=access_params_dict.get('annual_transition_improvement_factor', 0.007),
                annual_dropout_reduction_factor=access_params_dict.get('annual_dropout_reduction_factor', 0.01)
            )
        )
        
        self.quality = QualityModel(
            QualityParameters(
                teaching_practices=config.get('teaching_practices', {}),
                learning_environments=config.get('learning_environments', {}),
                assessment_systems=config.get('assessment_systems', {}),
                curricular_implementation=config.get('curricular_implementation', {}),
                annual_quality_improvement_factor=quality_params_dict.get('annual_quality_improvement_factor', 0.006)
            )
        )
        
        self.teachers = TeacherModel(
            TeacherParameters(
                qualification_distribution=teacher_params_dict.get('qualification_distribution', {}),
                experience_levels=teacher_params_dict.get('experience_levels', {}),
                professional_development=teacher_params_dict.get('professional_development', {}),
                workload_factors=teacher_params_dict.get('workload_factors', {}),
                motivation_indicators=teacher_params_dict.get('motivation_indicators', {}),
                # Pass specific dynamic params
                annual_qualification_improvement_factor=teacher_params_dict.get('annual_qualification_improvement_factor', 0.01),
                annual_experience_shift_factor=teacher_params_dict.get('annual_experience_shift_factor', 0.015),
                annual_pd_effectiveness_increase=teacher_params_dict.get('annual_pd_effectiveness_increase', 0.02),
                annual_workload_change_factor=teacher_params_dict.get('annual_workload_change_factor', 0.005),
                annual_motivation_increase_factor=teacher_params_dict.get('annual_motivation_increase_factor', 0.01)
            )
        )
        
        self.institutions = InstitutionModel(
            InstitutionParameters(
                governance_structures=config.get('governance_structures', {}),
                management_practices=config.get('management_practices', {}),
                resource_allocation=config.get('resource_allocation', {}),
                institutional_culture=config.get('institutional_culture', {}),
                # Pass specific params directly
                annual_leadership_improvement_factor=institution_params_dict.get('annual_leadership_improvement_factor', 0.005),
                annual_engagement_improvement_factor=institution_params_dict.get('annual_engagement_improvement_factor', 0.006),
                annual_resource_util_improvement_factor=institution_params_dict.get('annual_resource_util_improvement_factor', 0.004),
                annual_culture_improvement_factor=institution_params_dict.get('annual_culture_improvement_factor', 0.003)
            )
        )
        
        self.curriculum = CurriculumModel(
            CurriculumParameters(
                content_development=config.get('content_development', {}),
                competency_frameworks=config.get('competency_frameworks', {}),
                instructional_methods=config.get('instructional_methods', {}),
                learning_materials=config.get('learning_materials', {}),
                # Pass specific params directly
                annual_relevance_improvement_factor=curriculum_params_dict.get('annual_relevance_improvement_factor', 0.008),
                annual_skills_improvement_factor=curriculum_params_dict.get('annual_skills_improvement_factor', 0.010),
                annual_materials_improvement_factor=curriculum_params_dict.get('annual_materials_improvement_factor', 0.005),
                annual_innovation_improvement_factor=curriculum_params_dict.get('annual_innovation_improvement_factor', 0.007)
            )
        )
        
        self.edtech = EdTechModel(
            EdTechParameters(
                infrastructure_development=config.get('infrastructure_development', {}),
                technology_access=config.get('technology_access', {}),
                digital_capacity=config.get('digital_capacity', {}),
                pedagogical_integration=config.get('pedagogical_integration', {}),
                # Pass specific params directly
                annual_infra_improvement_factor=edtech_params_dict.get('annual_infra_improvement_factor', 0.015),
                annual_competency_improvement_factor=edtech_params_dict.get('annual_competency_improvement_factor', 0.012),
                annual_content_improvement_factor=edtech_params_dict.get('annual_content_improvement_factor', 0.010),
                annual_adoption_improvement_factor=edtech_params_dict.get('annual_adoption_improvement_factor', 0.008)
            )
        )
        
        self.finance = FinanceModel(
            FinanceParameters(
                revenue_generation=config.get('revenue_generation', {}),
                allocation_mechanisms=config.get('allocation_mechanisms', {}),
                expenditure_patterns=config.get('expenditure_patterns', {}),
                efficiency_measures=config.get('efficiency_measures', {}),
                # Pass specific params directly
                annual_funding_change_factor=finance_params_dict.get('annual_funding_change_factor', 0.0),
                annual_efficiency_improvement_factor=finance_params_dict.get('annual_efficiency_improvement_factor', 0.0),
                annual_management_improvement_factor=finance_params_dict.get('annual_management_improvement_factor', 0.0),
                annual_alternative_financing_growth_factor=finance_params_dict.get('annual_alternative_financing_growth_factor', 0.0)
            )
        )
        
    def run_simulation(self, years: Optional[int] = None) -> Dict[str, pd.DataFrame]:
        """Run the complete education simulation"""
        if years is None:
            years = self.years
            
        # Run component simulations
        access_results = self.access.simulate_access_dynamics(years)
        quality_results = self.quality.simulate_quality_dynamics(years)
        teacher_results = self.teachers.simulate_teacher_dynamics(0, years)
        institution_results = self.institutions.simulate_institutional_dynamics(years)
        curriculum_results = self.curriculum.simulate_curriculum_dynamics(years)
        edtech_results = self.edtech.simulate_edtech_dynamics(years)
        finance_results = self.finance.simulate_finance_dynamics(years)
        
        # Combine results
        results = {
            'access': access_results,
            'quality': quality_results,
            'teachers': teacher_results,
            'institutions': institution_results,
            'curriculum': curriculum_results,
            'edtech': edtech_results,
            'finance': finance_results
        }
        
        return results
    
    def analyze_results(self, results: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """Analyze simulation results and calculate key metrics"""
        analysis = {}
        
        # Calculate average metrics across years
        for component, df in results.items():
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for column in numeric_columns:
                if column != 'year':
                    # Store both the original casing and a lowercase version for robust lookups
                    original_key = f'{component}_{column}_mean'
                    lowercase_key = original_key.lower().replace(' ', '_')
                    
                    analysis[original_key] = df[column].mean()
                    analysis[lowercase_key] = df[column].mean()
                    
                    # Same for standard deviation
                    original_std_key = f'{component}_{column}_std'
                    lowercase_std_key = original_std_key.lower().replace(' ', '_')
                    
                    analysis[original_std_key] = df[column].std()
                    analysis[lowercase_std_key] = df[column].std()
        
        # Add key metrics for easier access
        analysis['Average Teacher Quality'] = results['teachers']['Teacher Quality'].mean()
        analysis['Average Teaching Effectiveness'] = results['teachers']['Teaching Effectiveness'].mean()
        analysis['Average Teacher Motivation'] = results['teachers']['Teacher Motivation'].mean()

        # Institution Metrics
        analysis['Average Leadership Effectiveness'] = results['institutions']['leadership_effectiveness'].mean()
        analysis['Average Community Engagement'] = results['institutions']['community_engagement'].mean()
        
        # Curriculum Metrics
        analysis['Average Curriculum Relevance'] = results['curriculum']['curriculum_relevance'].mean()
        analysis['Average 21st Century Skills'] = results['curriculum']['21st_century_skills'].mean()
        
        # EdTech Metrics
        analysis['Average Digital Infrastructure'] = results['edtech']['digital_infrastructure'].mean()
        analysis['Average Teacher Digital Competency'] = results['edtech']['teacher_digital_competency'].mean()
        
        # Finance Metrics
        analysis['Average Funding Adequacy'] = results['finance']['funding_adequacy'].mean()
        analysis['Average Allocation Efficiency'] = results['finance']['allocation_efficiency'].mean()

        return analysis
    
    def generate_report(self, results: Dict[str, pd.DataFrame], analysis: Dict[str, float], output_path: str = "simulation_report.html") -> str:
        """Generate a comprehensive report with visualizations"""
        report_generator = ReportGenerator(results, analysis)
        report = report_generator.generate_html_report(output_path)

        report += "--- Teacher Workforce ---\n"
        report += f"Average Teacher Quality Index: {analysis.get('Average Teacher Quality', 'N/A'):.3f}\n"
        report += f"Average Teaching Effectiveness Score: {analysis.get('Average Teaching Effectiveness', 'N/A'):.3f}\n"
        report += f"Average Teacher Motivation Score: {analysis.get('Average Teacher Motivation', 'N/A'):.3f}\n\n"

        report += "--- Institutional Development ---\n"
        report += f"Average Leadership Effectiveness: {analysis.get('Average Leadership Effectiveness', 'N/A'):.3f}\n"
        report += f"Average Community Engagement: {analysis.get('Average Community Engagement', 'N/A'):.3f}\n\n"
        
        report += "--- Curriculum Development ---\n"
        report += f"Average Curriculum Relevance: {analysis.get('Average Curriculum Relevance', 'N/A'):.3f}\n"
        report += f"Average 21st Century Skills: {analysis.get('Average 21st Century Skills', 'N/A'):.3f}\n\n"
        
        report += "--- Educational Technology ---\n"
        report += f"Average Digital Infrastructure: {analysis.get('Average Digital Infrastructure', 'N/A'):.3f}\n"
        report += f"Average Teacher Digital Competency: {analysis.get('Average Teacher Digital Competency', 'N/A'):.3f}\n\n"
        
        report += "--- Educational Finance ---\n"
        report += f"Average Funding Adequacy: {analysis.get('Average Funding Adequacy', 'N/A'):.3f}\n"
        report += f"Average Allocation Efficiency: {analysis.get('Average Allocation Efficiency', 'N/A'):.3f}\n"

        return report 