import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from tabulate import tabulate
import platform
import sys

class WebDataExtractor:
    def __init__(self, website_url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Exclude logging
        chrome_options.add_argument("--remote-debugging-port=0")  # Disable DevTools
        self.website_url = website_url
        self.driver = webdriver.Chrome(options=chrome_options)
        self.action_times = {}
        self.collected_data = []
        self.xpath = None

    def get_xpath(self):
        # This method attempts to fetch the XPath of the body element using JavaScript
        return self.driver.execute_script(
            'function getPathTo(element) {\
                if (element.tagName === "HTML")\
                    return "/HTML[1]";\
                if (element === document.body)\
                    return "/HTML[1]/BODY[1]";\
                let ix = 0;\
                let siblings = element.parentNode.childNodes;\
                for (let i = 0; i < siblings.length; i++) {\
                    let sibling = siblings[i];\
                    if (sibling === element)\
                        return (getPathTo(element.parentNode) +\
                            "/" + element.tagName + "[" + (ix + 1) + "]");\
                    if (sibling.nodeType === 1 &&\
                        sibling.tagName === element.tagName)\
                            ix++;\
                }\
            }\
            return getPathTo(arguments[0]);',
            self.driver.find_element(By.XPATH, "//body//*")
        )

    def extract_element_data(self, element):
        try:
            # Extract element tag, classes, and styles
            element_data = []
            element_data.append(element.tag_name)
            element_data.append(element.get_attribute("class"))
            element_data.append(element.get_attribute("style"))
            return element_data
        except Exception as e:
            print(f"Error occurred during element data extraction: {e}")
            return []

    def extract_body_data(self):
        try:
            self.driver.get(self.website_url)
            start_time = time.time()
            # Or any duration you wish
            while time.time() - start_time < 60:
                self.driver.refresh()
                self.xpath = self.get_xpath()
                body_element = self.driver.find_element(By.XPATH, self.xpath)
                if body_element:
                    print("Data extracted from the body section successfully")
                    elements = self.driver.find_elements(By.XPATH, self.xpath)
                    element_details = []
                    for element in elements:
                        element_data = self.extract_element_data(element)
                        element_details.append(element_data)
                    self.write_to_file(element_details, 'data.txt')
                else:
                    raise ValueError("Empty data, extraction failed")
                time.sleep(2)  # Pause for 2 seconds
                print("Data extraction successful.")
        except Exception as e:
            print(f"Error occurred: {e}")

    def write_to_file(self, data, file_path):
        try:
            headers = ["Tag Name", "Classes", "Styles", "Div", 'Selectors', "Containers", "Container", "ID", "Body", ".div", "div"]
            formatted_data = [headers] + data

            # Writing action times and data in a tabular format
            with open(file_path, 'a+') as file:
                # Writing action times
                file.write("Action Times:\n")
                for action, action_time in self.action_times.items():
                    file.write(f"{action}: {action_time} seconds\n")
                file.write("\n")

                # Writing data in a tabular format
                table = tabulate(formatted_data, tablefmt="plain")
                file.write(table)
                file.write("\n\n")
                self.collected_data.extend(formatted_data)

                print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while writing data to file: {e}")

    def run_extraction(self, duration, file_path):
        try:
            # Extract data initially
            self.extract_body_data()
            # Define start_time here
            start_time = time.time()

            while time.time() - start_time < duration:
                body_element = self.driver.find_element(By.XPATH, self.xpath)
                if body_element:
                    print("Data extracted from the body section successfully")
                    elements = self.driver.find_elements(By.XPATH, self.xpath)
                    element_details = []
                    for element in elements:
                        element_data = self.extract_element_data(element)
                        element_details.append(element_data)
                    self.write_to_file(element_details, file_path)
                else:
                    raise ValueError("Empty data, extraction failed")
                time.sleep(2)  # Pause for 2 seconds
            print(f"Extraction completed. Data saved to {file_path}")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # Updated to include duration and XPath
    if len(sys.argv) >= 3:
        website_url = sys.argv[1]
        file_path = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else None

        extractor = WebDataExtractor(website_url)
        extractor.run_extraction(duration, file_path)
    else:
        print("Please provide website_url, file_path, and duration arguments.")
