import pandas as pd
from datetime import datetime, timedelta
import hashlib
from config import EXCEL_COLUMNS

class ReportDeduplicator:
    def __init__(self):
        self.similarity_threshold = 0.6  # 60% similarity
        
    def calculate_report_hash(self, report_data, pdf_bytes=None):
        """Generate a unique hash for a report"""
        # Create a string representation of key data
        hash_string = ""
        
        # Include date and report type
        hash_string += str(report_data.get('Date', ''))
        hash_string += str(report_data.get('Report Type', ''))
        
        # Include key parameters
        key_params = ['Hemoglobin', 'RBC', 'WBC', 'Platelets', 
                     'Total Bilirubin', 'SGOT (AST)', 'SGPT (ALT)', 
                     'Glucose', 'Cholesterol']
        
        for param in key_params:
            if param in report_data and report_data[param] is not None:
                hash_string += f"{param}:{report_data[param]:.2f}"
        
        # If PDF bytes provided, include first 1KB
        if pdf_bytes:
            hash_string += pdf_bytes[:1024].hex()
        
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def calculate_similarity(self, report1, report2):
        """Calculate similarity between two reports (0 to 1)"""
        if pd.isna(report1.get('Date')) or pd.isna(report2.get('Date')):
            return 0
        
        # Check date difference (within 7 days)
        try:
            date1 = pd.to_datetime(report1['Date'])
            date2 = pd.to_datetime(report2['Date'])
            days_diff = abs((date1 - date2).days)
            
            if days_diff > 30:  # More than 30 days apart
                return 0
        except:
            return 0
        
        # Check report type
        if report1.get('Report Type') != report2.get('Report Type'):
            return 0
        
        # Calculate parameter similarity
        common_params = 0
        similar_params = 0
        
        for param in EXCEL_COLUMNS:
            if param in ['Date', 'Report Type', 'Notes']:
                continue
                
            val1 = report1.get(param)
            val2 = report2.get(param)
            
            # Both have values
            if pd.notna(val1) and pd.notna(val2):
                common_params += 1
                
                # For numeric values
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    # Calculate percentage difference
                    if val1 == 0 and val2 == 0:
                        similar_params += 1
                    elif val1 == 0 or val2 == 0:
                        # Handle zero values
                        similar_params += 0
                    else:
                        diff = abs(val1 - val2) / ((abs(val1) + abs(val2)) / 2)
                        if diff < 0.2:  # Within 20%
                            similar_params += 1
                # For string values (exact match)
                elif str(val1) == str(val2):
                    similar_params += 1
        
        if common_params == 0:
            return 0
            
        similarity = similar_params / common_params
        
        # Adjust by date difference
        date_factor = max(0, 1 - (days_diff / 30))
        return similarity * date_factor
    
    def find_similar_reports(self, new_report_data, existing_reports_df):
        """Find similar reports in existing data"""
        similar_reports = []
        
        for idx, existing_report in existing_reports_df.iterrows():
            similarity = self.calculate_similarity(
                new_report_data, 
                existing_report.to_dict()
            )
            
            if similarity > self.similarity_threshold:
                similar_reports.append({
                    'index': idx,
                    'report': existing_report.to_dict(),
                    'similarity': similarity,
                    'date': existing_report.get('Date'),
                    'report_type': existing_report.get('Report Type')
                })
        
        # Sort by similarity (highest first)
        similar_reports.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_reports
    
    def merge_reports(self, existing_report, new_report_data, merge_strategy='newer'):
        """Merge two reports intelligently"""
        merged = existing_report.copy()
        
        if merge_strategy == 'newer':
            # Prefer new values over old ones
            for key, new_value in new_report_data.items():
                if pd.notna(new_value):
                    merged[key] = new_value
                    
        elif merge_strategy == 'smart':
            # Smart merge: keep non-null values, prefer newer if both exist
            for key in EXCEL_COLUMNS:
                old_value = existing_report.get(key)
                new_value = new_report_data.get(key)
                
                if pd.isna(old_value) and pd.notna(new_value):
                    merged[key] = new_value
                elif pd.notna(old_value) and pd.notna(new_value):
                    # Both exist, use newer value
                    merged[key] = new_value
        
        return merged
    
    def get_merge_suggestions(self, existing_report, new_report_data):
        """Get suggestions on what changed between reports"""
        changes = []
        
        for param in EXCEL_COLUMNS:
            if param in ['Date', 'Report Type', 'Notes']:
                continue
                
            old_val = existing_report.get(param)
            new_val = new_report_data.get(param)
            
            if pd.notna(old_val) and pd.notna(new_val):
                if isinstance(old_val, (int, float)) and isinstance(new_val, (int, float)):
                    diff = new_val - old_val
                    percent_diff = (diff / old_val * 100) if old_val != 0 else 100
                    
                    if abs(percent_diff) > 10:  # More than 10% change
                        changes.append({
                            'parameter': param,
                            'old': old_val,
                            'new': new_val,
                            'change': f"{diff:+.2f} ({percent_diff:+.1f}%)"
                        })
        
        return changes