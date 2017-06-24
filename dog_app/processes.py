
from utils import dog_detector_from_path, face_detector_from_path, ResNet50_predict_breed_from_path

def dog_breed_guesser_from_path(image_file_path):

    is_dog = dog_detector_from_path(image_file_path)
    is_human = face_detector_from_path(image_file_path)
    # if is_dog:
    #     dog_in_img = "I think this is a dog"
    # if is_human:
    #     human_in_img = "I think this is a human"
    dog_class = ResNet50_predict_breed_from_path(image_file_path)
    if is_human and not is_dog:
        return "this is a human, and it resembles {}".format(dog_class)
    if not is_human and is_dog:
        return "the dog is a {}".format(dog_class)
    if is_human and is_dog:
        return "this is either human looks like a dog or a dog looks like a human, it looks like {}".format(dog_class)
    if not is_human and not is_dog:
        return "this looks neither like human nor dog, it looks like {}".format(dog_class)


if __name__ == "__main__":
    print(dog_breed_guesser_from_path('tmp/image.jpg'))
