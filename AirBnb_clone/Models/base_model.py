import uuid
import datetime


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at

    def save(self):
        """Update the updated_at timestamp to the current time."""
        from Models import storage
        self.updated_at = datetime.datetime.now()
        storage.new(self)

    def __str__(self):
        """Return string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        my_obj_dict = self.__dict__.copy()
        my_obj_dict["__class__"] = self.__class__.__name__
        my_obj_dict["created_at"] = self.created_at.isoformat()
        my_obj_dict["updated_at"] = self.updated_at.isoformat()
        return my_obj_dict