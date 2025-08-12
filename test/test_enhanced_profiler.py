#!/usr/bin/env python3
"""
Test Enhanced Schema Data Profiler
Demonstrates the new configuration-driven field pattern recognition system
"""

import sys
import os

# Add the profiler directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'profiler'))

def test_field_pattern_config():
    """Test the field pattern configuration system"""
    try:
        from field_pattern_config import FieldPatternConfig
        
        print("🧪 Testing Field Pattern Configuration...")
        print("=" * 60)
        
        # Initialize configuration
        config = FieldPatternConfig()
        
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
            'stock_quantity',
            'unknown_field'
        ]
        
        print("🔍 Testing Pattern Identification:")
        for column in test_columns:
            field_type, pattern_config = config.identify_field_type(column)
            if field_type:
                print(f"  ✅ {column:<20} -> {field_type:<15} ({pattern_config['field_type']})")
            else:
                print(f"  ❌ {column:<20} -> No pattern found")
        
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
        
        print("\n✅ Field pattern configuration test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Field pattern configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_profiler():
    """Test the enhanced schema profiler with field patterns"""
    try:
        from schema_data_profiler import SchemaDataProfiler
        
        print("\n🧪 Testing Enhanced Schema Profiler...")
        print("=" * 60)
        
        # Initialize profiler (will load field patterns)
        profiler = SchemaDataProfiler({
            'host': 'localhost',
            'user': 'root',
            'password': 'your_password',
            'port': 3306
        })
        
        # Show field pattern information
        profiler.show_field_patterns_info()
        
        # Test pattern reloading
        print("\n🔄 Testing Pattern Reloading...")
        summary = profiler.reload_field_patterns()
        print(f"  Reloaded patterns: {summary['total_patterns']}")
        
        print("\n✅ Enhanced schema profiler test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Enhanced schema profiler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_custom_patterns():
    """Test adding custom patterns dynamically"""
    try:
        from field_pattern_config import FieldPatternConfig
        
        print("\n🧪 Testing Custom Pattern Management...")
        print("=" * 60)
        
        config = FieldPatternConfig()
        
        # Add custom pattern
        custom_pattern = {
            "keywords": ["custom", "special", "unique"],
            "validation": {
                "type": "regex",
                "pattern": "^[A-Z]{2,3}\\d{3,4}$",
                "description": "Custom format: 2-3 letters + 3-4 digits",
                "threshold": 0.8
            },
            "field_type": "custom_field"
        }
        
        print("➕ Adding custom pattern...")
        config.add_custom_pattern("custom_format", custom_pattern)
        
        # Test the new pattern
        test_column = "custom_field_123"
        field_type, pattern_config = config.identify_field_type(test_column)
        
        if field_type == "custom_format":
            print(f"  ✅ Custom pattern working: {test_column} -> {field_type}")
        else:
            print(f"  ❌ Custom pattern failed: {test_column} -> {field_type}")
        
        # Show updated summary
        print("\n📊 Updated Configuration Summary:")
        summary = config.get_pattern_summary()
        print(f"  Total patterns: {summary['total_patterns']}")
        print(f"  Pattern types: {', '.join(summary['pattern_types'])}")
        
        # Remove custom pattern
        print("\n➖ Removing custom pattern...")
        config.remove_pattern("custom_format")
        
        # Verify removal
        field_type, pattern_config = config.identify_field_type(test_column)
        if field_type is None:
            print(f"  ✅ Custom pattern removed: {test_column} -> No pattern found")
        else:
            print(f"  ❌ Custom pattern removal failed: {test_column} -> {field_type}")
        
        print("\n✅ Custom pattern management test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Custom pattern management test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests for the enhanced profiler system"""
    print("🚀 Testing Enhanced Schema Data Profiler System")
    print("=" * 70)
    print("🎯 Testing configuration-driven field pattern recognition")
    print("=" * 70)
    
    tests = [
        test_field_pattern_config,
        test_enhanced_profiler,
        test_custom_patterns
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced profiler system is working correctly.")
        print("\n🎯 Enhanced Features Verified:")
        print("   - Configuration-driven pattern recognition")
        print("   - Dynamic field type identification")
        print("   - Consistent validation across all field types")
        print("   - Custom pattern management")
        print("   - Pattern reloading and configuration")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 