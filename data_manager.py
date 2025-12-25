'''import pandas as pd
import os
from config import REPORTS_DIR, EXCEL_COLUMNS

class DataManager:
    def __init__(self, username):
        self.username = username
        self.excel_file = os.path.join(REPORTS_DIR, f"{username}_reports.xlsx")
        self._ensure_excel_file()
    
    def _ensure_excel_file(self):
        """Create Excel file if it doesn't exist"""
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=EXCEL_COLUMNS)
            df.to_excel(self.excel_file, index=False)
    
    def add_report(self, report_data):
        """Add a new report to the Excel file"""
        try:
            df = pd.read_excel(self.excel_file)
            new_row = pd.DataFrame([report_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_excel(self.excel_file, index=False)
            return True, "Report added successfully"
        except Exception as e:
            return False, f"Error adding report: {str(e)}"
    
    def get_all_reports(self):
        """Get all reports for the user"""
        try:
            df = pd.read_excel(self.excel_file)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
            return df
        except Exception as e:
            return pd.DataFrame(columns=EXCEL_COLUMNS)
    
    def get_latest_report(self):
        """Get the most recent report"""
        df = self.get_all_reports()
        if not df.empty:
            return df.iloc[0].to_dict()
        return None
    
    def get_parameter_history(self, parameter):
        """Get history of a specific parameter"""
        df = self.get_all_reports()
        if parameter in df.columns:
            history = df[['Date', parameter]].dropna()
            return history
        return pd.DataFrame()
    
    def delete_report(self, index):
        """Delete a report by index"""
        try:
            df = pd.read_excel(self.excel_file)
            df = df.drop(index)
            df.to_excel(self.excel_file, index=False)
            return True, "Report deleted successfully"
        except Exception as e:
            return False, f"Error deleting report: {str(e)}"
    
    def update_report(self, index, report_data):
        """Update an existing report"""
        try:
            df = pd.read_excel(self.excel_file)
            for key, value in report_data.items():
                if key in df.columns:
                    df.at[index, key] = value
            df.to_excel(self.excel_file, index=False)
            return True, "Report updated successfully"
        except Exception as e:
            return False, f"Error updating report: {str(e)}"'''
            
'''import pandas as pd
import os
from config import REPORTS_DIR, EXCEL_COLUMNS
from report_deduplicator import ReportDeduplicator

class DataManager:
    def __init__(self, username):
        self.username = username
        self.excel_file = os.path.join(REPORTS_DIR, f"{username}_reports.xlsx")
        self.deduplicator = ReportDeduplicator()
        self._ensure_excel_file()
    
    def _ensure_excel_file(self):
        """Create Excel file if it doesn't exist"""
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=EXCEL_COLUMNS)
            df.to_excel(self.excel_file, index=False)
    
    def add_report(self, report_data, pdf_bytes=None, check_duplicates=True):
        """Add a new report to the Excel file with duplicate checking"""
        try:
            df = pd.read_excel(self.excel_file)
            
            # Check for duplicates if enabled
            if check_duplicates and not df.empty:
                similar_reports = self.deduplicator.find_similar_reports(report_data, df)
                
                if similar_reports:
                    # Return information about similar reports
                    return False, "DUPLICATE_FOUND", similar_reports
            
            # No duplicates found, add new report
            new_row = pd.DataFrame([report_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Sort by date
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
            
            df.to_excel(self.excel_file, index=False)
            return True, "Report added successfully", None
            
        except Exception as e:
            return False, f"Error adding report: {str(e)}", None
    
    def update_existing_report(self, index, report_data):
        """Update an existing report"""
        try:
            df = pd.read_excel(self.excel_file)
            
            # Update all columns
            for key, value in report_data.items():
                if key in df.columns:
                    df.at[index, key] = value
            
            df.to_excel(self.excel_file, index=False)
            return True, "Report updated successfully"
            
        except Exception as e:
            return False, f"Error updating report: {str(e)}"
    
    def merge_and_update_report(self, index, new_report_data, merge_strategy='newer'):
        """Merge new data with existing report and update"""
        try:
            df = pd.read_excel(self.excel_file)
            existing_report = df.iloc[index].to_dict()
            
            # Merge reports
            merged_report = self.deduplicator.merge_reports(
                existing_report, 
                new_report_data, 
                merge_strategy
            )
            
            # Update the report
            for key, value in merged_report.items():
                if key in df.columns:
                    df.at[index, key] = value
            
            df.to_excel(self.excel_file, index=False)
            return True, "Reports merged successfully"
            
        except Exception as e:
            return False, f"Error merging reports: {str(e)}"
    
    def get_all_reports(self):
        """Get all reports for the user"""
        try:
            df = pd.read_excel(self.excel_file)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
            return df
        except Exception as e:
            return pd.DataFrame(columns=EXCEL_COLUMNS)
    
    def get_latest_report(self):
        """Get the most recent report"""
        df = self.get_all_reports()
        if not df.empty:
            return df.iloc[0].to_dict()
        return None
    
    def get_parameter_history(self, parameter):
        """Get history of a specific parameter"""
        df = self.get_all_reports()
        if parameter in df.columns:
            history = df[['Date', parameter]].dropna()
            return history
        return pd.DataFrame()
    
    def delete_report(self, index):
        """Delete a report by index"""
        try:
            df = pd.read_excel(self.excel_file)
            df = df.drop(index).reset_index(drop=True)
            df.to_excel(self.excel_file, index=False)
            return True, "Report deleted successfully"
        except Exception as e:
            return False, f"Error deleting report: {str(e)}"
    
    def update_report(self, index, report_data):
        """Update an existing report (legacy method)"""
        try:
            df = pd.read_excel(self.excel_file)
            for key, value in report_data.items():
                if key in df.columns:
                    df.at[index, key] = value
            df.to_excel(self.excel_file, index=False)
            return True, "Report updated successfully"
        except Exception as e:
            return False, f"Error updating report: {str(e)}"
    
    def find_exact_duplicate(self, report_data):
        """Check if an exact duplicate exists"""
        df = self.get_all_reports()
        
        if df.empty:
            return None
        
        for idx, row in df.iterrows():
            match = True
            for col in EXCEL_COLUMNS:
                if col in report_data and col in row:
                    if report_data[col] != row[col]:
                        match = False
                        break
            
            if match:
                return idx
        
        return None'''
        
import pandas as pd
import os
from config import REPORTS_DIR, EXCEL_COLUMNS
from report_deduplicator import ReportDeduplicator

class DataManager:
    def __init__(self, username):
        self.username = username
        self.excel_file = os.path.join(REPORTS_DIR, f"{username}_reports.xlsx")
        self.deduplicator = ReportDeduplicator()
        self._ensure_excel_file()
    
    def _ensure_excel_file(self):
        """Create Excel file if it doesn't exist"""
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=EXCEL_COLUMNS)
            df.to_excel(self.excel_file, index=False)
    
    def add_report(self, report_data, pdf_bytes=None, check_duplicates=True):
        """Add a new report to the Excel file with duplicate checking"""
        try:
            df = pd.read_excel(self.excel_file)
            
            # Check for duplicates if enabled
            if check_duplicates and not df.empty:
                similar_reports = self.deduplicator.find_similar_reports(report_data, df)
                
                if similar_reports:
                    # Return information about similar reports
                    return False, "DUPLICATE_FOUND", similar_reports
            
            # No duplicates found, add new report
            new_row = pd.DataFrame([report_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Sort by date
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
            
            df.to_excel(self.excel_file, index=False)
            return True, "Report added successfully", None
            
        except Exception as e:
            return False, f"Error adding report: {str(e)}", None
    
    def update_existing_report(self, index, report_data):
        """Update an existing report"""
        try:
            df = pd.read_excel(self.excel_file)
            
            # Update all columns
            for key, value in report_data.items():
                if key in df.columns:
                    df.at[index, key] = value
            
            df.to_excel(self.excel_file, index=False)
            return True, "Report updated successfully"
            
        except Exception as e:
            return False, f"Error updating report: {str(e)}"
    
    def merge_and_update_report(self, index, new_report_data, merge_strategy='newer'):
        """Merge new data with existing report and update"""
        try:
            df = pd.read_excel(self.excel_file)
            existing_report = df.iloc[index].to_dict()
            
            # Merge reports
            merged_report = self.deduplicator.merge_reports(
                existing_report, 
                new_report_data, 
                merge_strategy
            )
            
            # Update the report
            for key, value in merged_report.items():
                if key in df.columns:
                    df.at[index, key] = value
            
            df.to_excel(self.excel_file, index=False)
            return True, "Reports merged successfully"
            
        except Exception as e:
            return False, f"Error merging reports: {str(e)}"
    
    def get_all_reports(self, format_date=True):
        """Get all reports for the user"""
        try:
            df = pd.read_excel(self.excel_file)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
                
                # Format date to show only date part (without time)
                if format_date:
                    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            
            return df
        except Exception as e:
            return pd.DataFrame(columns=EXCEL_COLUMNS)
    
    def get_latest_report(self):
        """Get the most recent report"""
        df = self.get_all_reports(format_date=False)  # Keep datetime for latest report
        if not df.empty:
            return df.iloc[0].to_dict()
        return None
    
    def get_parameter_history(self, parameter):
        """Get history of a specific parameter"""
        df = self.get_all_reports(format_date=False)
        if parameter in df.columns:
            history = df[['Date', parameter]].dropna()
            # Format date for display
            history['Date'] = history['Date'].dt.strftime('%Y-%m-%d')
            return history
        return pd.DataFrame()
    
    def delete_report(self, index):
        """Delete a report by index"""
        try:
            df = pd.read_excel(self.excel_file)
            df = df.drop(index).reset_index(drop=True)
            df.to_excel(self.excel_file, index=False)
            return True, "Report deleted successfully"
        except Exception as e:
            return False, f"Error deleting report: {str(e)}"
    
    def update_report(self, index, report_data):
        """Update an existing report (legacy method)"""
        try:
            df = pd.read_excel(self.excel_file)
            for key, value in report_data.items():
                if key in df.columns:
                    df.at[index, key] = value
            df.to_excel(self.excel_file, index=False)
            return True, "Report updated successfully"
        except Exception as e:
            return False, f"Error updating report: {str(e)}"
    
    def find_exact_duplicate(self, report_data):
        """Check if an exact duplicate exists"""
        df = self.get_all_reports(format_date=False)
        
        if df.empty:
            return None
        
        for idx, row in df.iterrows():
            match = True
            for col in EXCEL_COLUMNS:
                if col in report_data and col in row:
                    if report_data[col] != row[col]:
                        match = False
                        break
            
            if match:
                return idx
        
        return None