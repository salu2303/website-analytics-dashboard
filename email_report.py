import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openai

from transformers import pipeline

def generate_summary(top_products, device_stats):
    # Initialize the summarization pipeline with a pre-trained model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Prepare the text to be summarized
    product_lines = [f"- {p['name']} (SKU: {p['id']}): {p['quantity']} sold" for p in top_products]
    device_lines = [f"- {device.capitalize()}: {users} users" for device, users in device_stats.items()]
    full_text = (
        "Weekly Website Performance Report\n\n"
        "Top-Selling Products:\n" + "\n".join(product_lines) + "\n\n"
        "Visitor Device Statistics:\n" + "\n".join(device_lines)
    )

    # Generate the summary
    summary = summarizer(full_text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

def send_email(config, top_products, device_stats, page_views, summary, total_visitors):
    sender = config["email"]["sender"]
    receiver = config["email"]["receiver"]
    password = config["email"]["password"]

    # Construct email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Weekly Website Report"
    message["From"] = sender
    message["To"] = receiver

    html = f"""
    <html><body>
    <h2>🌐 Weekly Website Report</h2>
    <p><strong>Total Visitors:</strong> {total_visitors:,}</p>
    <h3>🛍 Top Products</h3>
    <ul>{''.join([f"<li>{p['name']}: {p['quantity']} sold</li>" for p in top_products])}</ul>
    <h3>📱 Device Breakdown</h3>
    <ul>{''.join([f"<li>{k}: {v} users</li>" for k, v in device_stats.items()])}</ul>
    <h3>📄 Page Views</h3>
    <ul>{''.join([f"<li>{k}: {v} views</li>" for k, v in page_views.items()])}</ul>
    <h3>🧠 Summary</h3><p>{summary}</p>
    </body></html>
    """

    message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
        print("✅ Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("❌ Failed to authenticate with Gmail. Did you use an App Password?")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")