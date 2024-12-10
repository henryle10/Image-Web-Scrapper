import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import os

def imagedown(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

    for image in images:
        link = image.get('src')
        if not link:
            continue 

        name = image.get('alt', '').strip()

        # Handle missing 'alt' by using the image file name from 'src'
        if not name:
            name = os.path.basename(link).split('.')[0]
        
        # Get the file extension from the src URL
        file_extension = os.path.splitext(link)[1].lower()  # e.g., ".jpg", ".png", ".svg"
        if file_extension not in ['.jpg', '.jpeg', '.png', '.svg']:
            continue  # Skip files without supported extensions

        # Replace invalid characters in the file name
        name = name.replace(' ', '-').replace('/', '')

        # Add the correct file extension
        file_name = f"{name}{file_extension}"
        
        # Download the image
        try:
            im = requests.get(link)
            with open(file_name, 'wb') as f:
                f.write(im.content)
            print('Downloaded:', file_name)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

# Example usage
imagedown('https://www.markslending.com/', 'homepage')
