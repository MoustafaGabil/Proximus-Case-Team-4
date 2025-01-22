import os
import json
import re
from dotenv import load_dotenv
from google import generativeai as genai
import random as rd

class GeminiConfig:
    """Class holding configuration settings"""
    DEFAULT_CONFIG = {
        "system_instruction": "You are an analyst that conducts company research. You are given a company name, and you will work on a company report. You have access to Google Search to look up company news, updates, metrics, public records and linkedin pages to write research reports. When given a company name, identify key aspects to research, look up that information and then write an elaborate company report. Thoroughly plan your work in detail and steps, but avoid discussing it. Do not add any additional comments after finishing the report.",
        "temperature": 0,
        "maxOutputTokens": 8000,
        "top_p": 0.9,
        "top_k": 5,
        "safety_settings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ],
        
        "schemas": {
            "main_company": {
                "subject": "str",
                "overview": "str",
                "source": "str"
            },
            "key_employees_roles":{
                "first_name": "str",
                "family_name":"str",
                "role":"str",
                "department":"str",
                "email_address":"str"
            },
            "departments": {
                "department": "str",
                "subdivision": "list[str]",
                "address":"str",
                "phone": "str",
                "vat": "str"
            },
            "colors":{
                "color_name_1":"str",
                "hex_code_1":"str",
                "rgb_code_1": "list[int]",
                "color_name_2":"str",
                "hex_code_2":"str",
                "rgb_code_2": "list[int]"
            },
            "providers":{
                "provider":"str",
                "service":"str",
                "type":"str",
                "provider_homepage":"str"
            }

        }
    }    

class GeminiConnector:
    def __init__(self):
        """Initialize the connector with a Google AI client."""
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.config = GeminiConfig.DEFAULT_CONFIG
        print("Successfully connected to the Google AI API.")

    def get_model(self):
        """Return the initialized model."""
        return self.model

    def get_config(self):
        """Return the configuration."""
        return self.config

class GenerateContent:
    def __init__(self, model, config):
        """Initialize with the Google AI model and configuration."""
        self.model = model
        self.config = config

    def generate(self, prompt):
        """Generate content using configuration settings."""
        # Create generation config
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.get("temperature", 0),
            top_p=self.config.get("top_p", 0.9),
            top_k=self.config.get("top_k", 5),
            max_output_tokens=self.config.get("maxOutputTokens", 8000),
        )

        # Prepare the complete prompt with system instruction
        system_instruction = self.config.get("system_instruction", "")
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt

        # Convert safety settings to dictionary format
        safety_settings = []
        if "safety_settings" in self.config:
            safety_settings = [
                {
                    "category": setting["category"],
                    "threshold": setting["threshold"]
                }
                for setting in self.config["safety_settings"]
            ]

        # Generate content
        response = self.model.generate_content(
            full_prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return response.text

    def generate_prompt(self, template, schema, company_name):
        """Helper to generate prompt based on template."""
        return template.format(company_name=company_name, schema=json.dumps(schema))

    def generate_main_report(self, company_name):
        """Create a company main report"""
        schema = self.config["schemas"]["main_company"]
        prompt = f"""
        Write a report about {company_name}.
        The report should contain an extensive overview of the most important news facts of the last 2 weeks. 
        Use this JSON schema: {json.dumps(schema)}
        Return: list[main_company_report_items]
        """
        return self.generate(prompt)
    
    def generate_key_employees_roles(self, company_name):
        """Create a report on key employees and roles in company"""
        schema = self.config["schemas"]["key_employees_roles"]
        prompt = f"""
        Write a report about {company_name}.
        The report should only contain a comprehensive summary of the employees in the company. 
        The report should contain, the complete first name and family name, an email address with this structure 
        "first name.family name@{company_name}.be" (put it all in lower case), the role that they have within the company and the department that they  make part of.
        Do not include abbreviations in names, and exclude employees whose full first and last names cannot be found.
        Give me as much grounded names that you can find with your research and put them all in the report.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[key_employees_roles_report]
        """
        return self.generate(prompt)

    def generate_departments(self, company_name):
        """Create report on departments of company"""
        schema = self.config["schemas"]["departments"]
        prompt = f"""
        Write a report about {company_name}
        The report should exclusively provide a detailed summary of the company's departments and their respective subdivisions, if any.
        Include in the report the full address where the headquarter of the provider is located.
        Do not include abbreviations in the report.
        Provide a detailed list, specifying only verified and public information. Do not include speculative or incomplete details.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[departments]
        """
        return self.generate(prompt)
    
    def generate_colors(self, company_name):
        """Creates a report on the company's main colors"""
        schema = self.config["schemas"]["colors"]
        prompt = f"""
        Write a report about {company_name}
        The report should exclusively provide the main colors of Company's branding, including any official color codes such as HEX or RGB. Focus on company's logo and website.
        Do not include speculative colors and focus only on the main ones.
        Thoroughly plan your work in detail and steps, but avoid discussing it. Do not add any additional comments after finishing the report.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[company_colors]
        """
        return self.generate(prompt)
    
    def generate_providers(self, company_name):
        """List the main service providers of the company"""
        schema = self.config["schemas"]["providers"]
        prompt = f"""
        Write a report about {company_name}
        List the main service providers of the company. Include any known suppliers, contractors, technology service providers, or any other third-part
        Provide the names of the service providers, type and description of the services they provide to the company. Also include the providers homepa
        Use this JSON schema: {json.dumps(schema)}
        Return: list[providers]
        """
        return self.generate(prompt)


class JSONHandler:
    @staticmethod
    def save_json_from_string(input_string, output_filename):
        """Extract JSON content from a string and save it to a file."""
        result = re.search(r'\[.*\]', input_string, re.DOTALL)
        if result:
            extracted_content = result.group(0)
            try:
                json_data = json.loads(extracted_content)
                with open(output_filename, "w", encoding="utf-8") as json_file:
                    json.dump(json_data, json_file, indent=4)
                print(f"JSON data has been successfully written to '{output_filename}'.")
                return True
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
            except Exception as e:
                print(f"An error occurred while writing the file: {e}")
        else:
            print("No content found within brackets.")
        return False
    
class ReportManager:
    def __init__(self, output_dir="output"):
        """Initialize the report manager."""
        self.connector = GeminiConnector()
        self.model = self.connector.get_model()
        self.config = self.connector.get_config()
        self.content_generator = GenerateContent(self.model, self.config)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_and_save_report(self, company_name, report_type, generator_func):
        """Generate and save a specific report."""
        print(f"\nGenerating {report_type} report for {company_name}...")
        report_content = generator_func(company_name)
        output_file = os.path.join(self.output_dir, f"{company_name.lower()}_{report_type}.json")
        JSONHandler.save_json_from_string(report_content, output_file)

    def generate_all_reports(self, company_name):
        """Generate all reports for a given company."""
        reports = {
            "main_company_report": self.content_generator.generate_main_report,
            "key_employees_roles_report": self.content_generator.generate_key_employees_roles,
            "departments": self.content_generator.generate_departments,
            "company_colors": self.content_generator.generate_colors,
            "providers": self.content_generator.generate_providers,
        }
        for report_type, generator_func in reports.items():
            self.generate_and_save_report(company_name, report_type, generator_func)


class ProviderManager:
    def __init__(self, input_file, output_file):
        """Initialize the ProviderManager with input and output file paths."""
        self.input_file = input_file
        self.output_file = output_file
        self.providers = []
        
        self.connector = GeminiConnector()
        self.model = self.connector.get_model()
        self.config = self.connector.get_config()
        self.content_generator = GenerateContent(self.model, self.config)
                
    def load_providers(self):
        """Load providers from the JSON input file."""
        try:
            with open(self.input_file, "r") as file:
                self.providers = json.load(file)
            print(f"Loaded providers from {self.input_file}")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: Invalid or missing file {self.input_file}")

    def pick_random_provider(self):
        """Pick a random provider from the list of providers."""
        if not self.providers:
            print("No providers available to choose from.")
            return None
        return rd.choice(self.providers)

    def save_provider(self, provider):
        """Save the selected provider to the JSON output file."""
        try:
            with open(self.output_file, "w") as json_file:
                json.dump([provider], json_file, indent=4)
            print(f"Data saved to {self.output_file}")
        except Exception as e:
            print(f"An error occurred while saving data: {e}")

    def generate_key_employees_roles_for_provider(self, provider_name, company_name):
        """Create a report on key employees and roles for the selected provider."""
        schema = self.config["schemas"]["key_employees_roles"]
        prompt = f"""
        Write a report about company {provider_name}. This company is a provider of {company_name}
        The report should only contain a comprehensive summary of the employees in the company.
        The report should contain, the complete first name and family name, an email address with this structure "first name.family name@{provider_name}.be" (put it all in lower case), the role that they have within the company and the department that they make part of.
        Do not include abbreviations in names, and exclude employees whose full first and last names cannot be found. Do not include employees of {company_name} in the report.
        Give me as much grounded names that you can find with your research and put them all in the report.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[key_employees_roles_report]
        """
        return self.content_generator.generate(prompt)

    def generate_colors_provider(self, provider_name, company_name):
        """Creates a report on the providers main colors"""
        schema = self.config["schemas"]["colors"]
        prompt = f"""
        Write a report about company {provider_name}. This company is a provider of {company_name}
        The report should exclusively provide the main colors of Company's branding, including any official color codes such as HEX or RGB. Focus on the primary colors used in the company's logo and website.
        Do not include speculative colors and focus only on the main ones.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[provider_colors]
        """
        return self.content_generator.generate(prompt)
    
    def generate_departments_provider(self, provider_name, company_name):
        """Creates a report on the providers departments"""
        schema = self.config["schemas"]["departments"]
        prompt = f"""
        Write a report about company {provider_name}. This company is a provider of {company_name}
        The report should exclusively provide a detailed summary of the company's departments and their respective subdivisions, if any.
        Include in the report the full address where the headquarter of the provider is located, the main phone number and vat number.
        Do not include abbreviations in the report.
        Provide a detailed list, specifying only verified and public information. Do not include speculative or incomplete details.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[provider_departments]
        """
        return self.content_generator.generate(prompt)



    def execute(self, company_name):
        """Execute the process of loading, picking, and saving a random provider."""
        self.load_providers()
        provider = self.pick_random_provider()
        if provider:
            print(f"Selected provider: {provider}")
            self.save_provider(provider)

        # Generating a report on a key employee for a provider
            provider_name = provider.get("provider")
            if provider_name and isinstance(provider_name, str):  # Sprawdzenie, czy nazwa jest poprawna

                # Generating a report on a key employee for a provider
                print(f"Generating key employees roles report for provider: {provider_name}")
                report = self.generate_key_employees_roles_for_provider(provider_name, company_name)
                output_path = os.path.join(os.path.dirname(self.output_file), f"{provider_name}_key_employees_roles.json")
                JSONHandler.save_json_from_string(report, output_path)
                print(f"Key employees roles report saved to {output_path}")

                # Generating a report on the providers main colors
                print(f"Generating a report on the providers main colors: {provider_name}")
                report = self.generate_colors_provider(provider_name, company_name)
                output_path = os.path.join(os.path.dirname(self.output_file), f"{provider_name}_main_colors.json")
                JSONHandler.save_json_from_string(report, output_path)
                print(f"Main colors report saved to {output_path}")

                # Generating a report on the providers departments
                print(f"Generating a report on the providers departments: {provider_name}")
                report = self.generate_departments_provider(provider_name, company_name)
                output_path = os.path.join(os.path.dirname(self.output_file), f"{provider_name}_departments.json")
                JSONHandler.save_json_from_string(report, output_path)
                print(f"Main colors report saved to {output_path}")