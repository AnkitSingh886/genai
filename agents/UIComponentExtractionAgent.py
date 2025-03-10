import os
import json
from PIL import Image
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class UIComponentExtractionAgent:
    """Extracts UI component specifications from multiple UI images and stores them in a JSON file."""

    def __init__(self, image_folder="../data/ui_images", output_json="../data/ui_components.json"):
        """Initialize the agent with image folder and output JSON file."""
        self.image_folder = image_folder
        self.output_json = output_json
        self.llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)

    def get_image_files(self):
        """Retrieves all image files from the specified folder."""
        supported_formats = [".png", ".jpg", ".jpeg"]
        return [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) 
                if os.path.splitext(f)[1].lower() in supported_formats]

    def extract_ui_components(self, image_path):
        """Extracts UI components from an image using an AI vision model."""
        print(f"📷 Processing image: {image_path}")

        # Load the image
        try:
            image = Image.open(image_path)
            image_format = image.format
            image_size = image.size
        except Exception as e:
            print(f"⚠️ Failed to open image {image_path}: {e}")
            return None

        # Define structured prompt for UI extraction
        prompt = f"""
        You are an AI specializing in UI/UX analysis. Extract all UI components from this image.
        
        Identify:
        - UI elements (buttons, modals, cards, forms, tables, inputs, navigation bars)
        - Layout details (grid system, spacing, margins, paddings)
        - Typography (font family, sizes, bold, italic)
        - Colors (primary, secondary, background, border)
        - Interactions (hover effects, click actions, animations)

        Image Info:
        - File: {os.path.basename(image_path)}
        - Format: {image_format}
        - Size: {image_size}

        Output must be in **valid JSON format**:
        ```json
        {{
            "UI_Components": [
                {{
                    "component_name": "Button",
                    "position": "top-right",
                    "color": "#007bff",
                    "size": "medium",
                    "text": "Submit",
                    "action": "Sends form data to API"
                }},
                {{
                    "component_name": "Modal",
                    "position": "center",
                    "background_color": "#ffffff",
                    "border_radius": "8px",
                    "header_text": "Confirm Action",
                    "body_text": "Are you sure you want to proceed?",
                    "buttons": ["Yes", "Cancel"]
                }}
            ],
            "Layout": {{
                "grid_system": "12-column",
                "spacing": "16px",
                "margins": "8px",
                "paddings": "12px"
            }},
            "Typography": {{
                "font_family": "Inter",
                "heading_size": "24px",
                "body_size": "16px"
            }},
            "Colors": {{
                "primary": "#007bff",
                "secondary": "#6c757d",
                "background": "#f8f9fa",
                "success": "#28a745",
                "error": "#dc3545"
            }}
        }}
        ```

        Extract and return details in this JSON format.
        """

        # Generate response using Groq LLM
        response = self.llm.invoke(prompt)

        # Parse JSON response
        return self.clean_json_response(response.content)

    def clean_json_response(self, raw_response):
        """Cleans and parses the extracted response into a properly formatted JSON."""
        try:
            structured_output = json.loads(raw_response.strip())
        except json.JSONDecodeError:
            print("⚠️ JSON Parsing Error: Attempting to clean the response...")
            raw_response = raw_response.strip().replace("\n", "").replace("\t", "")

            start_index = raw_response.find("{")
            end_index = raw_response.rfind("}")

            if start_index != -1 and end_index != -1:
                json_string = raw_response[start_index:end_index + 1]
                try:
                    structured_output = json.loads(json_string)
                    print("✅ Successfully cleaned and parsed JSON.")
                except json.JSONDecodeError:
                    structured_output = {"error": "Failed to clean JSON", "raw_response": raw_response}
            else:
                structured_output = {"error": "No valid JSON found", "raw_response": raw_response}

        return structured_output

    def process_all_images(self):
        """Processes all images in the folder and extracts UI components."""
        image_files = self.get_image_files()

        if not image_files:
            print("⚠️ No images found in the folder.")
            return

        extracted_data = []

        for image_path in image_files:
            data = self.extract_ui_components(image_path)
            if data:
                extracted_data.append({"image": os.path.basename(image_path), "components": data})

        # Save extracted UI components to JSON file
        with open(self.output_json, "w", encoding="utf-8") as json_file:
            json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)

        print(f"✅ UI components extracted and saved to: {self.output_json}")

# Run the UI extraction agent
if __name__ == "__main__":
    agent = UIComponentExtractionAgent()
    agent.process_all_images()
