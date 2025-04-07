import os
import sys
import json
from typing import Dict, Any

from product_description_generator.crew import ProductDescriptionGenerator


def run():
    """
    Run the crew.
    """
    # Get user query from environment variable or use default
    user_query = os.getenv("USER_QUERY", "Tell me about the latest smartphone")
    
    inputs = {
        "user_query": user_query
    }

    # Run the crew
    result = ProductDescriptionGenerator().crew().kickoff(inputs=inputs)
    
    # Print the result
    print(result)
    
    return result


def process_agent_space_request(request_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a request from AgentSpace.
    
    Args:
        request_json: The JSON request from AgentSpace
        
    Returns:
        A response dictionary with the generated product description
    """
    user_query = request_json.get("query", "")
    
    # Set environment variable for the crew to use
    os.environ["USER_QUERY"] = user_query
    
    # Run the crew
    result = run()
    
    # Return formatted response
    return {
        "response": result,
        "status": "success"
    }


if __name__ == "__main__":
    run()
