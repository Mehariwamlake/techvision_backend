from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Courses" 

    def __str__(self):
        return self.name



class Product(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    STATUS_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False) 
    description = models.TextField(null=False) 
    imageUrl = models.TextField(null=False)  
    price = models.IntegerField(null=False)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRIVATE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products" 

    def __str__(self):
        return self.name
    
    def is_free(self):
        """Return True if the product is free (price == 0)"""
        return self.price == 0

class CourseSection(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    STATUS_CHOICES = [(PUBLIC, "Public"), (PRIVATE, "Private")]

    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRIVATE)
    order = models.IntegerField(null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_sections"

class Lesson(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    PREVIEW = "preview"
    STATUS_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
        (PREVIEW, "Preview"),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)  # Allows optional descriptions
    youtube_video_id = models.TextField(null=False)  # Equivalent to `youtubeVideoId`
    order = models.IntegerField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRIVATE)
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name="lessons")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lessons"  

    def __str__(self):
        return self.name
    

class CourseProduct(models.Model):
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name="course_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="course_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_products"
        unique_together = ("course", "product")

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_accesses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="user_accesses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_course_access"
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_user_course_access")
        ]


class UserLessonComplete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="completed_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="completed_by_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_lesson_complete"
        unique_together = ("user", "lesson")  # Equivalent to Drizzle's primary key constraint

    def __str__(self):
        return f"{self.user} completed {self.lesson}"

class Purchase(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.IntegerField(null=False)
    product_details = models.JSONField(null=False)  # Stores product details as JSON
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name="purchases")
    chapa_session_id = models.TextField(unique=True, null=False)
    refunded_at = models.DateTimeField(null=True, blank=True)  # Nullable timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "purchases" 

    def __str__(self):
        return f"Purchase {self.id} - {self.user}"
    def associate_courses_with_user(self):
        """When a product is purchased, associate all courses with the user."""
        courses = self.product.course_products.all().values_list('course', flat=True)
        for course_id in courses:
            course = Course.objects.get(id=course_id)
            # Create a record for user access to this course
            UserCourseAccess.objects.get_or_create(user=self.user, course=course)
    
class Apply(models.Model):
    Front_end = "Front_end"
    DSA = "DSA"
    Back_end = "Back_end"

    STATUS_CHOICES = [
        (Front_end, "Front_end"),
        (DSA, "DSA"),
        (Back_end, "Back_end"),
    ]

    Inperson = "In-person"
    Online = "Online"
    STATUS_CHOICES_Schedule =[
            (Inperson, "In-person"),
            (Online, "Online")
        ]
    

    name = models.TextField(null=False)
    email = models.TextField(null=False)
    phoneNumber = models.TextField(null=False)
    interstedProgram = models.CharField(max_length=10, choices=STATUS_CHOICES, default=Front_end)
    schedule = models.CharField(max_length=10, choices=STATUS_CHOICES_Schedule, default=Online)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Candidates(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    skills = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Candidates" 

    def __str__(self):
        return self.name
    
class Company(models.Model):
    id= models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    location = models.TextField(null=False)
    class Meta:
        db_table = 'companys'
    def __str__(self):
        return self.name
    
class Department(models.Model):
    id= models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    companyId = models.ForeignKey(Company, on_delete=models.RESTRICT, related_name="departments")
    class Meta:
        db_table = "departments"
    def __str__(self):
        return self.name
    
class Employee(models.Model):
    id= models.BigAutoField(primary_key=True)
    name = models.TextField(null=True)
    salary = models.TextField(null=True)
    departmentId = models.ForeignKey(Department, on_delete=models.RESTRICT, related_name="employees", null=True)
    candidateId = models.ForeignKey(Candidates, on_delete=models.RESTRICT, related_name='candidates', null=True)
    class Meta:
        db_table = "employees"
    
    def __str__(self):
        return self.name