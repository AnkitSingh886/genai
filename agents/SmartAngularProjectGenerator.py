# import os
# import json

# class SmartAngularProjectGenerator:
#     """Generates an Angular project dynamically based on multiple JSON specifications."""

#     def __init__(self, srs_json="../data/extracted_data.json",
#                  ui_json="../data/ui_components.json",
#                  project_root="../data/angular_project"):
#         """Initialize the generator with extracted JSON files."""
#         self.srs_json = srs_json
#         self.ui_json = ui_json
#         self.project_root = project_root

#         # Load extracted JSON data
#         self.srs_data = self.load_json(self.srs_json)
#         self.ui_data = self.load_json(self.ui_json)
#     def create_folders(self):
#         """Creates the dynamically determined folder structure."""
#         folders = self.determine_folders()  # Ensure determine_folders() is correctly defined
#         for folder in folders:
#             folder_path = os.path.join(self.project_root, folder)
#             os.makedirs(folder_path, exist_ok=True)
#             print(f"✅ Created folder: {folder_path}")


#     def load_json(self, json_path):
#         """Loads JSON data from the given file."""
#         if not os.path.exists(json_path):
#             print(f"⚠️ JSON file not found: {json_path}")
#             return {}

#         with open(json_path, "r", encoding="utf-8") as json_file:
#             return json.load(json_file)

#     def determine_folders(self):
#         """Dynamically determines required folders based on extracted JSON data."""
#         folders = [
#             "src/app/components",
#             "src/app/pages",
#             "src/app/services",
#             "src/app/state",
#             "src/assets",
#             "src/styles",
#             "tests"
#         ]

#         # Add pages from SRS JSON
#         srs_ui_components = self.srs_data.get("UI_UX_Guidelines", {}).get("Components", [])
#         for component in srs_ui_components:
#             folders.append(f"src/app/pages/{component.lower().replace(' ', '-')}")

#         # Ensure UI_Components exists and is a list
#         if isinstance(self.ui_data, dict) and "UI_Components" in self.ui_data:
#             ui_components = [comp["component_name"] for comp in self.ui_data["UI_Components"]]
#             for component in ui_components:
#                 folders.append(f"src/app/components/{component.lower().replace(' ', '-')}")

#         # Add API service folder if API endpoints exist
#         if isinstance(self.srs_data, dict) and "API_Endpoints" in self.srs_data:
#             folders.append("src/app/services/api")

#         return list(set(folders))  # Remove duplicates


#     def create_required_files(self):
#         """Creates required files based on extracted JSON data."""
#         # Configuration Files
#         config_files = ["package.json", "angular.json", "README.md", ".env"]
#         for file in config_files:
#             file_path = os.path.join(self.project_root, file)
#             open(file_path, "w").close()
#             print(f"✅ Created config file: {file}")

#         # Extract UI components from both JSON files
#         all_components = set(
#             self.srs_data.get("UI_UX_Guidelines", {}).get("Components", [])
#         )

#         # Ensure UI_Components is properly extracted from the list-based UI JSON file
#         if isinstance(self.ui_data, list):
#             for item in self.ui_data:
#                 if isinstance(item, dict) and "components" in item:
#                     for comp in item["components"].get("UI_Components", []):
#                         all_components.add(comp["component_name"])

#         # Create component files
#         for component in all_components:
#             component_name = component.lower().replace(" ", "-")
#             component_folder = os.path.join(self.project_root, f"src/app/components/{component_name}")
#             os.makedirs(component_folder, exist_ok=True)

#             ts_path = os.path.join(component_folder, f"{component_name}.component.ts")
#             html_path = os.path.join(component_folder, f"{component_name}.component.html")
#             scss_path = os.path.join(component_folder, f"{component_name}.component.scss")

#             # Create TypeScript file
#             with open(ts_path, "w", encoding="utf-8") as ts_file:
#                 ts_file.write(f"""import {{ Component }} from '@angular/core';

#     @Component({{
#         selector: 'app-{component_name}',
#         templateUrl: './{component_name}.component.html',
#         styleUrls: ['./{component_name}.component.scss']
#     }})
#     export class {component_name.capitalize()}Component {{}}
#     """)

#             # Create HTML file
#             with open(html_path, "w", encoding="utf-8") as html_file:
#                 html_file.write(f"<p>{component} Component</p>")

#             # Create SCSS file
#             with open(scss_path, "w", encoding="utf-8") as scss_file:
#                 scss_file.write(f".{component_name} {{\n  padding: 10px;\n}}")

#             print(f"✅ Created component: {component_name}")

#         # API Service Files
#         api_endpoints = self.srs_data.get("API_Endpoints", [])
#         service_path = os.path.join(self.project_root, "src/app/services/api.service.ts")

#         with open(service_path, "w", encoding="utf-8") as service_file:
#             service_file.write("""import { Injectable } from '@angular/core';
#     import { HttpClient } from '@angular/common/http';
#     import { Observable } from 'rxjs';

#     @Injectable({
#         providedIn: 'root'
#     })
#     export class ApiService {
#         constructor(private http: HttpClient) {}
#     """)

#             for endpoint in api_endpoints:
#                 method = endpoint.get("method", "GET").lower()
#                 function_name = endpoint.get("endpoint", "/").replace("/", "_").strip("_")
#                 request_body = endpoint.get("request_body", {})

#                 if method == "get":
#                     service_file.write(f"""
#         {function_name}(): Observable<any> {{
#             return this.http.get('{endpoint["endpoint"]}');
#         }}
#     """)
#                 elif method in ["post", "put", "patch"]:
#                     service_file.write(f"""
#         {function_name}(data: any): Observable<any> {{
#             return this.http.{method}('{endpoint["endpoint"]}', data);
#         }}
#     """)

#             service_file.write("}\n")
#             print(f"✅ Created API service with endpoints")


#     def generate_project(self):
#         """Runs all functions to dynamically generate the full project."""
#         self.create_folders()
#         self.create_required_files()
#         print("🚀 Angular project setup complete!")

# # Run the generator
# if __name__ == "__main__":
#     generator = SmartAngularProjectGenerator()
#     generator.generate_project()




import os
import json

class SmartAngularProjectGenerator:
    """Dynamically generates an Angular project structure based on JSON specifications."""

    def __init__(self, srs_json="../data/extracted_data.json",
                 ui_json="../data/ui_components.json",
                 project_root="../data/angular_project"):
        """Initialize the generator with extracted JSON files."""
        self.srs_json = srs_json
        self.ui_json = ui_json
        self.project_root = project_root

        # Load extracted JSON data
        self.srs_data = self.load_json(self.srs_json)
        self.ui_data = self.load_json(self.ui_json)

    def load_json(self, json_path):
        """Loads JSON data from the given file."""
        if not os.path.exists(json_path):
            print(f"⚠️ JSON file not found: {json_path}")
            return {}

        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def determine_folders(self):
        """Dynamically determines required folders based on extracted JSON data."""
        folders = [
            "src/app/components",
            "src/app/pages",
            "src/app/services",
            "src/app/state",
            "src/assets",
            "src/styles",
            "tests"
        ]

        # Extract pages from UI JSON
        for page_data in self.ui_data:
            page_name = os.path.splitext(page_data["image"])[0]  # Extract page name
            folders.append(f"src/app/pages/{page_name}")

            # Add page-specific components
            for component in page_data["components"]["UI_Components"]:
                component_name = component["component_name"].lower().replace(" ", "-")
                folders.append(f"src/app/pages/{page_name}/components/{component_name}")

        # Extract common components from SRS JSON
        common_components = self.srs_data.get("UI_UX_Guidelines", {}).get("Components", [])
        for component in common_components:
            folders.append(f"src/app/components/{component.lower()}")

        # Add API service folder if API endpoints exist
        if "API_Endpoints" in self.srs_data:
            folders.append("src/app/services/api")

        return list(set(folders))  # Remove duplicates

    def create_folders(self):
        """Creates the dynamically determined folder structure."""
        folders = self.determine_folders()
        for folder in folders:
            folder_path = os.path.join(self.project_root, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Created folder: {folder_path}")

    def create_required_files(self):
        """Creates required files based on extracted JSON data."""
        # Configuration Files
        config_files = ["package.json", "angular.json", "README.md", ".env"]
        for file in config_files:
            file_path = os.path.join(self.project_root, file)
            open(file_path, "w").close()
            print(f"✅ Created config file: {file}")

        # Generate component files for each page and common components
        for page_data in self.ui_data:
            page_name = os.path.splitext(page_data["image"])[0]  # Extract page name
            for component in page_data["components"]["UI_Components"]:
                component_name = component["component_name"].lower().replace(" ", "-")
                self.create_component_files(f"src/app/pages/{page_name}/components/{component_name}")

        for component in self.srs_data.get("UI_UX_Guidelines", {}).get("Components", []):
            self.create_component_files(f"src/app/components/{component.lower()}")

        # Generate API service file
        if "API_Endpoints" in self.srs_data:
            self.create_api_service_file()

    def create_component_files(self, component_path):
        """Creates TypeScript, HTML, and SCSS files inside the correct component folder."""
        component_folder = os.path.join(self.project_root, component_path)
        os.makedirs(component_folder, exist_ok=True)  # Ensure the component folder exists

        component_name = os.path.basename(component_folder)  # Get the last part of the path (actual component name)

        ts_path = os.path.join(component_folder, f"{component_name}.component.ts")
        html_path = os.path.join(component_folder, f"{component_name}.component.html")
        scss_path = os.path.join(component_folder, f"{component_name}.component.scss")

        with open(ts_path, "w", encoding="utf-8") as ts_file:
            ts_file.write(f"""import {{ Component }} from '@angular/core';

    @Component({{
        selector: 'app-{component_name}',
        templateUrl: './{component_name}.component.html',
        styleUrls: ['./{component_name}.component.scss']
    }})
    export class {component_name.capitalize()}Component {{}}
    """)

        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(f"<p>{component_name} Component</p>")

        with open(scss_path, "w", encoding="utf-8") as scss_file:
            scss_file.write(f".{component_name} {{\n  padding: 10px;\n}}")

        print(f"✅ Created component files inside {component_folder}")

    def create_api_service_file(self):
        """Generates the API service file based on API endpoints from extracted JSON."""
        service_path = os.path.join(self.project_root, "src/app/services/api.service.ts")

        os.makedirs(os.path.dirname(service_path), exist_ok=True)  # Ensure folder exists

        with open(service_path, "w", encoding="utf-8") as service_file:
            service_file.write("""import { Injectable } from '@angular/core';
    import { HttpClient } from '@angular/common/http';
    import { Observable } from 'rxjs';

    @Injectable({
        providedIn: 'root'
    })
    export class ApiService {
        constructor(private http: HttpClient) {}
    """)

            # Add API endpoint methods dynamically
            for endpoint in self.srs_data.get("API_Endpoints", []):
                method = endpoint.get("method", "GET").lower()
                function_name = endpoint.get("endpoint", "/").replace("/", "_").strip("_")

                if method == "get":
                    service_file.write(f"""
        {function_name}(): Observable<any> {{
            return this.http.get('{endpoint["endpoint"]}');
        }}
    """)
                elif method in ["post", "put", "patch"]:
                    service_file.write(f"""
        {function_name}(data: any): Observable<any> {{
            return this.http.{method}('{endpoint["endpoint"]}', data);
        }}
    """)

            service_file.write("}\n")
        print(f"✅ Created API service file at {service_path}")


    def generate_project(self):
        """Runs all functions to dynamically generate the full project."""
        self.create_folders()
        self.create_required_files()
        print("🚀 Angular project setup complete!")

# Run the generator
if __name__ == "__main__":
    generator = SmartAngularProjectGenerator()
    generator.generate_project()
