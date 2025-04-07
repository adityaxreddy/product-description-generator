import sys

from product_description_generator.crew import ProductDescriptionGenerator


def run():
    """
    Run the crew.
    """
    inputs = {
        "product_name": "<Product Name>",
        "product_category": "<Product Category>",
        "target_audience": "<Target Audience>",
        "key_features": "<Key Features>"
    }

    ProductDescriptionGenerator().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "product_name": "UltraBoost Running Shoes",
        "product_category": "Athletic Footwear",
        "target_audience": "Serious runners and fitness enthusiasts",
        "key_features": "Responsive cushioning, breathable mesh, durable outsole"
    }
    try:
        ProductDescriptionGenerator().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ProductDescriptionGenerator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "product_name": "UltraBoost Running Shoes",
        "product_category": "Athletic Footwear",
        "target_audience": "Serious runners and fitness enthusiasts",
        "key_features": "Responsive cushioning, breathable mesh, durable outsole"
    }
    try:
        ProductDescriptionGenerator().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
