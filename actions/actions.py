import pandas as pd
from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from itertools import combinations

class ActionListElectives(Action):
    def name(self) -> Text:
        return "action_list_electives"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Load electives data
            df = pd.read_excel("electives.xlsx")
            electives_list = df["Course Name"].tolist()

            # Send response to user
            dispatcher.utter_message(text="Here are the available electives: " + ", ".join(electives_list))
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")
        return []


class ActionGetElectiveDetails(Action):
    def name(self) -> Text:
        return "action_get_elective_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get course code from user input
            course_code = tracker.get_slot("course_code")

            if not course_code:
                dispatcher.utter_message(text="Please specify the course code.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")
            elective_details = df[df["Course Code"] == course_code]

            if not elective_details.empty:
                details = elective_details.iloc[0]
                response = (
                    f"Course: {details['Course Name']}\n"
                    f"Credits: {details['Credits']}\n"
                    f"Faculty: {details['Faculty']}\n"
                )
            else:
                response = "Sorry, I couldn't find details for that course."

            dispatcher.utter_message(text=response)
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")
        return []


class ActionSuggestElectives(Action):
    def name(self) -> Text:
        return "action_suggest_electives"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the user's interests from the slot
            interests = tracker.get_slot("interest")

            if not interests:
                dispatcher.utter_message(text="Please tell me your area of interest, like finance, AI, or marketing.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")

            # Check if the DataFrame has the required columns
            if "Course Name" not in df.columns or "Course Description" not in df.columns:
                dispatcher.utter_message(text="The electives data is not formatted correctly.")
                return []

            # Convert interests to lowercase for case-insensitive matching
            interests = [interest.lower() for interest in interests]

            # Filter electives based on all interests
            suggested_electives = []
            for interest in interests:
                filtered = df[
                    (df["Course Description"].str.contains(interest, case=False, na=False)) |
                    (df["Course Name"].str.contains(interest, case=False, na=False))
                ]
                suggested_electives.extend(filtered["Course Name"].tolist())

            # Remove duplicates
            suggested_electives = list(set(suggested_electives))

            if suggested_electives:
                dispatcher.utter_message(
                    text=f"If you're interested in {', '.join(interests)}, you might like these electives: " + ", ".join(suggested_electives)
                )
            else:
                dispatcher.utter_message(
                    text=f"Sorry, I couldn't find any electives related to {', '.join(interests)}."
                )
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")
        return []


class ActionExplainCourse(Action):
    def name(self) -> Text:
        return "action_explain_course"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the course name or code from the user input
            course = tracker.get_slot("course")

            if not course:
                dispatcher.utter_message(text="Please specify the course you want to know about.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")

            # Check if the DataFrame has the required columns
            if "Course Name" not in df.columns or "Course Description" not in df.columns:
                dispatcher.utter_message(text="The electives data is not formatted correctly.")
                return []

            # Find the course by name or code
            course_details = df[
                (df["Course Name"].str.contains(course, case=False, na=False)) |
                (df["Course Code"].str.contains(course, case=False, na=False))
            ]

            if not course_details.empty:
                description = course_details.iloc[0]["Course Description"]
                credits = course_details.iloc[0]["Credits"]
                faculty = course_details.iloc[0]["Faculty"]
                dispatcher.utter_message(text=f"This is a {credits} course taught by {faculty}. Here's what the course is about: {description}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find details for the course: {course}.")
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")
        return []


class ActionListCoursesByCredits(Action):
    def name(self) -> Text:
        return "action_list_courses_by_credits"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the credits value from the user input
            credits = tracker.get_slot("credits")

            if not credits:
                dispatcher.utter_message(text="Please specify the number of credits for the courses you are looking for.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")

            # Convert credits to string in case it's stored as a different type
            df["Credits"] = df["Credits"].astype(str)

            # Filter courses based on the requested credit count
            courses = df[df["Credits"] == str(credits)]["Course Name"].tolist()

            if courses:
                dispatcher.utter_message(text=f"Courses with {credits} credits: " + ", ".join(courses))
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any courses with {credits} credits.")

        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")

        return []

class ActionSuggestElectivesByCredits(Action):
    def name(self) -> Text:
        return "action_suggest_electives_by_credits"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get slots
            interests = tracker.get_slot("interest")
            credit_min = tracker.get_slot("credit_min")
            credit_max = tracker.get_slot("credit_max")

            if not interests or not credit_min or not credit_max:
                dispatcher.utter_message(text="Please specify your interests and the credit range.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")

            # Convert interests to lowercase for case-insensitive matching
            interests = [interest.lower() for interest in interests]

            # Filter electives based on all interests
            suggested_electives = []
            for interest in interests:
                filtered = df[
                    (df["Course Description"].str.contains(interest, case=False, na=False)) |
                    (df["Course Name"].str.contains(interest, case=False, na=False))
                ]
                suggested_electives.extend(filtered["Course Name"].tolist())

            # Remove duplicates
            filtered_electives = list(set(suggested_electives))


            # Filter electives based on interests
            # Get the list of electives with their credits
            electives = filtered_electives[["Course Name", "Credits"]].values.tolist()

            # Find combinations of electives whose total credits fall within the range
            valid_combinations = []
            for r in range(1, len(electives) + 1):  # Try combinations of size 1 to all electives
                for combo in combinations(electives, r):
                    total_credits = sum(course[1] for course in combo)
                    if float(credit_min) <= total_credits <= float(credit_max):
                        valid_combinations.append(combo)

            # Prepare the response
            if valid_combinations:
                response = "Here are some elective combinations that match your interests and credit range:\n"
                for combo in valid_combinations:
                    course_names = [course[0] for course in combo]
                    total_credits = sum(course[1] for course in combo)
                    response += f"- {', '.join(course_names)} (Total Credits: {total_credits})\n"
            else:
                response = "Sorry, I couldn't find any elective combinations that match your interests and credit range."

            dispatcher.utter_message(text=response)
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")
        return []
    
class ActionSuggestElectivesByFaculty(Action):
    def name(self) -> Text:
        return "action_suggest_electives_by_faculty"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Get the credits value from the user input
            faculty = tracker.get_slot("faculty")

            if not faculty:
                dispatcher.utter_message(text="Please specify the faculty you are looking for.")
                return []

            # Load electives data
            df = pd.read_excel("electives.xlsx")

            # Convert credits to string in case it's stored as a different type
            df["Faculty"] = df["Faculty"].astype(str)

            # Filter courses based on the requested credit count
            courses = df[df["Faculty"] == str(faculty)]["Course Name"].tolist()

            if courses:
                dispatcher.utter_message(text=f"Courses taught by {faculty}: " + ", ".join(courses))
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any courses with {credits} credits.")

        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, I encountered an error: {str(e)}")

        return []
