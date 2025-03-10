# import os
# import json

# class SmartAngularCodeGenerator:
#     """Fetches existing files and updates them with generated code based on JSON specifications."""

#     def __init__(self, project_root="../data/angular_project",
#                  srs_json="../data/extracted_data.json",
#                  ui_json="../data/ui_components.json"):
#         """Initialize the generator with project folder and JSON files."""
#         self.project_root = project_root
#         self.srs_json = srs_json
#         self.ui_json = ui_json

#         # Load JSON files
#         self.srs_data = self.load_json(self.srs_json)
#         self.ui_data = self.load_json(self.ui_json)

#         # Scan the generated folder structure
#         self.files_structure = self.scan_folder_structure()

#     def load_json(self, json_path):
#         """Loads JSON data from the given file."""
#         if not os.path.exists(json_path):
#             print(f"⚠️ JSON file not found: {json_path}")
#             return {}

#         with open(json_path, "r", encoding="utf-8") as json_file:
#             return json.load(json_file)

#     def scan_folder_structure(self):
#         """Scans the generated project folder structure and returns a dictionary of files."""
#         files_dict = {}
#         for root, dirs, files in os.walk(self.project_root):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 relative_path = os.path.relpath(file_path, self.project_root)
#                 files_dict[relative_path] = file_path
#         return files_dict

#     def update_existing_component_files(self):
#         """Fetch each component and update it with code based on specifications."""
#         for relative_path, full_path in self.files_structure.items():
#             if relative_path.startswith("src/app/components/") and relative_path.endswith(".component.ts"):
#                 component_name = os.path.basename(relative_path).replace(".component.ts", "")
#                 component_specs = self.get_component_specifications(component_name)

#                 if component_specs:
#                     self.update_component_ts(full_path, component_name, component_specs)
#                     self.update_component_html(full_path.replace(".ts", ".html"), component_specs)
#                     self.update_component_scss(full_path.replace(".ts", ".scss"), component_specs)

#     def get_component_specifications(self, component_name):
#         """Fetch UI and API specifications for a given component from JSON files."""
#         specs = {"api": None, "styles": {}, "structure": ""}
        
#         # Get UI specifications from the UI JSON
#         if isinstance(self.ui_data, list):
#             for item in self.ui_data:
#                 if isinstance(item, dict) and "components" in item:
#                     for comp in item["components"]:
#                         if comp.get("component_name", "").lower() == component_name:
#                             specs["styles"] = comp.get("styles", {})
#                             specs["structure"] = comp.get("structure", "")

#         # Get API specifications from the SRS JSON
#         api_endpoints = self.srs_data.get("API_Endpoints", [])
#         for endpoint in api_endpoints:
#             if component_name in endpoint.get("related_component", "").lower():
#                 specs["api"] = endpoint

#         return specs if specs["styles"] or specs["api"] else None

#     def update_component_ts(self, ts_path, component_name, specs):
#         """Updates TypeScript file with correct logic based on specifications."""
#         api_call = ""
#         if specs["api"]:
#             api_method = specs["api"]["method"].lower()
#             api_endpoint = specs["api"]["endpoint"]
#             api_call = f"""
#     constructor(private apiService: ApiService) {{}}

#     fetchData() {{
#         this.apiService.{api_method}('{api_endpoint}').subscribe(response => {{
#             console.log("API Response:", response);
#         }});
#     }}"""

#         ts_code = f"""import {{ Component }} from '@angular/core';
# import {{ ApiService }} from '../services/api.service';

# @Component({{
#     selector: 'app-{component_name}',
#     templateUrl: './{component_name}.component.html',
#     styleUrls: ['./{component_name}.component.scss']
# }})
# export class {component_name.capitalize()}Component {{{api_call}
# }}
# """
#         with open(ts_path, "w", encoding="utf-8") as ts_file:
#             ts_file.write(ts_code)
#         print(f"✅ Updated TypeScript file for {component_name}")

#     def update_component_html(self, html_path, specs):
#         """Updates HTML file with correct UI structure based on specifications."""
#         if not specs["structure"]:
#             return

#         with open(html_path, "w", encoding="utf-8") as html_file:
#             html_file.write(specs["structure"])
#         print(f"✅ Updated HTML file for component")

#     def update_component_scss(self, scss_path, specs):
#         """Updates SCSS file with correct styling based on specifications."""
#         primary_color = specs["styles"].get("primary_color", "#007bff")
#         border_radius = specs["styles"].get("border_radius", "8px")

#         scss_code = f""".component {{
#     background-color: {primary_color};
#     border-radius: {border_radius};
#     padding: 10px;
# }}
# """
#         with open(scss_path, "w", encoding="utf-8") as scss_file:
#             scss_file.write(scss_code)
#         print(f"✅ Updated SCSS file for component")

#     def update_existing_services(self):
#         """Fetch API services and update them with endpoint logic."""
#         service_path = self.files_structure.get("src/app/services/api.service.ts")
#         if service_path:
#             api_endpoints = self.srs_data.get("API_Endpoints", [])

#             with open(service_path, "w", encoding="utf-8") as service_file:
#                 service_file.write("""import { Injectable } from '@angular/core';
# import { HttpClient } from '@angular/common/http';
# import { Observable } from 'rxjs';

# @Injectable({
#     providedIn: 'root'
# })
# export class ApiService {
#     constructor(private http: HttpClient) {}
# """)

#                 for endpoint in api_endpoints:
#                     function_name = endpoint.get("endpoint", "/").replace("/", "_").strip("_")
#                     method = endpoint.get("method", "GET").lower()

#                     if method == "get":
#                         service_file.write(f"""
#     {function_name}(): Observable<any> {{
#         return this.http.get('{endpoint["endpoint"]}');
#     }}
# """)
#                     elif method in ["post", "put", "patch"]:
#                         service_file.write(f"""
#     {function_name}(data: any): Observable<any> {{
#         return this.http.{method}('{endpoint["endpoint"]}', data);
#     }}
# """)

#                 service_file.write("}\n")
#             print(f"✅ Updated API service file.")

#     def generate_project_code(self):
#         """Runs all functions to modify the existing project files with generated code."""
#         self.update_existing_component_files()
#         self.update_existing_services()
#         print("🚀 Code generation for Angular project complete!")

# # Run the generator
# if __name__ == "__main__":
#     generator = SmartAngularCodeGenerator()
#     generator.generate_project_code()





import os
import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class SmartAngularCodeGenerator:
    """Fetches specifications and generates clean, efficient Angular code using AI."""

    def __init__(self, project_root="../data/angular_project",
                 srs_json="../data/extracted_data.json",
                 ui_json="../data/ui_components.json"):
        """Initialize the generator with project folder and JSON files."""
        self.project_root = project_root
        self.srs_json = srs_json
        self.ui_json = ui_json

        # Load JSON files
        self.srs_data = self.load_json(self.srs_json)
        self.ui_data = self.load_json(self.ui_json)

        # Scan the generated folder structure
        self.files_structure = self.scan_folder_structure()

        # Initialize AI Model (Groq Llama3-8B)
        self.ai_model = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)

    def load_json(self, json_path):
        """Loads JSON data from the given file."""
        if not os.path.exists(json_path):
            print(f"⚠️ JSON file not found: {json_path}")
            return {}

        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def scan_folder_structure(self):
        """Scans the generated project folder structure and returns a dictionary of files."""
        files_dict = {}
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.project_root)
                files_dict[relative_path] = file_path
        return files_dict

    def generate_ai_code(self, component_name, specs, file_type):
        """Uses AI to generate optimized Angular code for a given component."""
        
        api_info = ""
        if specs["api"]:
            api_info = f"""
            API Details:
            - Endpoint: {specs["api"]["endpoint"]}
            - Method: {specs["api"]["method"]}
            - Headers: {specs["api"].get("headers", {})}
            - Expected Request Body: {specs["api"].get("request_body", {})}
            - Expected Response: {specs["api"].get("response", {})}
            """

        ui_info = f"""
        UI Structure:
        - Layout: {specs["structure"]}
        - Styling: {json.dumps(specs["styles"], indent=4)}
        """

        prompt = f"""
        You are an expert Angular developer. Generate a clean, highly optimized {file_type} file for the `{component_name}` component.

        {ui_info}
        {api_info}

        **Guidelines:**
        - Use best Angular coding practices.
        - Ensure the component follows modular and reusable architecture.
        - If API integration is required, implement it properly.
        - Keep the styles clean and maintainable.
        - Ensure accessibility compliance.

        **Generated {file_type} Code:**
        Provide only the full {file_type} file content, without any explanations.
        """

        response = self.ai_model.invoke(prompt)
        return response.content.strip()

    def update_existing_files(self):
        """Fetch each component and update its files with AI-generated code."""
        for relative_path, full_path in self.files_structure.items():
            if relative_path.endswith(".component.ts"):
                component_name = os.path.basename(relative_path).replace(".component.ts", "")
                component_specs = self.get_component_specifications(component_name)

                if component_specs:
                    self.update_component_file(full_path, component_name, component_specs, "TypeScript")
                    self.update_component_file(full_path.replace(".ts", ".html"), component_name, component_specs, "HTML")
                    self.update_component_file(full_path.replace(".ts", ".scss"), component_name, component_specs, "SCSS")

    def get_component_specifications(self, component_name):
        """Fetch UI and API specifications for a given component from JSON files."""
        specs = {"api": None, "styles": {}, "structure": ""}
        
        # Get UI specifications from the UI JSON
        if isinstance(self.ui_data, list):
            for item in self.ui_data:
                if isinstance(item, dict) and "components" in item and isinstance(item["components"], list):
                    for comp in item["components"]:
                        if isinstance(comp, dict) and "component_name" in comp:  # Fix: Ensure comp is a dict
                            if comp["component_name"].lower() == component_name:
                                specs["styles"] = comp.get("styles", {})
                                specs["structure"] = comp.get("structure", "")

        # Get API specifications from the SRS JSON
        api_endpoints = self.srs_data.get("API_Endpoints", [])
        for endpoint in api_endpoints:
            if isinstance(endpoint, dict) and "related_component" in endpoint:
                if component_name.lower() in endpoint.get("related_component", "").lower():
                    specs["api"] = endpoint

        return specs if specs["styles"] or specs["api"] else None


    def update_component_file(self, file_path, component_name, specs, file_type):
        """Uses AI to generate and update a component file with clean Angular code."""
        if os.path.exists(file_path):
            ai_generated_code = self.generate_ai_code(component_name, specs, file_type)

            # Retry logic in case the AI response is empty
            if not ai_generated_code or len(ai_generated_code) < 10:
                print(f"⚠️ AI failed to generate {file_type} for {component_name}. Retrying...")
                ai_generated_code = self.generate_ai_code(component_name, specs, file_type)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(ai_generated_code)

            print(f"✅ Successfully updated {file_type} file for {component_name}")


    def update_existing_services(self):
        """Fetch API services and update them with AI-generated logic."""
        service_path = self.files_structure.get("src/app/services/api.service.ts")
        if service_path:
            api_endpoints = self.srs_data.get("API_Endpoints", [])

            if api_endpoints:
                ai_generated_code = self.generate_ai_code("api-service", {"endpoints": api_endpoints}, "TypeScript")
                with open(service_path, "w", encoding="utf-8") as service_file:
                    service_file.write(ai_generated_code)
                print(f"✅ Updated API service file.")

    def generate_project_code(self):
        """Runs all functions to modify the existing project files with AI-generated code."""
        self.update_existing_files()
        self.update_existing_services()
        print("🚀 AI-driven code generation for Angular project complete!")

# Run the AI-powered generator
if __name__ == "__main__":
    generator = SmartAngularCodeGenerator()
    generator.generate_project_code()
