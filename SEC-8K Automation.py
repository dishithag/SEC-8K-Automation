import json
import smtplib
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import traceback


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SECFilingsScraper:
    def __init__(self, config_file, item_key):
        try:
            with open(config_file) as file:
                self.config = json.load(file)
        except Exception as e:
            logging.error("Failed to load configuration file.")
            raise

        self.results = []
        self.driver = None
        self.fetch_days = self.config.get("fetch_days", 200)
        self.search_url = self.config["search_urls"].get(item_key)
        if not self.search_url:
            raise ValueError(f"No URL found for item '{item_key}' in configuration.")

    def _initialize_driver(self):
        options = webdriver.ChromeOptions()
        if self.config.get("chrome_headless"):
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _construct_search_url(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.fetch_days)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        return f"{self.search_url}&startdt={start_date_str}&enddt={end_date_str}&forms=8-K"

    def scrape_filings(self):
        self._initialize_driver()
        search_url = self._construct_search_url()
        logging.info(f"Opening URL: {search_url}")
        self.driver.get(search_url)

        # Wait for the table to load
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody"))
        )

        # Extract all rows in the table
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        logging.info(f"Found {len(rows)} rows in the table.")
        
        for index, row in enumerate(rows):
            try:
                # Validate the row content by checking for expected elements
                form_file_element = row.find_element(By.CSS_SELECTOR, "td.filetype a")
                filing_date_element = row.find_element(By.CSS_SELECTOR, "td.filed")
                entity_name_element = row.find_element(By.CSS_SELECTOR, "td.entity-name")

                # Extract the relevant data
                form_file = form_file_element.text.strip()
                filing_url = (
                    "https://www.sec.gov"
                    + form_file_element.get_attribute("href")
                )
                filing_date = filing_date_element.text.strip()
                entity_name = entity_name_element.text.strip()

                # Append the valid filing to results
                self.results.append({
                    "Form & File": form_file,
                    "Entity Name": entity_name,
                    "Filing URL": filing_url,
                    "Filing Date": filing_date,
                })
            except Exception:
                # Skip rows that don't contain expected elements
                logging.warning(f"Skipping row {index + 1} due to missing elements or errors.")
                continue

        self.driver.quit()
        logging.info(f"Scraping completed with {len(self.results)} valid filings found.")
        return self.results


class EmailNotifier:
    def __init__(self, config):
        self.sender_email = config["sender_email"]
        self.recipient_emails = config["recipient_emails"]
        self.smtp_server = config["smtp_server"]

    def build_email_body(self, results, item_key):
        if not results:
            return None  # Return None if no results to avoid sending an email

        email_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; font-size: 18px;">
                <p>Dear User,</p>
                <p>Please find below the latest SEC filings for <strong>Item {item_key}</strong>:</p>
                <table style="border-collapse: collapse; width: 100%; font-size: 18px;">
                    <tr>
                        <th style="border: 1px solid black; padding: 12px; background-color: #f2f2f2;">Form & File</th>
                        <th style="border: 1px solid black; padding: 12px; background-color: #f2f2f2;">Company Name</th>
                        <th style="border: 1px solid black; padding: 12px; background-color: #f2f2f2;">Filing Date</th>
                    </tr>
        """
        for result in results:
            email_body += f"""
                    <tr>
                        <td style="border: 1px solid black; padding: 10px;">{result['Form & File']}</td>
                        <td style="border: 1px solid black; padding: 10px;">
                            <a href="{result['Filing URL']}" target="_blank" style="text-decoration: underline; color: blue;">
                                {result['Entity Name']}
                            </a>
                        </td>
                        <td style="border: 1px solid black; padding: 10px;">{result['Filing Date']}</td>
                    </tr>
            """
        email_body += """
                </table>
                <p style="margin-top: 25px; font-size: 18px;">Thank you.</p>
            </body>
        </html>
        """
        return email_body

    def send_email(self, email_body, item_key):
        if not email_body:
            logging.info(f"No filings found for Item {item_key}. Skipping email sending.")
            return

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"SEC Filing Alert for Item {item_key}"
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(self.recipient_emails)
            msg.add_header("X-Priority", "1")  # High-priority email header
            msg.attach(MIMEText(email_body, "html"))

            with smtplib.SMTP(self.smtp_server) as server:
                server.sendmail(self.sender_email, self.recipient_emails, msg.as_string())
                logging.info(f"Email sent successfully for Item {item_key}.")
        except Exception as e:
            logging.error(f"Failed to send email for Item {item_key}.")
            logging.error(traceback.format_exc())


# Main execution
if __name__ == "__main__":
    try:
        with open("configuration.json") as config_file:
            config = json.load(config_file)

        for item_key, search_url in config["search_urls"].items():
            scraper = SECFilingsScraper("configuration.json", item_key)
            filings = scraper.scrape_filings()

            notifier = EmailNotifier(config)
            email_body = notifier.build_email_body(filings, item_key)
            notifier.send_email(email_body, item_key)

    except Exception as e:
        logging.error("Critical error in the script.")
        logging.error(traceback.format_exc())
