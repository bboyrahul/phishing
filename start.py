import os

# Apne script ka absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "log.txt")

# Example: File ko open karne ka sahi tareeka
with open(log_file, "a") as file:
    file.write("Bot started successfully!\n")
