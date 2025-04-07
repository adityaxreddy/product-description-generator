import json
import os
from typing import Dict, Any, List, Optional

from google.cloud import storage
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class GCSProductInfoTool(BaseTool):
    """Tool for retrieving product information from Google Cloud Storage."""
    
    name: str = "gcs_product_info_tool"
    description: str = "Retrieves product information from Google Cloud Storage based on product name or category"
    
    bucket_name: str = os.getenv("GCS_BUCKET_NAME", "product_info_bucket")
    
    def _get_client(self):
        """Get a GCS client."""
        return storage.Client()
    
    def _list_products(self) -> List[str]:
        """List all products in the bucket."""
        client = self._get_client()
        bucket = client.get_bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix="products/")
        return [blob.name.split("/")[-1].replace(".json", "") for blob in blobs if blob.name.endswith(".json")]
    
    def _get_product_info(self, product_name: str) -> Dict[str, Any]:
        """Get product information from GCS."""
        client = self._get_client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(f"products/{product_name}.json")
        
        if not blob.exists():
            return {"error": f"Product '{product_name}' not found"}
        
        content = blob.download_as_text()
        return json.loads(content)
    
    def _get_template(self, template_name: str) -> str:
        """Get a template from GCS."""
        client = self._get_client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(f"templates/{template_name}.md")
        
        if not blob.exists():
            return "No template found"
        
        return blob.download_as_text()
        
    def _run(self, query: str) -> str:
        """Run the tool to retrieve product information based on the query."""
        # First, try to get the product directly if it's an exact match
        try:
            product_info = self._get_product_info(query.strip())
            if "error" not in product_info:
                return json.dumps(product_info)
        except Exception as e:
            pass
        
        # If no exact match, list all products and find the closest match
        try:
            products = self._list_products()
            
            # Find products that contain the query string
            matching_products = [p for p in products if query.lower() in p.lower()]
            
            if matching_products:
                # Get the first matching product
                product_info = self._get_product_info(matching_products[0])
                return json.dumps(product_info)
            else:
                # No matching products found, generate information based on the query
                return self._generate_product_info(query)
        except Exception as e:
            # If there's an error with GCS, generate information
            return self._generate_product_info(query)

def _generate_product_info(self, query: str) -> str:
    """Generate product information when no match is found in GCS."""
    # Extract potential product details from the query
    product_name = query
    category = "Unknown"
    
    # Basic extraction of product name if query is complex
    if " for " in query:
        parts = query.split(" for ")
        product_name = parts[0].strip()
        target_audience = parts[1].strip()
    else:
        target_audience = "General consumers"
    
    # Determine category based on common keywords
    electronics_keywords = ["phone", "smartphone", "laptop", "computer", "tablet", "headphone", "earbud", "camera"]
    clothing_keywords = ["shirt", "pants", "dress", "jacket", "shoe", "hat", "sock", "glove"]
    home_keywords = ["furniture", "chair", "table", "bed", "sofa", "lamp", "rug", "curtain"]
    
    for keyword in electronics_keywords:
        if keyword in query.lower():
            category = "Electronics"
            break
    
    for keyword in clothing_keywords:
        if keyword in query.lower():
            category = "Clothing"
            break
    
    for keyword in home_keywords:
        if keyword in query.lower():
            category = "Home & Furniture"
            break
    
    # Create a basic product info structure
    generated_info = {
        "product_name": product_name,
        "category": category,
        "key_features": "Features extracted from query: " + query,
        "specifications": {
            "detail1": "Generated specification 1",
            "detail2": "Generated specification 2"
        },
        "target_audience": target_audience,
        "price": "Price not specified",
        "template": "Introducing the {product_name}: a quality product designed for {target_audience}. Featuring {key_features}, this {category} product delivers exceptional value.",
        "generated": True  # Flag to indicate this was generated, not retrieved
    }
    
    return json.dumps(generated_info)

