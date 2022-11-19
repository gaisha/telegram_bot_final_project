import logging
import argparse
import torch
import numpy as np
import re

from simplelstm import SimpleLSTM
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from torch.autograd import Variable
import torch.nn.functional as F

# Pre-assign menu text
FIRST_MENU = "<b>Menu</b>\n\n Generate song lyrics based on the first line."

# Pre-assign button text
GENERATE_BUTTON = "Generate example song!"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(GENERATE_BUTTON, callback_data=GENERATE_BUTTON)
]])

EXAMPLE_TEXT = "In the town where I was born\nLived a man who sailed to sea"

char_to_int = {'\n': 0, ' ': 1, '!': 2, '"': 3, "'": 4, '(': 5, ')': 6, ',': 7, '-': 8, '.': 9, '0': 10, '1': 11, '2': 12, '3': 13, '4': 14, '5': 15, '6': 16, '7': 17, '8': 18, '9': 19, ':': 20, ';': 21, '?': 22, '[': 23, ']': 24, 'a': 25, 'b': 26, 'c': 27, 'd': 28, 'e': 29, 'f': 30, 'g': 31, 'h': 32, 'i': 33, 'j': 34, 'k': 35, 'l': 36, 'm': 37, 'n': 38, 'o': 39, 'p': 40, 'q': 41, 'r': 42, 's': 43, 't': 44, 'u': 45, 'v': 46, 'w': 47, 'x': 48, 'y': 49, 'z': 50, '¶': 51, '¼': 52, 'ã': 53}
int_to_char = {0: '\n', 1: ' ', 2: '!', 3: '"', 4: "'", 5: '(', 6: ')', 7: ',', 8: '-', 9: '.', 10: '0', 11: '1', 12: '2', 13: '3', 14: '4', 15: '5', 16: '6', 17: '7', 18: '8', 19: '9', 20: ':', 21: ';', 22: '?', 23: '[', 24: ']', 25: 'a', 26: 'b', 27: 'c', 28: 'd', 29: 'e', 30: 'f', 31: 'g', 32: 'h', 33: 'i', 34: 'j', 35: 'k', 36: 'l', 37: 'm', 38: 'n', 39: 'o', 40: 'p', 41: 'q', 42: 'r', 43: 's', 44: 't', 45: 'u', 46: 'v', 47: 'w', 48: 'x', 49: 'y', 50: 'z', 51: '¶', 52: '¼', 53: 'ã'}
state, args, kwargs = torch.load("trained_model.model")
model_2 = SimpleLSTM(*args, **kwargs)
model_2.load_state_dict(state)
model_2.eval()
print(model_2)

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_song(song_start):
    variance = 0.25
    seq_length = 50
    generated = ''
    start_text = ''.join(sym.lower() for sym in song_start if sym.lower() in char_to_int)[:seq_length]

    generated = ''
    original = start_text
    window = start_text

    for i in range(200):
        x = np.zeros((1, seq_length))
        for t, char in enumerate(window):
            x[0, t] = char_to_int[char]

        x_in = Variable(torch.LongTensor(x))
        pred = model_2(x_in)
        pred = np.array(F.softmax(pred, dim=1).data[0].cpu())
        next_index = sample(pred, variance)
        next_char = int_to_char[next_index]  # noqa

        generated += next_char
        window = window[1:] + next_char  # Update Window for next char predict

    return original + generated

def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """

    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if len(update.message.text) < 50:
        context.bot.send_message(
            update.message.chat_id, 
            "Please enter beginning of the song with at least 50 characters",
            entities=update.message.entities
        )
        return
    try: 
        context.bot.send_message(
            update.message.chat_id, 
            generate_song(update.message.text), 
            entities=update.message.entities
        )
    except:
        context.bot.send_message(
            update.message.chat_id, 
            "Sorry, something went wrong. Please try again", 
            entities=update.message.entities
        )
        throw


def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """

    context.bot.send_message(
        update.message.from_user.id,
        FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )


def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    data = update.callback_query.data
    context.bot.send_message(
        update.callback_query.from_user.id,
        f"For the song input:\n\'{EXAMPLE_TEXT}\'\nThe generated output could be:\n\n" + generate_song(EXAMPLE_TEXT) + "\n\nTry yourself by sending a message!",
    )


def main(bot_token) -> None:
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CommandHandler("start", menu))

    dispatcher.add_handler(CallbackQueryHandler(button_tap))
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    config_arg = os.getenv('MY_BOT_SECRET')
    main(config_arg)