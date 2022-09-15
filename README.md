# Epic-Seven-Secret-Shop-Refresh

Programmed in Python 3.6.4

Use at your own risk. May skip BMs

## Benefits of using this secret shop refresh over other files
1. You can use your mouse. The other scripts will use your mouse to click but this program sends keys to BS5. However, it will still set your BS5 to foreground so it's still not perfect. 
2. Centralised settings for easy maintenance
3. Consistent image find - automatic bluestacks resize
4. Fast
5. Retries on fail attempts
6. Script pause
7. Prints results vs average

## Downsides
1. No randomised clicking

## Tested on these specific bluestacks 5 settings
1. Pixel density: 240 DPI
2. Graphics: Performance
3. Graphics Rendererr: OpenGL
4. Resolution: 1280x720 (the script will resize to this). 

Screenshots: All images were screenshotted on 1280x720 and screenshotted on these settings.

## Pre-requisites
1. Python 3
2. BlueStacks 5
3. BlueStacks 5 key mapped
4. BlueStacks 5 must be opened in your main display
5. Have the right side bar of BS5 opened
6. Script must be executed with admin mode

## Settings
If you need to tweak any of the settings read the comments in the python script.

The only classes you could tweak is UserSettings, FileNames, and Keys.

For keys, refer to https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

The sleep durations have been customised to my OWN internet so if your internet is not stable you may need to tweak all the sleeps accordingly. Do not set below these numbers.

## Mapping Instructions
You need to map 11 keys to BS5 in the refresh shop. 

### 9 Repeated tap buttons and swipe 

All repeated tap button settings: Count=2, Repeat until key up=False. Rest on default.

Swipe settings: all on default

1. Open secret refresh shop and key map A, B, C, D to the first four buy buttons in order.
2. Scroll all the way to the bottom and key map E, F to the last two buttons in order.
3. Click any buy button then key map R to the pop-up buy button.
4. Key map the refresh button to Y.
5. Put a swipe in the middle of the screen somewhere. Set the north of the circle key map to S, set the south to T. S should scroll down, T should scroll up.
6. Click refresh, and key map Z to the confirm button.

## Executing instructions
Assuming you have all the python libraries and is ready to execute...

1. Open secret shop (make sure there are no bought BMs on the screen)
2. Run refresh.py in admin mode. 
3. First thing the script does is check if it can find BS5 so it'll send a key. If it doesn't, just click BS5.
4. Enter in the start button (it is [ by default) in the terminal and it will start running
5. To pause the script spam the pause button (it is ] by default) into the terminal

Don't move your BS5

## Image checker
Within the script you can set image checker flag on True in the class user settings if you want to check if a certain image is being detected.

Make sure your epic seven is opened at the screen you want to check a specific image at.

If you want it to run faster then comment out the images you don't want to check in img_checker function.
