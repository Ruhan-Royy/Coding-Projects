from course_management import CourseItem, Course, CourseManager, DEFAULT_WEIGHTS




#Student 1: Benjamin Ho
#Spire ID: 35283268


#Student 2: Ruhan Roy
#Spire ID: 35265786



def display_menu():
    print("\nCourse Management System")
    print("1.  Add a new course")
    print("2.  View all courses")
    print("3.  Add an item to a course")
    print("4.  View all items in a course")
    print("5.  Mark an item as completed")
    print("6.  Update an item's score")
    print("7.  View pending items")
    print("8.  Calculate course grade")
    print("9.  Customize category weights")
    print("10. Exit")


def prompt_course_code(manager):
    """
    Display all current courses, then prompt the user to enter a course code.

    Steps:
        1. Print a header: "Current courses:"
        2. Print each string returned by manager.display_courses(), indented with "  ".
        3. Prompt: "Enter course code: "
        4. Call manager.find_course_by_code() with the entered code.
        5. If not found, print "Course not found." and return None.
        6. Return the matching Course object.

    Parameters:
        manager (CourseManager): The active course manager.

    Returns:
        Course or None.
    """

    print("Current courses:") #Shows all current courses
    courses = manager.display_courses()
    for course in courses:
        print(f"  {course}")

    code = input("Enter course code: ").strip() #Asks for course code and removes extra space with strip
    course = manager.find_course_by_code(code)

    if course is None: #If no course is found, prints it and return none
        print("Course not found.")
        return None
    return course



def main():
    manager = CourseManager()

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":

            course_name = input("Enter course name: ") #Asks for course info
            course_code = input("Enter course code: ")
            instructor_name = input("Enter instructor name: ")
            new_course = Course(course_name, course_code, instructor_name) #Creates course object
            manager.add_course(new_course) #Adds to manager

            print("Course added successfully.") #Added course


        elif choice == "2":

            courses = manager.display_courses() #Gets list of all courses
            for course in courses: #Prints each course on own line like screenshot
                print(course)


        elif choice == "3":

            course = prompt_course_code(manager) #Get course using course code
            if course is None: #If course is not found, go back!
                continue

            title = input("Enter item title: ") #Item details from the user
            category = input("Enter item category: ")
            due_date = input("Enter item due date: ")
            points_possible = float(input("Enter item points possible: "))

              # Creates new item and adds to the course
            newer_item = CourseItem(title, category, due_date, points_possible)
            course.add_item(newer_item)

            print("Item added successfully.") #Item is added



        elif choice == "4":

            course = prompt_course_code(manager) #Calls prompt course code manager
            if course is None: #If course isn't found go back
                continue

            items = course.display_items() #Get and display all items in course
            for item in items:
                print(item)

        elif choice == "5":

            course = prompt_course_code(manager) #Calls prompt course code manager
            if course is None: # If no course found go back
                continue

            title = input("Enter item title: ") #Asks for item title

            item = course.find_item(title) #Find the item in the course
            if item is None: #If item does not exist
                print("Item not found.")
            else:
                item.mark_complete() #If it exists mark complete
                print("Item marked successfully.") #Marked completion!


        elif choice == "6":
            course = prompt_course_code(manager)
            if course is None:
                continue
            title = input("Enter item title: ").strip()
            item = course.find_item(title)
            if item is None:
                print("Item not found.")
            else:
                score = float(input("Enter score earned: ").strip())
                item.update_score(score)  # save the new score
                print("Score updated successfully.")

        elif choice == "7":
            course = prompt_course_code(manager)
            if course is None:
                continue
            for line in course.display_pending_items(): # display each pending item
                print(line)


        elif choice == "8":
            # get the course
            course = prompt_course_code(manager)
            if course is None:
                continue
            # calculate grade
            result = course.calculate_grade()
            if result is None:
                print("No graded items yet.")
            else:
                percentage, letter = result
                # print grade info
                print(f"Course Grade for {course.course_code}: {course.course_name}")
                print(f"  Weighted average : {percentage:.2f}%")
                print(f"  Letter grade     : {letter}")
                print("\n  Category breakdown:")
                # loop through each category and print the breakdown
                for category, weight in course.weights.items():
                    graded = [i for i in course.items if i.category == category and i.points_earned is not None]
                    if not graded:
                        print(f"    {category} ({weight}%): No graded items")
                    else:
                        earned = sum(i.points_earned for i in graded)
                        possible = sum(i.points_possible for i in graded)
                        # print the final category breakdown line
                        print(f"    {category} ({weight}%): {earned}/{possible} = {earned / possible * 100:.1f}%")


        elif choice == "9":
            course = prompt_course_code(manager)
            if course is None:
                continue
            # show current weights
            print(f"Current weights for {course.course_code}:")
            for line in course.display_weights():
                print(line)
            print("Enter new weights for each category (must sum to 100).")
            print("Press Enter to keep the current value.")
            # get new weights from user
            new_weights = {}
            for category, current in course.weights.items():
                val = input(f"  {category} (currently {current}%): ").strip()
                new_weights[category] = current if val == "" else float(val)
            # check if valid then update
            total = sum(new_weights.values())
            if abs(total - 100.0) <= 0.01:
                course.set_weights(new_weights)
                print("Weights updated successfully.")
            else:
                print(f"Weights must sum to 100 (got {total:.2f}). No changes made.")

        elif choice == "10":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()