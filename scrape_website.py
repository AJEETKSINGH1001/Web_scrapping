import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve


# Function to scrape the website and save data to CSV
def scrape_website(url, output_directory, csv_filename):
    # Sending a GET request to the URL
    response = requests.get(url)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting text
        texts = [p.get_text(strip=True) for p in soup.find_all('p')]

        # Extracting image links
        image_links = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]

        # Extracting anchor links
        anchor_links = [a['href'] for a in soup.find_all('a', href=True)]

        # Writing data to CSV
        csv_path = os.path.join(output_directory, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Text', 'Image Link', 'Anchor Link'])
            writer.writerows(zip(texts, image_links, anchor_links))

        print(f"Scraped data saved to {csv_path} successfully.")

        # Downloading images
        download_images(image_links, output_directory)

    else:
        print("Failed to retrieve the webpage.")


# Function to download images
def download_images(image_links, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for img_link in image_links:
        try:
            img_name = os.path.basename(urlparse(img_link).path)
            img_path = os.path.join(output_directory, img_name)
            urlretrieve(img_link, img_path)
            print(f"Downloaded image: {img_path}")
        except Exception as e:
            print(f"Failed to download image: {img_link}")
            print(e)


# Main function
def main():
    # URL of the website you want to scrape
    url_to_scrape = input("Enter the URL of the website you want to scrape: ")
    # Output directory to save images
    output_directory = input("Enter the directory to save the images: ")
    # CSV filename to save the data
    csv_filename = input("Enter the filename to save the scraped data (e.g., scraped_data.csv): ")

    # Call the function to scrape the website and save data to CSV
    scrape_website(url_to_scrape, output_directory, csv_filename)

    print("Process completed.")


# Entry point of the script
if __name__ == "__main__":
    main()
