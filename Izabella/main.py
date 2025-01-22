import os
import json
from generatecontent import ReportManager, ProviderManager, GeminiConnector
from email_creator import EmailGenerator, GeminiConnectorEmails, DataProvider 
from gophish_manager import GophishCampaignManager


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
    events_emails = email_generator.generate_events_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_event=random_event
    )
    email_generator.save_emails_to_file(events_emails, output_dir=output_directory, email_type="events_emails")

    # Generate issue emails
    random_issue = data_provider.get_random_issues() 
    issues_emails = email_generator.generate_issue_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_issue=random_issue
    )
    email_generator.save_emails_to_file(issues_emails, output_dir=output_directory, email_type="issues_emails")

    print("Emails have been successfully generated and saved.")


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

        # print("All Gophish campaigns have been created successfully.")

if __name__ == "__main__":
    main()
