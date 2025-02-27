import os
import json
from generatecontent import ReportManager, ProviderManager, GeminiConnector, DataBlender
from email_creator import EmailGenerator, GeminiConnectorEmails, DataProvider, LogoFetcher, EmailTemplateGenerator
#from gophish_manager import GophishCampaignManager


def main():
    company_name = "Proximus"
    output_directory = "Izabella\\output\\generatecontent"
    os.makedirs(output_directory, exist_ok=True)

    # Generating reports
    report_manager = ReportManager(output_dir=output_directory)
    print(f"Starting report generation for {company_name}...")
    report_manager.generate_all_reports(company_name)
    print("All reports have been successfully generated and saved.")

    input_file = os.path.join(output_directory, "proximus_providers.json")
    provider_output_file = os.path.join(output_directory, "provider.json")

    # Provider selection process
    provider_manager = ProviderManager(
        input_file=input_file,
        output_file=provider_output_file
    )

    print("\nStarting provider selection process...")
    provider_manager.execute(company_name)
    print("Provider selection process completed.")

    # Read the provider from the provider.json file
    provider_file_path = os.path.join(output_directory, "provider.json")
    with open(provider_file_path, "r") as f:
        provider_data = json.load(f)

    # Extract provider from the first item in the list
    provider = provider_data[0].get("provider", "DefaultProvider")  # Default value in case 'provider' is not found

    # Blend data for company and provider
    blender = DataBlender(output_directory)
    blender.blend_company_data(company_name)

    # Get provider name from provider.json
    with open(provider_file_path, "r") as f:
        provider_data = json.load(f)
    provider = provider_data[0].get("provider", "DefaultProvider")
    blender.blend_provider_data(provider)

    # Initialize EmailGenerator
    email_output_file = os.path.join(output_directory, "generated_emails.json")
    gemini_connector = GeminiConnector()  # Initialize Gemini client
    data_provider = DataProvider(output_dir=output_directory)  # Create DataProvider instance

    # Initialize EmailGenerator
    email_generator = EmailGenerator(
        model=gemini_connector.get_model(),
        config=gemini_connector.get_config()
    )

    # Generate emails
    provider_departments = ["Consumer Market", "IT Infrastructure", "Enterprise Market"]  # List departments as needed
    random_employee = data_provider.get_random_employee()

    print("\nStarting email generation...")

    # Generate service emails
    service_emails = email_generator.generate_service_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee
    )
    email_generator.save_emails_to_file(service_emails, output_dir=output_directory, email_type="services_emails")

    # Generate events emails
    random_event = data_provider.get_random_events()
    random_date = email_generator.pick_random_date()    
    events_emails = email_generator.generate_events_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_event=random_event,
        random_date=random_date
    )
    email_generator.save_emails_to_file(events_emails, output_dir=output_directory, email_type="events_emails")

    # Generate issue emails
    random_issue = data_provider.get_random_issues() 
    random_date= email_generator.pick_random_date()
    issues_emails = email_generator.generate_issue_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_issue=random_issue,
        random_date=random_date
    )
    email_generator.save_emails_to_file(issues_emails, output_dir=output_directory, email_type="issues_emails")

    # Generate news emails
    news_file_path = os.path.join(output_directory, "proximus_main_company_report.json")
    news = data_provider.get_random_news(news_file_path)
    news_emails = email_generator.generate_news_email(
        provider=provider,
        company_name=company_name,
        random_employee=random_employee,
        news=news,
        output_directory=output_directory
    )

    # Save the emails to a file
    email_generator.save_emails_to_file(news_emails, output_dir=output_directory, email_type="news_emails")

    # Save all emails to a file
    # input_dir = "Izabella\\output\\generatecontent"
    # output_filename = "generated_emails.json"
    # files_to_merge = ["events.json", "issues.json", "services.json", "news.json"]
    # email_generator.merge_emails(input_dir, output_filename, files_to_merge)
    # print("Emails have been successfully generated and saved.")      

    # Initialize LogoFetcher
    logo_fetcher = LogoFetcher(output_dir=output_directory)

    # Fetch company logo
    company_logo = logo_fetcher.get_company_logo(company_name)
    print(f"Company logo for {company_name}: {company_logo}")

    # Fetch provider logo
    with open(provider_file_path, "r") as f:
        provider_data = json.load(f)
    provider = provider_data[0].get("provider", "DefaultProvider")
    provider_logo = logo_fetcher.get_provider_logo(provider)
    print(f"Provider logo for {provider}: {provider_logo}")

    # Optionally, save logos from the provider JSON file
    provider_logos = logo_fetcher.save_logos(provider_file_path)
    print("Additional logos saved:", provider_logos)


    # Define the directories
    json_dir = "Izabella\\output\\generatecontent"  # Directory where your input JSON files are located
    output_dir = "Izabella\\output\\generatecontent"  # Directory where blended data and emails will be saved

    generator = EmailTemplateGenerator(
        json_dir="Izabella\\output\\generatecontent",
        blend_provider_data="Izabella\\output\\generatecontent\\blend_provider_data.json"
    )
    generator.run([
        "events_emails.json",
        "issues_emails.json",
        "news_emails.json",
        "services_emails.json"
    ])      
#    Initialize Gophish campaign manager
    # print("\nInitializing Gophish campaign...")
    # gophish_manager = GophishCampaignManager()
    # 
    # if gophish_manager.test_connection():
        # Process each generated email type
        # for email_type in ["services_emails", "events_emails", "issues_emails"]:
            # email_file = os.path.join(output_directory, f"{email_type}.json")
            # 
            # with open(email_file, 'r') as f:
                # emails = json.load(f)
                # 
            # for idx, email in enumerate(emails):
                # Create template for each email
                # template = gophish_manager.create_email_template(
                    # name=f"{email_type}_template_{idx}",
                    # subject=email.get('subject', 'Important Update'),
                    # text=email.get('content', ''),
                    # html=f"<p>{email.get('content', '')}</p>"
                # )
                # 
                # Create landing page
                # gophish_manager.create_landing_page(
                    # name=f"{email_type}_page_{idx}",
                    # html='<html><body>Click <a href="{{.URL}}">here</a></body></html>'
                # )
                # 
                # Create SMTP profile if not exists
                # if not gophish_manager.smtp_profile:
                    # gophish_manager.create_smtp_profile(f"{email_type}_smtp_{idx}")
                # 
                # Create target group
                # targets = [
                    # {
                        # 'first_name': random_employee.get('first_name', ''),
                        # 'last_name': random_employee.get('last_name', ''),
                        # 'email': random_employee.get('email', '')
                    # }
                # ]
                # gophish_manager.create_target_group(f"{email_type}_group_{idx}", targets)
                # 
                # Create campaign
                # gophish_manager.create_campaign(f"{email_type}_campaign_{idx}")
                # 
                # print(f"Campaign created for {email_type} - {idx+1}/{len(emails)}")

        # print("All Gophish campaigns have been created successfully.") xyz

if __name__ == "__main__":
    main()
