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


class MentalHealthSupportCrew:
    def __init__(self):
        # Define the crew with agents and tasks
        self.crew = Crew(
            agents=[
                user_interaction_agent,
                assessment_agent,
                resource_recommendation_agent,
                monitoring_agent,
                crisis_management_agent,
            ],
            tasks=[
                user_interaction_task,
                assessment_task,
                resource_recommendation_task,
                monitoring_task,
                crisis_management_task,
            ],
            verbose=True,
        )

    def kickoff(self, inputs):
        """
        Executes the workflow and dynamically decides task paths.
        """
        # Ensure 'user_input' exists in inputs
        if "user_input" not in inputs:
            raise ValueError("Missing required input: 'user_input'")

        # Step 1: Run the workflow
        result = self.crew.kickoff(inputs=inputs)

        # Step 2: Extract output of user_interaction_task
        user_interaction_result = result["tasks_output"][0]  # First task is user_interaction_task
        interaction_summary = user_interaction_result.get("raw", "").lower()

        # Step 3: Determine next steps based on interaction_summary
        if "happy" in interaction_summary or "neutral" in interaction_summary:
            # Pass interaction_summary to monitoring_task
            self.crew.kickoff({"interaction_summary": interaction_summary})
            return {
                "response": "That's great to hear! Let me know if there's anything you'd like to share.",
                "tasks_executed": ["User Interaction Agent", "Monitoring Agent"],
            }

        elif "critical" in interaction_summary:
            # Pass user_input to crisis_management_task
            self.crew.kickoff({"user_input": inputs["user_input"]})
            return {
                "response": "Critical input detected. Crisis intervention initiated.",
                "tasks_executed": ["User Interaction Agent", "Crisis Management Agent"],
            }

        else:
            # Run assessment_task and resource_recommendation_task
            self.crew.kickoff({"user_input": inputs["user_input"]})
            return {
                "response": "Input processed. Additional resources have been recommended.",
                "tasks_executed": ["User Interaction Agent", "Assessment Agent", "Resource Recommendation Agent"],
            }
