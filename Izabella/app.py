import streamlit as st
import os
import json
import re
import random
from google import genai
from dotenv import load_dotenv

class CompanyResearchApp:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=api_key)
        
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.system_instruction = """You are an expert analyst conducting comprehensive company research in Belgium. 
        Your goal is to provide detailed, factual information about companies and their business ecosystem."""

    def extract_json(self, text):
        """Improved JSON extraction method"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            json_match = re.findall(r'\[.*?\]', text, re.DOTALL | re.MULTILINE)
            
            for match in json_match:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
            
            return []

    def generate_company_providers(self, company_name):
        """Generate list of providers for the company"""
        config = genai.types.GenerateContentConfig(
            system_instruction=self.system_instruction, 
            tools=[genai.types.Tool(google_search={})], 
            temperature=0,
            maxOutputTokens=8000, 
            top_p=0.9, 
            top_k=5, 
            safety_settings=self.safety_settings
        )

        providers_contents = f"""
        Research and list the main service providers for {company_name} in Belgium.
        
        JSON Schema:
        Providers = {{'provider_name': str, 'service_type': str, 'description': str}}
        Return: list[Providers]
        """
        
        providers_response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp', 
            config=config, 
            contents=providers_contents
        )

        providers = self.extract_json(providers_response.text)
        
        # Save providers to JSON
        providers_file = f'{company_name.lower().replace(" ", "_")}_providers.json'
        with open(providers_file, 'w') as f:
            json.dump(providers, f, indent=4)

        return providers

    def generate_provider_details(self, company_name, provider):
        """Generate detailed provider research"""
        config = genai.types.GenerateContentConfig(
            system_instruction=self.system_instruction, 
            tools=[genai.types.Tool(google_search={})], 
            temperature=0,
            maxOutputTokens=8000, 
            top_p=0.9, 
            top_k=5, 
            safety_settings=self.safety_settings
        )

        # Detailed research sections
        research_types = [
            ('employees', 'Write a detailed report about employees'),
            ('colors', 'Identify the main colors of the company\'s branding'),
            ('departments', 'Provide details about company departments')
        ]
        
        provider_data = {'provider_name': provider}
        
        for data_type, prompt in research_types:
            contents = f"""
            Write a report about {provider} company, a provider for {company_name}.
            {prompt}
            
            Use an appropriate JSON schema for the information type.
            """
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp', 
                config=config, 
                contents=contents
            )
            
            provider_data[data_type] = self.extract_json(response.text)
        
        # Save provider details
        details_file = f'{provider.lower().replace(" ", "_")}_details.json'
        with open(details_file, 'w') as f:
            json.dump(provider_data, f, indent=4)
        
        return provider_data

    def generate_sample_emails(self, company, provider, provider_details):
        """Generate sample phishing emails based on company and provider details"""
        config = genai.types.GenerateContentConfig(
            system_instruction=self.system_instruction, 
            temperature=0.7,
            maxOutputTokens=8000, 
            safety_settings=self.safety_settings
        )

        # Prepare email generation prompt
        email_prompt = f"""
        Generate a list of 3 realistic phishing email scenarios for {provider}, 
        a service provider for {company}. 
        
        Provide details for each email including:
        - Subject line
        - Email body content
        - Call to action
        - Sender details
        
        Return as a JSON list with the following schema:
        {{
            "subject": str,
            "body": str,
            "call_to_action": str,
            "sender_name": str,
            "sender_role": str
        }}
        """

        # Generate email scenarios
        email_response = self.client.models.generate_content(
            model='gemini-2.0-flash-exp', 
            config=config, 
            contents=email_prompt
        )

        # Extract JSON
        try:
            email_scenarios = self.extract_json(email_response.text)
        except Exception as e:
            st.error(f"Error generating email scenarios: {e}")
            email_scenarios = []

        # Generate HTML emails
        os.makedirs('samples', exist_ok=True)
        generated_emails = []

        for idx, email_data in enumerate(email_scenarios, 1):
            # Use provider details to enrich email
            departments = provider_details.get('departments', [{}])[0]
            department = departments.get('name', 'Customer Support')
            
            # Simulate additional details
            fake_link = f"https://www.{provider.lower().replace(' ', '')}.be"
            color_name = random.choice(['#007BFF', '#28a745', '#dc3545', '#ffc107'])
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{email_data.get('subject', 'Important Notification')}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }}
                    .email-container {{ border: 1px solid #ddd; padding: 20px; }}
                    .email-header {{ background-color: {color_name}; color: white; padding: 10px; text-align: center; }}
                    .email-body {{ margin-top: 20px; }}
                    .cta-button {{ 
                        display: inline-block; 
                        background-color: {color_name}; 
                        color: white; 
                        padding: 10px 20px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>{email_data.get('subject', 'Important Notification')}</h1>
                    </div>
                    <div class="email-body">
                        <p>Dear {company} Customer,</p>
                        <p>{email_data.get('body', 'We have an important update for you.')}</p>
                        <a href="{fake_link}" class="cta-button">{email_data.get('call_to_action', 'Click Here')}</a>
                        <p>Best regards,</p>
                        <p>
                            <strong>{email_data.get('sender_name', 'Customer Support Team')}</strong><br>
                            {email_data.get('sender_role', department)} | {provider}
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Save HTML file
            filename = f'samples/phishing_email_{company}_{provider}_scenario_{idx}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            generated_emails.append(filename)

        return generated_emails

    def run(self):
        """Streamlit application main interface"""
        st.title("Belgian Company and Provider Research")
        
        # Initialize session state
        if 'stage' not in st.session_state:
            st.session_state.stage = 'company'
        if 'providers' not in st.session_state:
            st.session_state.providers = []
        
        # Company search stage
        if st.session_state.stage == 'company':
            company = st.text_input("Enter a Belgian Company Name", placeholder="e.g., Proximus")
            
            if st.button("Find Company Providers") and company:
                with st.spinner('Researching company providers...'):
                    try:
                        # Generate providers for the company
                        st.session_state.providers = self.generate_company_providers(company)
                        st.session_state.company = company
                        st.session_state.stage = 'providers'
                        st.experimental_rerun()
                    
                    except Exception as e:
                        st.error(f"Error in research process: {e}")
        
        # Provider selection stage
        elif st.session_state.stage == 'providers':
            st.subheader(f"Providers for {st.session_state.company}")
            
            selected_provider = st.selectbox(
                "Choose a Provider to Research", 
                [p['provider_name'] for p in st.session_state.providers]
            )
            
            if st.button("Research Selected Provider"):
                with st.spinner(f'Researching {selected_provider}...'):
                    # Research provider details
                    provider_details = self.generate_provider_details(
                        st.session_state.company, 
                        selected_provider
                    )
                    
                    # Display provider details
                    for section, data in provider_details.items():
                        if section != 'provider_name':
                            st.subheader(section.capitalize())
                            st.json(data)
                    
                    # Generate sample phishing emails
                    st.subheader("Sample Phishing Email Scenarios")
                    generated_emails = self.generate_sample_emails(
                        st.session_state.company, 
                        selected_provider, 
                        provider_details
                    )
                    
                    # Display download links for generated emails
                    for email_file in generated_emails:
                        with open(email_file, 'r') as f:
                            st.download_button(
                                label=f"Download {os.path.basename(email_file)}",
                                data=f.read(),
                                file_name=os.path.basename(email_file),
                                mime="text/html"
                            )
            
            # Button to search another company
            if st.button("Search Another Company"):
                st.session_state.stage = 'company'
                st.session_state.providers = []
                st.experimental_rerun()

def main():
    app = CompanyResearchApp()
    app.run()

if __name__ == "__main__":
    main()