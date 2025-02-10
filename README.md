# Django App Development Notes

## Initial Setup & Backend-First Approach

### Reasoning for Backend-First Development:
- App structured as API-only backend with a separate frontend.
- Prioritising the backend first helps define API endpoints early, avoiding unnecessary UI elements.

## Project Setup & Core Models

### All Model Types:

`User, Student, Teacher, Admin, Course, Lesson, Assignment, Enrollment`

-- `User` can have a connceted object of `Admin`, `Student`, or `Teacher` each granting the different permissions and relational properties.

```python
# User model: AbstractBaseUser subclass
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
```

-- `Course` contains `Lesson`s and `Assignment`s as well as a list of the `Student` objects related as well as the `Teacher`.

```python
# Course models
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, related_name="courses_taught", on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField("Student", related_name="courses_enrolled", blank=True)
    lessons = models.ManyToManyField("Lesson", related_name="courses_with_lessons", blank=True)
    assignments = models.ManyToManyField("Assignment", related_name="courses_with_assignments", blank=True)
    objects = CourseManager()

    def __str__(self):
        return self.title
```

-- `Enrollment` tracks when a `Student` enrolled and can be queried by a `Student` to see which courses they are enrolled in.

```python
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments_in_course", on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

```

### Users & Roles:
- Users can be Admins, Teachers, or Students.
- **Custom User Model**: Extends Django’s `AbstractUser`.
  - Core fields: `username`, `email`, `first_name`, `last_name`, `is_staff`, `is_superuser`, `role`.
  - Django assigns a unique ID to each user.
  - Role-based models (Admin, Teacher, Student) automatically created when a user is created via create) user in course manager.
 
```python
  # Create the related role model based on the user role
  if role == 'student':
      Student.objects.get_or_create(user=user)
  elif role == 'teacher':
      Teacher.objects.get_or_create(user=user)
  elif role == 'admin':
      Admin.objects.get_or_create(user=user)
```

### User Subclasses & Relationships:
- **Student**: One-to-one with `User`, uses signals for cascading deletes. Tracks `enrolled_courses` via many-to-many.
- **Teacher**: Similar to Student model but tracks `teaching_courses`.
- **Admin**: No course tracking; has `is_staff=True` for admin access.

### Courses & Relationships:
- **Key Relationships**:
  - **One-to-One**: Course has one teacher.
  - **Many-to-Many**: Students enroll in multiple courses.
  - **Many-to-Many**: Courses have multiple lessons and assignments.
    
- **Enrollments**: 
  - Seperately store students, enrollment_data, and course. Avoids complexity and nested data. Updates via signals.


### Cascade Deletion & Signals:
- One-to-one relationships use `on_delete=models.CASCADE` to ensure deletion consistency across models.
- The reverse, if needed, happens through signals. i.e.
```python
# Delete user when teacher, student, or admin is deleted
@receiver(post_delete, sender=Teacher)
def delete_teacher_user(sender, instance, **kwargs):
    instance.user.delete()
```

## Serializers & Data Structure

### Serializers:
- Serializers structure API responses and handle data passed to views.
- Display serializers are used for nested data i.e. course in `student.enrolled_courses` displays only title and id.

```python 
class CourseDisplaySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
        ]
```

- Display serializers in the `id` and `title` format are used whenever an object is part of another objects view.
- Avoid excessive nesting to keep responses lightweight.


### ID-Based Data Structure:
- Built around IDs rather than deep nesting (e.g., `course_id` instead of embedding full course objects).
- Keeps responses fast and data consistent.


### User Serializers:
- Users are referenced by `user_id` only instead of their teacher, admin, or student id.
- This simplifies data tracking significantly as by getting user_id you have access to all the information

```python
class StudentSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Student
        fields = ['user_id', 'email', 'first_name', 'last_name', 'enrolled_courses']

    def get_enrolled_courses(self, obj):
        from .courses_serializers import CourseDisplaySerializer
        return CourseDisplaySerializer(obj.enrolled_courses.all(), many=True).data
```
The above gives a pretty good view of my thinking.
1. Using a display serializer to show the title of each course the student is enrolled in.
2. This also lets the frontend grab the ID and use this for fetches.
3. Customizing the serialized ID to it's parent objects id (`user_id`) to simplify.

## Permissions Overview

### Role-Based Access:

- **Students**:
  - **View**: courses, own enrollments
  - **Modify**: Cannot modify data/
  - **Enrollment**: Can enroll/unenroll in courses.

- **Teachers**:
  - **View**: Own courses detail. Can browse Courses.
  - **Modify**: Can manage lessons and assignments in their courses.
  - **Enrollment**: Can’t enroll or unenroll students.
    
- **Admins**:
  - **View**: Full access to all data.
  - **Modify**: Can create, update, delete users, courses, assignments, etc.

### Specific Permissions for Actions:
- Admins and teachers can manage courses and enrolments via the `/course-manager/` endpoint.
- Teachers and students have restricted access based on their role.

### Data Integrity:
- Ensures users can only access data relevant to them:
  - Students can only create or delete their own enrollments.
  - Teachers can only create and edit their own courses.
  - Admins have full access.

Example Custom Permission: 
``` python
class IsSelfStudentOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated and (
            request.user.role == 'student' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):

        if request.method in ['GET','DELETE']:
            return obj.student.user == request.user or request.user.is_staff
        
        return False
```

## 5. View Structure Overview

### General View Architecture:
- **GET**: Fetch list or detail data.
- **POST**: Handle creation or updates.
- **DELETE**: Only used for deleting users.

### Login View:
- Open to all, returns token for authentication.

### User Manager Views:
- **Create User View**: Admins can create users (admins, teachers, students).
- Otherwise, anyone can create a student user (by signing up).
- Only Admins can create non-student users.

### Course Manager View:
- Allows creation, updating, and deletion of courses, lessons, and enrollments through POST requests.
- Actions passed via named actions (e.g., "add_teacher", "enroll_student", "delete_course").
- `course_manager` POST requests is the only way to interact with, create, and delete courses.

### Browse Courses View:
- Displays available courses to authenticated users.

### Other Views:
- Basically all objects have a list view and detail view to display in tables or as solo objects.

## 6. API Endpoints Overview

### 1. Admin Section:
- `/admin/`: Default Django admin interface.

### 2. Authentication:
- `/token/`: POST to obtain an authentication token.

### 3. Accounts:
- `/accounts/login/`: POST for user login (returns token).
- `/accounts/signup/`: POST for user registration.

### 4. User Management:
- `/users/create/`: POST for creating a new user.
- `/users/delete/`: DELETE to delete a user.
- `/user/type/`: GET to fetch the role of the authenticated user.

### 5. Course Manager:
- `/course-manager/`: POST for course management (create, update, delete).

### 6. Users:
- `/students/`: GET to list all students. (admin only)
- `/teachers/`: GET to list all teachers. (admin only)
- `/admins/`: GET to list all admins. (admin only)

### 7. Courses:
- `/courses/`: GET to list all courses. 
- `/courses/browse/`: GET to list simplified course view.
- `/courses/int:pk/`: GET for detailed course info.

### 10. Lessons:
- `/lessons/int:pk/`: GET for lesson details.

### 11. Assignments:
- `/assignments/int:pk/`: GET for assignment details.

### 12. Enrolments:
- `/enrollments/`: GET to list enrollments.
- `/enrollments/int:pk/`: GET for specific enrolment details.

## Example Actions

This is an example flow. An Admin wants to to find a course, check it's Lessons and Assignments, then change which teacher is teaching the course.

### Accessing Course Data

In the frontend, to view a list of courses as an **admin**, navigate to the **Home Page** and click on **Courses**.

This triggers a `GET` request to the following endpoint:

```python
path('courses/', CourseListView.as_view(), name='course-list')
```

### Course List View

The `CourseListView` returns a list of courses. The implementation is as follows:

```python
# Courses
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsSelfTeacherOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(teacher=user.teacher)
```

⚠️ **Note**: While permissions are implemented, they are not relevant here as admins have full access.

### Course Serializer

The course data is serialized efficiently to prevent unnecessary nested data expansion:

```python
class CourseSerializer(serializers.ModelSerializer):
    teacher = UserDisplaySerializer()
    students = UserDisplaySerializer(many=True)
    lessons = LessonDisplaySerializer(many=True)
    assignments = AssignmentDisplaySerializer(many=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'teacher', 
            'students', 
            'lessons', 
            'assignments', 
        ]
```

<img width="1218" alt="Screenshot 2025-02-06 at 22 55 16" src="https://github.com/user-attachments/assets/a7bf613c-42d0-49d5-96ed-96bc0eb97455" />


### Viewing Course Details

Clicking on a course retrieves its **ID** and makes another `GET` request to:

```python
path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail')
```

 Note that each fetch is sent with a token in the header i.e.

```javascript
    const token = localStorage.getItem('token');

    const response = await fetch(`http://localhost:8000/${rowType}/${id}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
        },
    });
```

This returns detailed course information, including associated **lessons** and **assignments**, which are nested. These can be observed by being clicked to make a get request to their detail endpoints.

```python
    # Lessons
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Assignments
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
```

<img width="507" alt="Screenshot 2025-02-06 at 22 55 59" src="https://github.com/user-attachments/assets/5e6e0f49-b5c4-42e2-b3f6-8c05c91a61be" />

### Managing Courses

To modify course data, use the **Course Manager**:

```python
path('course-manager/', CourseManagerView.as_view(), name='course-manager')
```
<img width="459" alt="Screenshot 2025-02-06 at 22 57 49" src="https://github.com/user-attachments/assets/124d892f-6831-4dd2-ac5e-d2690d575c4e" />

For example, to **add a teacher**:
1. Fetch a list of teachers:

    ```python
    path('teachers/', TeacherListView.as_view(), name='teacher-list')
    ```
    Which displays to the user and when they click change...

2. Calls the **Course Manager API**, passing:
   - `course_id` (from the course list)
   - `user_id` (from the serialized teacher list)
   - action: `add_teacher`

   The backend processes the instruction (`add_teacher`) and updates the course.
   
   ```python
           elif action == 'add_teacher':
            teacher = Teacher.objects.get(user_id=user_id)
            course_manager.add_teacher(course, teacher)
            return Response({"message": "Teacher added successfully."}, status=status.HTTP_200_OK)
   ```

This updates the database and the React frontend by making another GET request for the updated object. 

----------------------------------------------------------------------

# Set Up and Usage

## Deploying Server Locally

### Prerequisites
Ensure you have **Python** installed.

### Steps to Deploy Backend Locally

1. **Clone the Repository**
   ```sh
   git clone https://github.com/timm167/lms-backend
   cd lms-backend
   ```

2. **Create a Virtual Environment** (optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```sh
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```sh
   python manage.py runserver
   ```

7. **Access the Application**
   Clone and run the frontend or access with swagger UI using http://localhost:8000/swagger/.

   Link to frontend (including deployment instructions): https://github.com/timm167/lms-frontend


## Technical Stack (Full-Stack)

- **Frontend:**
  - 🟨 JavaScript
  - ⚛️ React
  - ⚡ Vite
  - 🎨 Material UI
  - 📦 NPM (Node Package Manager)
  - 🛠️ React Testing Library + Vitest

  

- **Backend:**
  - 🐍 Python
  - 🚀 Django
  - 🎯 Django REST Framework (DRF)
  - 📜 Swagger UI
  - 🗄️ SQLite
  - 🔒 Django REST Authtoken
  - 🛠️ Django TestCase
  


## Simplified File Structure
```
📁 lms_backend
 ├── 📁 core
 │   ├── 📁 admin
 │   │   ├── 📁 __pycache__
 │   │   │   ├── __init__.cpython-313.pyc
 │   │   ├── admin.py
 │   ├── 📁 apps
 │   │   ├── apps.py
 │   ├── 📁 generate
 │   │   ├── generate.py
 │   ├── 📁 managers
 │   │   ├── course_manager.py
 │   │   ├── user_manager.py
 │   ├── 📁 migrations
 │   │   ├── 0001_initial.py
 │   ├── 📁 models
 │   │   ├── course_models.py
 │   │   ├── enrollment_models.py
 │   │   ├── user_models.py
 │   ├── 📁 serializers
 │   │   ├── admins_serializers.py
 │   │   ├── course_objects_serializers.py
 │   │   ├── courses_serializers.py
 │   │   ├── enrollments_serializers.py
 │   │   ├── students_serializers.py
 │   │   ├── teachers_serializers.py
 │   │   ├── users_serializers.py
 │   ├── 📁 signals
 │   │   ├── courses_signals.py
 │   │   ├── enrollments_signals.py
 │   │   ├── users_signals.py
 │   ├── 📁 tests
 │   │   ├── test_deletions.py
 │   │   ├── test_enrollments.py
 │   │   ├── test_models.py
 │   │   ├── test_permissions.py
 │   ├── 📁 views
 │   │   ├── courses_views.py
 │   │   ├── enrollments_views.py
 │   │   ├── login_views.py
 │   │   ├── 📁 manager_views
 │   │   │   ├── course_manager_views.py
 │   │   │   ├── user_manager_views.py
 │   │   ├── 📁 permissions
 │   │   │   ├── course_manager_permissions.py
 │   │   │   ├── students_permissions.py
 │   │   │   ├── teachers_permissions.py
 │   │   │   ├── user_validation.py
 │   │   ├── users_views.py
 ├── 📁 lms_backend
 │   ├── asgi.py
 │   ├── settings.py
 │   ├── urls.py
 │   ├── wsgi.py
 ├── 📄 db.sqlite3
 ├── 📄 manage.py
 ├── 📄 README.md
```
