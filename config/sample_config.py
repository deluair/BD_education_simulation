"""Sample configuration for Bangladesh Education Simulation - Updated with real data"""

SAMPLE_CONFIG = {
    'simulation_years': 10,  # 2025-2035
    
    # --------------------
    # Access Model Specific
    # --------------------
    'access_params': {
        'annual_enrollment_growth_factor': 0.005, 
        'annual_transition_improvement_factor': 0.007, 
        'annual_dropout_reduction_factor': 0.01 
    },
    
    # --------------------
    # Quality Model Specific
    # --------------------
     'quality_params': {
        'annual_quality_improvement_factor': 0.006 # Example base improvement factor
    },
    
    # --------------------
    # Teacher Model Specific
    # --------------------
    'teacher_params': {
        'annual_quality_improvement_factor': 0.008,
        'annual_motivation_change_factor': 0.002, # Can be positive or negative depending on policies
        'annual_expertise_improvement_factor': 0.007,
        "qualification_distribution": {
            "graduate": 0.6,
            "post_graduate": 0.3,
            "doctorate": 0.1
        },
        "experience_levels": {
            "less_than_5_years": 0.4,
            "5_to_10_years": 0.3,
            "more_than_10_years": 0.3
        },
        "professional_development": {
            "participation_rate": 0.7,
            "effectiveness": 0.6, # Initial effectiveness score (0-1)
            "funding_allocation": 0.05 # Percentage of budget
        },
        "workload_factors": {
            "average_hours": 45, # Average weekly hours
            "class_size": 35,
            "administrative_tasks": 0.2 # Proportion of time
        },
        "motivation_indicators": {
            "satisfaction_index": 0.65, # Survey-based score (0-1)
            "career_progression_rate": 0.1,
            "recognition_frequency": 0.3 # e.g., times per year
        },
        # Dynamic Annual Change Factors
        "annual_qualification_improvement_factor": 0.01, # 1% annual improvement in average qualification score
        "annual_experience_shift_factor": 0.015, # 1.5% annual shift towards higher experience brackets (proxy)
        "annual_pd_effectiveness_increase": 0.02, # 2% annual increase in PD effectiveness
        "annual_workload_change_factor": 0.005, # 0.5% annual increase in workload score
        "annual_motivation_increase_factor": 0.01 # 1% annual increase in motivation score
    },
    
    # --------------------
    # Institution Model Specific
    # --------------------
    'institution_params': {
        'annual_leadership_improvement_factor': 0.005,
        'annual_engagement_improvement_factor': 0.006,
        'annual_resource_util_improvement_factor': 0.004,
        'annual_culture_improvement_factor': 0.003,
        "governance_structures": {
            "autonomy_level": 0.6,
            "accountability_framework": 0.7,
            "stakeholder_participation": 0.5
        }
    },

    # --------------------
    # Curriculum Model Specific
    # --------------------
    'curriculum_params': {
        'annual_relevance_improvement_factor': 0.008,
        'annual_skills_improvement_factor': 0.010,
        'annual_materials_improvement_factor': 0.005,
        'annual_innovation_improvement_factor': 0.007,
        "content_development": {
            "relevance_score": 0.7,
            "update_frequency": 0.5, # times per year avg
            "stakeholder_input": 0.6
        }
    },

    # --------------------
    # EdTech Model Specific
    # --------------------
    'edtech_params': {
        'annual_infra_improvement_factor': 0.015,
        'annual_competency_improvement_factor': 0.012,
        'annual_content_improvement_factor': 0.010,
        'annual_adoption_improvement_factor': 0.008,
        "infrastructure_development": {
            "connectivity_level": 0.6,
            "device_availability": 0.5,
            "technical_support": 0.4
        }
    },

    # --------------------
    # Finance Model Specific
    # --------------------
    'finance_params': {
        'annual_funding_change_factor': 0.01, # Small positive change assumed
        'annual_efficiency_improvement_factor': 0.005,
        'annual_management_improvement_factor': 0.004,
        'annual_alternative_financing_growth_factor': 0.015,
        "revenue_generation": {
            "public_funding_share": 0.8,
            "private_funding_share": 0.1,
            "international_aid_share": 0.1
        }
    },

    # Population and demographics (Estimates based on general knowledge/previous config)
    'population_demographics': {
        'primary_age_population': 0.98,  # Net Enrollment Rate ~98% (GPE/UNESCO 2018)
        'secondary_age_population': 0.65, # Adjusted Net Enrollment ~60-70% (UNICEF 2021/UNFPA 2019)
        'tertiary_age_population': 0.24, # Gross Enrollment ~24% (TheGlobalEconomy 2023)
        'rural_population_share': 0.65,  # Approx. 65% rural
        'urban_population_share': 0.35   # Approx. 35% urban
    },
    
    # Geographic distribution (Estimates/placeholders)
    'geographic_distribution': {
        'urban_rural_ratio': 0.54, # Approx 35/65
        'school_density_urban': 0.8, # Placeholder - higher in urban
        'school_density_rural': 0.6, # Placeholder - lower in rural
        'transportation_access': 0.5 # Placeholder
    },
    
    # Socioeconomic factors (Estimates/placeholders, requires specific poverty/income data)
    'socioeconomic_factors': {
        'poverty_rate': 0.2,        # Placeholder - Bangladesh has made progress but poverty remains
        'household_income': 0.4,    # Placeholder
        'parental_education': 0.5, # Placeholder - correlates with literacy rates
        'gender_parity': 1.0       # Gender parity achieved/exceeded at primary/secondary (GPI > 1)
    },
    
    # Institutional capacity (Estimates/placeholders)
    'institutional_capacity': {
        'primary_schools': 0.8,     # Placeholder - high number of primary schools
        'secondary_schools': 0.7,   # Placeholder
        'teacher_training_institutions': 0.6, # Placeholder
        'classroom_availability': 0.6 # Placeholder - linked to teacher:student ratio
    },
    
    # Incentive programs (Estimates/placeholders)
    'incentive_programs': {
        'stipend_coverage': 0.5,    # Placeholder - stipends exist but coverage varies
        'dropout_prevention': 0.4,  # Placeholder - efforts exist, but dropout remains an issue
        'textbook_distribution': 0.9, # Placeholder - generally high distribution
        'school_feeding': 0.3       # Placeholder - limited coverage
    },
    
    # Physical infrastructure (Estimates/placeholders)
    'physical_infrastructure': {
        'school_density': 0.7,      # Placeholder (related to geographic distribution)
        'school_quality': 0.5,      # Placeholder - quality varies significantly
        'classroom_condition': 0.5, # Placeholder
        'sanitation_facilities': 0.6 # Placeholder - ~88% access improved sanitation (UNICEF 2021), school specific data needed
    },
    
    # Teaching practices (Estimates/placeholders - qualitative)
    'teaching_practices': {
        'reading_instruction_quality': 0.5, # Placeholder - Foundational reading skills moderate (UNICEF 2021)
        'math_instruction_quality': 0.4,    # Placeholder - Foundational numeracy skills low (UNICEF 2021)
        'science_instruction_quality': 0.4, # Placeholder
        'critical_thinking_emphasis': 0.3  # Placeholder - Traditionally less emphasis
    },
    
    # Learning environments (Estimates/placeholders)
    'learning_environments': {
        'classroom_quality': 0.5,    # Placeholder - linked to infrastructure/resources
        'student_engagement': 0.5,   # Placeholder
        'lab_facilities': 0.3,       # Placeholder - likely limited, especially rural/secondary
        'library_access': 0.4        # Placeholder - limited access often cited
    },
    
    # Assessment systems (Estimates/placeholders)
    'assessment_systems': {
        'reading_assessment_frequency': 0.5, # Placeholder
        'math_assessment_frequency': 0.5,    # Placeholder
        'continuous_assessment': 0.4,       # Placeholder - moves towards this, but implementation varies
        'standardized_testing': 0.6        # Placeholder - Standardized exams exist (SSC, HSC)
    },
    
    # Curricular implementation (Estimates/placeholders - qualitative)
    'curricular_implementation': {
        'math_curriculum_quality': 0.5,         # Placeholder
        'science_curriculum_quality': 0.5,      # Placeholder
        'critical_thinking_integration': 0.3,  # Placeholder
        'digital_literacy': 0.3               # Placeholder - growing importance, but access/integration issues (UNICEF 2021)
    },
    
    # Teacher recruitment
    'recruitment_patterns': {
        # Ratio calculation: Ideal 1:30=1.0, 1:40=0.75, 1:50=0.6. Primary ~30, Secondary ~42
        'teacher_student_ratio': 0.7, # Average based on Primary ~30:1 (UNESCO 2018) and Secondary ~42:1 (BANBEIS 2016)
        'qualified_teacher_ratio': 0.75, # ~74-77% primary teachers trained (GPE/TheGlobalEconomy 2023) - Needs secondary data
        'subject_specialist_ratio': 0.4, # Placeholder - often cited as a challenge, especially rural
        'female_teacher_ratio': 0.6     # Placeholder - High female ratio in primary, varies in secondary
    },
    
    # Teacher preparation (Linked to qualified teacher ratio)
    'preparation_quality': {
        'training_quality': 0.6,            # Placeholder - linked to % trained
        'training_completion_rate': 0.7,    # Placeholder
        'math_training_quality': 0.5,       # Placeholder
        'science_training_quality': 0.4     # Placeholder
    },
    
    # Professional development (Estimates/placeholders - qualitative)
    'professional_development': {
        'pd_effectiveness': 0.4,        # Placeholder
        'math_pd_impact': 0.3,          # Placeholder
        'science_pd_impact': 0.3,       # Placeholder
        'pedagogical_training': 0.5     # Placeholder - linked to overall training
    },
    
    # Working conditions (Estimates/placeholders - qualitative)
    'working_conditions': {
        'salary_adequacy': 0.4,         # Placeholder - often cited as low
        'job_satisfaction': 0.5,        # Placeholder
        'teacher_retention_rate': 0.6,  # Placeholder - linked to satisfaction/salary
        'years_of_experience': 0.5,     # Placeholder
        'recognition_system': 0.3,      # Placeholder
        'career_progression': 0.4       # Placeholder
    },
    
    # Governance structures (Estimates/placeholders - qualitative)
    'governance_structures': {
        'leadership_quality': 0.5,        # Placeholder
        'community_participation': 0.5,   # Placeholder
        'accountability': 0.4,            # Placeholder
        'vision_alignment': 0.5           # Placeholder
    },
    
    # Management practices (Estimates/placeholders - qualitative)
    'management_practices': {
        'strategic_planning': 0.5,      # Placeholder
        'community_outreach': 0.4,      # Placeholder
        'financial_management': 0.5,    # Placeholder - linked to overall finance efficiency
        'staff_morale': 0.5             # Placeholder - linked to working conditions
    },
    
    # Resource allocation (Linked to finance model, estimates)
    'resource_allocation': {
        'budget_management': 0.5,         # Placeholder
        'resource_efficiency': 0.5,       # Placeholder - linked to finance model
        'equitable_distribution': 0.4,   # Placeholder - disparities exist (urban/rural etc.)
        'transparency': 0.5              # Placeholder
    },
    
    # Institutional culture (Estimates/placeholders - qualitative)
    'institutional_culture': {
        'parent_involvement': 0.4,       # Placeholder
        'school_climate': 0.5,           # Placeholder
        'collaboration': 0.5,            # Placeholder
        'innovation': 0.4                # Placeholder
    },
    
    # Content development (Estimates/placeholders - qualitative)
    'content_development': {
        'content_quality': 0.5,           # Placeholder
        'digital_literacy': 0.3,          # Placeholder - Reflects EdTech challenges
        'supplementary_materials': 0.5,   # Placeholder
        'digital_content': 0.3            # Placeholder - Low online learning participation (UNICEF 2021)
    },
    
    # Competency frameworks (Estimates/placeholders - qualitative)
    'competency_frameworks': {
        'skill_alignment': 0.4,           # Placeholder - alignment with job market often questioned
        'critical_thinking': 0.3,         # Placeholder - reflects teaching practices
        'assessment_innovation': 0.4,     # Placeholder
        'learning_outcomes': 0.5          # Placeholder - moderate reading, low numeracy (UNICEF 2021)
    },
    
    # Instructional methods (Estimates/placeholders - qualitative)
    'instructional_methods': {
        'pedagogical_effectiveness': 0.5, # Placeholder
        'collaborative_learning': 0.4,    # Placeholder
        'resource_utilization': 0.5,      # Placeholder - linked to finance/infrastructure
        'active_learning': 0.4            # Placeholder - often traditional methods dominate
    },
    
    # Learning materials (Estimates/placeholders)
    'learning_materials': {
        'textbook_quality': 0.6,          # Placeholder - Textbooks widely distributed
        'digital_resources': 0.3,         # Placeholder - reflects EdTech model
        'local_content': 0.5,             # Placeholder
        'accessibility': 0.4              # Placeholder - linked to EdTech/infrastructure
    },
    
    # Infrastructure development (Estimates reflecting low online learning uptake - UNICEF 2021)
    'infrastructure_development': {
        'connectivity': 0.3,              # Placeholder - Low internet access cited as barrier
        'content_platforms': 0.3,         # Placeholder
        'innovation_readiness': 0.3,      # Placeholder
        'technical_support': 0.4          # Placeholder
    },
    
    # Technology access (Estimates reflecting low online learning uptake - UNICEF 2021)
    'technology_access': {
        'device_availability': 0.3,       # Placeholder - Lack of devices cited as barrier
        'resource_availability': 0.4,     # Placeholder
        'content_access': 0.3,            # Placeholder
        'connectivity_reliability': 0.4   # Placeholder
    },
    
    # Digital capacity (Estimates reflecting low online learning uptake - UNICEF 2021)
    'digital_capacity': {
        'teacher_training': 0.4,          # Placeholder
        'technical_support': 0.4,         # Placeholder
        'technical_expertise': 0.3,       # Placeholder
        'digital_literacy': 0.4           # Placeholder - applies to students and teachers
    },
    
    # Pedagogical integration (Estimates reflecting low online learning uptake - UNICEF 2021)
    'pedagogical_integration': {
        'tech_integration': 0.3,          # Placeholder - low actual use during COVID
        'content_utilization': 0.3,       # Placeholder
        'innovative_practices': 0.3,      # Placeholder
        'assessment_technology': 0.3      # Placeholder
    },
    
    # Revenue generation
    'revenue_generation': {
        'budget_share': 0.2,             # Education expenditure ~2% of GDP (UNESCO/WB 2018) - Low score
        'funding_stability': 0.5,        # Placeholder
        'private_sector': 0.3,           # Placeholder - private sector involvement exists but scale varies
        'community_contribution': 0.4    # Placeholder
    },
    
    # Allocation mechanisms (Estimates/placeholders)
    'allocation_mechanisms': {
        'equitable_distribution': 0.4,   # Placeholder - disparities exist
        'targeting_accuracy': 0.5,       # Placeholder
        'transparency': 0.5,             # Placeholder
        'partnership_effectiveness': 0.4 # Placeholder
    },
    
    # Expenditure patterns
    'expenditure_patterns': {
        'priority_alignment': 0.6,       # Placeholder - Gov't prioritizes education, but budget is low
        'accountability': 0.4,           # Placeholder
        'efficiency': 0.5,               # Placeholder - linked to overall efficiency measures
        'sustainability': 0.5            # Placeholder
    },
    
    # Efficiency measures
    'efficiency_measures': {
        'resource_utilization': 0.5,      # Placeholder - linked to allocation efficiency
        'budget_execution': 0.6,          # Placeholder
        'cost_recovery': 0.3,             # Placeholder - education is largely state-funded/subsidized
        'performance_monitoring': 0.5    # Placeholder
    }
} 