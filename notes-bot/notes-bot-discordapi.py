""""Bot-notes using discord API from https://github.com/Rapptz/discord.py."""

import os

import discord

from dataprocess import load_user

client = discord.Client()


async def message_received(message):
    """Process the received message and answer to it."""
    print(message.content)
    user = load_user(message.author.id)
    commande, *args = message.content.split()

    if commande == '!avg':
        try:
            module_ou_cours, *values = args
            if module_ou_cours in user.modules:
                await client.send_message(
                    message.channel,
                    str(user.get_module(module_ou_cours).average()))
            else:
                # Ce n'est pas un module donc on cherche un cours
                for name, module in user.modules.items():
                    if module_ou_cours in module.branches:
                        await client.send_message(
                            message.channel,
                            str(module.get_branch(module_ou_cours).average()))
        except ValueError:
            await client.send_message(
                message.channel,
                f'Pas assez d\'arguments\n{help_msg}')

    if commande == '!add':
        try:
            cours_ou_note, nom_module, nom_du_cours, *values = args
            if cours_ou_note == 'branch':
                try:
                    print(values)
                    try:
                        poids = int(values[0])
                    except IndexError:
                        poids = 1  # Default value if not specified
                    user.get_module(nom_module).add_branch(nom_du_cours,
                                                           poids)
                    await client.send_message(
                        message.channel,
                        f"Cours ajouté : {nom_du_cours} dans {nom_module}")
                    user.save()
                except TypeError:
                    await client.send_message(
                        message.channel,
                        f"Erreur : précisez le poids du cours.")

            elif cours_ou_note == 'grade':
                note, *poids = values
                try:
                    poids = poids[0]
                except IndexError:
                    poids = 1  # Default value
                user.get_module(
                    nom_module).get_branch(
                    nom_du_cours).add_grade(note, poids)
                await client.send_message(
                    message.channel,
                    f"Note ajoutée {note} ({poids}) dans {nom_du_cours}")
                user.save()
        except ValueError:
            await client.send_message(
                message.channel,
                f'Pas assez d\'arguments\n{help_msg}')

    if commande == '!del':
        try:
            module, *values = args
            if len(values):
                # values > 0, deleting a branch of the module.
                branch_name = values[0]
                if not user.get_module(module).delete_branch(branch_name):
                    await client.send_message(
                        message.channel,
                        f"Cours supprimé : {branch_name}")
                else:
                    await client.send_message(
                        message.channel,
                        f"Aucun cours de ce nom ({branch_name}"
                        f" dans ce module: {module}")
            else:
                # values = 0, deleting the module itself.
                if not user.delete_module(module):
                    await client.send_message(
                        message.channel,
                        f"Module supprimé : {module}")
                else:
                    await client.send_message(
                        message.channel,
                        f"Aucun module de ce nom: {module}")
            user.save()

        except ValueError:
            await client.send_message(
                message.channel,
                f'Pas assez d\'arguments\n{help_msg}')

    if commande == '!show':
        try:
            await client.send_message(
                message.channel,
                str(user) if str(user) != '' else 'Rien à afficher')
        except ValueError:
            await client.send_message(
                message.channel,
                f'Pas assez d\'arguments\n{help_msg}')

    if commande == '!help':
        await client.send_message(message.channel, help_msg)

    if commande == '!quit':
        pass
        # await client.send_message(message.channel, "Bye bye!")
        # await client.logout()


@client.event
async def on_ready():
    """"Discord client event : called when bot is ready."""
    print(f'{client.user.name} started\n-----------------')


@client.event
async def on_message(message):
    """"Discord client event : called when client received a message."""
    # Process only message from other users
    if message.author.id != client.user.id and message.channel.is_private:
        await message_received(message)


# Get help message from a file
with open("help_message.rst", encoding="UTF-8") as file:
    help_msg = file.read()

# Get the token from environment variable
if os.environ.get('TOKEN'):
    TOKEN = os.environ.get('TOKEN')
    print("TOKEN found:", TOKEN)
else:
    exit("Discord token not defined in environment variable")

# Launch bot
client.run(TOKEN)
