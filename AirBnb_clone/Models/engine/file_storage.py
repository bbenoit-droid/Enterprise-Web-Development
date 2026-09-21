import json
from Models.base_model import BaseModel
class FileStorage:
    """This class serializes instances to a JSON file and deserializes JSON file to instances."""   
    __file_path = "file.json"
    __objects = {}


    def all(self):
        """Return the dictionary of all objects."""
        return self.__objects
    def new(self, obj):
        """Add a new object to the storage dictionary."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize the objects to the JSON file."""
        with open(self.__file_path, 'w') as file:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, file)

    def reload(self):
        """Deserialize the JSON file to objects."""
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    cls = globals()[class_name]
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass        