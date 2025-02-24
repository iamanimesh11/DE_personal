from google.cloud import vision
import io
import os
# Path to your service account key file (downloaded from Google Cloud Console)
service_account_path = "lucid-container-450907-g4-adaceaaa7412.json"
image_folder = "tst_Captcha_images"

# Authenticate using the service account
client = vision.ImageAnnotatorClient.from_service_account_file(service_account_path)
results=[]

# Path to the image file
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder,image_name)

    # Read the image
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    # Convert image to Google Vision format
    image = vision.Image(content=content)

    # Perform OCR (text detection)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract the detected text (first annotation is the most relevant)
    detected_text = texts[0].description.strip() if texts else ""

    # Check if the detected text matches the filename (without extension)
    expected_text = os.path.splitext(image_name)[0]  # Remove file extension
    status = "Matched" if expected_text.lower() in detected_text.lower() else "Not Matched"

    # Print result
    print(f"{image_name}: {status}")

    # Store result
    results.append(f"{image_name}: {status}")

# Optional: Save results to a text file
with open("ocr_results.txt", "w") as f:
    f.write("\n".join(results))

print("✅ OCR processing completed. Results saved in 'ocr_results.txt'.")