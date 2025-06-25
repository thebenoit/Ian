""" inspired from the famous realtor from Montreal, 
Tatiana is a realtor agent that understand the need 
of the client and search an appartment according to his preferences"""

from agents.base_agent import BaseAgent

class Tatiana(BaseAgent):
    def __init__(self,model_name:str,tools:list):
        super().__init__(model_name,tools)
        
    