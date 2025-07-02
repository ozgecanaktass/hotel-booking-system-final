# app/services/agent_service.py

import os
import json
from openai import OpenAI
import re
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_booking_preferences(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that extracts hotel booking preferences.\n"
                        "Your ONLY job is to return a JSON like this:\n"
                        "{ \"city\": \"Paris\", \"budget\": 200 }\n"
                        "Respond ONLY with this format, no explanation."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()
        print("AI response:", content)
        return json.loads(content)

    except Exception as e:
        print("AI ERROR:", e)
        return {"error": "AI agent failed to parse user input."}


def parse_booking_request(message: str):
    result = {}

    # City (first capital word after "in")
    city_match = re.search(r"in ([A-Z][a-z]+)", message)
    if city_match:
        result["city"] = city_match.group(1)

    date_match = re.search(r"from (\w+ \d{1,2}) to (\w+ \d{1,2})", message)
    if date_match:
        try:
            year = datetime.now().year  # default: this year
            result["check_in"] = str(datetime.strptime(f"{date_match.group(1)} {year}", "%B %d %Y").date())
            result["check_out"] = str(datetime.strptime(f"{date_match.group(2)} {year}", "%B %d %Y").date())
        except:
            pass

    people_match = re.search(r"for (\d+) adults?", message)
    if people_match:
        result["people"] = int(people_match.group(1))

    budget_match = re.search(r"(?:budget|under|max(?:imum)?)\s*(?:is\s*)?\$?(\d+)", message.lower())
    if budget_match:
        result["budget"] = int(budget_match.group(1))
    else:
        result["budget"] = 300


    rating_match = re.search(r"(\d(?:\.\d)?)\s?\+?\s?stars?", message.lower())
    if rating_match:
        result["min_rating"] = float(rating_match.group(1))

    prefs = []
    for keyword in ["pool", "breakfast", "wifi", "city center"]:
        if keyword.lower() in message.lower():
            prefs.append(keyword)
    result["preferences"] = prefs

    return result
