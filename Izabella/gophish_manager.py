from gophish import Gophish
from gophish.models import Template, Page, SMTP, User, Group, Campaign
from dotenv import load_dotenv
import os
from typing import List

class GophishCampaignManager:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('GOPHISH_API_KEY')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.smtp_email = os.getenv('SMTP_EMAIL')
        
        # Initialize API connection
        self.api_url = 'https://localhost:3333'
        self.api = Gophish(self.api_key, host=self.api_url, verify=False)
        
        # Store created components
        self.template = None
        self.page = None
        self.smtp_profile = None
        self.group = None
        self.campaign = None

    def test_connection(self) -> bool:
        """Test the connection to Gophish API"""
        try:
            campaigns = self.api.campaigns.get()
            print(f"Successfully connected! Number of campaigns: {len(campaigns)}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def create_email_template(self, name: str, subject: str, text: str, html: str) -> Template:
        """Create an email template"""
        template = Template(
            name=name,
            subject=subject,
            text=text,
            html=html
        )
        self.template = self.api.templates.post(template)
        print(f"Template created with ID: {self.template.id}")
        return self.template

    def create_landing_page(self, name: str, html: str) -> Page:
        """Create a landing page"""
        page = Page(
            name=name,
            html=html
        )
        self.page = self.api.pages.post(page)
        print(f"Landing page created with ID: {self.page.id}")
        return self.page

    def create_smtp_profile(self, name: str) -> SMTP:
        """Create SMTP sending profile"""
        smtp = SMTP(name=name)
        smtp.host = "smtp.gmail.com:587"
        smtp.from_address = self.smtp_email
        smtp.interface_type = "SMTP"
        smtp.username = self.smtp_email
        smtp.password = self.smtp_password
        smtp.ignore_cert_errors = True

        self.smtp_profile = self.api.smtp.post(smtp)
        print(f"Sending profile created with ID: {self.smtp_profile.id}")
        return self.smtp_profile

    def create_target_group(self, name: str, targets: List[dict]) -> Group:
        """Create a group of targets"""
        users = [
            User(
                first_name=target['first_name'],
                last_name=target['last_name'],
                email=target['email']
            ) for target in targets
        ]
        
        group = Group(name=name, targets=users)
        self.group = self.api.groups.post(group)
        print(f"Group created with ID: {self.group.id}")
        return self.group

    def create_campaign(self, name: str) -> Campaign:
        """Create a phishing campaign"""
        if not all([self.template, self.page, self.smtp_profile, self.group]):
            raise ValueError("All components (template, page, SMTP profile, and group) must be created before campaign")

        campaign = Campaign(
            name=name,
            groups=[self.group],
            page=self.page,
            template=self.template,
            smtp=self.smtp_profile
        )

        self.campaign = self.api.campaigns.post(campaign)
        print(f"Campaign created with ID: {self.campaign.id}")
        return self.campaign

