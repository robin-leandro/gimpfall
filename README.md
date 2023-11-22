
#TODO open-ended "paper roll" mode
#TODO handle scryfall exceptions and be like hey this one thing exploded sorry dude
#TODO handle double sided cards (how tho lmao)
	# there should be a setting to choose between printing 2 cards or one double-sided cardgit add
	# printing 2 cards = easy: just have the scryfall utility return a tuple with all the images and unpack it
	# printing the actual backside = hard: i have to set up a certain number of frontside cards as backsides, align them properly and dynamically fill in the rest with normal backsides
	# FUN
#TODO print how many empty spaces where leftover after generating sheets
	# even better, give a warning with how many cards will be leftover and ask if continue
#TODO slightly upscale the cardback and center the cards inside it for more consistent results even when alignment is whack