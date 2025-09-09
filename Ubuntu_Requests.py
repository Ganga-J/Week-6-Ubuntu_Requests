import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename(url, content_type=None):
    """
    Extracts filename from URL or generates one.
    If no filename, it tries to use the content-type to get an extension.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        # Generate a unique name if no filename is in the URL path
        filename = hashlib.md5(url.encode()).hexdigest()
        if content_type and '/' in content_type:
            ext = content_type.split('/')[-1]
            filename += f".{ext}"
        else:
            filename += ".jpg" # Default to jpg
            
    return filename

def download_image(url, downloaded_hashes):
    """
    Downloads a single image, handles errors, and checks for duplicates.
    """
    try:
        # Fetch the image with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Check for duplicate images using a hash of the content
        image_hash = hashlib.sha256(response.content).hexdigest()
        if image_hash in downloaded_hashes:
            print(f"✗ Duplicate image detected, skipping: {url}")
            return
        
        # Determine filename
        content_type = response.headers.get('Content-Type')
        filename = get_filename(url, content_type)
        
        # Save the image
        filepath = os.path.join("Fetched_Images", filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        # Add the hash to the set of downloaded hashes
        downloaded_hashes.add(image_hash)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    """
    Main function to run the Ubuntu Image Fetcher.
    """
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get URLs from user
    urls_input = input("Please enter one or more image URLs, separated by a comma: ")
    urls = [url.strip() for url in urls_input.split(',')]
    
    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)
    
    # Use a set to store hashes of downloaded images to prevent duplicates
    downloaded_hashes = set()
    
    for url in urls:
        if url:
            download_image(url, downloaded_hashes)
            
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()