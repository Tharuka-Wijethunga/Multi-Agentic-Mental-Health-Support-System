from crewai import Task
from crewai.tasks import TaskOutput
from crewai.tasks.conditional_task import ConditionalTask

from agents import (
    user_interaction_agent,
    assessment_agent,
    resource_recommendation_agent,
    monitoring_agent,
    crisis_management_agent,
)


def is_crisis_detected(output: TaskOutput) -> bool:
    if output is None:
        return False
    crisis_keywords = [
        "suicide", "kill myself", "want to die",
        "self-harm", "hurt myself", "can't go on",
        "feeling hopeless", "no way out",
    ]
    input_text = output.pydantic.user_input.lower()
    return any(keyword in input_text for keyword in crisis_keywords)


def requires_resource_recommendation(output: TaskOutput) -> bool:
    if output is None:
        return False
    resource_trigger_keywords = [
        "stress", "anxiety", "depressed", "struggling",
        "need help", "overwhelmed", "mental health", "coping", "support",
    ]
    input_text = output.pydantic.user_input.lower()
    return any(keyword in input_text for keyword in resource_trigger_keywords)


user_interaction_task = Task(
    description="Receive and analyze user input: '{user_input}' to determine its nature and recommend a pathway.",
    expected_output=(
        "Categorization of input: "
        "1. Input type (neutral/stressful/critical) "
        "2. Recommended routing strategy "
        "3. Initial contextual understanding"
    ),
    agent=user_interaction_agent,
    async_execution=False,
)

assessment_task = ConditionalTask(
    description="Assess the user's emotional state based on input: '{user_input}'.",
    expected_output="Detailed assessment report.",
    context=[user_interaction_task],
    agent=assessment_agent,
    condition=lambda output: not is_crisis_detected(output),
    async_execution=False,
)

resource_recommendation_task = ConditionalTask(
    description="Provide resources tailored to the user input: '{user_input}' and assessment results.",
    expected_output="Personalized resources and coping strategies.",
    context=[user_interaction_task, assessment_task],
    agent=resource_recommendation_agent,
    condition=requires_resource_recommendation,
    async_execution=False,
)

monitoring_task = Task(
    description="Log the interaction summary: '' for progress tracking.",
    expected_output="Logged interaction details.",
    agent=monitoring_agent,
    async_execution=True,
)

crisis_management_task = ConditionalTask(
    description="Provide crisis intervention for critical input: '{user_input}'.",
    expected_output="Crisis intervention response.",
    context=[user_interaction_task],
    agent=crisis_management_agent,
    condition=is_crisis_detected,
    async_execution=False,
)

