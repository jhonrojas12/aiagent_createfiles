from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from agent import Agent

load_dotenv()
agent = Agent()
print('mi primer agente ia')

client = OpenAI()

while True:
    user_input = input("Tu: ").strip()
    if not user_input:
        print("Por favor, ingresa un mensaje.")
        continue
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("Saliendo del chat. ¡Hasta luego!")
        break

    # Agregar el mensaje del usuario a la lista de mensajes
    agent.messages.append({"role": "user", "content": user_input})
    while True:
        response = client.responses.create(
            model="gpt-5-nano",
            input=agent.messages,
            tools=agent.tools
        )
        # assistant_reply= response.output_text
        # messages.append({"role": "assistant", "content": assistant_reply})
        # print(f"Asistendte: {assistant_reply}")
        called_tool = agent.process_response(response)
        if not called_tool:
            break














