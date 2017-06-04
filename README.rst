.. image:: https://travis-ci.org/Gandus10/projetBot.svg?branch=master
   :target: https://travis-ci.org/Gandus10/projetBot
   :alt: Build Status

Discord bot : Bot-notes
=======================

Idée de base du projet
-----------------------

Le but du projet est de réaliser un Discord Bot que l'utilisateur
peut utiliser pour calculer sa moyenne de module
ou d'une matière. L'utilisateur peut ajouter ses notes en indicant
'le nom du cours/sa note/la pondération'. Il peut demander sa moyenne en indicant
moyenne 'nom du module' ou 'moyenne nom du cours'

Requirements
------------
- `Python 3.6 <https://www.python.org/>`_
- `aiohttp 2.1.0 <https://pypi.python.org/pypi/aiohttp>`_
- `Discord API <https://github.com/Rapptz/discord.py>`_

Installation
------------

.. code-block:: console

    $ pip install NotesBot

Configuration
-------------

Discord TOKEN is read from environnement variable at ``TOKEN``. Make sure to add yours before running the bot.

Run
---

.. code-block:: console

    $ python notes-bot/notes-bot-discordapi.py

Usage
-----

Send message to Bot-notes on Discord.
Use ``!help`` to show available commands.

.. include:: ./nots-bot/help_message.rst


Auteurs
-------

- Laurent Gander, laurent.gander@he-arc.ch
- Sylvain Renaud, sylvain.renaud@he-arc.ch
