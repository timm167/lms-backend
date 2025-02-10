from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Course, Student, Teacher
from core.managers import CourseManager
from ..permissions.course_manager_permissions import check_course_manager_permissions

default_video_url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4'


class CourseManagerView(APIView):
    
    def post(self, request, *args, **kwargs):
        # Get the course manager
        course_manager = CourseManager()

        # Get the action
        action = request.data.get('action')
        
        # Common fields
        course_id = request.data.get('course_id')
        if course_id:
            course = Course.objects.get(id=course_id)
        
        user_id = request.data.get('user_id', None)
        if not user_id:
            user_id = request.user.id
        item_id = request.data.get('item_id', None)
        title = request.data.get('title', None)
        content = request.data.get('content', None)
        description = request.data.get('description', None)

        #------------------------------------------------------------#

        # Check if user is authenticated and has permission to perform the action
        if request.user.is_authenticated == False:
            return Response({"error": "You must be logged in to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        if action == 'create_course':
            course = None
        if not check_course_manager_permissions(request.user, user_id, action, course):
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)


        #------------------------------------------------------------#
        # Create/Delete Course
        #------------------------------------------------------------#

        if action == 'create_course':
            teacher = request.user.teacher if request.user.role == 'teacher' else Teacher.objects.get(user_id=request.data.get('user_id'))
            course_manager.create_course(title, description, teacher)
            return Response({"message": "Course created successfully."}, status=status.HTTP_201_CREATED)

        elif action == 'delete_course':
            course_manager.delete_course(course)
            return Response({"message": "Course deleted successfully."}, status=status.HTTP_200_OK)
        

        #------------------------------------------------------------#
        # Lessons
        #------------------------------------------------------------#

        elif action == 'add_lesson':
            course_manager.add_lesson(course, title, content, video_url=default_video_url) 
            return Response({"message": "Lesson created successfully."}, status=status.HTTP_201_CREATED)
        
        elif action == 'delete_lesson':
            lesson = course.lessons.get(id=item_id)
            course_manager.delete_lesson(course, lesson)
            return Response({"message": "Lesson deleted successfully."}, status=status.HTTP_200_OK)
        

        #------------------------------------------------------------#
        # Assignments
        #------------------------------------------------------------#

        elif action == 'add_assignment':
            due_date = request.data.get('due_date', None)
            max_score = request.data.get('max_score', None)
            pass_score = request.data.get('pass_score', None)
            course_manager.add_assignment(course, title, description, due_date, max_score, pass_score)
            return Response({"message": "Assignment created successfully."}, status=status.HTTP_201_CREATED)
        
        elif action == 'delete_assignment':
            assignment = course.assignments.get(id=item_id)
            course_manager.delete_assignment(course, assignment)
            return Response({"message": "Assignment deleted successfully."}, status=status.HTTP_200_OK)
        
        #------------------------------------------------------------#
        # Enrollments
        #------------------------------------------------------------#
        
        elif action == 'enroll_student':
            student = Student.objects.get(user_id=user_id)
            course_manager.enroll_student(course, student)
            return Response({"message": "Student enrolled successfully."}, status=status.HTTP_200_OK)
        
        elif action == 'unenroll_student':
            student = course.students.get(user_id=user_id)
            course_manager.unenroll_student(course, student)
            return Response({"message": "Student unenrolled successfully."}, status=status.HTTP_200_OK)

        #------------------------------------------------------------#
        # Add/Remove Teachers
        #------------------------------------------------------------#

        elif action == 'add_teacher':
            teacher = Teacher.objects.get(user_id=user_id)
            course_manager.add_teacher(course, teacher)
            return Response({"message": "Teacher added successfully."}, status=status.HTTP_200_OK)
        
        elif action == 'remove_teacher':
            teacher = Teacher.objects.get(user_id=user_id)
            course_manager.remove_teacher(course, teacher)
            return Response({"message": "Teacher removed successfully."}, status=status.HTTP_200_OK)
        
        #------------------------------------------------------------#
        # Return error for invalid actions
        #------------------------------------------------------------#
        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
