import os
import easyocr
import PyPDF2
import docx
import google.generativeai as genai

# Configure API key directly
api_key = "AIzaSyC6nauzDhXcgA6WZgDdXVL9EWO5fGXlClA"

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    return '\n'.join(result)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip() if text else "No text extracted from PDF."

def extract_text_from_word(doc_path):
    doc = docx.Document(doc_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text.strip() if text else "No text extracted from Word document."

def send_to_gemini(user_input, chat_history):
    # Append user query to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Convert chat history into a single formatted string for Gemini
    conversation = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history)

    # Send the entire conversation history as a single text input
    response = model.generate_content(conversation)

    # Store AI response in chat history
    chat_history.append({"role": "assistant", "content": response.text})

    return response.text, chat_history

def process_document(file_path, file_type):
    if file_type == 'image':
        extracted_text = extract_text_from_image(file_path)
    elif file_type == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_type == 'word':
        extracted_text = extract_text_from_word(file_path)
    else:
        return "Unsupported file type", []

    # Initial system prompt
    initial_prompt = ("Analyze the provided legal document by identifying key legal clauses, "
                      "summarizing important sections, and highlighting any potential risks or ambiguities. "
                      "Offer a structured review with relevant legal insights and compliance considerations. "
                      "After the review, act as an interactive legal assistant, answering follow-up questions "
                      "and clarifying document-related concerns.")

    # Store initial prompt and document text as first messages in history
    chat_history = [
        {"role": "system", "content": initial_prompt},
        {"role": "user", "content": extracted_text}
    ]
    
    insights, chat_history = send_to_gemini(extracted_text, chat_history)
    return insights, chat_history

if __name__ == '__main__':
    file_path = "file.pdf"  # Ensure this file is in the same directory
    file_type = "pdf"
    insights, chat_history = process_document(file_path, file_type)
    
    print("Extracted Insights:")
    print(insights)

    while True:
        user_input = input("Ask follow-up questions (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response, chat_history = send_to_gemini(user_input, chat_history)
        print("AI Response:", response)
