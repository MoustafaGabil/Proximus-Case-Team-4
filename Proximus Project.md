
  
<img src="proxlogo.jpg" alt="Proximus" width="25%">

# Proximus Project

## :sparkles:Overview
**Repository**: `https://github.com/yusra2323/Proximus-Case-Team-4`  
**Type**: Phishing Email - Proximus Case  
**Duration**: 2 week  
**Deadline**: 24/01/2025  
**Team**: Group Project 

:chart_with_upwards_trend: Proximus Research and Data Aggregation Project
This project involves automating data gathering and reporting processes using advanced AI tools, specifically tailored to extract information about Proximus, a Belgian company. It utilizes the Google GenAI API and Python libraries to produce structured JSON outputs for different aspects of Proximus, such as news, employees, departments, branding, and service providers.



## :sparkles:Features
## Core Functions

1. **Automated Data Extraction**:

- Uses the Google GenAI API to extract structured information in JSON format for:
- News reports.
- Employee details.
- Department summaries.
- Branding color schemes.
- Service providers.

 
 2. **Data Aggregation:**:
 
- Merges extracted data from multiple JSON files into a comprehensive dataset.
- Outputs blended JSON files for easier consumption and further processing.

 3. **Email Writing Assistant:**:
 
- Generates tailored, professional emails for specific employees with varying tones, based on dynamic recipient data.
- Supports content personalization for effective communication.


 4. **Randomized Input Tools:**: 
 
- Random selection for dates, tones, and employees for dynamic testing and execution.


## :sparkles:Outputs
- JSON files for each category (e.g., proximus_employees.json, proximus_departments.json).
- Comprehensive merged JSON data (blended_data_proximus.json and blended_data_providers.json).
- Automated email drafts with structured JSON output.


## Setup Instructions

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
```
## :sparkles:Usage
1. **Run the Notebook**: Open notebook.ipynb in Jupyter Notebook or any supported IDE.
2. **Generate Outputs**: Execute cells sequentially to produce individual and aggregated JSON files.
3. **Customize**: Modify input parameters in the cells to tailor outputs, such as company name, date ranges, or report structures.


### Directory Structure
```
./
├── notebook.ipynb           # Main notebook for executing the project
├── README_project.md        # Project documentation
├── .env                     # Contains the API key (not included in repo for security)
├── proximus_news.json       # Generated JSON file for news
├── proximus_employees.json  # Generated JSON file for employees
├── proximus_departments.json# Generated JSON file for departments
├── proximus_colors.json     # Branding information
├── proximus_providers.json  # Service providers data
├── blended_data_proximus.json # Aggregated Proximus data
└── blended_data_providers.json# Aggregated provider data

```


### :sparkles:Future Enhancements
- Integrate additional analysis tools for deeper insights.
- Automate email delivery based on generated content.
- Enhance error handling during JSON parsing and data merging.



### :sparkles:Challenges

The project faces several challenges, including API limitations such as rate limiting and inconsistent response quality, which can lead to incomplete or inaccurate data requiring manual review. Parsing and integrating data from multiple JSON files can result in errors, especially when dealing with unexpected formats or missing fields, while data merging conflicts may arise due to inconsistent keys. Dynamic personalization poses the challenge of maintaining relevance and professionalism in randomized outputs like emails. Scaling the framework to support other companies or larger datasets without extensive reconfiguration is another hurdle. Additionally, handling missing or incomplete data, particularly for specific fields like employee roles or contact details, can create gaps in reports. Ensuring time-sensitive information like news updates remains relevant and addressing errors during API calls, file operations, and JSON manipulations are critical for seamless workflow. Lastly, maintaining up-to-date documentation as the project evolves is essential for clarity and replicability.

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
-Keeping the README and documentation up to date as the project evolves or scales.