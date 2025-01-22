import os
from generatecontent import ReportManager, ProviderManager, GeminiConnector
from email_creator import EmailGenerator, GeminiConnectorEmails, DataProvider 

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
    provider = "Proximus"
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
    email_generator.save_emails_to_file(service_emails, output_dir=output_directory, email_type="services_emails")  # Only output_dir is needed

    # Generate events emails
    random_event = data_provider.get_random_events()  
    events_emails = email_generator.generate_events_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_event=random_event
    )
    email_generator.save_emails_to_file(events_emails, output_dir=output_directory, email_type="events_emails")  # Only output_dir is needed

    # Generate issue emails
    random_issue = data_provider.get_random_issues() 
    issues_emails = email_generator.generate_issue_emails(
        provider=provider,
        provider_departments=provider_departments,
        company_name=company_name,
        random_employee=random_employee,
        random_issue=random_issue
    )
    email_generator.save_emails_to_file(issues_emails, output_dir=output_directory, email_type="issues_emails")  # Only output_dir is needed

    print("Emails have been successfully generated and saved.")

if __name__ == "__main__":
    main()
