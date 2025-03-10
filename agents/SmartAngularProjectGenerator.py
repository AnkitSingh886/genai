# import os
# import json

# class AngularProjectGenerator:
#     """Automatically generates an Angular project structure and components based on JSON data."""

#     def __init__(self, json_path="../data/extracted_data.json", project_root="../data/angular_project"):
#         """Initialize the Generator with the extracted JSON data."""
#         self.json_path = json_path
#         self.project_root = project_root

#         # Load extracted JSON data
#         self.data = self.load_json()

#     def load_json(self):
#         """Loads JSON data from the extracted file."""
#         if not os.path.exists(self.json_path):
#             raise FileNotFoundError(f"⚠️ JSON file not found: {self.json_path}")

#         with open(self.json_path, "r", encoding="utf-8") as json_file:
#             return json.load(json_file)

#     def create_folders(self):
#         """Creates the necessary folder structure for the Angular project."""
#         folders = [
#             "src/app/components",
#             "src/app/pages",
#             "src/app/services",
#             "src/app/state",
#             "src/assets",
#             "src/styles",
#             "tests"
#         ]
        
#         for folder in folders:
#             folder_path = os.path.join(self.project_root, folder)
#             os.makedirs(folder_path, exist_ok=True)
#             print(f"✅ Created folder: {folder_path}")

#     def create_component_files(self):
#         """Creates Angular component files based on the extracted UI components."""
#         components = self.data.get("UI_UX_Guidelines", {}).get("Components", [])

#         for component in components:
#             component_name = component.lower().replace(" ", "-")  # Convert to Angular naming convention
#             ts_path = os.path.join(self.project_root, f"src/app/components/{component_name}.component.ts")
#             html_path = os.path.join(self.project_root, f"src/app/components/{component_name}.component.html")
#             scss_path = os.path.join(self.project_root, f"src/app/components/{component_name}.component.scss")

#             # Create TypeScript file
#             with open(ts_path, "w", encoding="utf-8") as ts_file:
#                 ts_file.write(f"""import {{ Component }} from '@angular/core';

# @Component({{
#     selector: 'app-{component_name}',
#     templateUrl: './{component_name}.component.html',
#     styleUrls: ['./{component_name}.component.scss']
# }})
# export class {component_name.capitalize()}Component {{}}
# """)

#             # Create HTML file
#             with open(html_path, "w", encoding="utf-8") as html_file:
#                 html_file.write(f"<p>{component} Component</p>")

#             # Create SCSS file
#             with open(scss_path, "w", encoding="utf-8") as scss_file:
#                 scss_file.write(f".{component_name} {{\n  padding: 10px;\n}}")

#             print(f"✅ Created component: {component_name}")

#     def create_service_files(self):
#         """Creates Angular service files for API interactions."""
#         ts_path = os.path.join(self.project_root, "src/app/services/api.service.ts")
#         with open(ts_path, "w", encoding="utf-8") as ts_file:
#             ts_file.write("""import { Injectable } from '@angular/core';
# import { HttpClient } from '@angular/common/http';
# import { Observable } from 'rxjs';

# @Injectable({
#     providedIn: 'root'
# })
# export class ApiService {
#     constructor(private http: HttpClient) {}

#     getDashboardData(): Observable<any> {
#         return this.http.get('/api/dashboard');
#     }
# }
# """)
#         print(f"✅ Created service: api.service.ts")

#     def create_auth_files(self):
#         """Creates authentication service and model files."""
#         auth_service_path = os.path.join(self.project_root, "src/app/services/auth.service.ts")

#         with open(auth_service_path, "w", encoding="utf-8") as auth_file:
#             auth_file.write("""import { Injectable } from '@angular/core';
# import { HttpClient } from '@angular/common/http';
# import { Observable } from 'rxjs';

# @Injectable({
#     providedIn: 'root'
# })
# export class AuthService {
#     constructor(private http: HttpClient) {}

#     login(credentials: any): Observable<any> {
#         return this.http.post('/api/auth/login', credentials);
#     }
# }
# """)
#         print(f"✅ Created service: auth.service.ts")

#     def create_config_files(self):
#         """Creates project config files like package.json, angular.json, and README."""
#         package_json_path = os.path.join(self.project_root, "package.json")
#         angular_json_path = os.path.join(self.project_root, "angular.json")
#         readme_path = os.path.join(self.project_root, "README.md")

#         with open(package_json_path, "w", encoding="utf-8") as package_file:
#             package_file.write("""{
#   "name": "angular-project",
#   "version": "1.0.0",
#   "dependencies": {
#     "@angular/core": "^16.0.0",
#     "@angular/common": "^16.0.0",
#     "@angular/router": "^16.0.0",
#     "@angular/material": "^16.0.0",
#     "rxjs": "^7.0.0"
#   }
# }
# """)

#         with open(angular_json_path, "w", encoding="utf-8") as angular_file:
#             angular_file.write("""{
#   "projects": {
#     "angular-project": {
#       "projectType": "application",
#       "root": "",
#       "sourceRoot": "src"
#     }
#   }
# }
# """)

#         with open(readme_path, "w", encoding="utf-8") as readme_file:
#             readme_file.write("# Angular Project\n\nGenerated automatically from JSON.")

#         print(f"✅ Created config files: package.json, angular.json, README.md")

#     def generate_project(self):
#         """Runs all functions to generate the full project."""
#         self.create_folders()
#         self.create_component_files()
#         self.create_service_files()
#         self.create_auth_files()
#         self.create_config_files()
#         print("🚀 Angular project setup complete!")

# # Run the generator
# if __name__ == "__main__":
#     generator = AngularProjectGenerator()
#     generator.generate_project()





import os
import json

class SmartAngularProjectGenerator:
    """Generates an Angular project dynamically based on multiple JSON specifications."""

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
    def create_folders(self):
        """Creates the dynamically determined folder structure."""
        folders = self.determine_folders()  # Ensure determine_folders() is correctly defined
        for folder in folders:
            folder_path = os.path.join(self.project_root, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Created folder: {folder_path}")


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

        # Add pages from SRS JSON
        srs_ui_components = self.srs_data.get("UI_UX_Guidelines", {}).get("Components", [])
        for component in srs_ui_components:
            folders.append(f"src/app/pages/{component.lower().replace(' ', '-')}")

        # Ensure UI_Components exists and is a list
        if isinstance(self.ui_data, dict) and "UI_Components" in self.ui_data:
            ui_components = [comp["component_name"] for comp in self.ui_data["UI_Components"]]
            for component in ui_components:
                folders.append(f"src/app/components/{component.lower().replace(' ', '-')}")

        # Add API service folder if API endpoints exist
        if isinstance(self.srs_data, dict) and "API_Endpoints" in self.srs_data:
            folders.append("src/app/services/api")

        return list(set(folders))  # Remove duplicates


    def create_required_files(self):
        """Creates required files based on extracted JSON data."""
        # Configuration Files
        config_files = ["package.json", "angular.json", "README.md", ".env"]
        for file in config_files:
            file_path = os.path.join(self.project_root, file)
            open(file_path, "w").close()
            print(f"✅ Created config file: {file}")

        # Extract UI components from both JSON files
        all_components = set(
            self.srs_data.get("UI_UX_Guidelines", {}).get("Components", [])
        )

        # Ensure UI_Components is properly extracted from the list-based UI JSON file
        if isinstance(self.ui_data, list):
            for item in self.ui_data:
                if isinstance(item, dict) and "components" in item:
                    for comp in item["components"].get("UI_Components", []):
                        all_components.add(comp["component_name"])

        # Create component files
        for component in all_components:
            component_name = component.lower().replace(" ", "-")
            component_folder = os.path.join(self.project_root, f"src/app/components/{component_name}")
            os.makedirs(component_folder, exist_ok=True)

            ts_path = os.path.join(component_folder, f"{component_name}.component.ts")
            html_path = os.path.join(component_folder, f"{component_name}.component.html")
            scss_path = os.path.join(component_folder, f"{component_name}.component.scss")

            # Create TypeScript file
            with open(ts_path, "w", encoding="utf-8") as ts_file:
                ts_file.write(f"""import {{ Component }} from '@angular/core';

    @Component({{
        selector: 'app-{component_name}',
        templateUrl: './{component_name}.component.html',
        styleUrls: ['./{component_name}.component.scss']
    }})
    export class {component_name.capitalize()}Component {{}}
    """)

            # Create HTML file
            with open(html_path, "w", encoding="utf-8") as html_file:
                html_file.write(f"<p>{component} Component</p>")

            # Create SCSS file
            with open(scss_path, "w", encoding="utf-8") as scss_file:
                scss_file.write(f".{component_name} {{\n  padding: 10px;\n}}")

            print(f"✅ Created component: {component_name}")

        # API Service Files
        api_endpoints = self.srs_data.get("API_Endpoints", [])
        service_path = os.path.join(self.project_root, "src/app/services/api.service.ts")

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

            for endpoint in api_endpoints:
                method = endpoint.get("method", "GET").lower()
                function_name = endpoint.get("endpoint", "/").replace("/", "_").strip("_")
                request_body = endpoint.get("request_body", {})

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
            print(f"✅ Created API service with endpoints")


    def generate_project(self):
        """Runs all functions to dynamically generate the full project."""
        self.create_folders()
        self.create_required_files()
        print("🚀 Angular project setup complete!")

# Run the generator
if __name__ == "__main__":
    generator = SmartAngularProjectGenerator()
    generator.generate_project()
