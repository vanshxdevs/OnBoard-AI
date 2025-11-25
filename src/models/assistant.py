"""
AI Assistant class for handling conversations with employees.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.utils.logger import logger


class Assistant:
    """AI Assistant for employee onboarding conversations."""
    
    def __init__(
        self,
        system_prompt: str,
        llm,
        message_history: list = None,
        vector_store=None,
        employee_information: dict = None,
    ):
        """Initialize the Assistant.
        
        Args:
            system_prompt: System instructions for the AI
            llm: Language model instance
            message_history: List of previous messages
            vector_store: Vector store for retrieving policy information
            employee_information: Employee data dictionary
        """
        logger.info("Initializing Assistant instance")
        logger.debug("system_prompt=%s", repr(system_prompt)[:200])
        logger.debug("llm=%s", repr(llm))
        
        self.system_prompt = system_prompt
        self.llm = llm
        self.messages = message_history or []
        self.vector_store = vector_store
        self.employee_information = employee_information

        self.chain = self._get_conversation_chain()
        logger.info("Conversation chain created for Assistant")

    def get_response(self, user_input: str):
        """Get AI response for user input.
        
        Args:
            user_input: User's message
            
        Returns:
            Streaming response generator
        """
        import time
        logger.info("Assistant.get_response called with input length: %d chars", len(user_input))
        logger.debug("user_input=%s", user_input)
        try:
            start = time.time()
            result = self.chain.stream(user_input)
            logger.info("Assistant streaming response initiated successfully (%.2fs)", time.time() - start)
            return result
        except Exception as e:
            logger.error("Error while getting response: %s", str(e), exc_info=True)
            raise

    def _get_conversation_chain(self):
        """Build the conversation chain with RAG."""
        logger.info("Building conversation chain...")
        
        prompt = ChatPromptTemplate(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("conversation_history"),
                ("human", "{user_input}"),
            ]
        )

        output_parser = StrOutputParser()

        chain = (
            {
                "retrieved_policy_information": self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={
                        "k": 2,  # Reduced to 2 for fastest retrieval
                        "fetch_k": 5  # Pre-fetch only 5 candidates
                    }
                ),
                "employee_information": lambda x: self.employee_information,
                "user_input": RunnablePassthrough(),
                "conversation_history": lambda x: self.messages,
            }
            | prompt
            | self.llm
            | output_parser
        )
        
        logger.info("Conversation chain built successfully with retriever and output parser")
        return chain
