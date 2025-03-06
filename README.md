<div align="center">
  
### Label Mapping

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

## Datasets

### 1. WEED25 Dataset  
[WEED25 Dataset Publication](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1053329/full)

#### **🌿 Broadleaf Weeds**
- **Pigweed:** `742` images  
- **White Smartweed:** `671` images  
- **Chinese Knotweed:** `391` images  
- **Horseweed:** `191` images _(Check augmentation for this class)_  
- **Velvetleaf:** `622` images  
- **Cocklebur:** `745` images  
- **Goosefoot:** `593` images  
- **Purslane:** `730` images  

#### **🌱 Grass Weeds**
- **Barnyard Grass:** `563` images  
- **Crabgrass:** `594` images  
- **Green Foxtail:** `552` images _(High-quality field images)_

---

#### YOLO Version of WEED25
- **Total Images:** `6,394` images
- **Image Distribution:**
  - 🌿 **Broadleaf Weeds:** `4,716` images  
  - 🌱 **Grass Weeds:** `1,677` images  
- **Bounding Boxes:**
  - 🌿 **Broadleaf Weed Images:** `5,5588` bounding boxes  
  - 🌱 **Grass Weed Images:** `1,961` bounding boxes  
  - Each image may contain **multiple bounding boxes**, but every image is associated with a **single unique label**.
- **Backgrounds(empty image):**
  - ```pigweed (574).txt```
---

### 2. Sorghumweed Dataset  
[Sorghumweed Dataset Publication](https://data.mendeley.com/datasets/y9bmtf4xmr/1)

This dataset supports both classification and segmentation tasks with high-quality images.

### Sorghumweed Dataset – Classification
- **Total Images:** `4,312`
- **Class Distribution:**
  - 🌿 **Broadleaf Weeds:** `1,441` images  
  - 🌱 **Grass Weeds:** `1,467` images  
> *Note:* These images require manual labeling for classification.

### YOLO Version of Sorghumweed Dataset – Segmentation
- **Total Images:** `253` (containing both broadleaf and grass weeds)
- **Images with a Single Unique Label:**
  - 🌿 **Broadleaf Weeds:** `35` images  
  - 🌱 **Grass Weeds:** `8` images  
- **Images with Both Labels:** `140` images
- **Overall Image Count per Label:**
  - 🌿 **Broadleaf Weeds:** `175` images  
  - 🌱 **Grass Weeds:** `148` images
- **Empty Images (No Annotations):** `69` images
- **Number of Bounding Boxes per Label:**
  - 🌿 **Broadleaf Weeds:** `2,785` bounding boxes  
  - 🌱 **Grass Weeds:** `609` bounding boxes

---

## 3. Crop-and-Weed Dataset
 [Crop and Weed Publication](https://github.com/cropandweed/cropandweed-dataset)
#### YOLO Version of Crop-and-Weed Dataset – Statistics

- **Total Images:** `4,473`  
- **Images with a Single Unique Label:** `3,212`  
- **Images with Multiple Labels:** `1,261`

**Per Label Details:**

- **🌿 Broadleaf (0):**  
  - Images: `1,303`  
  - Single-label Images: `761`  
  - Bounding Boxes: `8,127`

- **🌱 Grass (1):**  
  - Images: `2,162`  
  - Single-label Images: `1,124`  
  - Bounding Boxes: `15,146`

- **🌽 Corn (2):**  
  - Images: `1,834`  
  - Single-label Images: `980`  
  - Bounding Boxes: `6,018`

- **🌻 Sunflower (4):**  
  - Images: `590`  
  - Single-label Images: `347`  
  - Bounding Boxes: `1,879`

---

### [Broad-Leaved Dock Dataset](https://www.kaggle.com/datasets/gavinarmstrong/open-sprayer-images/data)

#### **🌿 Broadleaf Weeds**
- **Broad-leaved docks (Rumex obtusifolius)** are considered a broadleaf weed.
- **Contains:**  
  - `1,307` images of broad-leaved docks  
  - `5,392` images of non broad-leaved docks (background & other elements)
- **Annotation Status:**
  - No annotations provided (requires manual labeling using bounding boxes)
- **Data Quality:**  
  - Many images are `shit`; however, select images may serve as useful background examples.

---