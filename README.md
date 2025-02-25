# Elective Selection Chatbot for IIM Amritsar

## Overview
This project is an AI-powered chatbot designed to assist students at IIM Amritsar in selecting electives based on their interests, credit requirements, and course details. Built using the **Rasa framework**, the chatbot integrates with an Excel database to provide personalized recommendations and detailed course information.

## Features
- **Elective Suggestions**: Recommends electives based on student interests (e.g., finance, analytics, marketing).
- **Credit Range Filtering**: Suggests combinations of courses within a specified credit range (e.g., "Suggest electives with 5-6 credits").
- **Course Details**: Provides detailed information about courses, including prerequisites, faculty, and descriptions.
- **Dynamic Filtering**: Supports multiple interests and handles partial matches for flexible querying.

## Technology Stack
- **Framework**: Rasa (Open-source conversational AI)
- **Programming Language**: Python
- **Data Storage**: Excel/CSV for course information
- **Libraries**: Pandas, NLTK (for synonyms and advanced filtering)

## How It Works
1. **User Input**: Students provide their interests and/or credit requirements.
2. **Intent Recognition**: Rasa NLU identifies the intent (e.g., `suggest_electives`, `explain_course`).
3. **Slot Filling**: Extracts entities like `interest`, `course`, `min_credits`, `max_credits`.
4. **Custom Actions**: Python scripts filter and process data from the Excel file.
5. **Response Generation**: The bot provides a list of suggested electives or course details.

## Setup Instructions
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Train the Model**:
   ```bash
    rasa train
   ```
3. **Run the Action Server**:
   ```bash
    rasa run actions
   ```
4. **Test the Chatbot in Shell**:
   ```bash
   rasa shell
   ```
   OR
   ```bash
   python app.py
   ```
