import os
from generatecontent import ReportManager, ProviderManager



def main():
    company_name = "Proximus"
    output_directory = "Izabella\\output\\generatecontent"
    os.makedirs(output_directory, exist_ok=True)

    report_manager = ReportManager(output_dir=output_directory)
    print(f"Starting report generation for {company_name}...")
    report_manager.generate_all_reports(company_name)
    print("All reports have been successfully generated and saved.")

    input_file = os.path.join(output_directory, "proximus_providers.json")
    provider_output_file = os.path.join(output_directory, "provider.json")

    provider_manager = ProviderManager(
        input_file=input_file,
        output_file=provider_output_file
    )

    print("\nStarting provider selection process...")
    provider_manager.execute(company_name)
    print("Provider selection process completed.")

if __name__ == "__main__":
    main()
