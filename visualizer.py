'''import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import NORMAL_RANGES

class Visualizer:
    def __init__(self):
        self.normal_ranges = NORMAL_RANGES
    
    def check_value_status(self, parameter, value):
        """Check if a value is within normal range"""
        if parameter not in self.normal_ranges or value is None or pd.isna(value):
            return "Unknown", "#808080"
        
        ranges = self.normal_ranges[parameter]
        if value < ranges["min"]:
            return "Low", "#FF4444"
        elif value > ranges["max"]:
            return "High", "#FF4444"
        else:
            return "Normal", "#00CC00"
    
    def create_trend_chart(self, df, parameter):
        """Create a trend line chart for a parameter"""
        if df.empty or parameter not in df.columns:
            return None
        
        data = df[['Date', parameter]].dropna()
        if data.empty:
            return None
        
        fig = go.Figure()
        
        # Add the trend line
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data[parameter],
            mode='lines+markers',
            name=parameter,
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        
        # Add normal range bands if available
        if parameter in self.normal_ranges:
            ranges = self.normal_ranges[parameter]
            fig.add_hrect(
                y0=ranges["min"],
                y1=ranges["max"],
                fillcolor="green",
                opacity=0.1,
                line_width=0,
                annotation_text="Normal Range",
                annotation_position="top left"
            )
            
            # Add range lines
            fig.add_hline(
                y=ranges["min"],
                line_dash="dash",
                line_color="green",
                annotation_text=f"Min: {ranges['min']}"
            )
            fig.add_hline(
                y=ranges["max"],
                line_dash="dash",
                line_color="green",
                annotation_text=f"Max: {ranges['max']}"
            )
        
        fig.update_layout(
            title=f"{parameter} Trend Over Time",
            xaxis_title="Date",
            yaxis_title=f"{parameter} ({self.normal_ranges.get(parameter, {}).get('unit', '')})",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_comparison_chart(self, latest_values):
        """Create a bar chart comparing current values with normal ranges"""
        parameters = []
        values = []
        colors = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                parameters.append(param)
                values.append(value)
                _, color = self.check_value_status(param, value)
                colors.append(color)
        
        if not parameters:
            return None
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=parameters,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Current Values vs Normal Ranges",
            xaxis_title="Parameter",
            yaxis_title="Value",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_status_table(self, latest_values):
        """Create a status summary table"""
        data = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                status, color = self.check_value_status(param, value)
                ranges = self.normal_ranges[param]
                data.append({
                    "Parameter": param,
                    "Value": f"{value} {ranges['unit']}",
                    "Normal Range": f"{ranges['min']} - {ranges['max']} {ranges['unit']}",
                    "Status": status
                })
        
        return pd.DataFrame(data)'''
        
        
''' import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import NORMAL_RANGES

class Visualizer:
    def __init__(self):
        self.normal_ranges = NORMAL_RANGES
    
    def check_value_status(self, parameter, value):
        """Check if a value is within normal range"""
        if parameter not in self.normal_ranges or value is None or pd.isna(value):
            return "Unknown", "#808080"
        
        ranges = self.normal_ranges[parameter]
        if value < ranges["min"]:
            return "Low", "#FF4444"
        elif value > ranges["max"]:
            return "High", "#FF4444"
        else:
            return "Normal", "#00CC00"
    
    def create_trend_chart(self, df, parameter):
    """Create a trend line chart for a parameter"""
    if df.empty or parameter not in df.columns:
        return None
    
    data = df[['Date', parameter]].dropna()
    if data.empty:
        return None
    
    # Calculate y-axis range
    min_val = data[parameter].min()
    max_val = data[parameter].max()
    
    # Always start from 0, but handle very small values
    y_min = 0
    y_max = max_val * 1.15  # Add 15% padding
    
    # For very small values (like A/G Ratio which is around 1-3), adjust scale
    if max_val < 10:
        y_max = max(10, max_val * 1.5)  # Ensure minimum scale for readability
    
    fig = go.Figure()
    
    # Add the trend line
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data[parameter],
        mode='lines+markers',
        name=parameter,
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                     f'{parameter}: %{{y:.2f}}' +
                     '<extra></extra>'
    ))
    
    # Add normal range bands if available
    if parameter in self.normal_ranges:
        ranges = self.normal_ranges[parameter]
        
        # Update y_max to include normal range if it's higher
        y_max = max(y_max, ranges["max"] * 1.15)
        
        # Add normal range background with black text
        fig.add_hrect(
            y0=ranges["min"],
            y1=ranges["max"],
            fillcolor="rgba(0, 255, 0, 0.1)",
            line_width=0,
            annotation_text=f"<b>Normal Range<br>{ranges['min']}-{ranges['max']}</b>",
            annotation_position="top left",
            annotation_font_size=10,
            annotation_font_color="black",
            annotation_bgcolor="rgba(255, 255, 255, 0.8)",
            annotation_bordercolor="black",
            annotation_borderwidth=1
        )
        
        # Add minimum line with black text
        fig.add_hline(
            y=ranges["min"],
            line_dash="dash",
            line_color="green",
            opacity=0.5,
            annotation_text=f"<b>Min: {ranges['min']}</b>",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="black",
            annotation_bgcolor="rgba(255, 255, 255, 0.8)"
        )
        
        # Add maximum line with black text
        fig.add_hline(
            y=ranges["max"],
            line_dash="dash",
            line_color="green",
            opacity=0.5,
            annotation_text=f"<b>Max: {ranges['max']}</b>",
            annotation_position="top right",
            annotation_font_size=10,
            annotation_font_color="black",
            annotation_bgcolor="rgba(255, 255, 255, 0.8)"
        )
        
        # Highlight abnormal values
        abnormal_data = data[data[parameter] < ranges["min"]]
        if not abnormal_data.empty:
            fig.add_trace(go.Scatter(
                x=abnormal_data['Date'],
                y=abnormal_data[parameter],
                mode='markers',
                name='Low',
                marker=dict(color='red', size=12, symbol='triangle-down'),
                hovertemplate='<b>LOW</b><br>%{x|%Y-%m-%d}<br>' +
                             f'{parameter}: %{{y:.2f}}<br>' +
                             f'Normal: {ranges["min"]}-{ranges["max"]}' +
                             '<extra></extra>'
            ))
        
        abnormal_data = data[data[parameter] > ranges["max"]]
        if not abnormal_data.empty:
            fig.add_trace(go.Scatter(
                x=abnormal_data['Date'],
                y=abnormal_data[parameter],
                mode='markers',
                name='High',
                marker=dict(color='orange', size=12, symbol='triangle-up'),
                hovertemplate='<b>HIGH</b><br>%{x|%Y-%m-%d}<br>' +
                             f'{parameter}: %{{y:.2f}}<br>' +
                             f'Normal: {ranges["min"]}-{ranges["max"]}' +
                             '<extra></extra>'
            ))
    
    # Add zero line for reference
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="gray",
        opacity=0.3
    )
    
    # Get unit for y-axis label
    unit = self.normal_ranges.get(parameter, {}).get('unit', '')
    
    fig.update_layout(
        title=dict(
            text=f"<b>{parameter} Trend Over Time</b>",
            font=dict(size=16, family="Arial", color="black")
        ),
        xaxis=dict(
            title="Date",
            title_font=dict(color="black", size=12),
            tickfont=dict(color="black", size=10),
            tickformat="%Y-%m-%d",
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        yaxis=dict(
            title=f"Value ({unit})" if unit else "Value",
            title_font=dict(color="black", size=12),
            tickfont=dict(color="black", size=10),
            range=[y_min, y_max],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='lightgray',
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        hovermode='x unified',
        height=450,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color="black"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="black", size=10)
        )
    )
    
    return fig
    
    def create_comparison_chart(self, latest_values):
        """Create a bar chart comparing current values with normal ranges"""
        parameters = []
        values = []
        colors = []
        statuses = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                parameters.append(param)
                values.append(value)
                status, color = self.check_value_status(param, value)
                colors.append(color)
                statuses.append(status)
        
        if not parameters:
            return None
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=parameters,
            y=values,
            marker_color=colors,
            text=[f"{v:.2f}" if v < 100 else f"{v:.0f}" for v in values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         'Value: %{y:.2f}<br>' +
                         'Status: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=statuses,
            textfont=dict(size=12, family="Arial")
        ))
        
        # Add normal range markers
        for i, param in enumerate(parameters):
            if param in self.normal_ranges:
                ranges = self.normal_ranges[param]
                # Add min line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["min"], y1=ranges["min"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
                # Add max line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["max"], y1=ranges["max"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
        
        # Calculate appropriate y-axis max
        max_value = max(values)
        max_normal = 0
        for param in parameters:
            if param in self.normal_ranges:
                max_normal = max(max_normal, self.normal_ranges[param]["max"])
        
        y_max = max(max_value, max_normal) * 1.3
        
        fig.update_layout(
            title=dict(
                text="<b>Current Health Parameters</b>",
                font=dict(size=16, family="Arial", color="#333")
            ),
            xaxis=dict(
                title="Parameter",
                tickangle=45,
                tickfont=dict(size=10),
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Value",
                range=[0, y_max],
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='lightgray',
                gridcolor='lightgray'
            ),
            height=500,
            margin=dict(l=50, r=50, t=80, b=100),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12),
            showlegend=False
        )
        
        # Add annotations for normal range
        fig.add_annotation(
            text="Dashed lines show normal range",
            xref="paper", yref="paper",
            x=0.5, y=-0.25,
            showarrow=False,
            font=dict(size=10, color="green")
        )
        
        return fig
    
    def create_status_table(self, latest_values):
        """Create a status summary table"""
        data = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                status, color = self.check_value_status(param, value)
                ranges = self.normal_ranges[param]
                data.append({
                    "Parameter": param,
                    "Value": f"{value:.2f}" if value < 100 else f"{value:.0f}",
                    "Unit": ranges['unit'],
                    "Normal Range": f"{ranges['min']} - {ranges['max']}",
                    "Status": status,
                    "Color": color
                })
        
        return pd.DataFrame(data)

    def create_overview_chart(self, df):
        """Create an overview chart showing all parameters in a grid"""
        if df.empty:
            return None
        
        # Get numeric columns that have normal ranges
        numeric_cols = [col for col in df.columns 
                       if col in self.normal_ranges and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return None
        
        # Limit to top 6 parameters for readability
        display_cols = numeric_cols[:6]
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set3
        for i, col in enumerate(display_cols):
            data = df[['Date', col]].dropna()
            if not data.empty:
                fig.add_trace(go.Scatter(
                    x=data['Date'],
                    y=data[col],
                    mode='lines+markers',
                    name=col,
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=4),
                    yaxis=f"y{i+1}" if i > 0 else "y"
                ))
        
        # Create subplot layout
        from plotly.subplots import make_subplots
        
        rows = min(3, len(display_cols))
        cols = 2 if len(display_cols) > 1 else 1
        fig = make_subplots(
            rows=rows, 
            cols=cols,
            subplot_titles=display_cols,
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        for i, col in enumerate(display_cols):
            row = i // cols + 1
            col_num = i % cols + 1
            
            data = df[['Date', col]].dropna()
            if not data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=data['Date'],
                        y=data[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=4)
                    ),
                    row=row, col=col_num
                )
                
                # Add normal range if available
                if col in self.normal_ranges:
                    ranges = self.normal_ranges[col]
                    fig.add_hrect(
                        y0=ranges["min"],
                        y1=ranges["max"],
                        fillcolor="rgba(0, 255, 0, 0.1)",
                        line_width=0,
                        row=row, col=col_num
                    )
                
                # Update y-axis to start at 0
                max_val = data[col].max()
                fig.update_yaxes(
                    range=[0, max_val * 1.2],
                    row=row, col=col_num
                )
        
        fig.update_layout(
            title=dict(
                text="<b>Health Parameters Overview</b>",
                font=dict(size=16, family="Arial", color="#333")
            ),
            height=200 * rows,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=11),
            showlegend=False
        )
        
        return fig'''
        

'''import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import NORMAL_RANGES

class Visualizer:
    def __init__(self):
        self.normal_ranges = NORMAL_RANGES
    
    def check_value_status(self, parameter, value):
        """Check if a value is within normal range"""
        if parameter not in self.normal_ranges or value is None or pd.isna(value):
            return "Unknown", "#808080"
        
        ranges = self.normal_ranges[parameter]
        if value < ranges["min"]:
            return "Low", "#FF4444"
        elif value > ranges["max"]:
            return "High", "#FF4444"
        else:
            return "Normal", "#00CC00"
    
    def create_trend_chart(self, df, parameter):
        """Create a trend line chart for a parameter"""
        if df.empty or parameter not in df.columns:
            return None
        
        data = df[['Date', parameter]].dropna()
        if data.empty:
            return None
        
        # Calculate y-axis range
        min_val = data[parameter].min()
        max_val = data[parameter].max()
        
        # Always start from 0, but handle very small values
        y_min = 0
        y_max = max_val * 1.15  # Add 15% padding
        
        # For very small values (like A/G Ratio which is around 1-3), adjust scale
        if max_val < 10:
            y_max = max(10, max_val * 1.5)  # Ensure minimum scale for readability
        
        fig = go.Figure()
        
        # Add the trend line
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data[parameter],
            mode='lines+markers',
            name=parameter,
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         f'{parameter}: %{{y:.2f}}' +
                         '<extra></extra>'
        ))
        
        # Add normal range bands if available
        if parameter in self.normal_ranges:
            ranges = self.normal_ranges[parameter]
            
            # Update y_max to include normal range if it's higher
            y_max = max(y_max, ranges["max"] * 1.15)
            
            # Add normal range background with black text
            fig.add_hrect(
                y0=ranges["min"],
                y1=ranges["max"],
                fillcolor="rgba(0, 255, 0, 0.1)",
                line_width=0,
                annotation_text=f"<b>Normal Range<br>{ranges['min']}-{ranges['max']}</b>",
                annotation_position="top left",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)",
                annotation_bordercolor="black",
                annotation_borderwidth=1
            )
            
            # Add minimum line with black text
            fig.add_hline(
                y=ranges["min"],
                line_dash="dash",
                line_color="green",
                opacity=0.5,
                annotation_text=f"<b>Min: {ranges['min']}</b>",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)"
            )
            
            # Add maximum line with black text
            fig.add_hline(
                y=ranges["max"],
                line_dash="dash",
                line_color="green",
                opacity=0.5,
                annotation_text=f"<b>Max: {ranges['max']}</b>",
                annotation_position="top right",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)"
            )
            
            # Highlight abnormal values
            abnormal_data = data[data[parameter] < ranges["min"]]
            if not abnormal_data.empty:
                fig.add_trace(go.Scatter(
                    x=abnormal_data['Date'],
                    y=abnormal_data[parameter],
                    mode='markers',
                    name='Low',
                    marker=dict(color='red', size=12, symbol='triangle-down'),
                    hovertemplate='<b>LOW</b><br>%{x|%Y-%m-%d}<br>' +
                                 f'{parameter}: %{{y:.2f}}<br>' +
                                 f'Normal: {ranges["min"]}-{ranges["max"]}' +
                                 '<extra></extra>'
                ))
            
            abnormal_data = data[data[parameter] > ranges["max"]]
            if not abnormal_data.empty:
                fig.add_trace(go.Scatter(
                    x=abnormal_data['Date'],
                    y=abnormal_data[parameter],
                    mode='markers',
                    name='High',
                    marker=dict(color='orange', size=12, symbol='triangle-up'),
                    hovertemplate='<b>HIGH</b><br>%{x|%Y-%m-%d}<br>' +
                                 f'{parameter}: %{{y:.2f}}<br>' +
                                 f'Normal: {ranges["min"]}-{ranges["max"]}' +
                                 '<extra></extra>'
                ))
        
        # Add zero line for reference
        fig.add_hline(
            y=0,
            line_dash="dot",
            line_color="gray",
            opacity=0.3
        )
        
        # Get unit for y-axis label
        unit = self.normal_ranges.get(parameter, {}).get('unit', '')
        
        fig.update_layout(
            title=dict(
                text=f"<b>{parameter} Trend Over Time</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            xaxis=dict(
                title="Date",
                title_font=dict(color="black", size=12),
                tickfont=dict(color="black", size=10),
                tickformat="%Y-%m-%d",
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            yaxis=dict(
                title=f"Value ({unit})" if unit else "Value",
                title_font=dict(color="black", size=12),
                tickfont=dict(color="black", size=10),
                range=[y_min, y_max],
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='lightgray',
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            hovermode='x unified',
            height=450,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12, color="black"),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="black", size=10)
            )
        )
        
        return fig
    
    def create_comparison_chart(self, latest_values):
        """Create a bar chart comparing current values with normal ranges"""
        parameters = []
        values = []
        colors = []
        statuses = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                parameters.append(param)
                values.append(value)
                status, color = self.check_value_status(param, value)
                colors.append(color)
                statuses.append(status)
        
        if not parameters:
            return None
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=parameters,
            y=values,
            marker_color=colors,
            text=[f"{v:.2f}" if v < 100 else f"{v:.0f}" for v in values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         'Value: %{y:.2f}<br>' +
                         'Status: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=statuses,
            textfont=dict(size=12, family="Arial")
        ))
        
        # Add normal range markers
        for i, param in enumerate(parameters):
            if param in self.normal_ranges:
                ranges = self.normal_ranges[param]
                # Add min line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["min"], y1=ranges["min"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
                # Add max line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["max"], y1=ranges["max"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
        
        # Calculate appropriate y-axis max
        max_value = max(values)
        max_normal = 0
        for param in parameters:
            if param in self.normal_ranges:
                max_normal = max(max_normal, self.normal_ranges[param]["max"])
        
        y_max = max(max_value, max_normal) * 1.3
        
        fig.update_layout(
            title=dict(
                text="<b>Current Health Parameters</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            xaxis=dict(
                title="Parameter",
                title_font=dict(color="black", size=12),
                tickangle=45,
                tickfont=dict(size=10, color="black"),
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Value",
                title_font=dict(color="black", size=12),
                range=[0, y_max],
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='lightgray',
                gridcolor='lightgray',
                tickfont=dict(color="black", size=10)
            ),
            height=500,
            margin=dict(l=50, r=50, t=80, b=100),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12, color="black"),
            showlegend=False
        )
        
        # Add annotations for normal range
        fig.add_annotation(
            text="Dashed lines show normal range",
            xref="paper", yref="paper",
            x=0.5, y=-0.25,
            showarrow=False,
            font=dict(size=10, color="black")
        )
        
        return fig
    
    def create_status_table(self, latest_values):
        """Create a status summary table"""
        data = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                status, color = self.check_value_status(param, value)
                ranges = self.normal_ranges[param]
                data.append({
                    "Parameter": param,
                    "Value": f"{value:.2f}" if value < 100 else f"{value:.0f}",
                    "Unit": ranges['unit'],
                    "Normal Range": f"{ranges['min']} - {ranges['max']}",
                    "Status": status,
                    "Color": color
                })
        
        return pd.DataFrame(data)

    def create_overview_chart(self, df):
        """Create an overview chart showing all parameters in a grid"""
        if df.empty:
            return None
        
        # Get numeric columns that have normal ranges
        numeric_cols = [col for col in df.columns 
                       if col in self.normal_ranges and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return None
        
        # Limit to top 6 parameters for readability
        display_cols = numeric_cols[:6]
        
        # Create subplot layout
        from plotly.subplots import make_subplots
        
        rows = min(3, len(display_cols))
        cols = 2 if len(display_cols) > 1 else 1
        fig = make_subplots(
            rows=rows, 
            cols=cols,
            subplot_titles=display_cols,
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        for i, col in enumerate(display_cols):
            row = i // cols + 1
            col_num = i % cols + 1
            
            data = df[['Date', col]].dropna()
            if not data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=data['Date'],
                        y=data[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=4)
                    ),
                    row=row, col=col_num
                )
                
                # Add normal range if available
                if col in self.normal_ranges:
                    ranges = self.normal_ranges[col]
                    fig.add_hrect(
                        y0=ranges["min"],
                        y1=ranges["max"],
                        fillcolor="rgba(0, 255, 0, 0.1)",
                        line_width=0,
                        row=row, col=col_num
                    )
                
                # Update y-axis to start at 0
                max_val = data[col].max()
                fig.update_yaxes(
                    range=[0, max_val * 1.2] if max_val > 0 else [0, 10],
                    row=row, col=col_num,
                    title_font=dict(color="black", size=10),
                    tickfont=dict(color="black", size=8)
                )
        
        fig.update_layout(
            title=dict(
                text="<b>Health Parameters Overview</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            height=200 * rows,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=11, color="black"),
            showlegend=False
        )
        
        # Update subplot titles to black
        for i in range(len(display_cols)):
            fig.update_annotations(
                font=dict(color="black", size=12),
                selector=dict(text=display_cols[i])
            )
        
        return fig'''
        
        
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import NORMAL_RANGES

class Visualizer:
    def __init__(self):
        self.normal_ranges = NORMAL_RANGES
    
    def check_value_status(self, parameter, value):
        """Check if a value is within normal range"""
        if parameter not in self.normal_ranges or value is None or pd.isna(value):
            return "Unknown", "#808080"
        
        ranges = self.normal_ranges[parameter]
        if value < ranges["min"]:
            return "Low", "#FF4444"
        elif value > ranges["max"]:
            return "High", "#FF4444"
        else:
            return "Normal", "#00CC00"
    
    def create_trend_chart(self, df, parameter):
        """Create a trend line chart for a parameter"""
        if df.empty or parameter not in df.columns:
            return None
        
        data = df[['Date', parameter]].dropna()
        if data.empty:
            return None
        
        # Calculate y-axis range
        min_val = data[parameter].min()
        max_val = data[parameter].max()
        
        # Always start from 0, but handle very small values
        y_min = 0
        y_max = max_val * 1.15  # Add 15% padding
        
        # For very small values (like A/G Ratio which is around 1-3), adjust scale
        if max_val < 10:
            y_max = max(10, max_val * 1.5)  # Ensure minimum scale for readability
        
        fig = go.Figure()
        
        # Add the trend line
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data[parameter],
            mode='lines+markers',
            name=parameter,
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                         f'{parameter}: %{{y:.2f}}' +
                         '<extra></extra>'
        ))
        
        # Add normal range bands if available
        if parameter in self.normal_ranges:
            ranges = self.normal_ranges[parameter]
            
            # Update y_max to include normal range if it's higher
            y_max = max(y_max, ranges["max"] * 1.15)
            
            # Add normal range background with black text
            fig.add_hrect(
                y0=ranges["min"],
                y1=ranges["max"],
                fillcolor="rgba(0, 255, 0, 0.1)",
                line_width=0,
                annotation_text=f"<b>Normal Range<br>{ranges['min']}-{ranges['max']}</b>",
                annotation_position="top left",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)",
                annotation_bordercolor="black",
                annotation_borderwidth=1
            )
            
            # Add minimum line with black text
            fig.add_hline(
                y=ranges["min"],
                line_dash="dash",
                line_color="green",
                opacity=0.5,
                annotation_text=f"<b>Min: {ranges['min']}</b>",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)"
            )
            
            # Add maximum line with black text
            fig.add_hline(
                y=ranges["max"],
                line_dash="dash",
                line_color="green",
                opacity=0.5,
                annotation_text=f"<b>Max: {ranges['max']}</b>",
                annotation_position="top right",
                annotation_font_size=10,
                annotation_font_color="black",
                annotation_bgcolor="rgba(255, 255, 255, 0.8)"
            )
            
            # Highlight abnormal values
            abnormal_data = data[data[parameter] < ranges["min"]]
            if not abnormal_data.empty:
                fig.add_trace(go.Scatter(
                    x=abnormal_data['Date'],
                    y=abnormal_data[parameter],
                    mode='markers',
                    name='Low',
                    marker=dict(color='red', size=12, symbol='triangle-down'),
                    hovertemplate='<b>LOW</b><br>%{x|%Y-%m-%d}<br>' +
                                 f'{parameter}: %{{y:.2f}}<br>' +
                                 f'Normal: {ranges["min"]}-{ranges["max"]}' +
                                 '<extra></extra>'
                ))
            
            abnormal_data = data[data[parameter] > ranges["max"]]
            if not abnormal_data.empty:
                fig.add_trace(go.Scatter(
                    x=abnormal_data['Date'],
                    y=abnormal_data[parameter],
                    mode='markers',
                    name='High',
                    marker=dict(color='orange', size=12, symbol='triangle-up'),
                    hovertemplate='<b>HIGH</b><br>%{x|%Y-%m-%d}<br>' +
                                 f'{parameter}: %{{y:.2f}}<br>' +
                                 f'Normal: {ranges["min"]}-{ranges["max"]}' +
                                 '<extra></extra>'
                ))
        
        # Add zero line for reference
        fig.add_hline(
            y=0,
            line_dash="dot",
            line_color="gray",
            opacity=0.3
        )
        
        # Get unit for y-axis label
        unit = self.normal_ranges.get(parameter, {}).get('unit', '')
        
        fig.update_layout(
            title=dict(
                text=f"<b>{parameter} Trend Over Time</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            xaxis=dict(
                title="Date",
                title_font=dict(color="black", size=12),
                tickfont=dict(color="black", size=10),
                tickformat="%Y-%m-%d",
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            yaxis=dict(
                title=f"Value ({unit})" if unit else "Value",
                title_font=dict(color="black", size=12),
                tickfont=dict(color="black", size=10),
                range=[y_min, y_max],
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='lightgray',
                gridcolor='lightgray',
                gridwidth=0.5
            ),
            hovermode='x unified',
            height=450,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12, color="black"),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="black", size=10)
            )
        )
        
        return fig
    
    def create_comparison_chart(self, latest_values):
        """Create a bar chart comparing current values with normal ranges"""
        parameters = []
        values = []
        colors = []
        statuses = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                parameters.append(param)
                values.append(value)
                status, color = self.check_value_status(param, value)
                colors.append(color)
                statuses.append(status)
        
        if not parameters:
            return None
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=parameters,
            y=values,
            marker_color=colors,
            text=[f"{v:.2f}" if v < 100 else f"{v:.0f}" for v in values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                         'Value: %{y:.2f}<br>' +
                         'Status: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=statuses,
            textfont=dict(size=12, family="Arial")
        ))
        
        # Add normal range markers
        for i, param in enumerate(parameters):
            if param in self.normal_ranges:
                ranges = self.normal_ranges[param]
                # Add min line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["min"], y1=ranges["min"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
                # Add max line
                fig.add_shape(
                    type="line",
                    x0=i-0.4, x1=i+0.4,
                    y0=ranges["max"], y1=ranges["max"],
                    line=dict(color="green", width=2, dash="dash"),
                    opacity=0.7
                )
        
        # Calculate appropriate y-axis max
        max_value = max(values)
        max_normal = 0
        for param in parameters:
            if param in self.normal_ranges:
                max_normal = max(max_normal, self.normal_ranges[param]["max"])
        
        y_max = max(max_value, max_normal) * 1.3
        
        fig.update_layout(
            title=dict(
                text="<b>Current Health Parameters</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            xaxis=dict(
                title="Parameter",
                title_font=dict(color="black", size=12),
                tickangle=45,
                tickfont=dict(size=10, color="black"),
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Value",
                title_font=dict(color="black", size=12),
                range=[0, y_max],
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='lightgray',
                gridcolor='lightgray',
                tickfont=dict(color="black", size=10)
            ),
            height=500,
            margin=dict(l=50, r=50, t=80, b=100),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12, color="black"),
            showlegend=False
        )
        
        # Add annotations for normal range
        fig.add_annotation(
            text="Dashed lines show normal range",
            xref="paper", yref="paper",
            x=0.5, y=-0.25,
            showarrow=False,
            font=dict(size=10, color="black")
        )
        
        return fig
    
    def create_status_table(self, latest_values):
        """Create a status summary table WITHOUT Color column"""
        data = []
        
        for param, value in latest_values.items():
            if param in self.normal_ranges and value is not None and not pd.isna(value):
                status, color = self.check_value_status(param, value)
                ranges = self.normal_ranges[param]
                data.append({
                    "Parameter": param,
                    "Value": f"{value:.2f}" if value < 100 else f"{value:.0f}",
                    "Unit": ranges['unit'],
                    "Normal Range": f"{ranges['min']} - {ranges['max']}",
                    "Status": status
                    # REMOVED: "Color": color
                })
        
        return pd.DataFrame(data)

    def create_overview_chart(self, df):
        """Create an overview chart showing all parameters in a grid"""
        if df.empty:
            return None
        
        # Get numeric columns that have normal ranges
        numeric_cols = [col for col in df.columns 
                       if col in self.normal_ranges and pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            return None
        
        # Limit to top 6 parameters for readability
        display_cols = numeric_cols[:6]
        
        # Create subplot layout
        from plotly.subplots import make_subplots
        
        rows = min(3, len(display_cols))
        cols = 2 if len(display_cols) > 1 else 1
        fig = make_subplots(
            rows=rows, 
            cols=cols,
            subplot_titles=display_cols,
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        for i, col in enumerate(display_cols):
            row = i // cols + 1
            col_num = i % cols + 1
            
            data = df[['Date', col]].dropna()
            if not data.empty:
                fig.add_trace(
                    go.Scatter(
                        x=data['Date'],
                        y=data[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=4)
                    ),
                    row=row, col=col_num
                )
                
                # Add normal range if available
                if col in self.normal_ranges:
                    ranges = self.normal_ranges[col]
                    fig.add_hrect(
                        y0=ranges["min"],
                        y1=ranges["max"],
                        fillcolor="rgba(0, 255, 0, 0.1)",
                        line_width=0,
                        row=row, col=col_num
                    )
                
                # Update y-axis to start at 0
                max_val = data[col].max()
                fig.update_yaxes(
                    range=[0, max_val * 1.2] if max_val > 0 else [0, 10],
                    row=row, col=col_num,
                    title_font=dict(color="black", size=10),
                    tickfont=dict(color="black", size=8)
                )
        
        fig.update_layout(
            title=dict(
                text="<b>Health Parameters Overview</b>",
                font=dict(size=16, family="Arial", color="black")
            ),
            height=200 * rows,
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=11, color="black"),
            showlegend=False
        )
        
        # Update subplot titles to black
        for i in range(len(display_cols)):
            fig.update_annotations(
                font=dict(color="black", size=12),
                selector=dict(text=display_cols[i])
            )
        
        return fig

