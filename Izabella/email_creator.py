import os
import json
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import generativeai as genai
import random as rd
from tavily import TavilyClient
from generatecontent import DataBlender


class GeminiConfig:
    """Class holding configuration settings"""
    def __init__(self, company_name: str, random_tone: str, random_employee: str, provider:str):
        self.company_name = company_name
        self.random_tone = random_tone
        self.random_employee = random_employee
        
        self.DEFAULT_CONFIG = {
            "system_instruction": f"""
            You are a skilled copywriter with a knack for creating emails that feel
            personal, relevant, urgent and engaging. Your task is to write emails to employees of
            {company_name} all while maintaining a tone that feels individual, tailored and professional. 
            The email should appear to come from a relevant source. Encourage actions like clicking links or downloading attachments with a sense of urgency. 
            Align the email subject with the sender's theme and message.
            Incorporate in your answer only complete emails.
            Everything about the sender address, subject, and email body is focused on the recipient interacting with the link.
            If you encounter any characters as "/", "\", "-","_" replace them with an empty string. 
            The email should have a {random_tone} tone.
            The receiver of the email is {random_employee['name']} and should be in {random_employee['language']}. Address the receiver formal and by his full name.
            The email signature should contain the first name, family name, role and the company name of one of the employees of {provider}.
            Do not include the link in the body of the email, as it will be implemented separately and placed below the text body,
            refer to it in the text body where it is placed. Just plain text in the body, nothing to include anymore.
            Give also suitable color for the call to action button based on the subject of the email in rgb.
            Create also a call to action text that is limited to maximum 3 words but do not include it in the body.
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
                    "call_to_action_text":"str",
                    "call_to_action_color":"list[int]",
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
    # 
    def get_random_news(self, file_path):
        """
        
        
        """
        try:
            # 
            with open(file_path, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
            if isinstance(news_data, list):
                return rd.choice(news_data)
            elif isinstance(news_data, dict) and 'news' in news_data:
                return news_data
            else:
                print("")
                return None
        except FileNotFoundError:
            print(f"{file_path}")
            return None
        except json.JSONDecodeError:
            print(f"{file_path}")
            return None

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


    def pick_random_date(self):
        # Define the time range
        start_hour = 9  # 9 AM
        end_hour = 16   # 4 PM (exclusive)

        # Get the current date
        today = datetime.now()

        # Generate a list of valid weekdays (Monday to Friday) within 7 days
        valid_days = []
        for i in range(1, 8):
            candidate_date = today + timedelta(days=i)
            if candidate_date.weekday() < 5:  # 0=Monday, 4=Friday
                valid_days.append(candidate_date)

        # Pick a random day from the valid weekdays
        random_day = rd.choice(valid_days)

        # Randomly choose an hour between 9 AM and 4 PM
        random_hour = rd.randint(start_hour, end_hour - 1)

        # Combine the random day and hour into a datetime object
        random_date = random_day.replace(hour=random_hour, minute=0, second=0, microsecond=0)

        return random_date

    def generate_prompt(self, template, schema, company_name):
        """Helper to generate prompt based on template."""
        return template.format(company_name=company_name, schema=json.dumps(schema))


    def generate_service_emails(self, provider, provider_departments, company_name, random_employee):
        """"""
        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an urgent matter that needs to be solved related to {company_name} concerning a service that {provider} offers. 
        Elaborate about the issue and point out why it needs to be solved as quickly as possible.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[service_emails_template]
        """
        
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        service_emails = json.loads(repaired_response)
        return service_emails

    def generate_events_emails(self, provider, provider_departments, company_name, random_employee, random_event, random_date):
        random_date = self.pick_random_date() # Generate a random date

        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an event that is organized by {provider}. 
        The event is {random_event} and is geared towards {random_employee['role']}. The event will take place {random_date.strftime('%A %d %B at %H hour')}.
        Do not include urgent in the subject of the email. State that the spots available are limited and urgent action is required.
       Use this JSON schema: {json.dumps(schema)}
        Return: list[events_emails_template]
        """
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        events_emails = json.loads(repaired_response)
        return events_emails
    
    def generate_issue_emails(self, provider, provider_departments, company_name, random_employee, random_issue, random_date):

        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. {provider} has these {provider_departments}.
        Write some tailored emails based on the role of {random_employee['role']} about an issue that {provider} have with {company_name}. 
        The issue is {random_issue} and is related to {random_employee['role']}.  Elaborate about the issue.
        The issue needs to be solved before {random_date.strftime('%A %d %B at %H hour')}
        Use this JSON schema: {json.dumps(schema)}
        Return: list[issue_emails_template]
        """
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        issues_emails = json.loads(repaired_response)
        return issues_emails
    
    def generate_news_email(self, provider, company_name, random_employee, news, output_directory):
        
        # Path to the JSON file
        news_file_path = os.path.join(output_directory, "proximus_main_company_report.json")
                
        # Load the contents of the JSON file
        try:
            with open(news_file_path, "r", encoding="utf-8") as file:
                report_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {news_file_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"The file {news_file_path} does not contain valid JSON.")
        
        # Extract the news content
        news = news.get("news", "No news available.")
                
        schema = self.config.get("schemas", {}).get("provider_email")
        prompt = f"""
        {provider} is a service provider of {company_name}. Write some tailored emails based on the role of {random_employee['role']} about 
        an business opportunity that {provider} can offer {company_name} regarding {news}.
        The particular business opportunity is also closely related to {random_employee}.
        Use this JSON schema: {json.dumps(schema)}
        Return: list[events_emails_template]
        """
        # Call the generate method with the constructed prompt
        response_text = self.generate(prompt)

        # Repair and parse the response
        repaired_response = self.repair_json_response(response_text)
        news_emails = json.loads(repaired_response)
        return news_emails

    
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
                                                    



    def merge_emails(self, input_dir, output_file, files_to_merge):
        """
        Scala pliki JSON z określonego katalogu wejściowego do jednego pliku wyjściowego.

        """
        # Przechowaj oryginalną listę plików do scalenia
        merged_data = files_to_merge.copy()
    
        # Wczytaj dodatkowe pliki z katalogu
        for filename in os.listdir(input_dir):
            if filename.endswith('.json') and filename not in merged_data:
                file_path = os.path.join(input_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        additional_data = json.load(f)
                        # Rozszerz listę tylko jeśli wczytane dane nie są None
                        if additional_data:
                            merged_data.extend(additional_data)
                except json.JSONDecodeError:
                    print(f"Błąd podczas wczytywania pliku {filename}")
    
        # Zapisz scalone dane do pliku wyjściowego
        with open(os.path.join(input_dir, output_file), 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)
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

class EmailTemplateGenerator:
    def __init__(self, json_dir, blend_provider_data):
        self.json_dir = json_dir
        self.blended_data_file = blend_provider_data
        self.blended_data = self._load_json(blend_provider_data)
    
    def _load_json(self, file_path):
        """Load a JSON file and return its content."""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"File {file_path} not found.")
    
    def _get_provider_info(self, provider_data):
        """Extract provider-specific information."""
        general_info = provider_data.get('general', {})
        provider = general_info.get('provider') or 'BICS'
        departments = provider_data.get('departments', [])
        address = (departments[0].get('address') if departments else None) or 'Boulevard du Roi Albert II, 27, B-1030 Brussels, Belgium'
        depart = (departments[0].get('department') if departments else None) or 'IT development'
        phone = (departments[0].get('phone') if departments else None) or '+32 2 547 52 10'
        vat = (departments[0].get('vat') if departments else None) or 'BE 0866 977 981'
        return provider, address, depart, phone, vat

    def _process_color(self, color_info):
        """Process the color information."""
        color_name = color_info.get('rgb_code_1') or [28, 151, 212]
        if isinstance(color_name, list):
            brightness_factor = 0.8
            color_name = [int(value * brightness_factor) for value in color_name]
            color_name = f"rgb{tuple(color_name)}"
        return color_name

    def generate_emails(self, specific_files):
        """Generate email templates for specified JSON files."""
        for filename in specific_files:
            file_path = os.path.join(self.json_dir, filename)
            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist. Skipping...")
                continue
            
            email_data = self._load_json(file_path)
            for email in email_data:
                self._generate_email_template(email)
    
    def _generate_email_template(self, email):
        """Generate an HTML email template."""
        subject = email["subject"]
        email_body = email["body"]
        sender_name = email["email_sign_fullname"]
        sender_role = email["email_sign_role"]
        company_name = email["email_sign_company"]
        receiver_name = email["addressing_the_receiver"]
        cta = email["call_to_action_text"]
        cta_color = email["call_to_action_color"]
        cta_color = f"rgb{tuple(cta_color)}" if isinstance(cta_color, list) else cta_color
        
        fake_link = "https://example.com"
        provider_data = next(iter(self.blended_data.values()))  # Example: using the first provider
        provider, address, depart, phone, vat = self._get_provider_info(provider_data)
        color_name = self._process_color(provider_data.get('color', {}))
        
        html_content = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{subject}</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            width: 600px;
                            margin: 20px auto;
                            background-color: #fff;
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            padding: 20px;
                        }}
                        .email-header {{
                            background-color: {color_name};
                            color: #fff;
                            padding: 10px 0;
                            text-align: center;
                        }}
                        .email-header img {{
                            width: 120px;
                            margin-bottom: 10px;
                        }}
                        .email-header h1 {{
                            font-size: 24px;
                            font-weight: bold;
                            margin: 0;
                        }}
                        .email-content {{
                            font-size: 16px;
                            color: #333;
                            margin-top: 20px;
                        }}
                        .cta-button {{
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: {cta_color};
                            color: white;
                            text-align: center;
                            font-weight: bold;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }}
                        .cta-button:hover {{
                            background-color: {color_name};
                        }}
                        .email-footer {{
                            font-size: 14px;
                            color: #777;
                            text-align: center;
                            margin-top: 20px;
                            border-top: 1px solid #ddd;
                            padding-top: 20px;
                        }}
                        .email-footer a {{
                            color: {color_name};
                            text-decoration: none;
                        }}
                        .social-icons {{
                            margin-top: 10px;
                            text-align: center;
                        }}
                        .social-icons a {{
                            margin: 0 10px;
                            display: inline-block;
                        }}
                        .social-icons img {{
                            width: 24px;
                            height: 24px;
                        }}
                        .additional-footer {{
                            font-size: 12px;
                            color: #333;
                            background-color: #d3d3d3; /* Gray background color */
                            text-align: center;
                            padding: 10px;
                            border-top: 1px solid #ccc;
                            border-radius: 0 0 10px 10px;
                            margin-top: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="email-header">
                            <img src="" alt="">    
                            <h1>{subject}</h1>
                        </div>
                        <div class="email-content">
                            <h2>{receiver_name}</h2>
                            <p>{email_body}</p>  <!-- Use the dynamically generated email body here -->
                            <a href="{fake_link}" class="cta-button">{cta}</a>
                            
                            <!-- Signature Directly Integrated -->
                            <p style="margin-top: 20px;">Best regards,</p>
                            <p style="margin: 5px 0;"><strong>{sender_name}</strong></p>
                            <p style="margin: 5px 0;">{sender_role}</p>
                            <p style="margin: 5px 0;">{company_name}</p>
                        </div>
                        <div class="email-footer">
                            <p><strong>{depart}</strong></p>
                            <p>Email: support@{provider.lower().replace(' ', '')}.be | Phone: {phone}</p>
                            <p>Visit our website: <a href="{fake_link}">www.{provider.lower().replace(' ', '')}.com</a></p>
                            <div class="social-icons">
                                <a href={fake_link}>
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Faceb
                                </a>
                                <a href={fake_link}>
                                    <img src="https://www.svgrepo.com/show/452123/twitter.svg" alt="Twitter">
                                </a>
                                <a href={fake_link}>
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" alt="LinkedIn">
                                </a>
                            </div>
                        </div>
                        <div class="additional-footer">
                            <p>Please be aware that this email and its links include data about your individual profile. 
                            In order to avoid that third parties can access your personal data, 
                            you should not forward this email and the links contained in it.</p>
                            <p><strong>© 2025 The {provider} Belgium n.v./s.a.</strong></p>
                            <p>{address}<br>KBO/BCE {vat} (RPR/RPM Brussel/Bruxelles)</p>
                            <p>
                                <a href={fake_link}>Terms of use</a> - 
                                <a href={fake_link}>Privacy policy</a> - 
                                <a href={fake_link}>Contact us</a>
                            </p>
                            <!-- Container for logo and QR code -->
                            <div class="unsubscribe-container" style="text-align: center; margin-top: 20px; font-size: 12px; color: #555;">
                                <p>If you no longer wish to receive notifications, you can 
                                    <a href="{fake_link}" style="color: #007BFF; text-decoration: none;">unsubscribe here</a>.
                                </p>
                            </div>
                        </div>
                    </div>
                </body>
                """

        # Save the email to an HTML file
        os.makedirs('samples', exist_ok=True)
        sanitized_subject = re.sub(r'[\/:*?"<>|]', '_', subject)
        filename = f"{receiver_name}_phishing_email_{sanitized_subject}.html"
        file_path = os.path.join('samples', filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

    def run(self, specific_files):
        """Run the full email generation process."""
        self.generate_emails(specific_files)
        print("Email templates generated successfully!")


