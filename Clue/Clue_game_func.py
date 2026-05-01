"""
ECE 122 Project 1: Mystery Deduction Game (Grader / Reference Solution)

This file contains the functions that main.py EXPECTS to exist.
Students will implement these same functions in their own mystery_game.py.

Big picture (how main.py uses this file):
- main.py calls build_game() once to get the option names and starting resources.
- main.py randomly chooses the hidden solution (the “envelope”) using INDEXES
  into the suspects/locations/items options.
- During the loop, main.py calls the functions below to:
  * print the notebook (display_game_state)
  * score a guess vs. the envelope (evaluate_guess)
  * check for a win (is_win)
  * cross off impossible options (update_all_notebooks)
  * apply duplicate guess penalty (check_and_record_guess)
  * spend clue tokens to eliminate an option (use_clue_token)
  * suggest which category to use a token on (best_clue_category)

Important design notes:
- The hidden solution is stored as INDEXES (not strings) in main.py.
- The notebook stores “still possible?” as True/False values.
- This version has NO witness reveal and NO separate cases.
"""
"""
Student 1: Ruhan Roy
Spire Id: 35265786

Student 2: Benjamin Ho
Spire Id: 35283268
"""
import random


def build_game():
    """
    Create and return the game data (no cases).

    This function sets up the game configuration:
    - suspects/locations/items: the options the player can choose from
    - max_attempts: how many attempts the player starts with in main.py
    - clue_tokens: how many clue tokens the player starts with in main.py

    Returns:
        suspects: all suspect name options shown in the menu
        locations: all location name options shown in the menu
        items: all item name options shown in the menu
        max_attempts: starting number of attempts (main.py copies this into attempts)
        clue_tokens: starting number of clue tokens (main.py copies this into tokens)
    """
    # --- Core game data ---
    # suspects/locations/items should be filled with the full set of names.
    # main.py will later choose the secret envelope by picking an INDEX into each set.

    #We defined the complete lists of the game options as required by the requirements/specs
    suspects = ["Colonel Mustard", "Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Mr. Green", "Dr. Orchid", "Sergeant Gray"]
    locations = ["Library", "Kitchen", "Ballroom", "Study", "Conservatory"]
    items = ["Candlestick", "Rope", "Wrench", "Knife", "Revolver"]

    # Randomize displayed order each run.
    # This makes the menu look different each time the program is run.
    # main.py chooses the envelope AFTER calling build_game(), so shuffling here is safe:
    # the indices still match the names for the entire run.
    random.shuffle(suspects)
    random.shuffle(locations)
    random.shuffle(items)

    # Per spec: player gets 4 attempts total.
    # main.py copies this into its variable "attempts".
    # max_attempts = 4

    max_attempts = 4 #Starting attempts set to 4 as for the requirements
    
    # Randomize starting clue tokens (resource system).
    # main.py copies this into its variable "tokens".
    # Adjust this range if you want tokens to be more/less common.
    clue_tokens = random.randint(1, 2)

    #Returns all the game data to main.py for initialization
    return suspects, locations, items, max_attempts, clue_tokens


def display_game_state(suspects, locations, items, pos_suspect, pos_location, pos_item, attempts, tokens):
    """
    Print the player's current notebook and remaining resources.

    Parameters (all are passed in from main.py each loop):
        suspects: the suspect names (used to print the numbered suspect menu)
        locations: the location names (used to print the numbered location menu)
        items: the item names (used to print the numbered item menu)

        pos_suspect: tracks which suspect options are still possible.
            main.py updates this over time as the player learns information.

        pos_location: tracks which location options are still possible.
            main.py updates this over time as the player learns information.

        pos_item: tracks which item options are still possible.
            main.py updates this over time as the player learns information.

        attempts: how many attempts the player has left right now.
            main.py decreases this after each suggestion (and duplicates may cost extra).

        tokens: how many clue tokens the player has left right now.
            main.py decreases this when a clue token successfully eliminates an option.

    Output:
        None (prints to the console)
    """
    # Only print options that are still marked as possible in the notebook.
    # NOTE: We display with numbering starting at 1 for user friendliness,
    # even though the internal indexes start at 0.

    #Printing blank line for formatting before the game state
    print()

    #Displaying header and the resource info
    print("DEDUCTION NOTEBOOK")
    print("Remaining Attempts:", attempts) #Shows the remaining attempts
    print("Clue Tokens:", tokens) #Shows the remaining clues token
    print()

    #Display the suspect section, only those still marked will be shown
    print("SUSPECTS:")
    for i in range(len(suspects)):
        #Checking if this suspect is still marked True in Notebook
        if pos_suspect[i] == True:
            print(f" {i + 1} {suspects[i]}")
    print() #prints blank line after suspects section

    #Displays LOCATION section
    print("LOCATIONS:")
    for i in range(len(locations)):
        #Check if location still possible
        if pos_location[i] == True:
            #Cycles through them
            print(f" {i + 1} {locations[i]}")
    print() # blank line after location section

    #displays items section, which only show those marked possible
    print("ITEMS:")
    for i in range(len(items)):
        #Check if this item is still possible
        if pos_item[i] == True:
            #Cycles through them
            print(f" {i+1} {items[i]}")
    print() #Blank line after items section


def evaluate_guess(guess_idx, solution_idx):
    """
    Compare a guess (indexes) to the hidden solution (indexes).

    Parameters:
        guess_idx: the player's guess as three indexes chosen in main.py:
            - guess_idx[0] is the suspect index they chose
            - guess_idx[1] is the location index they chose
            - guess_idx[2] is the item index they chose

        solution_idx: the secret envelope indexes created in main.py at startup:
            - solution_idx[0] is the correct suspect index
            - solution_idx[1] is the correct location index
            - solution_idx[2] is the correct item index

    Returns:
        result_list: three True/False values telling main.py what matched:
            - result_list[0] True if suspect index matches the envelope
            - result_list[1] True if location index matches the envelope
            - result_list[2] True if item index matches the envelope

    Example:
        guess_idx    = [1, 4, 0]
        solution_idx = [1, 2, 3]
        returns      = [True, False, False]
    """
    # We always compare 3 categories in this order:
    # 0 = suspect, 1 = location, 2 = item

    #Compare suspect indexes
    if guess_idx[0] == solution_idx[0]:
        suspect = True #Suspect guess matches the solution
    else:
        suspect = False #suspect guess is not correct

    #Comparing location index
    if guess_idx[1] == solution_idx[1]:
        location = True #Location guess matches solution
    else:
        location = False #location guess doesn't match

    #Compare item index
    if guess_idx[2] == solution_idx[2]:
        item = True #Item guess matches the solution
    else:
        item = False #item guess is not correct

    #Returns results as a list in the correct order of suspect, location, item
    return [suspect, location, item]



def is_win(result_list):
    """
    Determine whether the player has solved the mystery.

    Parameters:
        result_list: the True/False match results returned by evaluate_guess().
            main.py calls is_win right after evaluate_guess().

    Returns:
        True only if all three parts of the guess were correct.
    """
    #Using the 'and' operator makes sure all conditions must be true to win
    if result_list[0] and result_list[1] and result_list[2]:
        return True #Player has won since all three guesses are correct
    else:
        return False #Player hasn't won yet and at least 1 of the guesses were incorrect


def update_all_notebooks(pos_suspect, pos_location, pos_item, guess_idx, result_list):
    """
    Update the deduction notebook using ONLY correctness feedback.
    (No witness reveals in this version.)

    What this function is for:
    - main.py calls this after a non-winning guess.
    - It updates the notebook trackers so the next screen shows fewer possibilities.

    Notebook rule used here:
    - If a category was WRONG, cross off the guessed option for that category.
    - If a category was RIGHT, we do NOT automatically cross off other options here.
      (Some versions do, but this keeps updates minimal: only remove what you know is wrong.)

    Parameters (all come from main.py):
        pos_suspect: the notebook tracker for suspects (modified in place)
        pos_location: the notebook tracker for locations (modified in place)
        pos_item: the notebook tracker for items (modified in place)

        guess_idx: the player's most recent guess indexes (chosen in main.py)

        result_list: which parts were correct/incorrect (returned by evaluate_guess)

    Returns:
        None (the notebook trackers are updated in place)
    """
    # If the suspect part was incorrect, that specific suspect cannot be in the envelope,
    # so cross it off in the suspect notebook.

    # If the location part was incorrect, that specific location cannot be in the envelope,
    # so cross it off in the location notebook.

    # If the item part was incorrect, that specific item cannot be in the envelope,
    # so cross it off in the item notebook.

    #Check if suspect guess was wrong
    if result_list[0] == False:
        pos_suspect[guess_idx[0]] = False #Set this suspect to "Not possible"

    #Check if the location guess was wrong
    if result_list[1] == False:
        pos_location[guess_idx[1]] = False #Set this location to "not possible"

    #Check if item guess was wrong
    if result_list[2] == False:
        pos_item[guess_idx[2]] = False #Set this item to "not possible"



def check_and_record_guess(guess_history, guess_idx):
    """
    Check whether a guess is a duplicate, then record it in history.

    Why main.py uses this:
    - main.py discourages repeating the exact same suggestion.
    - It charges more attempts if the guess was already made.

    Duplicate penalty policy used by main.py:
    - New guess: costs 1 attempt
    - Duplicate guess: costs 2 attempts

    Parameters (both come from main.py):
        guess_history: the running record of all prior guesses this game.
            main.py keeps this across turns and passes it back in each time.

        guess_idx: the current guess triple (suspect/location/item indexes)
            that main.py just collected from the user.

    Returns:
        penalty: the number main.py should subtract from attempts for this guess
                 (2 if duplicate, otherwise 1)
    """
    # Search through history to see if the exact same triple was guessed before.
    # A "duplicate" means same suspect index AND same location index AND same item index.

    # Record the guess so future turns can detect duplicates.
    # Important: store the three index values, not a reference that might change later.

    # Return the attempt penalty amount so main.py can subtract it from attempts.

    #Initialize duplicate flag as false until proven correct
    duplicate = False

    #Loop through all guesses in history
    for i in range(len(guess_history)):
        if guess_history[i] == guess_idx:
            duplicate = True #Displays if there is match in history
            break #Exits the loop since we got a duplicate

    if duplicate:
        penalty = 2 #Duplicate guess cost 2 attempts
    else:
        penalty = 1 #New guess cost 1 attempt

    #Adds the current guess to history list
    guess_history.append(guess_idx)

    #Returns the attempt penalty amount so main.py can do the job and subtract it from attempts
    return penalty




def use_clue_token(possible_list, solution_index):
    """
    Use a clue token to eliminate ONE incorrect option in a category.

    How main.py uses this:
    - When the player spends a clue token, main.py chooses a category and passes in
      that category’s notebook tracker (for suspects OR locations OR items).
    - main.py also passes the correct envelope index for that category so we do NOT
      eliminate the true answer.

    Behavior in this reference solution:
    - Scan from low index to high index.
    - Find the first option that is still possible AND is not the correct one.
    - Eliminate it and report success.

    Parameters:
        possible_list: the notebook tracker for ONE category (passed in from main.py)
        solution_index: the correct envelope index for THIS category (passed in from main.py)

    Returns:
        eliminated: True if we eliminated something, False if we could not
                   (usually because only the correct option remains possible)
    """
    # Only eliminate an option if it is still possible
    # and it is not the solution_index (never eliminate the correct answer).

    # If we reach the end without eliminating anything, we couldn't use the token
    # to remove an incorrect option (often because only the correct one remains).

    #Loop through all indexes from lowest to highest
    for i in range(len(possible_list)):
        #checking if this option is still possible and isn't the correct solution
        if possible_list[i] == True and i != solution_index:
            #eliminate this incorrect option
            possible_list[i] = False
            return True # eliminated the option

    return False #If there isn't a eligible option found to eliminate


def best_clue_category(pos_suspect, pos_location, pos_item):
    """
    Choose which category is "best" to spend a clue token on.

    How main.py uses this:
    - main.py calls best_clue_category each loop and shows a hint to the player.
    - main.py also allows the player to choose "use suggested category" and then
      uses this return value.

    Strategy used:
    - Count how many options remain possible in each category.
    - Return the category with the largest count (most uncertainty).
    - If there is a tie, break ties consistently:
        suspects first, then locations, then items.

    Parameters (all are passed in from main.py):
        pos_suspect: notebook tracker for which suspects are still possible
        pos_location: notebook tracker for which locations are still possible
        pos_item: notebook tracker for which items are still possible

    Returns:
        category:
            0 means "suspects"
            1 means "locations"
            2 means "items"
    """
    # Count how many suspects are still possible.

    # Count how many locations are still possible.

    # Count how many items are still possible.

    # Return the category number with the most remaining possibilities.

    #initalizes counters for each category
    suspect_count = 0
    location_count = 0
    item_count = 0

    #Counting for how many suspects are still possible
    for i in range(len(pos_suspect)):
        if pos_suspect[i] == True:
            suspect_count += 1 #Increment count for each possible suspect

    #Now count for how many locations are still possible
    for i in range(len(pos_location)):
        if pos_location[i] == True:
            location_count += 1 #Increment count for each possible location

    #Count how many items are still possible
    for i in range(len(pos_item)):
        if pos_item[i] == True:
            item_count += 1 #Increment count for each possible item

    #Check if suspects have the most or equal/tie to the most
    if suspect_count >= location_count and suspect_count >= item_count:
        return 0 #Highest priority, returns suspects

    elif location_count >= item_count:
        return 1 #Returns for locations being second priority

    else:
        return 2 #Return for item lowest priority
