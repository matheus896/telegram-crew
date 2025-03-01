from crewai import Agent, Task, Crew, Process, LLM

from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

llm = LLM(model="cerebras/llama-3.3-70b")

class ChatAgent:
    def __init__(self):

        self.llm = llm

        self.create_crew()
   
    
    def create_crew(self):
        self.zoeiro = Agent(
            role='Assistente Virtual',
            goal='Responder perguntas de forma educada e útil',
            backstory='Você é um assistente amigável pronto para ajudar com qualquer dúvida.',
            verbose=True,
            memory=True,
            allow_delegation=False,
            llm = self.llm      
        )

        self.zoeiro_task = Task(
            description=(
                r"""Responda a seguinte mensagem de forma sarcástica, irônica e engraçada, 
                mas garantindo que a informação esteja correta:\n\n
                Usuário: {message}"""
            ),
            expected_output="Uma resposta zoeira, mas que ainda contenha a informação correta.",
            agent=self.zoeiro
        )


    def kickoff(self, inputs) -> str:
        """Recebe uma mensagem e retorna a resposta do agente."""
        
        crew = Crew(
                agents=[self.zoeiro], 
                tasks=[self.zoeiro_task], 
                process=Process.sequential)
        
        ret = crew.kickoff(inputs=inputs)
        
        return ret.raw
