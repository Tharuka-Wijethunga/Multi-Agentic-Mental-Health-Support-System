from crewai import Task

from agents import (
    user_interaction_agent,
    assessment_agent,
    resource_recommendation_agent,
    monitoring_agent,
    crisis_management_agent
)

user_interaction_task = Task(
    description=(
        "Receive {user_input} from the user about their mental health concerns. "
        "Determine if the input requires immediate crisis intervention. "
        "If a crisis is identified, pass the {user_input} to the crisis management agent."
        "If not a crisis, send input to assessment_agent for evaluation."
        "Then if the assessment agent gives OK to respond,without getting recommendations from resource "
        "recommendation agent, reply to the user accordingly."
        "If user just ask about the progress report, request the progress report from the monitoring agent."
    ),
    expected_output=(
        "A determination of whether the {user_input} requires "
        "crisis management or can proceed to assessment. "
    ),
    agent=user_interaction_agent,
    async_execution=False
)

assessment_task = Task(
    description=(
        "Analyze the {user_input} from the user_interaction_task. "
        "Evaluate the user's emotional state, identify potential mental health conditions, "
        "and categorize the severity of their issues. "
        "Determine if therapy recommendations are needed."
        "If therapy recommendations are not needed send OK to reply to the user by user interaction agent by himself."
        "Assessment reports always passed to the monitoring agent."
    ),
    expected_output=(
        "A detailed mental health assessment report for the {user_input}, including: "
        "1. Identified symptoms "
        "2. Possible conditions "
        "3. Severity levels "
        "4. Recommendation status (OK/Not OK for direct user response)"
    ),
    context=[user_interaction_task],
    agent=assessment_agent,
    async_execution=False
)

resource_recommendation_task = Task(
    description=(
        "Based on the assessment report, develop personalized "
        "resources and coping strategies for the user."
        "list should be passed to the user interaction agent."
    ),
    expected_output=(
        "A comprehensive list of: "
        "1. Tailored mental health resources "
        "2. Actionable coping strategies "
        "3. Specific recommendations for the user's condition"
    ),
    context=[assessment_task],
    agent=resource_recommendation_agent,
    async_execution=False
)

monitoring_task = Task(
    description=(
        "Monitor the user's interactions and track their progress over time. "
        "Evaluate if their mental health state is improving based on assessment_report, "
        "and schedule follow-ups as necessary."
        "Do not pass the progress report to the user interaction agent unless it is asked by the user."
    ),
    expected_output=(
        "A progress report detailing: "
        "1. User's mental health journey "
        "2. Observed trends "
        "3. Recommended follow-up schedule"
    ),
    context=[user_interaction_task, assessment_task],
    agent=monitoring_agent,
    async_execution=True
)

crisis_management_task = Task(
    description=(
        "Immediately respond to high-risk situations where the user "
        "exhibits signs of a crisis in the {user_input}, such as suicidal thoughts or extreme anxiety."
        "crisis intervention steps and the report should be passed to the user interaction agent."
    ),
    expected_output=(
        "An incident report including: "
        "1. Crisis intervention steps "
        "2. Current status of the user "
        "3. Emergency resource referrals "
        "4. Recommended immediate support message"
    ),
    context=[user_interaction_task],
    agent=crisis_management_agent,
    async_execution=False
)