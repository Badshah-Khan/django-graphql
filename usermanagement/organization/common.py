import qrcode
import os
import uuid
import qrcode
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import json

class CommonMethodOrg:
    def __init__(self, org = None):
        self.organization = org

    def generateQrCode(self):
        print(self.organization.id)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        org_data = json.dumps({
            'name': self.organization.name,
            'id': self.organization.id
        })
        qr.add_data(org_data)
        qr.make(fit=True)

        # Create an in-memory buffer to store the QR code image
        buffer = BytesIO()
        qr_img = qr.make_image()

        # Save the QR code image to the buffer
        qr_img.save(buffer)

        # Save the image to a file
        file_name = f'{uuid.uuid4()}.png'
        qr_file = ContentFile(buffer.getvalue(), name=file_name)

        qr_code_dir = os.path.join(settings.PUBLIC_FOLDER_PATH, 'qrcodes')
        os.makedirs(qr_code_dir, exist_ok=True)

        # Save the image to the public folder
        qr_code_path = os.path.join(qr_code_dir, file_name)
        with open(qr_code_path, 'wb') as f:
            f.write(qr_file.read())

        # Return the URL to download the image
        url = os.path.join('public', 'qrcodes', file_name)

        return url
    
    def upload_logo(self, base64_data):
        # Decode the base64 data
        decoded_image = base64.b64decode(base64_data)

        logo_dir = os.path.join(settings.PUBLIC_FOLDER_PATH, 'logo')
        os.makedirs(logo_dir, exist_ok=True)

        file_name = f'{uuid.uuid4()}.png'
        # Save the image to the public folder
        logo_path = os.path.join(logo_dir, file_name)
        # Save the image file to a location on your server
        with open(logo_path, 'wb') as f:
            f.write(decoded_image)

        return os.path.join('public', 'logo', file_name)
    
    def upload_user_profile(self, profile):
        decoded_image = base64.b64decode(profile)

        profile_dir = os.path.join(settings.PUBLIC_FOLDER_PATH, 'profile')
        os.makedirs(profile_dir, exist_ok=True)

        file_name = f'{uuid.uuid4()}.png'
        # Save the image to the public folder
        profile_path = os.path.join(profile_dir, file_name)
        # Save the image file to a location on your server
        with open(profile_path, 'wb') as f:
            f.write(decoded_image)

        return os.path.join('public', 'profile', file_name)

    def delete_file(self, file_path):
        if file_path != (None, ):
            print(type(file_path))
            if type(file_path) == tuple:
                file_path = file_path[0][7:]
            else:
                file_path = file_path[7:]
            print("public_path", file_path)
            file_url = os.path.join(settings.PUBLIC_FOLDER_PATH, file_path)
            if os.path.exists(file_url):
                # Delete the file
                os.remove(file_url)
                print(f"{file_path} deleted successfully.")
            else:
                print(f"The file {file_path} does not exist.")
