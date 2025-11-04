from strands import Agent


class StrandAgent:
    """Strands Agent implementation for processing user requests"""
    
    def __init__(self, user_message: str):
        """
        Initialize and execute Strands agent with the user message
        
        Args:
            user_message: The input prompt from the user
        """
        self.user_message = user_message
        self.message = self._execute_agent()
    
    def _execute_agent(self):
        """Execute the Strands agent and return the result"""
        try:
            agent = Agent()
            result = agent(self.user_message)
            return str(result)
        except Exception as e:
            return f"Error processing request with Strands: {str(e)}"

