

#Student 1: Benjamin Ho
#Spire ID: 35283268


#Student 2: Ruhan Roy
#Spire ID: 35265786


class CourseItem:
    def __init__(self, title, category, due_date, points_possible):
        """
        Initialize a CourseItem with the given attributes.

        Parameters:
            title (str): The name of the item (e.g., "HW1", "Quiz 1").
            category (str): The type of item (e.g., "Homework", "Quiz", "Exam", "Lecture Note").
            due_date (str): The due date as a string (e.g., "2026-03-20").
            points_possible (float): The maximum points for this item.

        Instance variables to set:
            self.title          -- the item title
            self.category       -- the item category
            self.due_date       -- the due date string
            self.points_possible -- max points for this item
            self.points_earned  -- starts as None (not yet graded)
            self.completed      -- starts as False
        """

        self.title = title
        self.category = category
        self.due_date = due_date
        self.points_possible = points_possible
        self.points_earned = None #This starts at none because none is graded
        self.completed = False #This started as false because it is not completed yet

    def mark_complete(self):
        """
        Mark this item as completed.

        Rules:
            - Sets self.completed to True.
            - Must not print anything.
        """

        self.completed = True #Marked this item as being done

    def update_score(self, score):
        """
        Record the score earned on this item.

        Parameters:
            score (float): The points earned to assign to self.points_earned.

        Rules:
            - Must not print anything.
        """

        self.points_earned = score #Saves the scores

    def display_info(self):
        """
        Return a formatted string describing this item.

        Format:
            "<category>: <title> | Due: <due_date> | Score: <score_text> | Status: <status>"

        Where:
            score_text is "Not graded" if points_earned is None,
                        otherwise "<points_earned>/<points_possible>"
            status is "Completed" if completed is True, otherwise "Incomplete"

        Returns:
            str: The formatted item info string.
        """
        #checks if graded or not
        if self.points_earned is None:
            score_text = "Not graded"
        else:
            score_text = f"{self.points_earned}/{self.points_possible}"

        #checks if completed or not
        status = "Completed" if self.completed else "Incomplete"

        return f"{self.category}: {self.title} | Due: {self.due_date} | Score: {score_text} | Status: {status}"


# Default category weights — must sum to 100.
# Each Course gets its own copy of these weights, which can be customized.
DEFAULT_WEIGHTS = {
    "Homework":     20.0,
    "Quiz":         10.0,
    "Exam":         30.0,
    "Lecture Note": 5.0,
    "Project":      35.0,
}


def score_to_letter(percentage):
    """
    Convert a numeric percentage to a US university letter grade.

    Standard scale:
        A  >= 93   A- >= 90
        B+ >= 87   B  >= 83   B- >= 80
        C+ >= 77   C  >= 73   C- >= 70
        D+ >= 67   D  >= 63   D- >= 60
        F  <  60

    Parameters:
        percentage (float): Grade percentage (0–100).

    Returns:
        str: The corresponding letter grade string (e.g., "A", "B+", "C-").
    """

    if percentage >= 93: #Converts percentage to letter grade based on scale provided
        return "A"
    elif percentage >= 90: #Goes down elif until matches correct percentage
        return "A-"
    elif percentage >= 87:
        return "B+"
    elif percentage >= 83:
        return "B"
    elif percentage >= 80:
        return "B-"
    elif percentage >= 77:
        return "C+"
    elif percentage >= 73:
        return "C"
    elif percentage >= 70:
        return "C-"
    elif percentage >= 67:
        return "D+"
    elif percentage >= 63:
        return "D"
    elif percentage >= 60:
        return "D-"
    else:
        return "F" #Returns Fail grade if all other statements are false




class Course:
    def __init__(self, course_name, course_code, instructor_name):
        """
        Initialize a Course.

        Parameters:
            course_name (str): Full name of the course (e.g., "Intro to Python").
            course_code (str): Course code (e.g., "ECE122").
            instructor_name (str): Name of the instructor.

        Instance variables to set:
            self.course_name     -- full course name
            self.course_code     -- course code
            self.instructor_name -- instructor name
            self.items           -- empty list (will hold CourseItem objects)
            self.weights         -- a copy of DEFAULT_WEIGHTS (use dict() to copy)
        """
        #sets the course info
        self.course_name = course_name
        self.course_code = course_code
        self.instructor_name = instructor_name
        #empty the list for items
        self.items = []
        #copy the default weights so each course has its own
        self.weights = dict(DEFAULT_WEIGHTS)

    # ── Weight management ─────────────────────────────────────────────────

    def set_weights(self, new_weights):
        """
        Replace this course's category weights with new_weights.

        Parameters:
            new_weights (dict): Mapping of category name -> percentage weight.
                                Values must sum to 100 (within 0.01 tolerance).

        Returns:
            bool: True if weights were successfully set,
                  False if they do not sum to ~100.

        Rules:
            - Must not print anything.
        """

        total = 0
        for weight in new_weights: #Cycles through dictionary and add weights to total
            total += new_weights[weight]

        if abs(total - 100) < 0.01: #Checks if total equals 100 within 0.01 tolerance
            self.weights = new_weights #If true then it updates the weights
            return True
        else:
            return False


    def display_weights(self):
        """
        Return a list of formatted strings showing the current category weights.

        Format for each entry:
            "  <category>: <weight>%"

        Returns:
            list[str]: One string per category in self.weights.
        """

        result = [] #Created an empty list to store formatted weight strings
        for category, weight in self.weights.items(): #Cycles through weight and category
            result.append(f"  {category}: {weight}%")  #Add formatted to the list
        return result

    # ── Item management ───────────────────────────────────────────────────

    def add_item(self, item):
        """
        Add a CourseItem to this course's items list.

        Parameters:
            item (CourseItem): The item to add.

        Rules:
            - Must not print anything.
        """

        self.items.append(item) #Adds item to the course item list


    def remove_item(self, item_title):
        """
        Remove an item from this course by title (case-insensitive).

        Parameters:
            item_title (str): Title of the item to remove.

        Returns:
            bool: True if the item was found and removed, False otherwise.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """

        for item in self.items: #Loops through all items in course
            if item.title.lower() == item_title.lower(): #Checking if the title matches
                self.items.remove(item) #Removes indexed item
                return True #Successful removal
        return False #No matches were found

    def find_item(self, item_title):
        """
        Find and return a CourseItem by title (case-insensitive).

        Parameters:
            item_title (str): Title to search for.

        Returns:
            CourseItem: The matching item, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        for item in self.items: #Loop through items and find the one that matches
            if item.title.lower() == item_title.lower():
                return item
        return None

    def display_items(self):
        """
        Return a list of formatted strings for all items in this course.

        Returns:
            list[str]: One string per item from display_info(),
                       or ["No items found."] if the course has no items.
        """
        #Returns default message if no items
        if not self.items:
            return ["No items found."]
        return [item.display_info() for item in self.items]

    def display_pending_items(self):
        """
        Return a list of formatted strings for all incomplete items.

        Returns:
            list[str]: Strings from display_info() for items where completed is False,
                       or ["No pending items."] if all items are complete.
        """

        #Get all incomplete items
        pending = [item.display_info() for item in self.items if not item.completed]
        if not pending:
            return ["No pending items."]
        return pending


    def calculate_grade(self):
        """
        Calculate the weighted overall grade for this course.

        Algorithm:
            For each category in self.weights that has weight > 0:
              1. Collect all graded items in that category
                 (items where points_earned is not None).
              2. If none exist, skip this category entirely.
              3. Compute category_pct = sum(points_earned) / sum(points_possible) * 100.
              4. Add category_pct * weight to a running weighted_sum.
              5. Add weight to a running active_weight.
            Final percentage = weighted_sum / active_weight.

        Returns:
            tuple(float, str) or None:
                A tuple of (percentage rounded to 2 decimal places, letter grade string)
                if at least one item has been graded.
                None if no items have been graded yet.

        Rules:
            - Only items with points_earned != None count as graded.
            - Categories with no graded items are excluded from the calculation.
            - Use score_to_letter() to convert the final percentage to a letter grade.
            - Must not print anything.
        """

        graded_items = []
        for item in self.items: #Creates a list to store graded items
            if item.points_earned is not None:
                graded_items.append(item)

        if not graded_items: #Returns none if there is not graded items
            return None

        earned_total = {} #Dictionaries to track points possible and earned
        possible_total = {} # in each category
        for item in graded_items: #Cycles through graded items and adds points to category
            category = item.category

            if category not in earned_total: #If category isn't seen, total starts at 0
                earned_total[category] = 0
                possible_total[category] = 0

            earned_total[category] += item.points_earned #Add item points to category total
            possible_total[category] += item.points_possible

        weight_sum = 0 #Tracking weighted sum and total weight of category
        active_weight = 0 #Needed to find final percentage at the end
        for category, weight in self.weights.items(): #Loops through each category and weight
            if weight > 0 and category in earned_total: #Includes categories with weight (required by instructions)
                a = earned_total[category] / possible_total[category] #Stored a, then multiplied to get a percentage
                category_pct = a * 100 #Calculating percentage for category
                weight_sum += category_pct * (weight/100)
                active_weight += weight #Added the weight to total

        if active_weight == 0: #If the category not contribute to the total return it to none
            return None

        final_percentage = weight_sum / active_weight #Calculating final percentage
        letter_grade = score_to_letter(final_percentage) #Convert
        return float(f"{final_percentage:.2f}"), letter_grade #Rounding 2 decimal places







class CourseManager:
    def __init__(self):
        """
        Initialize the CourseManager with an empty list of courses.

        Instance variables to set:
            self.courses -- empty list (will hold Course objects)
        """

        self.courses = [] #Creates list to store courses

    def add_course(self, course):
        """
        Add a Course object to the manager's list.

        Parameters:
            course (Course): The Course object to add.

        Rules:
            - Must not print anything.
        """

        self.courses.append(course) #Adds the course to the list

    def find_course(self, course_name):
        """
        Find and return a Course by name (case-insensitive).

        Parameters:
            course_name (str): The course name to search for.

        Returns:
            Course: The matching Course object, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        #Loops through courses and find the one that matches
        for course in self.courses:
            if course.course_name.lower() == course_name.lower():
                return course
        return None

    def find_course_by_code(self, course_code):
        """
        Find and return a Course by course code (case-insensitive).

        Parameters:
            course_code (str): The course code to search for (e.g., "ECE122").

        Returns:
            Course: The matching Course object, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        #Loops through courses and find the one with matching code
        for course in self.courses:
            if course.course_code.lower() == course_code.lower():
                return course
        return None

    def display_courses(self):
        """
        Return a list of formatted strings for all courses.

        Format for each entry:
            "<course_code>: <course_name> (<instructor_name>)"

        Returns:
            list[str]: One string per course,
                       or ["No courses available."] if no courses have been added.
        """

        #Return default message if no courses
        if not self.courses:
            return ["No courses available."]
        return [f"{course.course_code}: {course.course_name} ({course.instructor_name})"
                for course in self.courses]
