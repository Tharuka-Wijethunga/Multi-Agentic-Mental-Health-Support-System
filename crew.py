from crewai import Crew
import warnings
from agents import (
    user_interaction_agent,
    assessment_agent,
    resource_recommendation_agent,
    monitoring_agent,
    crisis_management_agent
)
from tasks import (
    user_interaction_task,
    assessment_task,
    resource_recommendation_task,
    monitoring_task,
    crisis_management_task
)

warnings.filterwarnings('ignore')

mental_health_support_crew = Crew(
    agents=[
        user_interaction_agent,
        assessment_agent,
        resource_recommendation_agent,
        monitoring_agent,
        crisis_management_agent],

    tasks=[
        user_interaction_task,
        assessment_task,
        resource_recommendation_task,
        monitoring_task,
        crisis_management_task],

    verbose=True
)

# mental_health_support_inputs = {
#     'user_input': """I've been feeling a bit stressed lately with work. Some days are harder than others,
#     but I'm trying to manage."""
# }
#
#
# result = mental_health_support_crew.kickoff(inputs=mental_health_support_inputs)
# print(result)