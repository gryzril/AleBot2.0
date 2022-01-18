# AleBot2.0
AleBot2.0 is the second iteration the Ale Discord Bot, this time written in Python using the Discord.py library.

Some commands include:

Play audio from .mp3 files and Youtube:
  - get_volume        
  - list_files        - (Lists all audio files AleBot2.0 has saved)
  - play              - (Streams from a url [URL])
  - play_saved        - (Plays an audio file that AleBot2.0 has saved [File])
  - stop              
  - volume            

Virtual Bitcoin Economy:
  - BTC               - (Get Current BTC Price)
  - TaxMan            - (Get TaxMan's BTC holdings)
  - all_balances      - (Get Balances of all Users)
  - balance           - (Get your BTC Balance)
  - transfer          - (Transfer BTC to another user [Username, amount])
  - burn              - (Burn BTC [amount])
  - mine              - (Mine BTC [Times to Mine])
  Gambling:
  - bet_flip          - (Bet BTC on a Coin Flip [bet])

Misc:
  - clear             
  - get_users         
  - hello             
  - help              - (Returns 'help' if bot is running)
  - join              
  - kick              
  - kill              - (Kills Bot process)
  - pick              
  - quote               
  - speak             - (Text to Speach ["Text"])
  - speakl            - (Text to speach + language ["Text", Language Code])
  - test              
  
  Override user's BTC balance {requires key}:
  - set_balance     
