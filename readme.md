
melee overlay - cool thing with a bad name

[what it can do](https://gfycat.com/IdolizedSafeArgentinehornedfrog)

quick install instructions:

linux and osx only, sorry windows boiz

get a version of dolphin that has memorywatcher stuff. smash ladder netplay version is too old, if you want to be safe just get the latest build

gotta have melee obviously

get python 3 (idk how python 2 will fare) and pyside, via however you install python stuff based on your setup

clone this branch of my fork of [p3](https://github.com/sepharoth213/p3/tree/more_state_data). i'll eventually pr some of this into the official p3 repo but for now this will have to do. either add the git dir to your PYTHONPATH or take the p3 folder _inside_ the git dir and put it in this folder.

run `python overlay.py /path/to/dolphin/home/dir`, replacing with your dolphin home dir

it's probably either `~/.local/share/dolphin-emu` or `~/.dolphin-emu` for linux
`/Users/username/Library/Application Support/Dolphin` for osx

run dolphin and start the game, the overlay should do stuff, if not dude idk figure it out

if you run the overlay anytime after the css it probably won't work, safest bet is to go to the css after starting the overlay

to get the transparency to work you'll need a compositor, i use compton