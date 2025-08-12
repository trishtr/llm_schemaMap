#!/usr/bin/env python3
"""
Field Pattern Configuration for Schema Data Profiler
Handles dynamic pattern recognition and validation based on configuration files
"""

import json
import re
import pandas as pd
from pathlib import Path

class FieldPatternConfig:
    def __init__(self, config_file='field_patterns.json'):
        """Initialize field pattern configuration"""
        self.config_file = Path(__file__).parent / config_file
        self.patterns = self._load_patterns()
    
    def _load_patterns(self):
        """Load patterns from configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                print(f"✅ Loaded field patterns from {self.config_file}")
                return config['field_patterns']
        except FileNotFoundError:
            print(f"⚠️  Config file {self.config_file} not found, using defaults")
            return self._get_default_patterns()
        except json.JSONDecodeError as e:
            print(f"⚠️  Invalid JSON in config file: {e}, using defaults")
            return self._get_default_patterns()
        except Exception as e:
            print(f"⚠️  Error loading config: {e}, using defaults")
            return self._get_default_patterns()
    
    def _get_default_patterns(self):
        """Fallback default patterns if config file is not available"""
        return {
            "email": {
                "keywords": ["email", "mail"],
                "validation": {
                    "type": "regex", 
                    "pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.[\\w]+$",
                    "description": "Email address format",
                    "threshold": 0.7
                },
                "field_type": "email_field"
            },
            "phone": {
                "keywords": ["phone", "tel"],
                "validation": {
                    "type": "regex",
                    "pattern": "^[\\d\\s\\-\\(\\)]{7,}$",
                    "description": "Phone number format",
                    "threshold": 0.7
                },
                "field_type": "phone_field"
            },
            "identifier": {
                "keywords": ["id", "key"],
                "validation": {
                    "type": "numeric",
                    "description": "Numeric identifier",
                    "threshold": 0.8
                },
                "field_type": "identifier_field"
            }
        }
    
    def identify_field_type(self, column_name):
        """Identify field type based on column name"""
        column_lower = column_name.lower()
        
        # Check each pattern for keyword matches
        for pattern_name, pattern_config in self.patterns.items():
            for keyword in pattern_config['keywords']:
                if keyword in column_lower:
                    return pattern_name, pattern_config
        
        return None, None
    
    def validate_field_value(self, field_type, value, pattern_config):
        """Validate field value based on pattern configuration"""
        validation = pattern_config.get('validation', {})
        validation_type = validation.get('type')
        
        try:
            if validation_type == 'regex':
                pattern = validation.get('pattern')
                if pattern:
                    return bool(re.match(pattern, str(value)))
                return True
            
            elif validation_type == 'numeric':
                try:
                    float(value)
                    return True
                except (ValueError, TypeError):
                    return False
            
            elif validation_type == 'numeric_range':
                try:
                    num_value = float(value)
                    min_val = validation.get('min', float('-inf'))
                    max_val = validation.get('max', float('inf'))
                    return min_val <= num_value <= max_val
                except (ValueError, TypeError):
                    return False
            
            elif validation_type == 'date_format':
                try:
                    pd.to_datetime(value)
                    return True
                except (ValueError, TypeError):
                    return False
            
            elif validation_type == 'text_format':
                # Check if text contains only letters, spaces, and common punctuation
                text = str(value)
                return bool(re.match(r'^[a-zA-Z\s\-\'\.]+$', text))
            
            elif validation_type == 'boolean_like':
                # Check for boolean-like values
                bool_like = str(value).lower()
                return bool_like in ['true', 'false', '1', '0', 'yes', 'no', 'a', 'i']
            
            return True  # Default to valid if no validation specified
            
        except Exception as e:
            print(f"⚠️  Validation error for {field_type}: {e}")
            return True  # Default to valid on error
    
    def get_validation_threshold(self, pattern_config):
        """Get validation threshold for a pattern"""
        validation = pattern_config.get('validation', {})
        return validation.get('threshold', 0.7)  # Default threshold
    
    def reload_patterns(self):
        """Reload patterns from configuration file"""
        print("🔄 Reloading field patterns...")
        self.patterns = self._load_patterns()
        return self.patterns
    
    def get_pattern_summary(self):
        """Get summary of loaded patterns"""
        summary = {
            'total_patterns': len(self.patterns),
            'pattern_types': list(self.patterns.keys()),
            'validation_types': set()
        }
        
        for pattern_config in self.patterns.values():
            validation_type = pattern_config.get('validation', {}).get('type', 'unknown')
            summary['validation_types'].add(validation_type)
        
        summary['validation_types'] = list(summary['validation_types'])
        return summary
    
    def add_custom_pattern(self, pattern_name, pattern_config):
        """Add a custom pattern dynamically"""
        self.patterns[pattern_name] = pattern_config
        print(f"✅ Added custom pattern: {pattern_name}")
        return True
    
    def remove_pattern(self, pattern_name):
        """Remove a pattern"""
        if pattern_name in self.patterns:
            del self.patterns[pattern_name]
            print(f"✅ Removed pattern: {pattern_name}")
            return True
        else:
            print(f"⚠️  Pattern not found: {pattern_name}")
            return False
    
    def export_patterns(self, filename='exported_patterns.json'):
        """Export current patterns to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump({'field_patterns': self.patterns}, f, indent=2)
            print(f"✅ Patterns exported to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error exporting patterns: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Test the configuration
    config = FieldPatternConfig()
    
    print("\n🔍 Testing Field Pattern Configuration:")
    print("=" * 50)
    
    # Test pattern identification
    test_columns = [
        'customer_email',
        'phone_number', 
        'user_id',
        'created_date',
        'total_amount',
        'postal_code',
        'website_url',
        'first_name',
        'is_active',
        'stock_quantity'
    ]
    
    for column in test_columns:
        field_type, pattern_config = config.identify_field_type(column)
        if field_type:
            print(f"✅ {column:<20} -> {field_type:<15} ({pattern_config['field_type']})")
        else:
            print(f"❌ {column:<20} -> No pattern found")
    
    # Show configuration summary
    print("\n📊 Configuration Summary:")
    summary = config.get_pattern_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test validation
    print("\n🧪 Testing Validation:")
    test_values = {
        'email': ['test@example.com', 'invalid-email', 'user@domain.org'],
        'phone': ['555-1234', '1234567890', 'invalid-phone'],
        'numeric': ['123', '456', 'abc', '789']
    }
    
    for field_type, values in test_values.items():
        print(f"\n  {field_type}:")
        for value in values:
            # Find pattern for this field type
            pattern_config = None
            for pattern_name, config_data in config.patterns.items():
                if field_type in pattern_name:
                    pattern_config = config_data
                    break
            
            if pattern_config:
                is_valid = config.validate_field_value(field_type, value, pattern_config)
                status = "✅" if is_valid else "❌"
                print(f"    {status} {value}")
            else:
                print(f"    ⚠️  {value} (no pattern config)") 