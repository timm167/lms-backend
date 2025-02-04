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
