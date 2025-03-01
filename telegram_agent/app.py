import sys
import os

from PIL import Image # Importa o módulo Pillow
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crew_conversa import ChatAgent
from telegram_bot_sandeco import TelegramBotSandeco

from instagram_send import InstagramSend

async def gerenciar_mensagem(message: str) -> str:
    """Função que será registrada no bot para processar mensagens."""    
    inputs = {"message": message}
    agent_text = agent.kickoff(inputs=inputs)
    return agent_text

async def gerenciar_foto(image_path, caption):
    """Recebe e processa uma foto enviada pelo usuário."""  

    InstagramSend.send_instagram(image_path, caption)
    
    return  f"📸 Foto salva da {caption}."
    


if __name__ == "__main__":
    
    agent = ChatAgent()
    
    bot = TelegramBotSandeco(
        callback=gerenciar_mensagem,
        callback_foto=gerenciar_foto,  # Agora também recebe imagens
        saudacao="Olá doidera"
    )
    bot.run()
