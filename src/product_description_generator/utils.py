import json
from typing import Dict, Any, Optional

def parse_product_info(info_str: str) -> Dict[str, Any]:
    """Parse product information from string to dictionary."""
    try:
        return json.loads(info_str)
    except json.JSONDecodeError:
        # If not valid JSON, try to parse structured text
        result = {}
        lines = info_str.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        return result

def format_output(product_info: Dict[str, Any], description: str, refined_description: str) -> str:
    """Format the final output."""
    product_name = product_info.get('product_name', 'Product')
    
    output = f"""# {product_name} Description

{refined_description}

---

*This description was generated based on product information and refined for optimal engagement and SEO performance.*
"""
    return output

def apply_template(template: str, product_info: Dict[str, Any]) -> str:
    """Apply a template to product information."""
    if not template or template == "No template found":
        return ""
    
    result = template
    for key, value in product_info.items():
        if isinstance(value, str):
            placeholder = "{" + key + "}"
            result = result.replace(placeholder, value)
    
    return result
