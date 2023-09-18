import os
from flask import Flask, request, Response
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime
from web3 import Web3
import utils

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(TELEGRAM_API_TOKEN)
web3 = Web3(
  Web3.HTTPProvider("https://eth.llamarpc.com/rpc/01GM5A8MGDW6P9ZEJJS1ZYCEGQ"))

ve = web3.eth.contract(address=utils.ve_addr, abi=utils.ve_abi)
crv = web3.eth.contract(address=utils.crv_addr, abi=utils.crv_abi)
circ = web3.eth.contract(address=utils.circ_addr, abi=utils.circ_abi)


@app.route('/notify', methods=['POST'])
def notify():
  # Extract logs from request
  logs = request.json['event']['data']['block']['logs']

  # Check if logs array is empty
  if (len(logs) == 0):
    print("Empty logs array received, skipping")
  else:
    # Loop through each log in the logs array
    for i in range(0, len(logs)):
      # Extract topic1, topic2, and amount from the log
      provider = "0x" + logs[i]['topics'][1][26:]
      locktime = int(logs[i]['topics'][2], 16)
      locktime = datetime.utcfromtimestamp(locktime).strftime('%d-%m-%Y')
      hash = logs[i]['transaction']['hash']

      # hyperlink
      hyperlink = f'''<a href="https://etherscan.io/tx/{hash}">Tx Hash</a> | <a href="https://etherscan.io/address/{provider}">Wallet Address</a>'''

      # decode hex string into value, type and ts
      hex = str(logs[i]['data'])
      value = round(int(hex[2:2 + 64], 16) / 1e18, 2)
      value_msg = str('{:,}'.format(value))
      ts = int(hex[-8:], 16)
      ts = datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y')

      # total crv locked
      total_crv_locked = ve.functions.supply().call()
      total_crv_locked_m = round(total_crv_locked / 1e24, 2)
      total_crv_locked_m = '{:,}'.format(total_crv_locked_m)

      # crv locked into liquid derivatives
      cvxcrv = round(
        ve.functions.locked(utils.cvxcrv_addr).call()[0] / 1e18, 2)
      cvxcrv_M = round((cvxcrv / 1e6), 2)
      sdcrv = round(ve.functions.locked(utils.sdcrv_addr).call()[0] / 1e18, 2)
      sdcrv_M = round((sdcrv / 1e6), 2)
      ycrv = round(ve.functions.locked(utils.ycrv_addr).call()[0] / 1e18, 2)
      ycrv_M = round((ycrv / 1e6), 2)
      perpetuity = round((cvxcrv + ycrv + sdcrv) / 1e6, 2)
      perpetuity = '{:,}'.format(perpetuity)

      # circ supply locked
      circ_supply = round(circ.functions.circulating_supply().call() / 1e18, 2)
      supply_locked = round(ve.functions.supply().call() / 1e18, 2)
      supply_lock_ratio = round(
        supply_locked / (supply_locked + circ_supply) * 100, 2)

      # Create message to send to Telegram
      if provider == "0x989aeb4d175e16225e39e87d0d97a3360524ad80":
        message = f'''CONVEX just locked {value_msg} $CRV
Total $CRV locked into CONVEX: {cvxcrv_M}M
Total $CRV locked: {total_crv_locked_m}M ({str(supply_lock_ratio)}% of current supply)
Locked in perpetuity: {perpetuity}M
{hyperlink}'''

      elif provider == "0xf147b8125d2ef93fb6965db97d6746952a133934":
        message = f'''YEARN just locked {value_msg} $CRV
Total $CRV locked into YEARN: {ycrv_M}M
Total $CRV locked: {total_crv_locked_m}M ({str(supply_lock_ratio)}% of current supply)
Locked in perpetuity: {perpetuity}M
{hyperlink}'''

      elif provider == "0x52f541764e6e90eebc5c21ff570de0e2d63766b6":
        message = f'''STAKEDAO just locked {value_msg} $CRV
Total $CRV locked into STAKEDAO: {sdcrv_M}M
Total $CRV locked: {total_crv_locked_m}M ({str(supply_lock_ratio)}% of current supply)
Locked in perpetuity: {perpetuity}M
{hyperlink}'''

      else:
        message = f'''{provider} just locked {value_msg} $CRV until {locktime}
Total $CRV locked: {total_crv_locked_m}M ({str(supply_lock_ratio)}% of current supply)
Locked in perpetuity: {perpetuity}M
{hyperlink}'''

      # Send the message to the user
      if value > 10000:
        bot.send_message(chat_id="",
                         text=message,
                         parse_mode="HTML",
                         disable_web_page_preview=True)
      else:
        pass

  # Return a success response to the request
  return Response(status=200)


def start(update: Update, context: CallbackContext):
  global user_chat_id
  user_chat_id = update.effective_chat.id
  update.message.reply_text("You will now receive notifications.")


updater = Updater(TELEGRAM_API_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))

# Start the bot
updater.start_polling()

# Start Flask app
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
