from PIL import Image
import numpy as np

paths = [
    "/Users/sathwikbadda/Assigment/Manim-Assignment/images/ace_disease_1.png",
    "/Users/sathwikbadda/Assigment/Manim-Assignment/images/ace_disease_2.png",
    "/Users/sathwikbadda/Assigment/Manim-Assignment/images/ace_disease_3.png"
]

for p in paths:
    img = Image.open(p).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    # find rows and cols where alpha > 0
    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]] if np.any(rows) else (0, 0)
    cmin, cmax = np.where(cols)[0][[0, -1]] if np.any(cols) else (0, 0)
    print(f"{p.split('/')[-1]}: visually active area y=[{rmin}, {rmax}], x=[{cmin}, {cmax}], height={rmax-rmin}")
