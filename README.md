
  
<img src="proxlogo.jpg" alt="Proximus" width="25%">

# Proximus Project

## :sparkles:Overview
**Repository**: `https://github.com/yusra2323/Proximus-Case-Team-4`  
**Type**: Phishing Email - Proximus Case  
**Duration**: 2 week  
**Deadline**: 24/01/2025  
**Team**: Group Project 

:chart_with_upwards_trend:This project automates the creation of sophisticated phishing emails targeting Proximus employees by leveraging the power of Large Language Models (LLMs) and integrating with the Gophish phishing framework.  It performs comprehensive company research, generates personalized email content, and facilitates seamless deployment through Gophish.




## :sparkles:Features


* **Automated Proximus Research:**  Gathers extensive information about Proximus, including news, employees, departments, branding, and service providers using the Google Gemini API. This data is structured and saved in JSON format for easy processing.
* **Dynamic Email Generation:** Creates highly personalized phishing emails tailored to specific Proximus employees based on their roles and departments. Email tone, content, and call to action are dynamically adjusted for increased effectiveness.
* **Gophish Integration:** Streamlines the deployment of phishing campaigns by automating the creation of email templates, landing pages, sending profiles, user groups, and campaigns within Gophish.
* **Randomized Input and Personalization:** Employs randomized selection of dates, email tones, employee details, and Proximus news to enhance the variety and realism of phishing emails.
* **HTML Email Generation:** Creates visually appealing HTML emails with embedded branding elements (colors, logos) and personalized content for a convincing phishing experience.


## :sparkles:Outputs
- JSON files for each category (e.g., proximus_employees.json, proximus_departments.json).
- Comprehensive merged JSON data (blended_data_proximus.json and blended_data_providers.json).
- Automated email drafts with structured HTML output.


## :sparkles:Setup Instructions

### :boom:Prerequisites

 1. Python 3.8+
2. Required Python libraries:
- google-genai
- dotenv
- os
- re
- random
3. Google GenAI API Key:
- Place your key in a .env file under the variable GEMINI_API_KEY.
4. Gophish API Key:
- Place your key in a .env file under the variable GOPHISH_API_KEY.
- Place your SMTP Credentials in a .env file under the variable SMTP_EMAIL and SMTP_PASSWORD


## :boom:Installation
1. Clone this repository:
```
git clone <repository_url>
cd <repository_directory>
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Add your API key:
- Create a .env file:

```
GEMINI_API_KEY=your_api_key_here
GOPHISH_API_KEY=your_api_key_here
SMTP_EMAIL=your_email_here
SMTP_PASSWORD=your_password_here
```
## :sparkles:Usage
1. **Run the Notebook**: Open notebook.ipynb in Jupyter Notebook or any supported IDE.
2. **Generate Outputs**: Execute cells sequentially to produce individual and aggregated JSON files.
3. **Customize**: Modify input parameters in the cells to tailor outputs, such as company name, date ranges, or report structures.


### :boom:Directory Structure
```
.
├── notebook.ipynb              # Main Jupyter Notebook for data collection, email generation, and Gophish interaction
├── train_LLM.ipynb             # Jupyter Notebook for training the custom LLM (optional)
├── .env                        # Environment variables (API keys, SMTP credentials) - DO NOT COMMIT THIS FILE
├── proximus_news.json          # Example JSON output: Proximus news data
├── proximus_employees.json     # Example JSON output: Proximus employee data
├── proximus_departments.json   # Example JSON output: Proximus department data
├── proximus_colors.json        # Example JSON output: Proximus branding colors
├── proximus_providers.json     # Example JSON output: Proximus service providers
├── blended_data_proximus.json  # Example JSON output: Aggregated Proximus data
├── blended_data_providers.json # Example JSON output: Aggregated provider data
├── provider_*.json             # Example JSON outputs: Data about specific providers
├── samples/                    # Directory containing generated HTML email files
├── requirements.txt            # Project dependencies
└── README.md                   # This file

```


### :sparkles:Future Enhancements

* **Automated Proximus Research:**  Gathers extensive information about Proximus, including news, employees, departments, branding, and service providers using the Google Gemini API. This data is structured and saved in JSON format for easy processing.
* **Dynamic Email Generation:** Creates highly personalized phishing emails tailored to specific Proximus employees based on their roles and departments. Email tone, content, and call to action are dynamically adjusted for increased effectiveness.
* **Gophish Integration:** Streamlines the deployment of phishing campaigns by automating the creation of email templates, landing pages, sending profiles, user groups, and campaigns within Gophish.
* **Randomized Input and Personalization:** Employs randomized selection of dates, email tones, employee details, and Proximus news to enhance the variety and realism of phishing emails.
* **HTML Email Generation:** Creates visually appealing HTML emails with embedded branding elements (colors, logos) and personalized content for a convincing phishing experience.




### :sparkles:Challenges


####  1. API Limitations:
- Rate Limiting: Restrictions on the number of API calls per minute/hour can slow data collection.
- Response Quality: The API might produce incomplete or inaccurate responses that need manual review and correction.

#### 2. Data Parsing and Integration:
- JSON Parsing Errors: Errors during parsing due to unexpected API response formats.
- Data Merging Conflicts: Inconsistent keys or missing data while consolidating JSON files.

#### 3. Dynamic Personalization:
- Balancing randomization with relevance to ensure the outputs (e.g., emails) remain meaningful and professional.

#### 4. Scaling and Adaptability:
- Adapting the project framework for different companies or larger datasets without significant reconfiguration.

#### 5. Handling Missing or Incomplete Data:
- Some required data fields (e.g., employee roles or contact details) may not be available in public sources, leading to gaps in reports.

#### 6. Time Sensitivity:
-  Ensuring the news and updates retrieved are relevant and fall within the defined time frame.

#### 7. Error Handling:
- Dealing with errors during API calls, file I/O operations, and JSON manipulations while ensuring minimal interruptions to the workflow.

#### 8. Documentation Maintenance:

-  Keeping the README and documentation up to date as the project evolves or scales.

## :sparkles:Fine-Tune GPT-2 for Domain-Specific Text Generation
train_LLM.ipynb demonstrates a MVP for fine-tuning the GPT-2 language model to generate domain-specific text, such as phishing email simulations. The model was trained on a small dataset as part of the MVP design.

The training process was conducted in Google Colab, leveraging its GPU capabilities to handle the computational demands. However, due to the free tier's limitations in GPU memory and RAM, the training process was constrained but still effective for demonstration purposes.

#### The code includes:

Preprocessing and tokenizing input text using a custom PyTorch Dataset class.
Fine-tuning GPT-2 using the Hugging Face Transformers library with tailored training arguments.
Implementation of a custom loss function and basic evaluation metrics.
Saving the fine-tuned model to Google Drive for later use.
You can adapt this code with your own dataset to fine-tune a language model that generates text in a style consistent with your domain-specific needs.

#### Required Libraries:

transformers
torch
pandas
datasets
This setup offers an accessible starting point for generating high-quality text tailored to specialized content requirements.


## :sparkles:Disclaimer

This project is for educational and research purposes only.  Use it responsibly and ethically. Do not use it for illegal or malicious activities.  Phishing simulations should only be conducted with the explicit consent of the target organization.

Key improvements in this README:

Clearer Structure: Sections are better organized with descriptive headings.

Expanded Feature List: Provides more details about the project's capabilities.

Detailed Project Structure: Explains the purpose of each file and directory.

Improved Setup Instructions: Provides step-by-step instructions for running the project.

Challenges and Improvements Section: Highlights potential issues and areas for future development.

Important Disclaimer: Emphasizes the ethical considerations and responsible use of the project.

Concise Language: Uses more direct and concise wording for better readability. Removed unnecessary introductory phrases.


## :sparkles:Our team

#### For more details, feel free to explore the repository and get in touch via GitHub issues.



:crown:Rik: Team leader:
- GitHub: https://github.com/ricosaxo
- Linkedin: www.linkedin.com/in/rik-sas-456b7611/?trk=public-profile-join-page


:crown:Yusra: repo manager
- GitHub: https://github.com/yusra2323
- Linkedin: www.linkedin.com/in/yusra-ali-9a3566308


:crown:Mustafa:
- GitHub: https://github.com/
- Linkedin: www.linkedin.com/moustafa-gabil


:crown:Izabella:
- GitHub: https://github.com/IzaMacBor
- Linkedin: www.linkedin.com/in/izabela-mac-borkowska-752b9a2b1


:crown:Maarten:
- GitHub: https://github.com/Mrtnwrnz
- Linkedin: https://www.linkedin.com/in/maarten-w/


:crown:Majid: 
- GitHub: https://github.com/majidaskary
- Linkedin: www.linkedin.com/in/majidaskary