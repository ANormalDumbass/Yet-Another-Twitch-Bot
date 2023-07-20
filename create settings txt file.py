import os
def create_settings_file(username, token, message, channel, command):
    file_path = os.path.join(os.getcwd(), "settings.txt")
    with open('settings.txt', 'w') as file:
        file.write(f"Username: '{botusername}'\n")
        file.write(f"Token: '{token}'\n")
        file.write(f"Message: '{message}'\n")
        file.write(f"Channel: '{channel}'\n")
        file.write(f"Command: '{command}'\n")

if __name__ == "__main__":
    botusername = input("Enter the username of the bot: ")
    token = input("Enter the token of the bot: ")
    command = input("Enter the message which the bot should respond to: ")
    message = input("Enter the message which the bot should send: ")
    channel = input("Enter the channel where the bot should send the messages: ")
    
    create_settings_file(botusername, token, message, channel, command)
    print("File 'settings.txt' created successfully.")
