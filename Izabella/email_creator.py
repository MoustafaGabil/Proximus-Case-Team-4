import os
import json
import re
import requests
from dotenv import load_dotenv
from google import generativeai as genai
import random as rd
from tavily import TavilyClient


class GeminiConfig:
    """Class holding configuration settings"""
    def __init__(self, company_name: str, random_tone: str):
        self.company_name = company_name
        self.random_tone = random_tone
        
        self.DEFAULT_CONFIG = {
            "system_instruction": f"""
            You are a skilled copywriter with a knack for creating emails that feel
            personal, relevant, urgent and engaging. Your task is to write emails to employees of
            {company_name} all while maintaining a tone that feels individual, tailored and professional. 
            The email should appear to come from a relevant source. Encourage actions like clicking links or downloading attachments with a sense of urgency. Align the email subject with the sender's theme and message.
            Incorporate in your answer only complete emails.
            Everything about the sender address, subject, and email body is focused on the recipient interacting with the link or attachment.
            The email should have a {random_tone} tone.
            """,
            "temperature": 1,
            "maxOutputTokens": 8000,
            "top_p": 0.9,
            "top_k": 40,
            "safety_settings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ],
            "schemas": {
                "provider_email": {
                    "subject": "str",
                    "body": "str",
                    "email_sign_fullname": "str",
                    "email_sign_role": "str",
                    "email_sign_company": "str",
                    "receiver_full_name": "str"
                }
            }
        }


class GeminiConnectorEmails:
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
    

class DataProvider:
    """Manages data resources for email generation"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.email_tones = [
            "Urgent", "Firm", "Action Required", "Time-Sensitive", "Critical",
            "Pressing", "Immediate Response", "High-Priority", "Polite",
            "Friendly", "Professional", "Supportive", "Respectful", "Casual",
            "Empathetic"
        ]
        self.proximus_employees = [
            {
                "name": "Marie Declercq",
                "email": "marie.declercq@proximus.be",
                "role": "Data Analyst",
                "language": "Dutch",
                "department": "Consumer Market"
            },
            {
                "name": "Luc Vandenberg",
                "email": "luc.vandenberg@proximus.be",
                "role": "Cybersecurity Specialist",
                "language": "Dutch",
                "department": "Network & Wholesale"
            },
            {
                "name": "Emma Wouters",
                "email": "emma.wouters@proximus.be",
                "role": "Marketing Specialist",
                "language": "English",
                "department": "Enterprise Market"
            },
            {
                "name": "Jai Mehta",
                "email": "jai.mehta@proximus.be",
                "role": "System Administrator",
                "language": "English",
                "department": "IT Infrastructure"
            },
            {
                "name": "Guillaume Boutin",
                "email": "guillaume.boutin@proximus.be",
                "role": "Chief Executive Officer",
                "language": "French",
                "department": "Chief Executive Officer's Department"
            }
        ]
        self.telecom_employee_events = [
            "Seminars", "Presentations", "Networking Meetings", "Workshops",
            "Training Sessions", "Industry Roundtables", "Panel Discussions",
            "Webinars", "Conferences", "Hackathons", "Product Demos",
            "Leadership Forums", "Strategic Planning Meetings",
            "Customer Experience Sessions", "Innovation Labs"
        ]
        self.urgent_provider_issues = [
            "Network Outages", "SLA Violations", "Payment Delays",
            "Contract Breach", "Quality Failures", "Security Risks",
            "Price Increases", "Missed Deadlines", "Regulatory Issues",
            "Billing Discrepancies"
        ]

    def get_random_tone(self):
        """Get a random tone from email_tones."""
        return rd.choice(self.email_tones)
    
    def get_random_employee(self):
        """Get a random employee from proximus_employees."""
        return rd.choice(self.proximus_employees)
    
    def get_random_events(self):
        """Get a random event from telecom_employee_events"""
        return rd.choice(self.telecom_employee_events)
    
    def get_random_issues(self):
        """Get a random issue from urgent_provider_issues"""
        return rd.choice(self.urgent_provider_issues)


class EmailGenerator:
    def __init__(self, model, config):
        """Initialize with the Google AI model and configuration."""
        self.model = model
        self.config = config

    def generate(self, prompt):
        """Generate content using configuration settings."""
        # Create generation config
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.get("temperature", 1),
            top_p=self.config.get("top_p", 0.9),
            top_k=self.config.get("top_k", 40),
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


    def generate_service_emails(self, provider, provider_departments, company_name, random_employee):
        """"""
        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an urgent matter that needs to be solved related to {company_name} concerning a service that {provider} offers. Elaborate about the issue and point out why it needs to be solved as quickly as possible.
        The receiver of the email is {random_employee['name']} and should be in {random_employee['language']}. Address the receiver formally and by their last name.
        The email signature should contain the first name, family name, role, and the company name of one of the employees of {provider}.
        Do not include the link in the body of the email, as it will be implemented separately and placed below the text body, refer to it in the text body where it is placed.
        Just plain text in the body, nothing to include anymore.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[service_emails_template]
        """
        
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        service_emails = json.loads(repaired_response)
        return service_emails

    def generate_events_emails(self, provider, provider_departments, company_name, random_employee, random_event):

        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an event that is organized by {provider}. 
        The event is {random_event} and is geared towards {random_employee['role']}.
        Do not include urgent in the subject of the email. State that the spots available are limited and urgent action is required.
        The receiver of the email is {random_employee['name']} and should be in {random_employee['language']}. Address the receiver formal and by his last name.
        The email signature should contain the first name, family name, role and the company name of one of the employees of {provider}. 
        Do not include the link in the body of the email, as it will be implemented separately and placed below the text body, refer to it in the text body where it is placed.
        Just plain text in the body, nothing to include anymore.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[events_emails_template]
        """
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        events_emails = json.loads(repaired_response)
        return events_emails
    
    def generate_issue_emails(self, provider, provider_departments, company_name, random_employee, random_issue):

        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an issue that {provider} have with {company_name}. 
        The issue is {random_issue} and is related to {random_employee['role']}.
        Do not include urgent in the subject of the email.
        The receiver of the email is {random_employee['name']} and should be in {random_employee['language']}. Address the receiver formal and by his last name.
        The email signature should contain the first name, family name, role and the company name of one of the employees of {provider}. 
        Do not include the link in the body of the email, as it will be implemented separately and placed below the text body, refer to it in the text body where it is placed.
        Just plain text in the body, nothing to include anymore.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[issue_emails_template]
        """
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        issues_emails = json.loads(repaired_response)
        return issues_emails
    
    def repair_json_response(self, response_text):
        """
        Repairs a potentially malformed JSON string from `response.text`.
        Ensures it starts with '[' and ends with ']' after the last complete dictionary.

        Args:
            response_text (str): The response text containing a potentially malformed JSON string.

        Returns:
            str: The repaired JSON string.

        Raises:
            ValueError: If the string cannot be repaired into valid JSON.
        """
        # Remove the unwanted prefix if it exists
        if response_text.strip().startswith("```json") or response_text.strip().startswith("[```json"):
            response_text = response_text.replace("```json", "", 1).replace("[```json", "", 1).strip()

        # Ensure the string starts with '['
        if not response_text.strip().startswith("["):
            response_text = "[" + response_text

        # Find the last closing brace ('}')
        last_brace_index = response_text.rfind("}")
        if last_brace_index == -1:
            raise ValueError("No closing brace found in the response text.")

        # Trim the string up to the last complete dictionary and close the list
        repaired_string = response_text[:last_brace_index + 1].rstrip(", \n") + "]"
        
        # Return the repaired JSON string
        return repaired_string

    def save_emails_to_file(self, emails, email_type, output_dir):
        """Save the generated emails to a JSON file based on the type of email."""
        # Generate file name based on email type
        output_file = os.path.join(output_dir, f"{email_type}.json")
        
        # Save the emails to the file
        with open(output_file, 'w') as file:
            json.dump(emails, file, indent=4)
        print(f"Emails saved to {output_file}")
        
        
        
class LogoFetcher:
    def __init__(self, output_dir='output/logos'):
        """Initialize LogoFetcher with output directory."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        
        load_dotenv()
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        if not self.tavily_api_key:
            raise ValueError("TAVILY_API_KEY not found in .env file")
        
        self.tavily_client = TavilyClient(api_key=self.tavily_api_key)

    def _get_logo_url(self, name):
        """Internal method to fetch logo URL."""
        try:
            response = self.tavily_client.search(
                f"{name} logo", 
                include_images=True, 
                include_image_descriptions=True
            )
            return response['images'][0]['url'] if response['images'] else None
        except Exception as e:
            print(f"Error searching logo for {name}: {e}")
            return None

    def get_logo(self, name, logo_type='company'):
        """
        General method to fetch and save logo.
        
        Args:
            name (str): Name of entity
            logo_type (str): Type of logo ('company' or 'provider')
        
        Returns:
            str: Path to saved logo or None
        """
        logo_url = self._get_logo_url(name)
        if not logo_url:
            print(f"No logo found for {name}")
            return None

        try:
            image_response = requests.get(logo_url)
            if image_response.status_code != 200:
                print(f"Failed to retrieve logo for {name}")
                return None

            file_extension = os.path.splitext(logo_url)[1] or '.png'
            output_file = os.path.join(
                self.output_dir, 
                f"{logo_type}_{name.lower().replace(' ', '_')}{file_extension}"
            )

            with open(output_file, "wb") as file:
                file.write(image_response.content)

            print(f"Logo saved for {name} at {output_file}")
            return output_file

        except Exception as e:
            print(f"Error saving logo for {name}: {e}")
            return None

    def get_company_logo(self, company_name):
        """Fetch logo for a specific company."""
        return self.get_logo(company_name, logo_type='company')

    def get_provider_logo(self, provider_name):
        """Fetch logo for a specific provider."""
        return self.get_logo(provider_name, logo_type='provider')

    def save_logos(self, provider_json_path):
        """
        Save logos for entities in a JSON file.
        
        Args:
            provider_json_path (str): Path to JSON with provider/company names
        
        Returns:
            dict: Mapping of names to logo paths
        """
        try:
            with open(provider_json_path, 'r') as file:
                data = json.load(file)
            
            logos = {}
            entities = data if isinstance(data, list) else data.keys()
            
            for entity in entities:
                name = entity.get('name', entity) if isinstance(entity, dict) else entity
                logo_path = self.get_logo(name)
                if logo_path:
                    logos[name] = logo_path
            
            return logos
        
        except Exception as e:
            print(f"Error processing JSON: {e}")
            return {}