from crewai import Agent, Task, Crew, Process,LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="cerebras/llama-3.3-70b")

class InstagramPostCrew:
    """
    Classe para criar postagens no Instagram utilizando CrewAI.
    """

    def __init__(self):
        """
        Inicializa os serviços, ferramentas, e configura os agentes e tarefas.
        """

        # Modelos LLM para os agentes
        self.llm_captioner = llm

        # Criar a Crew e configurar agentes e tarefas
        self.create_crew()

    def create_crew(self):
        """
        Configura os agentes e tarefas da Crew para gerar postagens no Instagram.
        """



        # Agente para criação de legendas
        captioner = Agent(
            role="Você é um Criador de Conteúdo para Instagram",
            goal="""Escrever legendas divertidas e sarcásticas sempre 
            tirando Sarro do Sandeco, sempre envolventes 
            para postagens no Instagram com hashtags relevantes.""",
            backstory=(
                """Você é um assistente de IA super descolado, 
                    divertido e sarcástico, com um humor afiado e um 
                    talento especial para tirar sarro do Sandeco de 
                    forma bem-humorada e criativa. 
                    Sua missão é transformar os insumos fornecidos em uma 
                    legenda única e cativante, sempre combinando 
                    irreverência e estilo."""
            ),
            memory=True,
            allow_delegation=False,
            llm=self.llm_captioner,
            verbose=True
        )





        # Tarefa de criação de legendas
        captioner_task = Task(
            description=(
                    r"""
Criar uma postagem no Instagram usando os seguintes insumos:
                        
**Recebendo os seguintes insumos:**  
1. **Insumo principal:**  
   - Gênero: Indica o estilo de palavras e abordagem, delimitado por `<genero>`.  
   - Caption: Uma breve ideia inicial ou descrição enviada por Sandeco, delimitada por `<caption>`.  
   - Tamanho: Define o comprimento da legenda em palavras, delimitado por `<tamanho>`.  

2. **Insumos secundários:**  
   - Descrição da imagem: Detalhamento do conteúdo da imagem gerado por IA, delimitado por `<describe>`.  
   - Estilo de escrita: O tom desejado para a legenda, delimitado por `<estilo>`.  
   - Pessoa: Define a perspectiva usada na legenda (primeira, segunda ou terceira pessoa), delimitado por `<pessoa>`.  
   - Sentimento: Indica o tom emocional, delimitado por `<sentimento>` (padrão é positivo).  
   - Emojis: Define se emojis podem ser usados, delimitado por `<emojs>`.  
   - Gírias: Indica se gírias podem ser incluídas, delimitado por `<girias>`.  

**Instruções de Geração de Texto:**  
- Você combina todos os insumos de forma natural e criativa, gerando uma legenda que:  
  1. O insumo principal tem maior relevância na geração do texto
  2. Use o estilo e humor característico para destacar as façanhas do Sandeco.  
  3. Incorpore aleatoriamente **somente duas zoeiras** numeradas, sem repetição.  
  4. Adicione de 5 a 10 hashtags relacionadas ao conteúdo da imagem e ao contexto da postagem. 
  5. Se por acasso no texto do <caption> mencionar "eu" mude para "Sandeco". Exemplo "Eu estou aqui na práia" para "Sandeco tá lá na praia e eu aqui trabalhando, ah! mizeravi kkk.". Faça variações . 
  6. Adicione pequenas risadinhas depois de uma zoeira como "kkk". Mas somente uma vez no texto.

**Zoeiras numeradas:**  
1. Vasco da Gama: "Postar no Instagram é fácil, difícil é ser campeão com o Vasco!"  
2. Pouco cabelo: "Postar no Instagram é moleza, difícil é pentear o cabelo do Sandeco!"  
3. Meio gordinho: "Postar no Instagram é tranquilo, difícil é resistir a um rodízio com o Sandeco!"  
4. Orgulho nordestino: "Só quem é do Nordeste sabe fazer as coisas com tanto estilo, né, Sandeco?"  
5. Bordão 'Ah! Mizeravi': "Ah! Mizeravi, essa postagem tá espetacular!"  
6. Expressão 'Esse desgramado': "Esse desgramado do Sandeco tá impossível hoje!"  
7. Professor sem muito dinheiro: "Postar no Instagram é tranquilo, difícil é esperar o salário do professor cair!"  
8. Professor e pesquisador em IA: "Postar no Instagram é fácil, difícil é explicar pra IA o que o Sandeco tá tentando fazer!" ou "Esse desgramado do Sandeco quer ensinar até o algoritmo a tirar sarro dele!"  
9. Use o caption como referência do que o Sandeco está falando, fazendo ou onde ele está e use isso para zoeira.

**Transformação de Caption:**  
Ao receber um Caption, ajuste o texto para referenciar Sandeco na terceira pessoa de forma irreverente. Exemplos:  
- "Estou aqui com meu amigo" → "Sandeco tá lá com o amigo dele"  
- "Eu e Minha esposa" → "Sandeco é a esposa dele"  
- "Meu filho" → "Filho do Sandeco" 


**Exemplo de legenda gerada:**  
*"Ah! Mizeravi, hoje foi dia de rodízio! Esse desgramado do Sandeco tá impossível! 😎🍖*  



                    
                    <genero>{genero}</genero>
                    <caption>{caption}</caption>
                    <describe>{describe}</describe>
                    <estilo>{estilo}</estilo>
                    <pessoa>{pessoa}<estilo>
                    <sentimento>{sentimento}<sentimento>
                    <tamanho>{tamanho}</tamanho>
                    <emojs>{emojs}</emojs>
                    <girias>{girias}</girias>
                    
                    """
            ),
            expected_output=(
                "Uma postagem formatada para o Instagram que inclua:\n"
                "1. Uma legenda divertida, sarcástica e envolvente e que integre os insumos.\n"
                "2. Uma lista de 5 a 10 hashtags relevantes e populares."
            ),
            agent=captioner
        )

        # Configura a Crew com os agentes e tarefas
        self.crew = Crew(
            agents=[captioner],
            tasks=[captioner_task],
            verbose=True,
            process=Process.sequential  # Executar as tarefas em sequência
        )

    def kickoff(self, inputs):
        """
        Executa o processo de geração de postagem no Instagram.

        Args:
            inputs (dict): Entradas para o processo, incluindo imagem e preferências de escrita.

        Returns:
            str: Postagem gerada com legenda e hashtags.
        """
        resultado = self.crew.kickoff(inputs=inputs)
        return resultado.raw
