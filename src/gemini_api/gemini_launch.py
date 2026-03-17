import google.generativeai as genai
# from google import genai
from PIL import Image
import json
import re
import cv2
genai.configure(api_key="AIzaSyAJOfx9fy2PpU9f7Nh_IrnjFn1yso0KASI")

model = genai.GenerativeModel("gemini-3-flash-preview")

img = Image.open("gazebo.png")


# prompt = """
# Detect objects in this image.

# Return ONLY JSON:
# {
#  "objects":[
#    {"name":"object","center":[x,y]}
#  ]
# }
# """

# response = model.generate_content([prompt, img])

# text = response.text

# def extract_json(text):
#     text = re.sub(r"```json|```", "", text).strip()
#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     return json.loads(match.group())

# data = extract_json(text)

# print(data)

prompt = """
Detect objects in the image.

Return ONLY JSON:
{
 "objects":[
   {"name":"object","bbox":[xmin,ymin,xmax,ymax]}
 ]
}

Coordinates must be normalized between 0 and 1.
"""

response = model.generate_content([prompt, img])
text = re.sub(r"```json|```", "", response.text).strip()
data = json.loads(re.search(r"\{.*\}", text, re.DOTALL).group())

frame = cv2.imread("gazebo.png")
h, w = frame.shape[:2]

for obj in data["objects"]:
    xmin = int(obj["bbox"][0] * w)
    ymin = int(obj["bbox"][1] * h)
    xmax = int(obj["bbox"][2] * w)
    ymax = int(obj["bbox"][3] * h)

    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (0,255,0), 2)
    cv2.putText(frame, obj["name"], (xmin, ymin-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

cv2.imshow("Gemini Detection", frame)
cv2.waitKey(0)