# Schema Mapping Data Profiler

A powerful and efficient data profiling tool designed specifically for schema mapping use cases. This tool analyzes database schemas, identifies field patterns, and provides insights for mapping data between different systems with varying naming conventions.

## 🚀 **NEW: Configuration-Driven Field Pattern Recognition**

The profiler now features a **dynamic, configuration-driven approach** that makes it easy to:

- **Add new field types** without code changes
- **Configure validation rules** for each field type
- **Maintain consistent validation** across all patterns
- **Customize thresholds** and patterns per field type

### ✨ **Key Features**

- **🔍 Smart Pattern Recognition**: Automatically identifies field types based on column names
- **✅ Comprehensive Validation**: Validates all identified fields (not just email)
- **⚙️ Configuration-Driven**: Easy to modify patterns via JSON configuration
- **🔄 Dynamic Updates**: Reload patterns without restarting the profiler
- **📊 Consistent Insights**: Uniform validation approach across all field types
- **🎯 Schema-Focused**: Optimized for schema mapping rather than comprehensive data analysis

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Enhanced Profiler                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │ SchemaDataProfiler │    │      FieldPatternConfig       │ │
│  │                 │    │                                 │ │
│  │ • Profile tables│    │ • Load patterns from JSON       │ │
│  │ • Analyze schema│    │ • Identify field types          │ │
│  │ • Generate      │    │ • Validate field values         │ │
│  │   insights      │    │ • Manage custom patterns        │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
│           │                           │                      │
│           └───────────────────────────┘                      │
│                    │                                        │
│                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              field_patterns.json                        │ │
│  │                                                         │ │
│  │ • Field type definitions                               │ │
│  │ • Validation rules                                     │ │
│  │ • Thresholds                                           │ │
│  │ • Keywords for identification                          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 **Project Structure**

```
llm_based/
├── profiler/
│   ├── schema_data_profiler.py      # Main profiler class
│   ├── field_pattern_config.py      # Pattern configuration manager
│   └── field_patterns.json          # Field pattern definitions
├── test_enhanced_profiler.py        # Test the enhanced system
├── demo_enhanced_profiler.py        # Demo the new features
└── README.md                        # This file
```

## 🎯 **Field Pattern Types Supported**

| Pattern Type    | Keywords              | Validation    | Description          |
| --------------- | --------------------- | ------------- | -------------------- |
| **Email**       | email, mail, e-mail   | Regex pattern | Email address format |
| **Phone**       | phone, tel, mobile    | Regex pattern | Phone number format  |
| **Identifier**  | id, key, pk, fk       | Numeric check | Numeric identifier   |
| **Date**        | date, time, created   | Date format   | Date/time format     |
| **Monetary**    | price, amount, cost   | Numeric range | Monetary value range |
| **Postal Code** | zip, postal, postcode | Regex pattern | Postal code format   |
| **URL**         | url, link, website    | Regex pattern | URL format           |
| **Name**        | name, first, last     | Text format   | Name format          |
| **Status**      | status, state, active | Boolean-like  | Status indicator     |
| **Quantity**    | quantity, qty, stock  | Numeric check | Numeric quantity     |

## 🚀 **Quick Start**

### 1. **Install Dependencies**

```bash
pip install mysql-connector-python pandas python-dotenv
```

### 2. **Configure Database Connection**

```bash
cp config.env.example config.env
# Edit config.env with your database credentials
```

### 3. **Run the Enhanced Profiler**

```bash
# Test the system
python test_enhanced_profiler.py

# See a demo
python demo_enhanced_profiler.py

# Run the actual profiler
python profiler/schema_data_profiler.py
```

## ⚙️ **Configuration**

### **Adding New Field Types**

Edit `profiler/field_patterns.json`:

```json
{
  "field_patterns": {
    "custom_type": {
      "keywords": ["custom", "special", "unique"],
      "validation": {
        "type": "regex",
        "pattern": "^[A-Z]{2,3}\\d{3,4}$",
        "description": "Custom format: 2-3 letters + 3-4 digits",
        "threshold": 0.8
      },
      "field_type": "custom_field"
    }
  }
}
```

### **Validation Types Available**

- **`regex`**: Pattern matching with custom regex
- **`numeric`**: Numeric value validation
- **`numeric_range`**: Numeric value within range
- **`date_format`**: Date/time format validation
- **`text_format`**: Text format validation
- **`boolean_like`**: Boolean-like value validation

### **Dynamic Pattern Management**

```python
from profiler.field_pattern_config import FieldPatternConfig

config = FieldPatternConfig()

# Add custom pattern
config.add_custom_pattern("new_type", pattern_config)

# Remove pattern
config.remove_pattern("old_type")

# Reload from file
config.reload_patterns()

# Export patterns
config.export_patterns("my_patterns.json")
```

## 🔍 **What the Profiler Analyzes**

### **Schema Information**

- ✅ Table structures and relationships
- ✅ Column names, types, and constraints
- ✅ Primary keys, foreign keys, and indexes
- ✅ Naming conventions (snake_case, PascalCase, UPPER_CASE)

### **Field Pattern Recognition**

- ✅ **Automatic field type identification** based on column names
- ✅ **Comprehensive validation** for all identified field types
- ✅ **Configurable validation rules** and thresholds
- ✅ **Consistent error reporting** across all patterns

### **Mapping Insights**

- ✅ Naming convention differences
- ✅ Data type compatibility
- ✅ Potential mapping issues
- ✅ Complexity assessment (LOW/MEDIUM/HIGH)

## 📊 **Sample Output**

```
🔍 FIELD PATTERN CONFIGURATION INFO
============================================================
📊 Total Patterns: 10
🏷️  Pattern Types: email, phone, identifier, date, monetary, postal_code, url, name, status, quantity
✅ Validation Types: regex, numeric, numeric_range, date_format, text_format, boolean_like

📋 Detailed Pattern Information:

  🏷️  email:
     Keywords: email, mail, e-mail, email_address
     Field Type: email_field
     Validation: regex
     Threshold: 0.7
     Description: Email address format

  🏷️  phone:
     Keywords: phone, tel, mobile, cell, phone_number
     Field Type: phone_field
     Validation: regex
     Threshold: 0.7
     Description: Phone number format
```

## 🎯 **Use Cases**

### **Schema Mapping Projects**

- **Data Warehouse Migration**: Map source systems to target schemas
- **System Integration**: Align different naming conventions
- **Data Quality Assessment**: Validate field formats across systems
- **Compliance Checking**: Ensure data meets business rules

### **Development and Testing**

- **Rapid Prototyping**: Quick schema analysis for new projects
- **Regression Testing**: Validate schema changes
- **Documentation**: Generate comprehensive schema reports
- **Training**: Educate teams on data structures

## 🔧 **Customization**

### **Adding Custom Validation Types**

Extend the `FieldPatternConfig` class:

```python
def validate_field_value(self, field_type, value, pattern_config):
    validation_type = pattern_config.get('validation', {}).get('type')

    if validation_type == 'custom_type':
        return self._custom_validation(value, pattern_config)
    # ... existing validation logic
```

### **Custom Field Type Handlers**

```python
def _custom_validation(self, value, pattern_config):
    # Your custom validation logic here
    custom_rules = pattern_config.get('custom_rules', {})
    # Implement custom validation
    return True  # or False
```

## 📈 **Performance Benefits**

- **⚡ Fast Pattern Recognition**: O(1) lookup for field types
- **🔄 Efficient Validation**: Only validates identified fields
- **💾 Memory Efficient**: Small sample data (5 rows) instead of full datasets
- **🚀 Scalable**: Handles large numbers of tables and columns

## 🤝 **Contributing**

To add new field patterns or validation types:

1. **Update `field_patterns.json`** with new patterns
2. **Extend `FieldPatternConfig`** if new validation types needed
3. **Test with `test_enhanced_profiler.py`**
4. **Document in this README**

## 📝 **License**

This project is open source and available under the MIT License.

---

**🎉 The enhanced profiler now provides consistent, configurable, and maintainable field pattern recognition for all your schema mapping needs!**
