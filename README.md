<div align="center">

# 🌱 GREEN-MELON

[![Lint and Format](https://github.com/dinjazelena98/green-melon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/dinjazelena98/green-melon/actions/workflows/ci.yml)

## Target Mapping

🌿 **Broadleaf** → `0`  
🌱 **Grass** → `1`  
🌽 **Corn** → `2`  
🌾 **Wheat** → `3`  
🌻 **Sunflower** → `4`  

</div>

---

## Models for Each Target Crop vs. Weed Species
- **Broadleaf, Grass, and Wheat**
- **Broadleaf, Grass, and Corn**
- **Broadleaf, Grass, and Sunflower**

---

## DATASETS

### [WEED25 Dataset](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1053329/full)

#### **🌿 Broadleaf Weeds**
- **Pigweed** → `744` images
- **White Smartweed** → `670` images
- **Chinese Knotweed** → `391` images
- **Horseweed** → `190` images _(Check augmentation for this class)_
- **Velvetleaf** → `623` images
- **Cocklebur** → `750` images
- **Goosefoot** → `594` images
- **Purslane** → `730` images

#### **🌱 Grass Weeds**
- **Barnyard Grass** → `564` images
- **Crabgrass** → `595` images
- **Green Foxtail** → `553` images _(High-quality images in the field)_

---

### YOLO Version of WEED25

- **Total Images:** `6,394` images of broadleaf and grass weeds.
- **Image Distribution:**
  - 🌿 **Broadleaf Weeds:** `4,717` images
  - 🌱 **Grass Weeds:** `1,677` images
- **Bounding Boxes:**
  - 🌿 **Broadleaf Weed Images:** `5,590` bounding boxes
  - 🌱 **Grass Weed Images:** `1,961` bounding boxes
- **Annotation Details:**  
  Each image may contain **multiple bounding boxes**, but every image is associated with a **single unique label**.

---

### [BROAD-LEAVED-DOCK Dataset](https://www.kaggle.com/datasets/gavinarmstrong/open-sprayer-images/data)

#### **🌿 Broadleaf Weeds**
- **Broad-leaved docks (Rumex obtusifolius)** are considered a broadleaf weed.
- **Contains:**  
  - `1,307` images of broad-leaved docks.  
  - `5,392` images of non broad-leaved docks (background & other elements).
- **Annotation Status:**
  - No annotations provided.
  - Requires manual labeling (bounding boxes).
- **Data Quality:**  
  - Most images are **shit**, but some could be useful.
  - Check non broad-leaved dock images for potential **background images**.

---

### [Sorghum-Weed-Dataset](https://data.mendeley.com/datasets/y9bmtf4xmr/1) _(TODO)_

---

### [CROP-AND-WEED Dataset](https://github.com/cropandweed/cropandweed-dataset) _(TODO)_

---