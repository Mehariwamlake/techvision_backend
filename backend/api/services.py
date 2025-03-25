from django.db import transaction
from .models import CourseSection

def get_next_course_section_order(course_id):
    """
    Get the next available order for a CourseSection within a course.
    """
    last_section = CourseSection.objects.filter(course_id=course_id).order_by("-order").first()
    return (last_section.order + 1) if last_section else 0


def insert_section(course_id, name, status="private"):
    """
    Insert a new CourseSection into the database.
    """
    order = get_next_course_section_order(course_id)
    section = CourseSection.objects.create(
        name=name,
        status=status,
        order=order,
        course_id=course_id
    )
    return section


def update_section(section_id, data):
    """
    Update a CourseSection with the given data.
    """
    try:
        section = CourseSection.objects.get(id=section_id)
        for key, value in data.items():
            setattr(section, key, value)
        section.save()
        return section
    except CourseSection.DoesNotExist:
        raise ValueError("Section not found")


def delete_section(section_id):
    """
    Delete a CourseSection by ID.
    """
    try:
        section = CourseSection.objects.get(id=section_id)
        section.delete()
        return section
    except CourseSection.DoesNotExist:
        raise ValueError("Section not found")


def update_section_orders(section_ids):
    """
    Update section orders based on the given list of section IDs.
    """
    with transaction.atomic():
        for index, section_id in enumerate(section_ids):
            CourseSection.objects.filter(id=section_id).update(order=index)
