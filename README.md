Made using ChatGPT in ~2 hours cause it was being dumb, made sure it works as intended.  
Title is a bit misleading, this merges all keybinds in multiple options.txt files, not replacing unbound keybinds in the main options.txt.   

If you do not know how to use this, just get pycharm by jetbrains, and drag this code in somewhere.  

Files/Folders you need to know: 
+ merge.py (runs the code)
+ /options_main stores your main options.txt, and uses all "options" from this file.
  - (Make in vanilla, unless you have a modded options.txt that you like.)
+ /options_other (stores other options.txts, and copies, in alphabetical order, keybinds.)
  - (The rest of the options.txts get processed in alphabetical order)

other files:
+ get_catergories.py (used for testing)
+ merge_old.py (old testing, tried to do catergory sort but realized its useless)
