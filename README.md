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

### [WEED25 Dataset](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1053329/full)

#### **🌿 Broadleaf Weeds**
- **Pigweed:** `744` images  
- **White Smartweed:** `670` images  
- **Chinese Knotweed:** `391` images  
- **Horseweed:** `190` images _(Check augmentation for this class)_  
- **Velvetleaf:** `623` images  
- **Cocklebur:** `750` images  
- **Goosefoot:** `594` images  
- **Purslane:** `730` images  

#### **🌱 Grass Weeds**
- **Barnyard Grass:** `564` images  
- **Crabgrass:** `595` images  
- **Green Foxtail:** `553` images _(High-quality field images)_

---

#### YOLO Version of WEED25
- **Total Images:** `6,394` images (broadleaf and grass weeds)  
- **Image Distribution:**
  - 🌿 **Broadleaf Weeds:** `4,717` images  
  - 🌱 **Grass Weeds:** `1,677` images  
- **Bounding Boxes:**
  - 🌿 **Broadleaf Weed Images:** `5,590` bounding boxes  
  - 🌱 **Grass Weed Images:** `1,961` bounding boxes  
- **Annotation Details:**  
  Each image may contain **multiple bounding boxes**, but every image is associated with a **single unique label**.

---

### [Sorghumweed Dataset](https://data.mendeley.com/datasets/y9bmtf4xmr/1)

#### Sorghumweed Dataset Classification
- **Total Images:** `4,312` images  
- **Class Distribution:**
  - **🌿Broadleaf Weeds:** `1,441` images
  - **🌱Grass Weeds:** `1,467` images
- High quality images but would requiry manual labeling.

#### YOLO Version of Sorghumweed Dataset Segmentation

- **Total Images:** `253` images (broadleaf and grass weeds)

- **Images with a Unique Label (per label):**
  - **🌿 Broadleaf Weeds:** `35` images  
  - **🌱 Grass Weeds:** `8` images  

- **Images with Both Labels:** `140` images

- **Overall Image Count per Label:**
  - **🌿 Broadleaf Weeds:** `175` images  
  - **🌱 Grass Weeds:** `148` images

- **Empty Images (No Annotations):** `69` images

- **Number of Bounding Boxes per Label:**
  - **🌿 Broadleaf Weeds:** `2785` bounding boxes  
  - **🌱 Grass Weeds:** `609` bounding boxes

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

### [Crop-and-Weed Dataset](https://github.com/cropandweed/cropandweed-dataset)

#### YOLO Version of Crop-and-Weed Dataset

- Total Images: `6,990` images

- **Bounding Box Count per Label:**
  - **🌿 Broadleaf Weeds:** 37,501 boxes  
  - **🌱 Grass Weeds:** 21,758 boxes  
  - **🌽 Corn:** 6,162 boxes  
  - **🌻 Sunflower:** 1,916 boxes  
  *(Note: Wheat (3) did not yield any annotations.)*

- **Image Count per Label:**
  - **🌿 Broadleaf Weeds:** found in 5,098 images  
  - **🌱 Grass Weeds:** found in 3,000 images  
  - **🌽 Corn:** found in 1,882 images  
  - **🌻 Sunflower:** found in 607 images

---