from flask import Flask, render_template, request

import pickle
import json

# -----------------------------------
# INITIALIZE FLASK APP
# -----------------------------------

app = Flask(__name__)

# -----------------------------------
# LOAD TRAINED ML MODEL
# -----------------------------------

with open("chatbot_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# -----------------------------------
# LOAD VECTORIZER
# -----------------------------------

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# -----------------------------------
# LOAD CHATBOT RESPONSES
# -----------------------------------

with open("intents.json", "r") as file:
    responses = json.load(file)

# -----------------------------------
# MYSQL TEMPORARILY DISABLED
# -----------------------------------

# import mysql.connector

# connection = mysql.connector.connect(
#
#     host="localhost",
#
#     user="root",
#
#     password="Ateeb@30",
#
#     database="ecommerce_chatbot"
# )
#
# cursor = connection.cursor()

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    user_message = ""
    bot_response = ""

    if request.method == "POST":

        # Get user message
        user_message = request.form["message"]

        # Convert text into vector
        message_vector = vectorizer.transform([user_message])

        # Predict intent
        predicted_intent = model.predict(message_vector)[0]

        # Default chatbot response
        bot_response = responses.get(

            predicted_intent,

            "Sorry, I could not understand your query."
        )

        # -----------------------------------
        # ORDER TRACKING DISABLED
        # -----------------------------------

        if predicted_intent == "order_tracking":

            bot_response = (
                "Order tracking service is unavailable "
                "in deployed version."
            )

        # -----------------------------------
        # COMPLAINT STORAGE DISABLED
        # -----------------------------------

        # Complaint storage disabled for deployment

        # -----------------------------------
        # CHAT HISTORY DISABLED
        # -----------------------------------

        # Chat history disabled for deployment

    return render_template(

        "index.html",

        user_message=user_message,

        bot_response=bot_response
    )

# -----------------------------------
# RUN FLASK APP
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True)