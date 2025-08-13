#!/usr/bin/env python3
"""
SQLite3 Enhanced Schema Data Profiler
A fast, efficient data profiler designed for schema mapping use cases.
Works with SQLite3 databases and includes configuration-driven field pattern recognition.
"""

import sqlite3
import pandas as pd
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import the field pattern configuration
from field_pattern_config import FieldPatternConfig

class SQLiteSchemaDataProfiler:
    def __init__(self, db_paths):
        """Initialize the SQLite schema data profiler with database paths"""
        self.db_paths = db_paths
        self.connections = {}
        self.profiling_results = {}
        self.sample_size = 5  # Number of sample rows to collect
        
        # Initialize field pattern configuration
        self.field_patterns = FieldPatternConfig()
        print(f"✅ Field pattern configuration loaded: {self.field_patterns.get_pattern_summary()['total_patterns']} patterns available")
    
    def connect_to_database(self, db_path, connection_name):
        """Establish connection to a specific SQLite database"""
        try:
            connection = sqlite3.connect(db_path)
            connection.row_factory = sqlite3.Row  # Enable dictionary-like access
            
            self.connections[connection_name] = connection
            print(f"✅ Connected to {db_path} ({connection_name})")
            return connection
                
        except Exception as e:
            print(f"✗ Error connecting to {db_path}: {e}")
            return None
    
    def profile_table(self, connection, table_name, source_system):
        """Profile a single table - KEEPS ALL ORIGINAL FUNCTIONALITY"""
        start_time = time.time()
        
        try:
            cursor = connection.cursor()
            
            # ORIGINAL: Get table structure (SQLite3 equivalent)
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            
            # ORIGINAL: Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            row_count = cursor.fetchone()['count']
            
            # ORIGINAL: Get sample data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {self.sample_size}")
            sample_data = cursor.fetchall()
            
            # ORIGINAL: Get indexes (SQLite3 equivalent)
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes_info = cursor.fetchall()
            
            # ORIGINAL: Get table creation info (SQLite3 equivalent)
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            create_table_info = cursor.fetchone()
            
            cursor.close()
            
            profiling_time = time.time() - start_time
            
            # ORIGINAL: Identify naming convention
            naming_convention = self._identify_naming_convention(columns_info)
            
            # ENHANCED: Generate mapping insights with field patterns
            mapping_insights = self._generate_mapping_insights(columns_info, sample_data, naming_convention, source_system)
            
            # ORIGINAL: Analyze table structure
            structure_analysis = self._analyze_table_structure(columns_info, indexes_info, create_table_info)
            
            # ORIGINAL: Compile profiling results
            profiling_result = {
                'table_name': table_name,
                'source_system': source_system,
                'profiling_time': profiling_time,
                'row_count': row_count,
                'columns_info': columns_info,
                'sample_data': sample_data,
                'indexes_info': indexes_info,
                'create_table_info': create_table_info,
                'naming_convention': naming_convention,
                'mapping_insights': mapping_insights,
                'structure_analysis': structure_analysis
            }
            
            print(f"✅ Profiled {table_name} ({row_count} rows) in {profiling_time:.2f}s")
            return profiling_result
            
        except Exception as e:
            print(f"✗ Error profiling table {table_name}: {e}")
            return None
    
    def _identify_naming_convention(self, columns_info):
        """ORIGINAL: Identify naming convention from column names"""
        if not columns_info:
            return 'unknown'
        
        snake_case_count = 0
        pascal_case_count = 0
        upper_case_count = 0
        
        for col in columns_info:
            col_name = col['name']  # SQLite3 uses 'name' instead of 'Field'
            
            if '_' in col_name and col_name.islower():
                snake_case_count += 1
            elif col_name[0].isupper() and not col_name.isupper():
                pascal_case_count += 1
            elif col_name.isupper():
                upper_case_count += 1
        
        total_columns = len(columns_info)
        
        if snake_case_count / total_columns > 0.5:
            return 'snake_case'
        elif pascal_case_count / total_columns > 0.5:
            return 'PascalCase'
        elif upper_case_count / total_columns > 0.5:
            return 'UPPER_CASE'
        else:
            return 'mixed'
    
    def _analyze_table_structure(self, columns_info, indexes_info, create_table_info):
        """ORIGINAL: Analyze table structure, keys, and constraints"""
        structure_analysis = {
            'total_columns': len(columns_info),
            'primary_keys': [],
            'foreign_keys': [],
            'unique_constraints': [],
            'indexes': [],
            'data_types': {},
            'nullable_columns': [],
            'default_values': {}
        }
        
        # Analyze columns
        for col in columns_info:
            col_name = col['name']
            col_type = col['type']
            col_notnull = col['notnull']
            col_pk = col['pk']
            col_default = col['dflt_value']
            
            # Track data types
            if col_type not in structure_analysis['data_types']:
                structure_analysis['data_types'][col_type] = []
            structure_analysis['data_types'][col_type].append(col_name)
            
            # Track keys and constraints
            if col_pk:
                structure_analysis['primary_keys'].append(col_name)
            
            # Track nullable columns
            if not col_notnull:
                structure_analysis['nullable_columns'].append(col_name)
            
            # Track default values
            if col_default is not None:
                structure_analysis['default_values'][col_name] = col_default
        
        # Analyze indexes
        for idx in indexes_info:
            index_info = {
                'name': idx['name'],
                'unique': bool(idx['unique']),
                'type': 'BTREE'  # SQLite3 default
            }
            structure_analysis['indexes'].append(index_info)
        
        return structure_analysis
    
    def _generate_mapping_insights(self, columns_info, sample_data, naming_convention, source_system):
        """ENHANCED: Generate mapping insights using configuration-driven patterns"""
        insights = {
            'naming_convention': naming_convention,
            'mapping_recommendations': [],
            'data_type_notes': [],
            'sample_patterns': {},
            'potential_issues': [],
            'mapping_complexity': 'LOW'
        }
        
        # Analyze sample data patterns using configuration
        if sample_data:
            # Convert SQLite3 Row objects to dictionaries for pandas
            sample_dicts = [dict(row) for row in sample_data]
            df_sample = pd.DataFrame(sample_dicts)
            
            for col in columns_info:
                col_name = col['name']
                
                if col_name in df_sample.columns:
                    sample_values = df_sample[col_name].dropna()
                    
                    if len(sample_values) > 0:
                        # Use configuration-driven pattern recognition
                        field_type, pattern_config = self.field_patterns.identify_field_type(col_name)
                        
                        if field_type:
                            insights['sample_patterns'][col_name] = pattern_config['field_type']
                            
                            # Validate all identified fields (not just email)
                            validation_result = self._validate_field_sample(
                                sample_values, pattern_config
                            )
                            
                            if validation_result['is_valid']:
                                insights['data_type_notes'].append(
                                    f"{col_name}: Valid {field_type} format in sample"
                                )
                            else:
                                insights['potential_issues'].append(
                                    f"{col_name}: {validation_result['issues']}"
                                )
        
        # Generate mapping recommendations
        if source_system == 'source1':
            insights['mapping_recommendations'].append("Use snake_case to standardized mapping")
        elif source_system == 'source2':
            insights['mapping_recommendations'].append("Use PascalCase to standardized mapping")
        elif source_system == 'source3':
            insights['mapping_recommendations'].append("Use UPPER_CASE to standardized mapping")
        
        # Assess mapping complexity
        if len(insights['potential_issues']) > 3:
            insights['mapping_complexity'] = 'HIGH'
        elif len(insights['potential_issues']) > 1:
            insights['mapping_complexity'] = 'MEDIUM'
        
        return insights
    
    def _validate_field_sample(self, sample_values, pattern_config):
        """ENHANCED: Validate sample values using pattern configuration"""
        validation = pattern_config.get('validation', {})
        validation_type = validation.get('type')
        
        valid_count = 0
        total_count = len(sample_values)
        issues = []
        
        for value in sample_values:
            if self.field_patterns.validate_field_value(
                pattern_config['field_type'], value, pattern_config
            ):
                valid_count += 1
            else:
                issues.append(f"Invalid value: {value}")
        
        validation_percentage = (valid_count / total_count) * 100
        threshold = self.field_patterns.get_validation_threshold(pattern_config) * 100
        
        return {
            'is_valid': validation_percentage >= threshold,
            'valid_percentage': validation_percentage,
            'valid_count': valid_count,
            'total_count': total_count,
            'threshold': threshold,
            'issues': issues[:3]  # Limit to first 3 issues
        }
    
    def profile_all_systems(self):
        """ORIGINAL: Profile all source systems and target"""
        print("\n🚀 Starting comprehensive schema profiling...")
        print("=" * 60)
        
        # Profile source systems
        source_systems = [
            ('source1', 'data/source1_ecommerce.db'),
            ('source2', 'data/source2_crm.db'),
            ('source3', 'data/source3_inventory.db')
        ]
        
        for source_name, db_path in source_systems:
            print(f"\n📊 Profiling {source_name} ({db_path})...")
            
            connection = self.connect_to_database(db_path, source_name)
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    cursor.close()
                    
                    source_results = []
                    for table in tables:
                        table_name = table['name']
                        result = self.profile_table(connection, table_name, source_name)
                        if result:
                            source_results.append(result)
                    
                    self.profiling_results[source_name] = source_results
                        
                except Exception as e:
                    print(f"✗ Error profiling {source_name}: {e}")
        
        # Profile target system
        print(f"\n📊 Profiling target system...")
        target_connection = self.connect_to_database('data/target_datawarehouse.db', 'target')
        if target_connection:
            try:
                cursor = target_connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                cursor.close()
                
                target_results = []
                for table in tables:
                    table_name = table['name']
                    result = self.profile_table(target_connection, table_name, 'target')
                    if result:
                        target_results.append(result)
                
                self.profiling_results['target'] = target_results
                    
            except Exception as e:
                print(f"✗ Error profiling target: {e}")
        
        print("\n✅ Schema profiling completed!")
        return self.profiling_results
    
    def generate_schema_report(self):
        """ORIGINAL: Generate comprehensive schema report"""
        print("\n📋 Generating Schema Report...")
        print("=" * 60)
        
        for source_name, results in self.profiling_results.items():
            if isinstance(results, list):
                print(f"\n🏢 {source_name.upper()} SYSTEM:")
                for result in results:
                    if result:
                        table_name = result['table_name']
                        row_count = result['row_count']
                        naming = result['naming_convention']
                        complexity = result['mapping_insights']['mapping_complexity']
                        
                        print(f"  📊 {table_name}: {row_count} rows, {naming} naming, {complexity} complexity")
                        
                        # Show field patterns
                        patterns = result['mapping_insights']['sample_patterns']
                        if patterns:
                            print(f"     🏷️  Field patterns: {', '.join(patterns.values())}")
                        
                        # Show issues
                        issues = result['mapping_insights']['potential_issues']
                        if issues:
                            print(f"     ⚠️  Issues: {len(issues)} found")
    
    def show_column_mapping_comparison(self):
        """ORIGINAL: Show column mapping comparison between sources and target"""
        print("\n🔄 Column Mapping Comparison")
        print("=" * 60)
        
        # This would show how columns map between different systems
        # Implementation depends on your specific mapping requirements
        print("Column mapping analysis would be implemented here based on your specific needs")
    
    def export_schema_report(self):
        """ORIGINAL: Export detailed schema report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sqlite_schema_report_{timestamp}.json"
        
        try:
            # Convert SQLite3 Row objects to serializable format
            serializable_results = {}
            for source_name, results in self.profiling_results.items():
                if isinstance(results, list):
                    serializable_results[source_name] = []
                    for result in results:
                        if result:
                            # Convert SQLite3 Row objects to dictionaries
                            serializable_result = result.copy()
                            if 'sample_data' in serializable_result:
                                serializable_result['sample_data'] = [dict(row) for row in result['sample_data']]
                            if 'columns_info' in serializable_result:
                                serializable_result['columns_info'] = [dict(col) for col in result['columns_info']]
                            serializable_results[source_name].append(serializable_result)
            
            with open(filename, 'w') as f:
                json.dump(serializable_results, f, indent=2, default=str)
            print(f"✅ Schema report exported to {filename}")
        except Exception as e:
            print(f"✗ Error exporting report: {e}")
    
    def reload_field_patterns(self):
        """ENHANCED: Reload field patterns from configuration file"""
        print("🔄 Reloading field patterns...")
        self.field_patterns.reload_patterns()
        print(f"✅ Field patterns reloaded: {self.field_patterns.get_pattern_summary()['total_patterns']} patterns available")
        return self.field_patterns.get_pattern_summary()
    
    def show_field_patterns_info(self):
        """ENHANCED: Show information about available field patterns"""
        summary = self.field_patterns.get_pattern_summary()
        
        print("\n" + "="*60)
        print("🔍 FIELD PATTERN CONFIGURATION INFO")
        print("="*60)
        print(f"📊 Total Patterns: {summary['total_patterns']}")
        print(f"🏷️  Pattern Types: {', '.join(summary['pattern_types'])}")
        print(f"✅ Validation Types: {', '.join(summary['validation_types'])}")
        
        print("\n📋 Detailed Pattern Information:")
        for pattern_name, pattern_config in self.field_patterns.patterns.items():
            validation = pattern_config.get('validation', {})
            print(f"\n  🏷️  {pattern_name}:")
            print(f"     Keywords: {', '.join(pattern_config['keywords'])}")
            print(f"     Field Type: {pattern_config['field_type']}")
            print(f"     Validation: {validation.get('type', 'none')}")
            print(f"     Threshold: {validation.get('threshold', 'N/A')}")
            if validation.get('description'):
                print(f"     Description: {validation['description']}")
    
    def close_connections(self):
        """ORIGINAL: Close all database connections"""
        for name, connection in self.connections.items():
            connection.close()
            print(f"✓ Closed connection to {name}")

def main():
    """Main function to run the SQLite3 enhanced schema data profiler"""
    # Database paths
    db_paths = {
        'source1': 'data/source1_ecommerce.db',
        'source2': 'data/source2_crm.db', 
        'source3': 'data/source3_inventory.db',
        'target': 'data/target_datawarehouse.db'
    }
    
    # Initialize profiler
    profiler = SQLiteSchemaDataProfiler(db_paths)
    
    try:
        # Show field pattern information
        profiler.show_field_patterns_info()
        
        # Run comprehensive schema profiling
        results = profiler.profile_all_systems()
        
        # Generate schema report
        profiler.generate_schema_report()
        
        # Show column mapping comparison
        profiler.show_column_mapping_comparison()
        
        # Export detailed report
        profiler.export_schema_report()
        
    except Exception as e:
        print(f"✗ Error during profiling: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close connections
        profiler.close_connections()

if __name__ == "__main__":
    main() 