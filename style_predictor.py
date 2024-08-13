import platform
import pathlib
plt = platform.system()
pathlib.WindowsPath = pathlib.PosixPath
import fastai
from fastai.vision.all import PILImage
from fastai.data.block import DataBlock
from fastai.vision.all import *
from fastai.text.all import *

def custom_get_y(x):
    style_name = Path(x).parent.name
    return class_mapping.get(style_name, 0)  


class ImageStylePredictor:
    def __init__(self, model_path="./architecture_classifier.pkl"):
        self.class_mapping = {
            'Achaemenid architecture': 0,
            'American craftsman style': 1,
            'American Foursquare architecture': 2,
            'Ancient Egyptian architecture': 3,
            'Art Deco architecture': 4,
            'Art Nouveau architecture': 5,
            'Baroque architecture': 6,
            'Bauhaus architecture': 7,
            'Beaux-Arts architecture': 8,
            'Brutalism architecture': 9,
            'Byzantine architecture': 10,
            'Chicago school architecture': 11,
            'Classical': 12,
            'Colonial architecture': 13,
            'Deconstructivism': 14,
            'Edwardian architecture': 15,
            'Georgian architecture': 16,
            'Gothic architecture': 17,
            'Greek Revival architecture': 18,
            'International style': 19,
            'Japanese': 20,
            'Novelty architecture': 21,
            'Palladian architecture': 22,
            'Postmodern architecture': 23,
            'Queen Anne architecture': 24,
            'Romanesque architecture': 25,
            'Russian Revival architecture': 26,
            'Tudor Revival architecture': 27
        }
        self.learn = load_learner(cpu=True, fname=model_path)
        self.final_size = 224
        self.transforms = [*aug_transforms(min_scale=0.5, size=self.final_size), Normalize.from_stats(*imagenet_stats)]
        self.plt = platform.system()

    def predict_style(self, img):
        img = PILImage.create(img)
        pred_class, pred_idx, probs = self.learn.predict(img)
        predicted_style = list(self.class_mapping.keys())[int(pred_class)]
        return { 'predicted_style': predicted_style, 'confidence': float(probs[pred_idx]) }

if __name__ == '__main__':
    predictor = ImageStylePredictor()
    image_paths = [
        "./test_images/warsaw_skyscrapers.jpg",
        "./test_images/church_of_St.Wojciech.jpeg",
        "./test_images/egyptian_pyramids.jpg",
        "./test_images/byzantine.jpg"
    ]
    style_probabilities = {}

    for img_path in image_paths:
        style_probabilities[img_path] = (predictor.predict_style(img_path))

    print(style_probabilities)

# Output
# {
#     './test_images/warsaw_skyscrapers.jpg': { 'predicted_style': 'International style', 'confidence': 0.6540950536727905 },
#     './test_images/church_of_St.Wojciech.jpeg': { 'predicted_style': 'Gothic architecture', 'confidence': 0.5576282739639282 },
#     './test_images/egyptian_pyramids.jpg': { 'predicted_style': 'Ancient Egyptian architecture', 'confidence': 0.49120032787323 },
#     './test_images/byzantine.jpg': { 'predicted_style': 'Byzantine architecture', 'confidence': 0.5188705921173096 }
# }