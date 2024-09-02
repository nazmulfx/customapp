import frappe
import qrcode
from io import BytesIO
from frappe.utils.file_manager import save_file

def generate_qr_code(doc, method):
    # Generate QR code with Sales Order ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(doc.name)
    qr.make(fit=True)

    # Create an image file from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Save the QR code image and attach it to the Sales Order document
    file_doc = save_file(
        f"{doc.name}_qr.png", 
        img_buffer.getvalue(), 
        "Sales Order", 
        doc.name, 
        is_private=0
    )

    # Update the sales order with the link to the QR code image
    doc.custom_qr_code = file_doc.file_url
    doc.save()



