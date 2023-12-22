import os
import time
import sys
import platform
import requests
import warnings
import socket
import subprocess
import ctypes
import wave
import threading
import pyaudio
import eyed3  # or mutagen for audio metadata
import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime, timedelta
from pydub import AudioSegment
from typing import Sequence, Any, Dict
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from tabulate import tabulate
from bs4 import BeautifulSoup
from pydub.playback import play



# Declare root as a global variable
root = None
ffmpeg_path = 'C:\\Users\\radut\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\ffmpeg'
AudioSegment.ffmpeg = ffmpeg_path
x_data = []
y_data_1 = []
y_data_2 = []
y_data_3 = []
audio_data = []
ax = None
root = None
logging.getLogger("pydub.converter").setLevel(logging.ERROR)


class IPAddress:
    def __init__(self, website_url):
        self.driver = None
        self.website_url = website_url
        self.website_ip = None
        self.website_name = None
        self.ipv4_address = None
        self.ipv6_address = None
        self.gateway_address = None
        self.api_endpoint = None

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_website_ip(self):
        try:
            self.website_ip = socket.gethostbyname(self.website_url)
            self.website_name = socket.gethostbyaddr(self.website_ip)[0]
            return self.website_ip
        except Exception as e:
            print(f"Error getting website IP address: {e}")
            return None


    def perform_combined_data_extraction(web_extractor, duration=30, file_path="data.txt"):
        image_extraction_times = []
        text_extraction_times = []
        method_extraction_times = []

        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=duration)

        while datetime.now() < end_time:
            try:
                # Extract images
                extraction_start_time = time.time()
                images_folder = f"Imagini_extrase_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                web_extractor.extract_images(images_folder)
                extraction_end_time = time.time()
                image_extraction_times.append(extraction_end_time - extraction_start_time)

                # Extract text
                extraction_start_time = time.time()
                text_data = web_extractor.extract_text()
                extraction_end_time = time.time()
                text_extraction_times.append(extraction_end_time - extraction_start_time)

                # Extract method
                extraction_start_time = time.time()
                extraction_method = web_extractor.extract_method()
                extraction_end_time = time.time()
                method_extraction_times.append(extraction_end_time - extraction_start_time)

                time.sleep(10)  # Simulated delay between extractions

            except Exception as e:
                print(f"Error occurred during extraction: {e}")
                break

        # Plotting the extraction duration after data extraction completes
        plot_data_extraction_chart(image_extraction_times, text_extraction_times, method_extraction_times)

        try:
            start_time = time.time()

            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
            print(f"Extracting data from {web_extractor.website_url} for {duration} seconds...")

            driver.get(web_extractor.website_url)
            time.sleep(duration)

            body_element = driver.find_element(By.XPATH, "//body")
            extracted_data = body_element.text

            with open(file_path, 'w') as file:
                file.write(extracted_data)

            elapsed_time = round(time.time() - start_time, 2)
            print(f"Data extraction completed in {elapsed_time} seconds. Data saved to {file_path}")

        except Exception as e:
            print(f"Error occurred during data extraction: {e}")

        finally:
            driver.quit()


    def extract_website_ip(self):
        try:
            parsed_uri = urlparse(self.website_url)
            domain = parsed_uri.netloc
            ip_address = socket.gethostbyname(domain)
            print(f"Website IP address for {domain}: {ip_address}")
            return ip_address
        except Exception as e:
            print(f"Error getting website IP address: {e}")
            return None


    def check_website_address(self, url):
        try:
            # Add scheme if missing (http:// or https://)
            if not url.startswith('http://') and not url.startswith('https://'):
                url = f'http://{url}'

            response = requests.head(url)
            if response.status_code == 200:
                print(f"Website address '{url}' is correct and active.")
                return True
            else:
                print(f"Website address '{url}' is incorrect or not active.")
                return False
        except requests.RequestException as e:
            print(f"Error occurred while checking website address: {e}")
            return False

    def extract_audio_metadata(file_path):
        # Example using eyed3
        audiofile = eyed3.load(file_path)
        return audiofile.tag.artist, audiofile.tag.title


    def get_ipv4_ipv6(self):
        try:
            self.ipv4_address = socket.gethostbyname(socket.gethostname())
            self.ipv6_address = [addrinfo[4][0] for addrinfo in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)]
        except Exception as e:
            print(f"Error getting IPv4 and IPv6 addresses: {e}")

    def get_gateway_address(self):
        try:
            if self.is_admin():
                result = subprocess.run('ipconfig', shell=True, capture_output=True)
                output = result.stdout.decode('utf-8')
                gateway_lines = [line for line in output.split('\n') if 'Default Gateway' in line]
                if gateway_lines:
                    gateway_address = gateway_lines[0].split(':')[-1].strip()
                    self.gateway_address = gateway_address
                    return gateway_address
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(f"Error getting gateway address: {e}")
            return None


    def check_firewall(self):
        try:
            if self.website_ip:
                response = requests.get(f"http://{self.website_ip}")
                if response.status_code == 200:
                    return True
                else:
                    return False
            else:
                return None
        except Exception as e:
            print(f"Error checking firewall: {e}")
            return None


    def find_api_endpoint(self):
        try:
            response = requests.get(self.website_url)
            if response.status_code == 200:
                website_content = response.text
                api_endpoint_candidates = [
                    "api.website.com",  # Example API endpoint pattern
                    "api/v1",           # Another example pattern
                    # Add more patterns that might indicate the API endpoint
                ]

                found_endpoints = []

                for candidate in api_endpoint_candidates:
                    if candidate in website_content:
                        self.api_endpoint = candidate
                        found_endpoints.append(candidate)

                if found_endpoints:
                    print("Potential API endpoints found:")
                    with open('api_endpoints.txt', 'w', encoding='utf-8') as file:
                        for endpoint in found_endpoints:
                            ip_address = socket.gethostbyname(endpoint)
                            print(f"Endpoint: {endpoint}, IP Address: {ip_address}")
                            file.write(f"Endpoint: {endpoint}, IP Address: {ip_address}\n")
                else:
                    print("No potential API endpoints found on the website.")
            else:
                print("Failed to retrieve website content.")
        except Exception as e:
            print(f"Error occurred while finding the API endpoint: {e}")


    def dns_resolution_check(self, hosts):
        self.dns = socket.gethostbyname(url)
        try:
            dns_server = '8.8.8.8'  # Using Google's DNS server as an example
            ip_addresses = []

            for host in hosts:
                response = requests.get(f"http://{dns_server}", headers={"Host": host})
                ip = socket.gethostbyname(host)
                ip_addresses.append([host, ip])

            if ip_addresses:
                headers = ["Host", "IP Address"]
                print(tabulate(ip_addresses, headers=headers))
                with open("dns_resolution.txt", "w", encoding="utf-8") as file:
                    file.write(tabulate(ip_addresses, headers=headers, tablefmt="plain"))
                print("DNS resolution check successful.")
            else:
                print("No IP addresses found.")
        except Exception as e:
            print(f"Error occurred during DNS resolution check: {e}")


    def get_website_ip_from_ping(self, url):
        try:
            # Initiating a ping request to get the IP address resolved from DNS
            ping_response = subprocess.Popen(['ping', url], stdout=subprocess.PIPE, shell=True)
            output, _ = ping_response.communicate()
            lines = output.decode('utf-8').splitlines()
            for line in lines:
                if 'Pinging' in line:
                    # Extracting IP address from the output of ping command
                    ip_address = line.split()[-1].strip('()')
                    print(f"IP address resolved from DNS: {ip_address}")
                    return ip_address
            print("Failed to extract IP address from ping response.")
            return None
        except Exception as e:
            print(f"Error occurred during ping request: {e}")
            return None


    def get_head_section_details(self):
        try:
            head_details = []
            self.driver.find_elements
            while True:
                # Extract details from the head section
                head_element = self.driver.find_element(By.XPATH, "//head")
                head_details.append(self.extract_element_data(head_element))
                # Write head details to a file (append mode)
                with open('head_details.txt', 'a+') as file:
                    file.write(str(head_details[-1]) + '\n')

        except Exception as e:
            print(f"Error occurred while getting head section details: {e}")
            head_details = []  # Reset to empty list in case of an error
        finally:
            self.head_section_details = head_details


    def get_headers(self):
        try:
            self.driver.get(self.website_url)
            # Maximum number of attempts to get the XPath
            attempts = 3
            self.driver.find_elements
            for _ in tqdm(range(attempts), desc="Fetching XPath"):
                self.xpath = self.get_xpath()
                if self.xpath:
                    # Print obtained XPath for debugging
                    print(f"Obtained XPath: {self.xpath}")
                    body_element = self.driver.find_element(By.XPATH, self.xpath)
                    if body_element:
                        elements = self.driver.find_elements(By.XPATH, self.xpath)
                        headers = [element.tag_name for element in elements if element.tag_name]
                        if not headers:
                            raise ValueError("Empty headers, extraction failed")
                        break
                    else:
                        raise ValueError("Empty data, headers extraction failed")
                else:
                    print("Getting XPath failed. Retrying...")
                    self.driver.refresh()  # Refresh the page to try again
                    time.sleep(2)  # Wait for 2 seconds before retrying
        except Exception as e:
            print(f"Error occurred during headers extraction: {e}")
            headers = []
        finally:
            self.headers = headers
            # Close the driver and print message about the session's closure
            # Assuming you have a method to close the driver
            self.close_driver()
            print("Connection has been closed successfully. Session closed.")


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

class WebDataExtractor:
    def __init__(self, website_url=None):
        start_time = time.time()
        self.website_url = website_url
        self.driver = None
        self.action_times = {}
        self.initialize_driver()  # Initialize driver upon object creation
        self.xpath = None  # Initialize xpath attribute
        self.collected_data = []  # Initialize collected_data attribute
        self.audio_directory = 'audio'
        self.video_directory = 'videos'
        os.makedirs(self.audio_directory, exist_ok=True)
        os.makedirs(self.video_directory, exist_ok=True)
        # Check for ffmpeg or avconv
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                from pydub import AudioSegment
                AudioSegment.ffmpeg
            except RuntimeWarning as warning:
                raise ValueError("Error: ffmpeg or avconv not found. Data extraction might be affected.") from warning


    # Add a method to use plot_audio_data inside the class
    def visualize_sound_files(self, sound_files, horizontal=True, **kwargs):
        fig, axs = plot_audio_data(sound_files, horizontal=horizontal, **kwargs)
        plt.show()  # Show the plot (you can modify this behavior as needed)
        return fig, axs


    def initialize_driver(self):
        try:
            start_time = time.time()
            chrome_options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=chrome_options)
            elapsed_time = round(time.time() - start_time, 2)
            self.action_times['initialize_driver'] = elapsed_time
            print(f"Driver initialized successfully in {elapsed_time} seconds.")
        except WebDriverException as e:
            print(f"Error initializing the driver: {e}")


    def close_driver(self):
        try:
            if self.driver:
                self.driver.quit()
                print("Driver closed successfully.")
        except Exception as e:
            print(f"Error occurred while closing the driver: {e}")

    def get_xpath(self):
        start_time = time.time()
        # This method attempts to fetch the XPath of the body element using JavaScript
        return self.driver.execute_script(
            'function getPathTo(element) { \
                if (element.tagName === "HTML") \
                    return "/HTML[1]"; \
                if (element === document.body) \
                    return "/HTML[1]/BODY[1]"; \
                let ix = 0; \
                let siblings = element.parentNode.childNodes; \
                for (let i = 0; i < siblings.length; i++) { \
                    let sibling = siblings[i]; \
                    if (sibling === element) \
                        return (getPathTo(element.parentNode) + \
                            "/" + element.tagName + "[" + (ix + 1) + "]"); \
                    if (sibling.nodeType === 1 && \
                        sibling.tagName === element.tagName) \
                            ix++; \
                } \
            } \
            return getPathTo(arguments[0]);',
            self.driver.find_element(By.XPATH, "//body//*")
        )
        return self.xpath

    def extract_text(self):
        try:
            start_time = time.time()
            response = requests.get(self.website_url)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                extracted_text = soup.get_text()
                elapsed_time = round(time.time() - start_time, 2)
                self.action_times['extract_text'].append(elapsed_time)  # Append elapsed time to the list
                return extracted_text
            else:
                print("Failed to retrieve website content.")
        except Exception as e:
            print(f"Error occurred while extracting text: {e}")
        return None

    def save_links(self, file_path):
        try:
            start_time = time.time()
            if not hasattr(self, 'website_url') or not self.website_url:
                raise ValueError("Website URL is not defined or is empty.")

            response = requests.get(self.website_url)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                link_tags = soup.find_all('a')
                links = [link.get('href') for link in link_tags if link.get('href')]

                with open(file_path, 'w') as file:
                    file.write("\n".join(links))

                print(f"All links saved to {file_path}")
                elapsed_time = round(time.time() - start_time, 2)
                self.action_times['save_links'].append(elapsed_time)  # Append elapsed time to the list
            else:
                print("Failed to retrieve website content.")
        except Exception as e:
            print(f"Error occurred while extracting links: {e}")


    def plot_time_series(self):
        plt.figure(figsize=(10, 6))
        for action, times in self.action_times.items():
            plt.plot(times, label=action)
            plt.xlabel('Time taken (seconds)')
            plt.ylabel('Iteration')
            plt.title('Time Series of Function Durations')
            plt.legend()
            plt.grid(True)
            plt.show()


    def save_to_text_file(self, data):
        file_path = 'extracted_data.txt'
        with open(file_path, 'a') as file:
            file.write(data + '\n')

    def download_images(self, folder_path):
        try:
            start_time = time.time()
            response = requests.get(self.website_url)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                img_tags = soup.find_all('img')
                img_urls = [img['src'] for img in img_tags if img.get('src')]

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                count = 0
                for idx, img_url in enumerate(img_urls):
                    if count >= 10:  # Adjust this number to the desired maximum number of images to download
                        break

                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img_name = f'image_{idx}.jpg'
                        img_path = os.path.join(folder_path, img_name)
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_response.content)
                        print(f"Image {idx + 1} saved: {img_path}")
                        count += 1
                    else:
                        print(f"Failed to download image {idx + 1}")

                if count < 10:  # If fewer than 10 images are found on the page, print the actual count
                    print(f"Downloaded only {count} images.")
            else:
                print("Failed to retrieve website content.")
        except Exception as e:
            print(f"Error occurred while extracting images: {e}")

    def extract_images(self, folder_path):
        try:
            start_time = time.time()
            if self.driver:
                self.driver.get(self.website_url)

                # Collect image elements
                image_elements = self.driver.find_elements(By.TAG_NAME, 'img')  # Use By.TAG_NAME here
                if image_elements:
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    count = 0
                    for idx, img_element in enumerate(image_elements):
                        img_url = img_element.get_attribute('src')
                        if img_url:
                            img_response = requests.get(img_url)
                            if img_response.status_code == 200:
                                img_name = f'image_{idx}.jpg'  # Modify the naming scheme as needed
                                img_path = os.path.join(folder_path, img_name)
                                with open(img_path, 'wb') as img_file:
                                    img_file.write(img_response.content)
                                print(f"Image {idx + 1} saved: {img_path}")
                                count += 1
                            else:
                                print(f"Failed to download image {idx + 1}")

                    print(f"Extracted {count} images.")
                else:
                    print("No image elements found on the website.")
            else:
                print("Driver initialization failed. Image extraction aborted.")
        except Exception as e:
            print(f"Error occurred while extracting images: {e}")
        finally:
            self.close_driver()

    def check_ffmpeg_avconv():
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print("FFmpeg found and accessible.")
        except FileNotFoundError:
            try:
                subprocess.run(["avconv", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                print("avconv found and accessible.")
            except FileNotFoundError:
                raise FileNotFoundError("FFmpeg or avconv not found. Install either FFmpeg or avconv and ensure it is in the system PATH.")


    def save_file(url, directory):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = os.path.join(directory, os.path.basename(url))
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                return file_name
            else:
                return None
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None



    def extract_audio(self, element):
        audio_url = element.get_attribute("src")
        if audio_url.lower().endswith('.mp3'):
            saved_file = save_file(audio_url, self.audio_directory)
            if saved_file:
                return saved_file
        return None

    def extract_video(self, element):
        video_url = element.get_attribute("src")
        if video_url.lower().endswith('.mp4'):
            saved_file = save_file(video_url, self.video_directory)
            if saved_file:
                return saved_file
        return None

    def close_driver(self):
        try:
            start_time = time.time()
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Error closing the driver: {e}")


    def extract_styles(self):
        try:
            start_time = time.time()
            if self.driver:
                self.driver.get(self.website_url)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                js_styles = self.driver.execute_script('''
                    var elements = document.querySelectorAll('*');
                    var styles = [];
                    elements.forEach(function(element) {
                        var computedStyles = window.getComputedStyle(element);
                        var elementStyles = {
                            "element": element.tagName.toLowerCase(),
                            "styles": computedStyles.cssText
                        };
                        styles.push(elementStyles);
                    });
                    return styles;
                ''')

                js_styles_file_path = 'js_styles.txt'
                with open(js_styles_file_path, 'w') as file:
                    for style in js_styles:
                        file.write(str(style) + '\n')

                print(f"JavaScript styles associated with HTML elements saved to {js_styles_file_path}")
            else:
                print("Driver initialization failed. Styles extraction aborted.")
        except Exception as e:
            print(f"Error occurred while extracting styles: {e}")

    def write_to_file(self, data, file_path):
        try:
            start_time = time.time()
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

                elapsed_time = round(time.time() - start_time, 2)
                print(f"Data successfully saved to {file_path} in {elapsed_time} seconds.")
        except Exception as e:
            print(f"Error occurred while writing data to file: {e}")
            print(f"Data saving to {file_path} failed.")


    def get_user_input(self):
        try:
            start_time = time.time()
            website_url = input("Enter the website address: ")
            file_path = input("Enter the file path to save the data: ")
            duration = int(input("Enter the duration of the script (in seconds): "))
            xpath = input("Enter the XPath of the website: ")
            elapsed_time = round(time.time() - start_time, 2)
            print(f"User input captured in {elapsed_time} seconds.")
            return website_url, file_path, duration, xpath
        except Exception as e:
            print(f"Error occurred during user input: {e}")
            return None, None, None, duration

    def run_extraction(self, website_ip, duration, file_path):
        try:
            start_time = time.time()
            print(f"Extracting data from {website_ip} for {duration} seconds...")

            # Your extraction logic here
            # Placeholder code; replace with your actual extraction process
            extracted_data = self.perform_extraction(duration)  # Perform the actual data extraction

            # Save the extracted data to the specified file path
            with open(file_path, 'w') as file:
                file.write(extracted_data)

            elapsed_time = round(time.time() - start_time, 2)
            print(f"Data extraction completed in {elapsed_time} seconds. Saved to {file_path}")
        except Exception as e:
            print(f"Error occurred during data extraction: {e}")


    def perform_extraction(self, driver):
        try:
            start_time = time.time()

            text_elements = driver.find_elements(By.XPATH, "//your_text_element_xpath")
            text_data = [self.extract_text(elem) for elem in text_elements]

            link_elements = driver.find_elements(By.XPATH, "//your_link_element_xpath")
            link_data = [self.extract_links(elem) for elem in link_elements]

            image_elements = driver.find_elements(By.XPATH, "//your_image_element_xpath")
            image_data = [self.extract_images(elem) for elem in image_elements if self.extract_images(elem) is not None]

            data_mapping = {
                'text': text_data,
                'links': link_data,
                'images': image_data
            }

            elapsed_time = round(time.time() - start_time, 2)
            print(f"Extraction completed in {elapsed_time} seconds")

            # Generate chart based on data mapping
            self.generate_data_mapping_chart(data_mapping)

            return data_mapping
        except Exception as e:
            print(f"Error occurred during data extraction: {e}")
            return None


    def plot_in_thread():
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.after(100, update_plot)  # Update the plot in the main thread after some time
            root.mainloop()
        except RuntimeError:
            # Handle the RuntimeError, switch to a backup method using Matplotlib's backend directly
            plt.figure(figsize=(6, 4))
            plt.plot([1, 2, 3], [4, 5, 6])  # Your plotting logic here
            plt.show()

    def generate_data_mapping_chart(self, data_mapping):
        # Create a chart to represent the data mapping
        categories = list(data_mapping.keys())
        counts = [len(data) for data in data_mapping.values()]

        plt.figure(figsize=(8, 6))
        plt.bar(categories, counts, color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Count')
        plt.title('Data Mapping Chart')
        plt.grid(axis='y')
        plt.tight_layout()

        # Save the plot as an image or show it
        plt.savefig('data_mapping_chart.png')  # Save as an image
        # Show plot
        plt.show()

    def generate_extraction_duration_plot(self, function_names, execution_times):
        # Create a time series for each function execution
        timestamps = [datetime.now() + timedelta(seconds=i) for i in range(len(execution_times[0]))]

        plt.figure(figsize=(12, 10))

        # Plot data as a line
        plt.subplot(2, 1, 1)  # Top subplot for the line plot
        for idx, func_name in enumerate(function_names):
            plt.plot(timestamps, execution_times[idx], marker='o', linestyle='-', label=func_name)

        plt.title('Function Execution Duration Over Time (Time Series)')
        plt.xlabel('Time')
        plt.ylabel('Execution Duration (seconds)')
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.gca().margins(x=0)
        plt.gca().fmt_xdata = lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S")

        # Plot data as a bar stack
        plt.subplot(2, 1, 2)  # Bottom subplot for the bar plot
        for idx, func_name in enumerate(function_names):
            plt.bar(timestamps, execution_times[idx], label=func_name)

            # Add text labels with values on top of bars
            for i, v in enumerate(execution_times[idx]):
                plt.text(timestamps[i], v + 0.1, str(v), ha='center')

        plt.title('Function Execution Duration Over Time (Bar Stacks)')
        plt.xlabel('Time')
        plt.ylabel('Execution Duration (seconds)')
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.gca().margins(x=0)
        plt.gca().fmt_xdata = lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S")

        plt.show()


    def perform_extraction(self, driver):
            try:
                start_time = time.time()

                text_elements = driver.find_elements(By.XPATH, "//your_text_element_xpath")
                text_data = [self.extract_text(elem) for elem in text_elements]

                link_elements = driver.find_elements(By.XPATH, "//your_link_element_xpath")
                link_data = [self.extract_links(elem) for elem in link_elements]

                image_elements = driver.find_elements(By.XPATH, "//your_image_element_xpath")
                image_data = [self.extract_images(elem) for elem in image_elements if self.extract_images(elem) is not None]

                # Locate figure elements
                figure_elements = driver.find_elements(By.XPATH, "//your_figure_element_xpath")
                figure_data = [self.extract_figures(elem) for elem in figure_elements if self.extract_figures(elem) is not None]

                # Locate audio elements (MP3 files)
                audio_elements = driver.find_elements(By.XPATH, "//your_audio_element_xpath")
                audio_data = [self.extract_audio(elem) for elem in audio_elements if self.extract_audio(elem) is not None]

                # Locate video elements (MP4 files)
                video_elements = driver.find_elements(By.XPATH, "//your_video_element_xpath")
                video_data = [self.extract_video(elem) for elem in video_elements if self.extract_video(elem) is not None]

                data_mapping = {
                    'text': text_data,
                    'links': link_data,
                    'images': image_data,
                    'figures': figure_data,
                    'audio': audio_data,
                    'video': video_data
                }

                elapsed_time = round(time.time() - start_time, 2)
                print(f"Extraction completed in {elapsed_time} seconds")

                # Generate chart based on data mapping
                self.generate_data_mapping_chart(data_mapping)

            except Exception as e:
                print(f"Error occurred during extraction: {e}")





    def extract_media_queries(self, website_url, file_path):
        try:
            start_time = time.time()
            # Fetch the website content
            response = requests.get(website_url)
            if response.status_code == 200:
                html_content = response.text

                # Parse HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find all style tags containing media queries
                style_tags = soup.find_all('style')
                media_queries_content = []

                for style_tag in style_tags:
                    style_text = style_tag.get_text()
                    if '@media' in style_text:
                        media_queries_content.append(style_text)

                if media_queries_content:
                    # Save media queries to a file
                    with open(file_path, 'w') as file:
                        file.write("\n\n".join(media_queries_content))

                    elapsed_time = round(time.time() - start_time, 2)
                    print(f"Media queries structure saved to {file_path} in {elapsed_time} seconds")
                else:
                    print("No media queries found on the website.")
            else:
                print("Failed to retrieve website content.")
        except Exception as e:
            print(f"Error occurred while extracting media queries: {e}")

    def extract_body_data(self):
        try:
            start_time = time.time()
            elapsed_time = 0

            headers = self.get_headers()
            if headers:
                headers.insert(0, "Tag Name")  # Adding "Tag Name" as the first header
                self.write_to_file([headers], 'data.txt')  # Writing headers to file

                while elapsed_time < 60:
                    self.driver.refresh()
                    self.xpath = self.get_xpath()
                    body_element = self.driver.find_element(By.XPATH, self.xpath)
                    if body_element:
                        print("Data extracted from the body section successfully")
                        elements = self.driver.find_elements(By.XPATH, self.xpath)
                        element_details = [self.extract_element_data(element) for element in elements]
                        self.write_to_file(element_details, 'data.txt')
                    else:
                        raise ValueError("Empty data, extraction failed")
                    time.sleep(2)  # Pause for 2 seconds
                    print("Data extraction successful.")
                    elapsed_time = round(time.time() - start_time, 2)

                if elapsed_time >= 60:
                    print("Extraction time limit reached.")
            else:
                raise ValueError("Empty headers, extraction failed")
        except Exception as e:
            print(f"Error occurred: {e}")


    def extract_data(self, duration, file_path):
        try:
            start_time = time.time()
            end_time = start_time + duration

            print(f"Extracting data from {self.website_ip} for {duration} seconds...")

            while time.time() < end_time:
                # Your data extraction logic goes here using self.driver
                # Example: Scraping data from the website using self.driver.get(...)
                self.driver.get(f"http://{self.website_ip}")
                body_element = self.driver.find_element(By.XPATH, "//body")
                extracted_data = body_element.text

                # Save the extracted data to the file
                with open(file_path, 'w') as file:
                    file.write(extracted_data)

                print(f"Data saved to {file_path}")
                time.sleep(2)  # Wait for 2 seconds before re-extracting (adjust as needed)

            print("Extraction completed.")
        except Exception as e:
            print(f"Error occurred during data extraction: {e}")
        finally:
            # Close the driver after extraction
            self.close_driver()




    def extract_method(self):
        # Simulated code for extracting method details
        extraction_method = "Sample extraction method used"
        print("Extraction method:", extraction_method)
        return extraction_method

    def plot_data_extraction_chart(image_extraction_times, text_extraction_times, method_extraction_times):
        # Create traces for different extractions
        image_trace = go.Scatter(
            x=list(range(len(image_extraction_times))),
            y=image_extraction_times,
            mode='lines+markers',
            name='Image Extraction'
        )

        text_trace = go.Scatter(
            x=list(range(len(text_extraction_times))),
            y=text_extraction_times,
            mode='lines+markers',
            name='Text Extraction'
        )

        method_trace = go.Scatter(
            x=list(range(len(method_extraction_times))),
            y=method_extraction_times,
            mode='lines+markers',
            name='Method Extraction'
        )

        # Create layout for the chart
        layout = go.Layout(
            title='Data Extraction Duration Over Time',
            xaxis=dict(title='Extraction Iterations'),
            yaxis=dict(title='Time (seconds)'),
            hovermode='closest'
        )

        # Combine traces and layout into a figure
        fig = go.Figure(data=[image_trace, text_trace, method_trace], layout=layout)

        # Show the interactive plot
        fig.show()

    # Function to capture audio data from the microphone
    def capture_audio(WAVE_OUTPUT_FILENAME="output.wav", MP3_OUTPUT_FILENAME="output.mp3"):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5  # Adjust the duration as needed

        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save audio to a WAV file
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # Convert WAV to MP3 using pydub
        sound = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
        sound.export(MP3_OUTPUT_FILENAME, format="mp3")

        # Optionally, read the MP3 file to get decoded data
        # audio_data, _ = sf.read(MP3_OUTPUT_FILENAME)

        # Return the filenames of the created audio files
        return WAVE_OUTPUT_FILENAME, MP3_OUTPUT_FILENAME


    # Function to update plot in real-time
    def update_plot_data(ax, x_data, y_data_1, y_data_2, y_data_3, audio_data):
        # Update data for the plot (replace with actual extracted data)
        x_data.append(time.time())
        y_data_1.append(10)  # Replace 10 with extracted value 1
        y_data_2.append(20)  # Replace 20 with extracted value 2
        y_data_3.append(15)  # Replace 15 with extracted value 3

        # Update the audio plot
        audio_frames = capture_audio()
        audio_data.extend(audio_frames)

        ax.clear()  # Clear the existing plot
        ax.plot(x_data, y_data_1, linestyle='--', label='Data 1', color='blue')
        ax.plot(x_data, y_data_2, linestyle='--', label='Data 2', color='orange')
        ax.plot(x_data, y_data_3, linestyle='--', label='Data 3', color='green')

        # Plot audio data
        ax.specgram(audio_data, Fs=44100, cmap='viridis')

        ax.legend()
        ax.figure.canvas.draw()

        # Example usage
        root = tk.Tk()  # Create the root window
        sound_files = [('sound1', 10), ('sound2', 15), ('sound3', 5), ('sound4', 20)]  # Example sound_files

        # Pass 'root' to the functions that require it
        fig, axs = plot_audio_data(sound_files, root, horizontal=True, width_ratios=[1, 2, 1], subplot_kw={'projection': 'polar'})
        update_plot_data(root)
        root.mainloop()


    def update_plot():
        global x_data, y_data_1, y_data_2, y_data_3, audio_data, ax, root

        # Simulate data extraction
        data_1, data_2, data_3, audio_frames = simulate_web_scraping()

        # Update data for the plot with extracted data
        x_data.extend([time.time() + i for i in range(len(data_1))])
        y_data_1.extend(data_1)
        y_data_2.extend(data_2)
        y_data_3.extend(data_3)

        # Update the line plots (Data 1, Data 2, Data 3)
        ax.plot(x_data[-len(data_1):], y_data_1[-len(data_1):], linestyle='--', label='Data 1', color='blue')
        ax.plot(x_data[-len(data_2):], y_data_2[-len(data_2):], linestyle='--', label='Data 2', color='orange')
        ax.plot(x_data[-len(data_3):], y_data_3[-len(data_3):], linestyle='--', label='Data 3', color='green')

        # Clear the existing audio specgram plot
        clear_audio_plot(ax)

        # Update and plot audio data (specgram)
        audio_data.extend(audio_frames)
        plot_audio_specgram(ax, audio_data)

        ax.legend()
        ax.figure.canvas.draw()

        # Schedule the next plot update after 1000ms (1 second)
        root.after(1000, update_plot)

    def clear_audio_plot(ax):
        # Clear the existing audio specgram plot
        for artist in ax.get_children():
            if isinstance(artist, matplotlib.image.AxesImage):
                artist.remove()

    def plot_audio_specgram(ax, audio_data):
        # Plot audio data (specgram)
        ax.specgram(audio_data, Fs=44100, cmap='viridis')



    def update_plot_thread():
        global root
        root = tk.Tk()
        root.title('Real-time Data Extraction')
        root.geometry('800x600')

        fig, ax = plt.subplots(figsize=(8, 4))
        canvas = fig.canvas
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        ax.set_title('Real-time Data Extraction')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.grid(True)

        x_data = []
        y_data_1 = []
        y_data_2 = []
        y_data_3 = []
        audio_data = []

    def update_plot():
        global x_data, y_data_1, y_data_2, y_data_3, audio_data, ax
        while True:
            # Update the plot with the extracted data in real-time
            ax.clear()  # Clear the existing plot

            # Your web scraping code to extract data from a website here
            # Replace this with your actual web scraping logic
            new_data = perform_extraction()

            # Update the data
            x_data.append(time.time())  # Replace with your x-axis data
            y_data_1.append(new_data[0])  # Replace with your extracted value 1
            y_data_2.append(new_data[1])  # Replace with your extracted value 2
            y_data_3.append(new_data[2])  # Replace with your extracted value 3

            # Update the plot with the extracted data
            ax.plot(x_data, y_data_1, linestyle='--', label='Data 1', color='blue')
            ax.plot(x_data, y_data_2, linestyle='--', label='Data 2', color='orange')
            ax.plot(x_data, y_data_3, linestyle='--', label='Data 3', color='green')

            ax.legend()
            ax.figure.canvas.draw()

            time.sleep(2)  # Sleep for a while before updating again


    def simulate_web_scraping():
        # Simulate extracting data from a website (here generating random data)
        data_1 = np.random.randint(10, 30, size=10)
        data_2 = np.random.randint(20, 40, size=10)
        data_3 = np.random.randint(15, 35, size=10)
        audio_frames = np.random.randn(44100 * 3)  # Generating random audio frames (3 seconds)

        return data_1, data_2, data_3, audio_frames



    def update_plot_data(ax, x_data, y_data_1, y_data_2, y_data_3, audio_data):
        # Simulate data extraction
        data_1, data_2, data_3, audio_frames = simulate_web_scraping()

        # Update data for the plot with extracted data
        x_data.extend([time.time() + i for i in range(len(data_1))])
        y_data_1.extend(data_1)
        y_data_2.extend(data_2)
        y_data_3.extend(data_3)

        # Update the audio plot
        audio_data.extend(audio_frames)

        ax.clear()  # Clear the existing plot
        ax.plot(x_data, y_data_1, linestyle='--', label='Data 1', color='blue')
        ax.plot(x_data, y_data_2, linestyle='--', label='Data 2', color='orange')
        ax.plot(x_data, y_data_3, linestyle='--', label='Data 3', color='green')

        # Plot audio data
        ax.specgram(audio_data, Fs=44100, cmap='viridis')

        ax.legend()
        ax.figure.canvas.draw()

    def plot_audio_data(sound_files,
                        horizontal: bool = False,
                        **kwargs) -> tuple[plt.Figure, Any]:
        fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True, **kwargs)

        # Remove the plotting commands
        axs[0].set_title('Bar Chart')
        axs[1].set_title('Scatter Plot')
        axs[2].set_title('Line Plot')

        plt.suptitle('Categorical Plotting of Sound Files')
        plt.tight_layout()

        return fig, axs

    # Example: Scan audio files using os.walk


    def scan_audio_files(directory):
        audio_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.ogg')):  # Adjust file extensions as needed
                    audio_files.append(os.path.join(root, file))
        return audio_files

    # Scan audio files in a directory and store their data
    audio_directory = 'P:\\Project Python\\Online Store\\venv\\Sound files for script\\DECompleted.mp3'  # Replace with the actual directory path
    audio_files = scan_audio_files(audio_directory)

    # Use extracted audio files to plot data
    # For example, let's create a list of tuples with some placeholder data
    sound_files = [('sound1', 10), ('sound2', 15), ('sound3', 5), ('sound4', 20)]  # Replace with actual data

    # Create horizontal plots of the extracted data
    fig, axs = plot_audio_data(sound_files, horizontal=True, width_ratios=[1, 2, 1], subplot_kw={'projection': 'polar'})
    plt.show()


    def main_extraction_process(self):
        # Simulate extraction actions and gather time durations
        action_times = {}

        # Example of data extraction actions with time durations
        for i in range(1, 4):
            start_time = time.time()
            # Your data extraction logic here, e.g., scraping data from a website
            # Simulate an action taking some time
            time.sleep(2)
            end_time = time.time()

            # Record the time duration for the action
            action_name = f"Extraction {i}"
            duration = end_time - start_time
            action_times[action_name] = duration

            print(f"Action '{action_name}' took {duration:.2f} seconds.")

        # Save the extracted data to a text file
        self.save_to_text_file("Example extracted data")

        # Set the action times in the class attribute
        self.action_times = action_times

    def extract_from_autovit(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Your scraping logic here to extract data from Autovit website
            # Example: Extract title, price, description, images, etc.
            title = soup.find('h1', class_='offer-title').text.strip()
            price = soup.find('span', class_='offer-price__number').text.strip()
            description = soup.find('div', class_='offer-description').text.strip()
            images = [img['src'] for img in soup.find_all('img', class_='gallery-indicator__img')]
            # Process the extracted data as needed

            # Print extracted data as an example
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Description: {description}")
            print(f"Images: {images}")

# Usage:
if __name__ == "__main__":
    website_url = 'https://www.autovit.ro/autoturisme/anunt/'

    web_extractor = WebDataExtractor(website_url)  # Pass the website URL to the constructor
    web_extractor.extract_images(folder_path='P:\\Project Python\\Online Store\\venv')  # Extract website IP address
    web_extractor.main_extraction_process()  # Perform main extraction process
    web_extractor.website_url
    web_extractor.perform_extraction()
    web_extractor.extract_text()
    web_extractor.save_links('P:\\Project Python\\Online Store\\')
    web_extractor.simulate_web_scraping()
