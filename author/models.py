from django.db import models


class Author(models.Model):
    """
    This class represents an Author.
    Attributes:
    -----------
    - name: Describes the first name of the author (max_length=20).
    - surname: Describes the last name of the author (max_length=20).
    - patronymic: Describes the middle name of the author (max_length=20).
    - books: A ManyToMany relationship with the Book model.
    """
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20, blank=True)
    patronymic = models.CharField(max_length=20, blank=True)
    books = models.ManyToManyField('book.Book', related_name='book_authors', blank=True)  # Updated related_name
    id = models.AutoField(primary_key=True)
    class Meta:
        permissions = [
            ("can_view_authors", "Can view authors"),
            ("can_edit_authors", "Can edit authors"),
        ]

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __repr__(self):
        """
        Magic method to display the class name and ID of the Author.
        """
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        """
        Retrieves an author by their ID.
        :param author_id: The ID of the author to find.
        :return: The Author object or None if not found.
        """
        try:
            return Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        """
        Deletes an author by their ID.
        :param author_id: The ID of the author to delete.
        :return: True if deleted, False otherwise.
        """
        try:
            author = Author.objects.get(pk=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        """
        Creates a new Author object and saves it to the database.
        :param name: Author's first name.
        :param surname: Author's last name.
        :param patronymic: Author's middle name.
        :return: The new Author object.
        """
        if name and len(name) <= 20 and surname and len(surname) <= 20 and patronymic and len(patronymic) <= 20:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author

    def to_dict(self):
        """
        Converts an Author object into a dictionary format.
        :return: Dictionary with author's details.
        """
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    def update(self, name=None, surname=None, patronymic=None):
        """
        Updates the Author's details.
        :param name: New name for the author (optional).
        :param surname: New surname for the author (optional).
        :param patronymic: New patronymic for the author (optional).
        """
        if name and len(name) <= 20:
            self.name = name
        if surname and len(surname) <= 20:
            self.surname = surname
        if patronymic and len(patronymic) <= 20:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        """
        Returns all authors as a QuerySet.
        :return: QuerySet of all authors.
        """
        return Author.objects.all()
