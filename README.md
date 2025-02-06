# Django App Development Notes

## 1. Initial Setup & Backend-First Approach

### Reasoning for Backend-First Development:
- App structured as API-only backend with a separate frontend.
- Prioritising the backend first helps define API endpoints early, avoiding unnecessary UI elements.

## 2. Project Setup & Core Models

### Users & Roles:
- Users can be Admins, Teachers, or Students.
- **Custom User Model**: Extends Django’s `AbstractUser`.
  - Core fields: `username`, `email`, `first_name`, `last_name`, `is_staff`, `is_superuser`, `role`.
  - Django assigns a unique ID to each user.
  - Role-based models (Admin, Teacher, Student) automatically created when a user is created via create)user in course manager.

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
- The reverse, if needed, happens through signals.

## 3. Serializers & Data Structure

### Serializers:
- Serializers structure API responses and handle data passed to views.
- Display serializers are used for nested data i.e. course in `student.enrolled_courses` displays only title and id.
- This method is used whenever an object is part of another objects view.
- Avoid excessive nesting to keep responses lightweight.

### ID-Based Data Structure:
- Built around IDs rather than deep nesting (e.g., `course_id` instead of embedding full course objects).
- Keeps responses fast and data consistent.

### User Serializers:
- Users referenced by `user_id`, ensuring consistency across the system.
- This simplifies data tracking significantly as by getting user_id you have access to all the information
- Other objects simply user their own `id`

### Course based logic:
- The idea was to use a course based logic. Users and Courses exist and have various properties and relationships with each other.
- These two object types are the only two 'core' object types.
- Enrollments help track some of these relationships (between courses and users). Others are tracked only using single layer nesting.

### Course & Enrollment Serializers:
- Course serializers use display serializers to avoid over-nesting.
- **Browse Course Serializer**: Useful for browsing courses.
- **Enrollment Serializer**: Displays user and course with a shortened date format.

## 4. Course Views and Permissions

### Course/Enrollments Permissions Overview:
- **Teachers** can only alter their own courses.
- **Students** can browse courses freely.
- Custom query sets mean that when not 'browsing' teachers only view the courses they teach.
- Students can only view their own enrollments but can see who is signed up for a given course. 

### Querysets & Custom Permissions:
- Custom permissions are set for each action 

## 5. View Structure Overview

### General View Architecture:
- **GET**: Fetch list or detail data.
- **POST**: Handle creation or updates.
- **DELETE**: Only used for deleting users.

### Login View:
- Open to all, returns token for authentication.

### User Views:
- **Create User View**: Admins create users (teachers, students).
- Otherwise, anyone can create a user (by signing up).
- Only Admins can create non-student users.
- **Get User Type View**: Returns the role of the user. (Useful for ui immediately creating custom displays for users)

### Course Manager View:
- Allows creation, updating, and deletion of courses, lessons, and enrolments through POST requests.
- Actions passed via named actions (e.g., "add_teacher", "enroll_student").
- This is the central object for performing any kinds of actions relating to learning i.e. non user creation/deletion.
- Should be the only source of interaction with courses through POST. 

### Browse Courses View:
- Displays available courses to authenticated users.

### Enrollment View:
- Allows admins to see all enrollments. Allows users to view their own enrollments.

## 6. API Endpoints Overview

### User Management Endpoints:
- `/user/`: Create and view users.
  - `POST`: Create new users.
  - `GET`: Retrieve user details.

### Course Management Endpoints(GET):
- `/courses/`: Display restricted courses.
- `/courses/browse/`: Public course list.
- `/course/`: View course objects in focus.

### Enrollment Management Endpoints:
- `/enrollments/`: `GET`

## 7. Permissions File

All views have custom permissions.

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
- `/enrolments/`: GET to list enrollments.
- `/enrolments/int:pk/`: GET for specific enrolment details.

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
  - Students can only see their courses.
  - Teachers can only access their courses.
  - Admins have full access.

## Example Actions

An example flow would be for an Admin to find a course, check it's Lessons and Assignments, then change which teacher is teaching the course.

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

```
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

---


## Deploying Server Locally

To run the server locally using `requirements.txt`, follow these steps:

### Prerequisites
Ensure you have **Python** installed.

### Steps to Deploy Backend Locally

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-folder>
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

   Link to fronted (including deployment instructions): https://github.com/timm167/lms-frontend
