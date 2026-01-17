import dspy
import json
from typing import Literal, Optional, Union

class ClassifierFactory:
    @staticmethod
    def create_signature(topic: str, categories: dict, subcategories: dict):
        # 1. Prepare Instructions
        cat_str = json.dumps(categories, indent=2)
        subcat_str = json.dumps(subcategories, indent=2)
        
        instructions = (
            f"You are an AI assistant tasked with categorizing questions related to {topic}. "
            f"Classify the query into one of the following categories and subcategories:\n"
            f"{cat_str}\n"
            f"Subcategories:\n{subcat_str}\n\n"
            f"Return 'None' for subcategory if it does not apply."
        )

        # 2. Define the Fields Dictionary
        # This dict acts as the "body" of the class
        class_body = {
            "__doc__": instructions, # The docstring becomes the DSPy instructions
            "question": dspy.InputField(desc="The query to be classified"),
            "category": dspy.OutputField(desc="Select the most relevant category"),
            "subcategory": dspy.OutputField(desc="Select the relevant subcategory or 'None'")
        }

        # 3. Create the Class Dynamically
        # Syntax: type(name, bases, dict)
        # We inherit from dspy.Signature
        SignatureClass = type(
            f"{topic.replace(' ', '')}Classifier", 
            (dspy.Signature,), 
            class_body
        )

        # 4. Inject Type Hints for Validation (The Literal Logic)
        # Create the dynamic literals
        CategoryType = Literal.__getitem__(tuple(categories.keys()))
        subcat_keys = list(subcategories.keys()) + ['None']
        SubcategoryType = Literal.__getitem__(tuple(subcat_keys))
        
        # Patch the annotations so DSPy sees the types
        SignatureClass.__annotations__ = {
            "question": str,
            "category": CategoryType,
            "subcategory": SubcategoryType
        }

        # Inject Valid Options for our Validator to read later
        SignatureClass._valid_cats = list(categories.keys())
        SignatureClass._valid_subcats = list(subcategories.keys()) + ['None']
        
        return SignatureClass

    
# --- 2. The Generic Module with Manual Retry ---
class GenericCategorizer(dspy.Module):
    def __init__(self, topic, categories, subcategories, max_retries=2):
        super().__init__()
        self.Signature = ClassifierFactory.create_signature(topic, categories, subcategories)
        self.predictor = dspy.ChainOfThought(self.Signature)
        self.max_retries = max_retries
    
    def forward(self, question):
        # 1. First Attempt
        prediction = self.predictor(question=question)
        
        # 2. Validation Loop (The "Guardrail")
        for i in range(self.max_retries):
            errors = []
            
            # Check Category
            valid_cats = self.Signature._valid_cats
            if prediction.category not in valid_cats:
                errors.append(f"Category '{prediction.category}' is invalid. Must be one of: {valid_cats}.")
            
            # Check Subcategory
            valid_subcats = self.Signature._valid_subcats
            if prediction.subcategory not in valid_subcats:
                errors.append(f"Subcategory '{prediction.subcategory}' is invalid. Must be one of: {valid_subcats}.")
            
            # If no errors, we are done!
            if not errors:
                return prediction
            
            # 3. If errors, Retry with Feedback
            # We explicitly tell the model what it did wrong (Self-Correction)
            error_msg = " ".join(errors)
            print(f"Retry {i+1}: {error_msg}") # Optional logging
            
            # We use the 'demos' or context feature of ChainOfThought to inject the error
            # Or simply re-run with a modified prompt. 
            # A simple way in DSPy is to just call it again with the error appended to the question
            # or use the 'rationale' history if available.
            
            # Here is the cleanest "Stateful" retry pattern:
            prediction = self.predictor(
                question=question + f"\n\nPREVIOUS ERROR: I answered incorrectly. {error_msg} Please correct this."
            )
            
        return prediction    
    
# --- Usage Example ---

