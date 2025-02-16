# Frame Hunter
A python program for mGBA that starts an encounter for every frame  
# Features
## Encountering
The way this all works is: the program pauses the game, advances one frame, creates a save state, encounters the Pokémon, if it's not shiny it reloads the save state, and restarts the loop. In the GBA Pokémon games, RNG is tied to the frame rate. Through this method, the program effectively encounters every version of this Pokémon, in order. Along with frame-by-frame encountering Pokémon, this program also utilizes mGBA's speed up feature to encounter even more Pokémon in less the time. I've gotten as low as **one second** per encounter.  
## Logging
Tracks and saves the total encounters and elapsed time to `resets.json`.  
## Shiny Detection
The shiny detection is pretty simple, by choosing a color from the non-shiny variant that doesn't appear on the shiny variant, the program can tell if an encounter is shiny. The program simply checks if a specific pixel is a certain color, if it is that color, then it's not shiny. But if it isn't that color, then you found a shiny!  
## Discord Notifying
Through the use of a discord webhook, the program will notify you when it finds a shiny.  
<img src="img/Webhookoutput.png" alt="Webhook">  