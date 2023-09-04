import openai
import os
from pathlib import Path
import json

# Read API key from environment variable or secret management service
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Read the file contents into string variables
facilitator_system = Path("facilitator_system.txt").read_text()
debate_system = Path("debate_system.txt").read_text()

# Debate Set Up
def set_up():
    topic = input("Debate topic:\n")
    bot_number = int(input("Amount of bots participating in debate:\n"))
    facilitator_rating = input("Facilitator participation (1-3) | 1 = bare amount of facilitation, 3 = highest amount of participation |")

    main_conversation = [
        {"role": "system", "content": facilitator_system},
        {"role": "user", "content": f"INPUTS: Topic: {topic}, Facilitator Scale: {facilitator_rating}, Number of Agents: {str(bot_number)}"},
    ]

    try:
        facilitator = openai.ChatCompletion.create(
            model="gpt-4",
            messages=main_conversation
        )
    except Exception as e:
        print(f"Error: {e}")
        return

    print(facilitator['choices'][0]['message']['content'])
    main_conversation.append({"role": "assistant", "content": "FACILITATOR: " + facilitator['choices'][0]['message']['content']})

    if input("Press 'ENTER' to start the debate") != "":
        print('\nENDING DEBATE')
        exit()
    
    print("Starting Debate...\n\n") 
    sub_conversation = [
        {"role": "system", "content": debate_system},
        {"role": "user", "content": facilitator['choices'][0]['message']['content']}
    ]

    while True:
        for bot in range(bot_number):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=sub_conversation
                )
            except Exception as e:
                print(f"Error: {e}")
                return

            response_content = response['choices'][0]['message']['content']
            sub_conversation.append({"role": "assistant", "content": response_content})
            main_conversation.append({"role": "user", "content": response_content})
            print(response_content + '\n\n')

        try:
            facilitator = openai.ChatCompletion.create(
                model="gpt-4",
                messages=main_conversation
            )
        except Exception as e:
            print(f"Error: {e}")
            return

        print(facilitator['choices'][0]['message']['content'])
        main_conversation.append({"role": "assistant", "content": "FACILITATOR: " + facilitator['choices'][0]['message']['content']})
        sub_conversation.append({"role": "user", "content": "FACILITATOR: " + facilitator['choices'][0]['message']['content']})
        
        if input("Press 'ENTER' to continue") != "":
            print('\nENDING DEBATE')
            print(json.dumps(main_conversation, indent=2))
            exit()

if __name__ == '__main__':
    set_up()
