#!/usr/bin/env python3
"""
Demo Enhanced Schema Data Profiler
Shows the new configuration-driven field pattern recognition system in action
"""

import sys
import os
import json

# Add the profiler directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'profiler'))

def demo_field_patterns():
    """Demonstrate field pattern recognition capabilities"""
    try:
        from field_pattern_config import FieldPatternConfig
        
        print("🎯 FIELD PATTERN RECOGNITION DEMO")
        print("=" * 60)
        
        # Initialize configuration
        config = FieldPatternConfig()
        
        # Demo 1: Pattern Identification
        print("\n🔍 Demo 1: Pattern Identification")
        print("-" * 40)
        
        demo_columns = [
            'customer_email_address',
            'user_phone_number',
            'product_id',
            'order_created_date',
            'total_purchase_amount',
            'customer_postal_code',
            'company_website_url',
            'customer_first_name',
            'account_is_active',
            'inventory_stock_quantity'
        ]
        
        for column in demo_columns:
            field_type, pattern_config = config.identify_field_type(column)
            if field_type:
                validation = pattern_config.get('validation', {})
                print(f"  📝 {column:<30} -> {field_type:<15} ({validation.get('type', 'none')})")
            else:
                print(f"  ❓ {column:<30} -> No pattern found")
        
        # Demo 2: Validation Examples
        print("\n🧪 Demo 2: Validation Examples")
        print("-" * 40)
        
        validation_examples = {
            'email': ['john.doe@company.com', 'invalid-email', 'user@domain.org', 'test@test'],
            'phone': ['555-123-4567', '1234567890', 'invalid-phone', '+1-555-123-4567'],
            'postal_code': ['12345', 'A1B2C3', '12345-6789', 'invalid'],
            'monetary': ['99.99', '0.00', '1000000.01', 'invalid-price', '-50.00']
        }
        
        for field_type, values in validation_examples.items():
            print(f"\n  💰 {field_type.upper()} Validation:")
            
            # Find pattern for this field type
            pattern_config = None
            for pattern_name, config_data in config.patterns.items():
                if field_type in pattern_name:
                    pattern_config = config_data
                    break
            
            if pattern_config:
                threshold = config.get_validation_threshold(pattern_config)
                print(f"     Threshold: {threshold:.1%}")
                
                for value in values:
                    is_valid = config.validate_field_value(field_type, value, pattern_config)
                    status = "✅" if is_valid else "❌"
                    print(f"     {status} {value}")
            else:
                print(f"     ⚠️  No pattern configuration found")
        
        # Demo 3: Configuration Management
        print("\n⚙️  Demo 3: Configuration Management")
        print("-" * 40)
        
        # Show current patterns
        summary = config.get_pattern_summary()
        print(f"  📊 Current patterns: {summary['total_patterns']}")
        print(f"  🏷️  Types: {', '.join(summary['pattern_types'][:5])}...")
        
        # Add a custom pattern
        custom_pattern = {
            "keywords": ["sku", "product_code", "item_code"],
            "validation": {
                "type": "regex",
                "pattern": "^[A-Z]{2,3}\\d{4,6}$",
                "description": "SKU format: 2-3 letters + 4-6 digits",
                "threshold": 0.8
            },
            "field_type": "sku_field"
        }
        
        print("\n  ➕ Adding custom SKU pattern...")
        config.add_custom_pattern("sku", custom_pattern)
        
        # Test the new pattern
        test_sku = "ABC12345"
        field_type, pattern_config = config.identify_field_type(test_sku)
        if field_type == "sku":
            print(f"     ✅ Custom pattern working: {test_sku} -> {field_type}")
        else:
            print(f"     ❌ Custom pattern failed: {test_sku} -> {field_type}")
        
        # Show updated summary
        updated_summary = config.get_pattern_summary()
        print(f"  📊 Updated patterns: {updated_summary['total_patterns']}")
        
        # Export patterns
        print("\n  💾 Exporting patterns...")
        if config.export_patterns('demo_exported_patterns.json'):
            print("     ✅ Patterns exported successfully")
        else:
            print("     ❌ Pattern export failed")
        
        print("\n✅ Field pattern demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Field pattern demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_enhanced_profiler():
    """Demonstrate the enhanced profiler capabilities"""
    try:
        from schema_data_profiler import SchemaDataProfiler
        
        print("\n🎯 ENHANCED SCHEMA PROFILER DEMO")
        print("=" * 60)
        
        # Initialize profiler
        profiler = SchemaDataProfiler({
            'host': 'localhost',
            'user': 'root',
            'password': 'your_password',
            'port': 3306
        })
        
        # Show field pattern information
        profiler.show_field_patterns_info()
        
        # Demo pattern reloading
        print("\n🔄 Demo: Pattern Reloading")
        print("-" * 40)
        
        print("  Reloading field patterns...")
        summary = profiler.reload_field_patterns()
        print(f"  ✅ Patterns reloaded: {summary['total_patterns']} patterns available")
        
        # Demo custom pattern addition
        print("\n➕ Demo: Adding Custom Pattern")
        print("-" * 40)
        
        custom_pattern = {
            "keywords": ["hash", "md5", "sha", "checksum"],
            "validation": {
                "type": "regex",
                "pattern": "^[a-fA-F0-9]{32,64}$",
                "description": "Hash format: 32-64 hex characters",
                "threshold": 0.9
            },
            "field_type": "hash_field"
        }
        
        profiler.field_patterns.add_custom_pattern("hash", custom_pattern)
        print("  ✅ Added hash pattern")
        
        # Show updated patterns
        updated_summary = profiler.field_patterns.get_pattern_summary()
        print(f"  📊 Total patterns now: {updated_summary['total_patterns']}")
        
        # Test the new pattern
        test_hash = "a1b2c3d4e5f6789012345678901234567890abcdef"
        field_type, pattern_config = profiler.field_patterns.identify_field_type(test_hash)
        if field_type == "hash":
            print(f"  ✅ Hash pattern working: {test_hash[:20]}... -> {field_type}")
        else:
            print(f"  ❌ Hash pattern failed: {test_hash[:20]}... -> {field_type}")
        
        print("\n✅ Enhanced profiler demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Enhanced profiler demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_configuration_file():
    """Demonstrate the configuration file structure and usage"""
    print("\n📁 CONFIGURATION FILE DEMO")
    print("=" * 60)
    
    try:
        # Read and display the configuration file
        config_file = 'profiler/field_patterns.json'
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            print(f"📂 Configuration file: {config_file}")
            print(f"📊 Total patterns: {len(config_data['field_patterns'])}")
            
            print("\n🔍 Pattern Examples:")
            for i, (pattern_name, pattern_config) in enumerate(config_data['field_patterns'].items()):
                if i >= 3:  # Show only first 3
                    print(f"  ... and {len(config_data['field_patterns']) - 3} more patterns")
                    break
                
                validation = pattern_config.get('validation', {})
                print(f"\n  🏷️  {pattern_name}:")
                print(f"     Keywords: {', '.join(pattern_config['keywords'][:3])}...")
                print(f"     Field Type: {pattern_config['field_type']}")
                print(f"     Validation: {validation.get('type', 'none')}")
                print(f"     Threshold: {validation.get('threshold', 'N/A')}")
            
            print("\n💡 Configuration Benefits:")
            print("  ✅ Easy to add new field types")
            print("  ✅ Configurable validation rules")
            print("  ✅ Centralized pattern management")
            print("  ✅ No code changes needed for new patterns")
            print("  ✅ Consistent validation across all field types")
            
        else:
            print(f"❌ Configuration file not found: {config_file}")
            return False
        
        print("\n✅ Configuration file demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Configuration file demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all demos for the enhanced profiler system"""
    print("🚀 Enhanced Schema Data Profiler Demo")
    print("=" * 70)
    print("🎯 Demonstrating configuration-driven field pattern recognition")
    print("=" * 70)
    
    demos = [
        demo_field_patterns,
        demo_enhanced_profiler,
        demo_configuration_file
    ]
    
    completed = 0
    total = len(demos)
    
    for demo in demos:
        if demo():
            completed += 1
        print()
    
    print("=" * 70)
    print(f"📊 Demo Results: {completed}/{total} demos completed")
    
    if completed == total:
        print("🎉 All demos completed successfully!")
        print("\n🎯 What You've Seen:")
        print("   - Dynamic field pattern recognition")
        print("   - Configuration-driven validation")
        print("   - Custom pattern management")
        print("   - Pattern reloading and configuration")
        print("   - Consistent validation across all field types")
        
        print("\n🚀 Next Steps:")
        print("   1. Run 'python test_enhanced_profiler.py' to test the system")
        print("   2. Modify 'profiler/field_patterns.json' to add new patterns")
        print("   3. Use the enhanced profiler in your schema mapping projects")
        
    else:
        print("⚠️  Some demos failed. Please check the errors above.")
    
    return completed == total

if __name__ == "__main__":
    main() 