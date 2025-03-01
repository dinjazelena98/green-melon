<div align="center">

# GREEN-MELON

[![Lint and Format](https://github.com/dinjazelena98/green-melon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/dinjazelena98/green-melon/actions/workflows/ci.yml)

</div>

<div align="center">

<h2 style="font-family: monospace; font-size: 1.5em;">
{
    "broadleaf": 0,
    "grass": 1,
    "corn": 2,
    "wheat": 3,
    "sunflower": 4
}
</h2>

</div>

Models for each target crop versus weed species:

- **Broadleaf, Grass, and Wheat**
- **Broadleaf, Grass, and Corn**
- **Broadleaf, Grass, and Sunflower**

## DATASETS
---

### [WEED25 Dataset](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1053329/full)

#### **BROADLEAF**
- **Pigweed** → 744 images
- **White Smartweed** → 670 images
- **Chinese Knotweed** → 391 images
- **Horseweed** → 190 images _(Check augmentation for this class)_
- **Velvetleaf** → 623 images
- **Cocklebur** → 750 images
- **Goosefoot** → 594 images
- **Purslane** → 730 images

#### **GRASS**
- **Barnyard Grass** → 564 images
- **Crabgrass** → 595 images
- **Green Foxtail** → 553 images _(High-quality images in field)_


### YOLO Version

- **Total Images:** 6,394 images of broadleaf and grass weeds.
- **Image Distribution:**
  - **Broadleaf Weeds:** 4,717 images
  - **Grass Weeds:** 1,677 images
- **Bounding Boxes:**
  - **Broadleaf Weed Images:** 5,590 bounding boxes
  - **Grass Weed Images:** 1,961 bounding boxes
- **Annotation Details:** Each image may contain multiple bounding boxes, but every image is associated with a single unique label.

---

### [BROAD-LEAVED-DOCK Dataset](https://www.kaggle.com/datasets/gavinarmstrong/open-sprayer-images/data)

#### **BROADLEAF**
 - broad-leaved docks (Rumex obtusifolius) are considered a broadleaf weed,
 - Contains 1307 images of broad-leaved docks.
 - Contains 5392 images of non broad-leaved docks which is everything else.
 - It comes without annotations, we have to manually pick and choose images and draw bounding boxes.
 - Most of the image are shit, but could potentionally contain good ones.
 - Check for non broad-leaved docks images for inclusion of background images.
 
---

### [CROP-AND-WEED Dataset](https://github.com/cropandweed/cropandweed-dataset)(TODO)

#### **BROADLEAF**
- Category 1

#### **GRASS**
- Category 1

---
### [Sorghum-Weed-Dataset](https://data.mendeley.com/datasets/y9bmtf4xmr/1)(TODO)

#### **BROADLEAF**
- Category 1

#### **GRASS**
- Category 1
