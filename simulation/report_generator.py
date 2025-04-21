import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict
import os

class ReportGenerator:
    """Generate HTML reports with interactive visualizations"""
    
    def __init__(self, results: Dict[str, pd.DataFrame], analysis: Dict[str, float]):
        self.results = results
        self.analysis = analysis
        self.colors = px.colors.qualitative.Vivid
        
    def create_trend_plot(self, component: str, metrics: list) -> go.Figure:
        """Create a trend plot for multiple metrics over time"""
        fig = go.Figure()
        
        # Check if 'year' is a column or if the DataFrame is indexed by 'Year'
        df = self.results[component]
        if 'year' in df.columns:
            x_values = df['year']
        elif 'Year' in df.columns:
            x_values = df['Year']
        else:
            # Use the index if it's likely a year index
            x_values = df.index
        
        # For debugging
        print(f"Creating trend plot for {component} with metrics: {metrics}")
        print(f"Available columns: {df.columns.tolist()}")
        
        for i, metric in enumerate(metrics):
            if metric in df.columns:
                fig.add_trace(go.Scatter(
                    x=x_values,
                    y=df[metric],
                    name=metric.replace('_', ' ').title(),
                    line=dict(color=self.colors[i % len(self.colors)], width=3),
                    mode='lines+markers',
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=dict(
                text=f"{component.title()} Trends Over Time",
                font=dict(size=24, color="#333333")
            ),
            xaxis_title=dict(text="Year", font=dict(size=18)),
            yaxis_title=dict(text="Value", font=dict(size=18)),
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(240,240,240,0.5)',
            width=900,
            height=500,
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        return fig
    
    def create_metric_comparison(self, metrics: list) -> go.Figure:
        """Create a bar chart comparing final year metrics"""
        fig = go.Figure()
        
        data = []
        labels = []
        
        for i, (component, metric) in enumerate(metrics):
            if component in self.results and metric in self.results[component].columns:
                value = self.results[component].iloc[-1][metric]
                data.append(value)
                labels.append(f"{component.title()}: {metric.replace('_', ' ').title()}")
        
        # Use a gradient of colors based on values
        colorscale = px.colors.sequential.Viridis
        normalized_values = [(x - min(data)) / (max(data) - min(data)) for x in data]
        colors = [colorscale[int(val * (len(colorscale)-1))] for val in normalized_values]
        
        fig.add_trace(go.Bar(
            x=labels,
            y=data,
            marker_color=colors,
            text=data,
            textposition='auto',
            texttemplate='%{y:.2f}'
        ))
        
        fig.update_layout(
            title=dict(
                text="Final Year Metric Comparison",
                font=dict(size=24, color="#333333")
            ),
            xaxis_title=dict(text="", font=dict(size=18)),
            yaxis_title=dict(text="Value", font=dict(size=18)),
            template='plotly_white',
            plot_bgcolor='rgba(240,240,240,0.5)',
            width=900,
            height=600,
            margin=dict(l=60, r=40, t=80, b=120),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12)
            )
        )
        
        return fig
    
    def create_correlation_heatmap(self, components: list) -> go.Figure:
        """Create a correlation heatmap between components"""
        # Extract key metrics from each component for correlation
        data_dict = {}
        sample_metrics = {
            'access': ['primary_enrollment', 'secondary_transition'],
            'quality': ['reading_proficiency', 'numeracy_skills'],
            'teachers': ['Teacher Quality', 'Teaching Effectiveness', 'Teacher Motivation'],
            'institutions': ['leadership_effectiveness', 'community_engagement'],
            'curriculum': ['curriculum_relevance', '21st_century_skills'],
            'edtech': ['digital_infrastructure', 'teacher_digital_competency'],
            'finance': ['funding_adequacy', 'allocation_efficiency']
        }
        
        # Print available results for debugging
        print("\nAvailable components for heatmap:", list(self.results.keys()))
        
        years = []
        # Extract years from any available component
        for component in self.results:
            if self.results[component] is not None and not self.results[component].empty:
                if 'year' in self.results[component].columns:
                    years = self.results[component]['year'].tolist()
                    break
                elif self.results[component].index.name == 'Year' or isinstance(self.results[component].index[0], int):
                    years = self.results[component].index.tolist()
                    break
        
        if not years:
            years = list(range(10))  # Fallback if no years found
        
        # Create a dataframe with years as index
        df = pd.DataFrame(index=years)
        
        # Add available metrics from each component
        for component in components:
            if component not in self.results or self.results[component] is None or self.results[component].empty:
                print(f"Skipping {component} - not in results or empty")
                continue
                
            metrics = sample_metrics.get(component, [])
            if not metrics:
                continue
                
            for metric in metrics:
                if metric in self.results[component].columns:
                    # Create a friendly display name
                    display_name = f"{component.title()}: {metric.replace('_', ' ').title()}"
                    
                    # Extract values - handle both normal columns and indexed dataframes
                    if self.results[component].index.name == 'Year' or isinstance(self.results[component].index[0], int):
                        df[display_name] = self.results[component][metric]
                    else:
                        # Extract data and align with years
                        year_col = 'year' if 'year' in self.results[component].columns else 'Year'
                        if year_col in self.results[component].columns:
                            temp_df = pd.DataFrame({
                                'year': self.results[component][year_col],
                                'value': self.results[component][metric]
                            })
                            for year in years:
                                if year in temp_df['year'].values:
                                    df.loc[year, display_name] = temp_df[temp_df['year'] == year]['value'].values[0]
        
        # If we don't have enough data or columns, return an empty figure with message
        if df.shape[1] < 2:
            fig = go.Figure()
            fig.add_annotation(
                text="Not enough data for correlation heatmap.<br>Need at least 2 metrics.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#333")
            )
            fig.update_layout(
                title=dict(
                    text="Component Correlation Heatmap - Insufficient Data",
                    font=dict(size=24, color="#333333")
                ),
                template='plotly_white',
                width=900,
                height=500
            )
            return fig
        
        # Calculate correlation matrix
        corr = df.corr(method='pearson', min_periods=3)
        
        # Mask the diagonal (self-correlations)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        corr_masked = corr.mask(mask)
        
        # Create heatmap with improved styling
        heat_data = []
        for i, row in enumerate(corr.index):
            for j, col in enumerate(corr.columns):
                if i < j:  # Only use upper triangle
                    heat_data.append(
                        dict(
                            y=row, 
                            x=col, 
                            z=corr.loc[row, col],
                            text=f"{corr.loc[row, col]:.2f}",
                            hovertext=f"{row} vs {col}<br>Correlation: {corr.loc[row, col]:.2f}"
                        )
                    )
        
        # Create the figure with better layout
        fig = go.Figure()
        
        # Add the heatmap
        fig.add_trace(go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(corr.values, 2),
            texttemplate='%{text:.2f}',
            textfont=dict(size=10),
            hoverinfo='text',
            colorbar=dict(
                title='Correlation',
                titleside='right',
                titlefont=dict(size=14),
                tickfont=dict(size=12),
            )
        ))
        
        # Improve layout
        fig.update_layout(
            title=dict(
                text="Component Correlation Heatmap",
                font=dict(size=24, color="#333333")
            ),
            template='plotly_white',
            width=900,
            height=max(700, 150 + 40 * len(corr.columns)),  # Dynamic height based on metrics count
            margin=dict(l=140, r=80, t=100, b=80)
        )
        
        # Improve axis labeling
        fig.update_xaxes(
            tickangle=-45,
            tickfont=dict(size=11)
        )
        fig.update_yaxes(
            tickfont=dict(size=11)
        )
        
        return fig
    
    def generate_html_report(self, output_path: str = "simulation_report.html"):
        """Generate a complete HTML report with all visualizations"""
        # Debug: Print analysis keys for troubleshooting
        print("\nAnalysis dictionary keys:")
        for key in sorted(self.analysis.keys()):
            if 'teacher' in key.lower():
                print(f"  {key} = {self.analysis[key]}")
                
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bangladesh Education Simulation Report</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
            <style>
                body { 
                    font-family: 'Roboto', sans-serif; 
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background-color: #f8f9fa;
                    line-height: 1.6;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #006A4E 0%, #006A4E 50%, #F42A41 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
                .header h1 {
                    font-size: 2.5rem;
                    margin: 0;
                    font-weight: 700;
                }
                .header p {
                    font-size: 1.2rem;
                    margin-top: 10px;
                    opacity: 0.9;
                }
                .section {
                    background: white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    border-radius: 8px;
                    margin: 30px 0;
                    overflow: hidden;
                }
                .section-header {
                    padding: 20px 30px;
                    background-color: #006A4E;
                    color: white;
                }
                .section-header h2 {
                    margin: 0;
                    font-size: 1.8rem;
                    font-weight: 500;
                }
                .section-content {
                    padding: 30px;
                }
                .plot-container {
                    margin: 20px 0;
                    overflow-x: auto;
                }
                .metric-card {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                    border-left: 4px solid #006A4E;
                }
                .metric-card h3 {
                    color: #006A4E;
                    margin-top: 0;
                    font-size: 1.4rem;
                }
                .metric-list {
                    list-style: none;
                    padding: 0;
                }
                .metric-list li {
                    padding: 8px 0;
                    border-bottom: 1px solid #e9ecef;
                }
                .metric-list li:last-child {
                    border-bottom: none;
                }
                .metric-name {
                    font-weight: 500;
                    color: #495057;
                }
                .metric-value {
                    float: right;
                    font-weight: 600;
                    color: #212529;
                }
                .footer {
                    text-align: center;
                    padding: 20px;
                    color: #6c757d;
                    font-size: 0.9rem;
                }
                .summary-cards {
                    display: flex;
                    flex-wrap: wrap;
                    margin: 0 -15px;
                }
                .summary-card {
                    flex: 1 0 200px;
                    margin: 15px;
                    padding: 25px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .summary-card .value {
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #006A4E;
                    margin: 10px 0;
                }
                .summary-card .label {
                    font-size: 1rem;
                    color: #6c757d;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                @media (max-width: 768px) {
                    .summary-card {
                        flex: 1 0 100%;
                    }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Bangladesh Education Simulation Report</h1>
                <p>Projecting Educational Developments from 2025 to 2050</p>
            </div>
            <div class="container">
        """
        
        # Add summary section with key metrics
        html_content += """
        <div class="section">
            <div class="section-header">
                <h2>Executive Summary</h2>
            </div>
            <div class="section-content">
                <p>This report presents the results of a comprehensive simulation of Bangladesh's education system from 2025 to 2050. 
                The simulation models various aspects of the education ecosystem including access, quality, 
                teacher workforce, institutional development, curriculum evolution, technology integration, 
                and financing mechanisms.</p>
                
                <div class="summary-cards">
        """
        
        # Add summary cards for key metrics
        key_metrics = [
            ("Teacher Quality", self.analysis.get("Average Teacher Quality", 0)),
            ("Teaching Effectiveness", self.analysis.get("Average Teaching Effectiveness", 0)),
            ("Curriculum Relevance", self.analysis.get("Average Curriculum Relevance", 0)),
            ("Digital Infrastructure", self.analysis.get("Average Digital Infrastructure", 0))
        ]
        
        for label, value in key_metrics:
            html_content += f"""
            <div class="summary-card">
                <div class="label">{label}</div>
                <div class="value">{value:.2f}</div>
            </div>
            """
        
        html_content += """
                </div>
            </div>
        </div>
        """
        
        # Add trend plots for each component
        components = {
            'access': ['primary_enrollment', 'secondary_transition'],
            'quality': ['reading_proficiency', 'numeracy_skills'],
            'teachers': ['Teacher Quality', 'Teaching Effectiveness', 'Teacher Motivation'],
            'institutions': ['leadership_effectiveness', 'community_engagement'],
            'curriculum': ['curriculum_relevance', '21st_century_skills'],
            'edtech': ['digital_infrastructure', 'teacher_digital_competency'],
            'finance': ['funding_adequacy', 'allocation_efficiency']
        }
        
        for component, metrics in components.items():
            fig = self.create_trend_plot(component, metrics)
            html_content += f"""
            <div class="section">
                <div class="section-header">
                    <h2>{component.title()} Trends</h2>
                </div>
                <div class="section-content">
                    <div class="plot-container">
                        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
            </div>
            """
        
        # Add metric comparison
        comparison_metrics = [
            ('access', 'primary_enrollment'),
            ('quality', 'reading_proficiency'),
            ('teachers', 'Teacher Quality'),
            ('institutions', 'leadership_effectiveness'),
            ('curriculum', 'curriculum_relevance'),
            ('edtech', 'digital_infrastructure'),
            ('finance', 'funding_adequacy')
        ]
        
        fig = self.create_metric_comparison(comparison_metrics)
        html_content += f"""
        <div class="section">
            <div class="section-header">
                <h2>Final Year Metric Comparison</h2>
            </div>
            <div class="section-content">
                <div class="plot-container">
                    {fig.to_html(full_html=False, include_plotlyjs='cdn')}
                </div>
            </div>
        </div>
        """
        
        # Add correlation heatmap
        fig = self.create_correlation_heatmap(list(components.keys()))
        html_content += f"""
        <div class="section">
            <div class="section-header">
                <h2>Component Correlations</h2>
            </div>
            <div class="section-content">
                <div class="plot-container">
                    {fig.to_html(full_html=False, include_plotlyjs='cdn')}
                </div>
            </div>
        </div>
        """
        
        # Add detailed analysis section
        html_content += """
        <div class="section">
            <div class="section-header">
                <h2>Detailed Analysis</h2>
            </div>
            <div class="section-content">
        """
        
        for component, metrics in components.items():
            html_content += f"""
            <div class="metric-card">
                <h3>{component.title()} Analysis</h3>
                <ul class="metric-list">
            """
            
            valid_metrics = [m for m in metrics if component in self.results and m in self.results[component].columns]
            
            if not valid_metrics:
                html_content += """
                    <li>No valid metrics found for this component</li>
                """
            else:
                for metric in valid_metrics:
                    # For teacher metrics, use exact case sensitivity
                    if component == 'teachers':
                        # Use the exact keys from the analysis dictionary
                        mean_key = f'teachers_{metric}_mean'
                        std_key = f'teachers_{metric}_std'
                        
                        mean = self.analysis.get(mean_key)
                        std = self.analysis.get(std_key)
                    else:
                        # For other components, try different key formats
                        possible_keys = [
                            f'{component}_{metric}_mean',
                            f'{component}_{metric}_mean'.lower(),
                            f'{component}_{metric}_mean'.lower().replace(' ', '_'),
                            f'{component}_{metric.lower()}_mean',
                            f'{component.lower()}_{metric.lower()}_mean',
                            f'{component.lower()}_{metric.lower()}_mean'.replace(' ', '_')
                        ]
                        
                        mean = None
                        std = None
                        
                        # Try to find the metric in analysis dictionary
                        for key in possible_keys:
                            if key in self.analysis:
                                mean = self.analysis[key]
                                # Try to find corresponding std key
                                std_key = key.replace('_mean', '_std')
                                if std_key in self.analysis:
                                    std = self.analysis[std_key]
                                break
                    
                    # Format values properly
                    if mean is not None and std is not None:
                        html_content += f"""
                            <li>
                                <span class="metric-name">{metric.replace('_', ' ')}</span>
                                <span class="metric-value">Mean: {mean:.3f} | SD: {std:.3f}</span>
                            </li>
                        """
                    else:
                        # Debug output for this metric
                        if component == 'teachers':
                            print(f"Could not find teacher metrics for {metric} - tried keys: {mean_key}, {std_key}")
                        else:
                            print(f"Could not find metrics for {component}.{metric} - tried multiple keys")
                        
                        html_content += f"""
                            <li>
                                <span class="metric-name">{metric.replace('_', ' ')}</span>
                                <span class="metric-value">Mean: N/A | SD: N/A</span>
                            </li>
                        """
                    
            html_content += """
                </ul>
            </div>
            """
        
        html_content += """
            </div>
        </div>
        <div class="footer">
            <p>Bangladesh Education Simulation Report &copy; 2023 | Generated using Python, Pandas, and Plotly</p>
        </div>
        </div>
        </body>
        </html>
        """
        
        # Save the HTML report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path 