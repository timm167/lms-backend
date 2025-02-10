def check_course_manager_permissions(user, user_id, action, course=None):

    # Create course: Admins and teachers can create courses
    if action == 'create_course':
        return user.is_staff or user.role == 'teacher'
    
    # Delete course: Only admins can delete courses
    elif action == 'delete_course':
        return user.is_staff
    
    # Enroll student: Admins and students can enroll students
    elif action == 'enroll_student':
        return is_self_student(user, user_id)
        
    # Unenroll student: Admins and students can unenroll students
    elif action == 'unenroll_student': 
        return is_self_student(user, user_id)
    
    # Add teacher: Admins can add teachers
    elif action == 'add_teacher':
        return user.is_staff
    
    # Remove teacher: Admins can remove teachers
    elif action == 'remove_teacher':
        return user.is_staff
    
    # Add lesson: Admins and teachers can add lessons
    elif action == 'add_lesson':
        return is_self_teacher(user, course)
    
    # Remove lesson: Admins and teachers can remove lessons
    elif action == 'delete_lesson':
        return is_self_teacher(user, course)
    
    # Add assignment: Admins and teachers can add assignments
    elif action == 'add_assignment':
        return is_self_teacher(user, course)
    
    # Remove assignment: Admins and teachers can remove assignments
    elif action == 'delete_assignment':
        return is_self_teacher(user, course)

    # Default case for undefined actions
    return False


def is_self_teacher(user, course):
    if user.role == 'teacher':
        return course.teacher == user.teacher
    return user.is_staff or user.role == 'teacher'

def is_self_student(user, user_id):
    if user.role == 'student':
        return user.id == user_id
    return user.is_staff