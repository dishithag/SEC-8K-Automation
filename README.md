# SEC-8K-Automation
## **Overview**
This project automates the process of fetching SEC-8K filings related to cybersecurity incidents, providing an efficient and timely alerting mechanism. By leveraging web scraping and email notifications, it simplifies the tracking of material cybersecurity events reported by U.S. public companies to the Securities and Exchange Commission (SEC).
Whenever a company undergoes a cybersecurity breach or incident and files an SEC-8K report (under Items 1.05 or 8.01), this project automates the retrieval process, ensuring that stakeholders are promptly notified and equipped with the official filing documents.

## **What is SEC, EDGAR, and SEC-8K?**

- **SEC (Securities and Exchange Commission):**  
  The SEC is a U.S. regulatory authority responsible for overseeing securities markets, ensuring transparency, and protecting investors.

- **EDGAR (Electronic Data Gathering, Analysis, and Retrieval System):**  
  EDGAR is the SEC's public database where all U.S. public companies file mandatory disclosures, including material events like cybersecurity breaches.

- **SEC-8K Forms:**  
  SEC-8K is a filing used to disclose significant events that could affect a company's stock or financial standing. In the context of cybersecurity:
  - **Item 1.05 - Material Cybersecurity Incidents:**  
    Companies must disclose cybersecurity breaches that materially impact their business or operations.
  - **Item 8.01 - Other Events:**  
    Filed when companies cannot yet determine if the incident has a material impact but want to disclose it proactively.

These filings play a critical role in understanding a company's cybersecurity posture and assessing potential market impacts.

## **What is Web Scraping?**

Web scraping is a technique used to extract data from websites by automating interactions and data retrieval. In this project, web scraping is used to navigate the SEC EDGAR website, dynamically search for filings, and extract relevant details about material cybersecurity events.

## **Technology Stack and Libraries**

- **Programming Language:** Python 3.7+
- **Libraries Used:**
  - `selenium`: For web scraping and navigating the SEC EDGAR website.
  - `webdriver_manager`: To automatically download and manage ChromeDriver.
  - `smtplib`: To send email notifications via SMTP.
  - `json`: To handle configuration and dynamic parameters.
  - `logging`: For structured debugging and monitoring.
  - `email.mime`: To create email content in HTML format.
  - `datetime`: For date manipulations in dynamic searches.

## **Key Features**

- **Automated Alerts:** Fetches SEC-8K filings for Items 1.05 and 8.01 related to cybersecurity events and sends email notifications summarizing the findings.  
- **Dynamic Date Filtering:** Allows retrieval of filings from a user-defined date range (default: past 200 days).  
- **Error and Exception Handling:** Incorporates mechanisms to handle missing elements, timeouts, and unexpected website changes for reliable execution.  
- **Multi-Item Support:** Tracks multiple filing types (e.g., Items 1.05 and 8.01) in a single execution.  

## **Technical Details**

- **Object-Oriented Design (OOP):** Encapsulates functionality into reusable classes for scalability and modularity.  
- **Error and Exception Handling:** Ensures seamless execution by handling errors in web scraping, email notifications, and configuration parsing.  
- **Time Complexity:**  
  - **Scraping rows:** **O(n)**, where `n` is the number of rows in the SEC filing table.  
  - **Email generation:** **O(m)**, where `m` is the number of filings retrieved.  
- **Space Complexity:**  
  - **Storage:** **O(n)**, proportional to the number of rows processed.  

## **Impact**

- **Proactive Risk Management:** Automates monitoring of SEC filings, enabling organizations to stay ahead of material cybersecurity incidents.  
- **Enhanced Incident Response:** Delivers timely insights into cybersecurity disclosures, helping stakeholders make faster and more informed decisions.  
- **Investor Confidence:** Assists investors in assessing potential stock impacts and the overall cybersecurity posture of U.S. public companies.  
- **Operational Efficiency:** Reduces manual monitoring efforts, improving efficiency and focusing resources on critical decision-making.  

## **Configuration Instructions**

1. **Update the Configuration File:**
   - Open the `configuration.json` file (included in the repository) and update the following placeholders with your details:
     - Replace `"your-email@example.com"` with your email address.
     - Replace `"recipient1@example.com"` with the recipient's email addresses.
     - Replace `"add-your-smtp-server-here"` with your SMTP server address.
     - Ensure the `"fetch_days"` value reflects how far back you want to retrieve SEC filings (default is 200 days).

2. **Install ChromeDriver:**
   Ensure **ChromeDriver** is installed and available in the same directory where the code runs.  
   Alternatively, use the `webdriver_manager` library (already integrated) for automatic downloads.

---
## **How to Run**

1. **Install Dependencies and Run the Script:**
   - Install the required libraries using pip:
     ```bash
     pip install selenium webdriver_manager
     ```
   - Execute the script in your terminal:
     ```bash
     python SEC-8K_Automation.py
     ```

2. **Email Alerts:**
   - Once executed, the tool will:
     - Fetch SEC-8K filings for Items 1.05 and 8.01.
     - Send email notifications to the configured recipients with the filing details.




