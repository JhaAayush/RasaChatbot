from flask import Flask, render_template, request, jsonify, send_file
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO

app = Flask(__name__)

# Store conversation history
conversation = []

@app.route("/")
def home():
    return render_template("index.html", conversation=conversation)

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form["user_message"]
    
    # Add user message to conversation history
    conversation.append({"sender": "user", "message": user_message})

    # Send user message to Rasa server
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "user123",  # Unique sender ID
        "message": user_message
    }
    response = requests.post(rasa_url, json=payload)

    # Add bot response to conversation history
    if response.status_code == 200:
        bot_response = response.json()[0]["text"]
        conversation.append({"sender": "bot", "message": bot_response})
    else:
        conversation.append({"sender": "bot", "message": "Sorry, I couldn't process your request."})

    return jsonify({"status": "success", "conversation": conversation})

@app.route("/download_chat", methods=["GET"])
def download_chat():
    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add a title to the PDF
    title = Paragraph("Chat Conversation", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))

    # Add each message to the PDF
    for message in conversation:
        sender = message["sender"]
        text = message["message"]
        chat_line = Paragraph(f"<b>{sender}:</b> {text}", styles["BodyText"])
        story.append(chat_line)
        story.append(Spacer(1, 6))

    # Build the PDF
    pdf.build(story)

    # Move the buffer's cursor to the beginning
    buffer.seek(0)

    # Return the PDF as a downloadable file
    return send_file(
        buffer,
        as_attachment=True,
        download_name="chat_conversation.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)