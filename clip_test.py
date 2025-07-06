import clip
import torch
from PIL import Image

model, preprocess = clip.load("ViT-B/32", device="cpu")
image = preprocess(Image.open("myimage.jpg")).unsqueeze(0).to("cpu")
text = clip.tokenize(["a photo of a cat", "a photo of a dog"]).to("cpu")

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

similarity = (image_features @ text_features.T).softmax(dim=-1)
print(similarity)
