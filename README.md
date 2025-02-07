## **Sign Language Detection with Hand Landmarks**

This repository provides a method for recognizing sign language gestures using **hand landmarks** provided by the **MediaPipe library**. The **hand landmarks** are used to detect the relative positioning of the fingers in 3D space, which allows for gesture recognition. 

The gestures are detected by comparing the **x** and **y** coordinates of the landmarks and analyzing their relative positions.

### **Hand Landmarks:**

The **21 hand landmarks** correspond to the joints and tips of the fingers. The **x** and **y** coordinates are used to determine the relative positions of these landmarks for gesture recognition.

#### **Landmark Breakdown:**
1. **Landmark 0 (Wrist)**: The base of the palm (root landmark).
2. **Landmark 1 (Thumb base)**: The base joint of the thumb, near the wrist.
3. **Landmark 2 (Thumb first joint)**: The first joint of the thumb.
4. **Landmark 3 (Thumb second joint)**: The second joint of the thumb.
5. **Landmark 4 (Thumb tip)**: The tip of the thumb.
6. **Landmark 5 (Index base)**: The base joint of the index finger.
7. **Landmark 6 (Index first joint)**: The first joint of the index finger.
8. **Landmark 7 (Index second joint)**: The second joint of the index finger.
9. **Landmark 8 (Index tip)**: The tip of the index finger.
10. **Landmark 9 (Middle base)**: The base joint of the middle finger.
11. **Landmark 10 (Middle first joint)**: The first joint of the middle finger.
12. **Landmark 11 (Middle second joint)**: The second joint of the middle finger.
13. **Landmark 12 (Middle tip)**: The tip of the middle finger.
14. **Landmark 13 (Ring base)**: The base joint of the ring finger.
15. **Landmark 14 (Ring first joint)**: The first joint of the ring finger.
16. **Landmark 15 (Ring second joint)**: The second joint of the ring finger.
17. **Landmark 16 (Ring tip)**: The tip of the ring finger.
18. **Landmark 17 (Pinky base)**: The base joint of the pinky finger.
19. **Landmark 18 (Pinky first joint)**: The first joint of the pinky.
20. **Landmark 19 (Pinky second joint)**: The second joint of the pinky.
21. **Landmark 20 (Pinky tip)**: The tip of the pinky finger.

**Hand Landmark Image**:  
![Hand Landmarks](path_to_image.jpg)  
*The image above shows the positions of the 21 hand landmarks on the hand.*

---

### **Logic for Gesture Detection Using Hand Landmarks**

Here’s a detailed explanation of how gestures are detected based on the relative positions of the hand landmarks, focusing on the **x** and **y** coordinates:

---

### **1. LIKE (Thumbs-Up) 👍**

#### **Key Landmarks:**
- **Thumb (1-4)** and **Other Fingers (5-20)**

#### **Logic:**
- The **thumb** should be fully extended, meaning the **y-coordinate** of the **thumb tip (landmark 4)** should be **greater** than the previous joints (landmarks 3, 2, 1) in an **ascending order**.
    - **thumb tip (landmark 4)**: Should have the smallest **y-coordinate** compared to its joints.
    - **thumb second joint (landmark 3)**: Should have a larger **y-coordinate** than the tip.
    - **thumb first joint (landmark 2)**: Should have a larger **y-coordinate** than the second joint.
    - **thumb base (landmark 1)**: Should have the largest **y-coordinate**.
    
- **Other fingers** (index, middle, ring, pinky) should be folded, i.e., the **y-coordinates** of the tips (landmarks 8, 12, 16, 20) should be higher than their respective base joints (landmarks 5, 9, 13, 17).

#### **How it Works:**
- The **thumb’s** landmarks are compared based on their **y-coordinates** to check if it is extended upward.
- The **fold status** of other fingers is evaluated by checking if the **y-coordinates** of the tips are greater than those of the base joints.

```python
if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y:
    if all(finger_fold_status):
        print("LIKE👍 gesture detected")
```

---

### **2. DISLIKE (Thumbs-Down) 👎**

#### **Key Landmarks:**
- **Thumb (1-4)** and **Other Fingers (5-20)**

#### **Logic:**
- The **thumb tip (landmark 4)**'s **y-coordinate** should be **greater** than the previous joints (landmarks 3, 2, 1), meaning the thumb is extended downward.
- All other fingers (index, middle, ring, pinky) should be folded, so the **y-coordinates** of the tips (landmarks 8, 12, 16, 20) should be above their respective base joints (landmarks 5, 9, 13, 17).

#### **How it Works:**
- The **thumb tip (landmark 4)** should have a larger **y-coordinate** than its preceding joints.
- The **fold status** for the other fingers should be true, i.e., the **y-coordinates** of the tips are higher than their respective base joints.

```python
if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
    if all(finger_fold_status):
        print("DISLIKE👎 gesture detected")
```

---

### **3. OK 👌**

#### **Key Landmarks:**
- **Thumb (1-4)** and **Index Finger (5-8)**

#### **Logic:**
- The **thumb tip (landmark 4)** should be **close** to the **index tip (landmark 8)**. This is checked by calculating the **Euclidean distance** between the two.
- All other fingers should be folded, so their **y-coordinates** should be above their respective base joints.

#### **How it Works:**
- The **Euclidean distance** between the **thumb tip (landmark 4)** and **index tip (landmark 8)** is calculated.
- If the distance is below a set threshold, the **thumb and index** fingers are considered to be touching.
- The other fingers are checked for folding (i.e., their **y-coordinates** are above the base joints).

```python
distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
if distance < 0.05:
    if not finger_fold_status[1] and not finger_fold_status[2] and not finger_fold_status[3]:
        print("OK👌 gesture detected")
```

---

### **4. PEACE ✌️**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Ring Finger (13-16)**, **Pinky Finger (17-20)**, **Index Finger (5-8)**

#### **Logic:**
- The **thumb tip (landmark 4)** should be **close to** the **ring tip (landmark 16)** and **pinky tip (landmark 20)**. This is verified by calculating the **Euclidean distance** between the landmarks.
- The **index** and **middle fingers** should be extended (not folded).

#### **How it Works:**
- The distances between the **thumb**, **ring**, and **pinky** are calculated.
- If the distances are below a set threshold (indicating proximity), and the **index** and **middle fingers** are extended, the gesture is recognized as a **peace** sign.

```python
distance_thumb_ring = ((thumb_x - ring_x) ** 2 + (thumb_y - ring_y) ** 2) ** 0.5
distance_ring_pinky = ((ring_x - pinky_x) ** 2 + (ring_y - pinky_y) ** 2) ** 0.5
if distance_thumb_ring < 0.05 and distance_ring_pinky < 0.05:
    if not finger_fold_status[0] and not finger_fold_status[1]:
        print("PEACE✌️ gesture detected")
```

---

### **5. CALL ME 🤙**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Pinky Finger (17-20)**, **Index Finger (5-8)**, **Middle Finger (9-12)**

#### **Logic:**
- The **thumb tip (landmark 4)** and **pinky tip (landmark 20

)** should be far apart, and the **x-coordinates** should be checked to ensure they are not close to each other.
- The **index**, **middle**, and **ring fingers** should be folded.

#### **How it Works:**
- The **Euclidean distance** between the **thumb** and **pinky** is calculated. If the distance is large enough (i.e., the thumb and pinky are far apart), and the other fingers are folded, the gesture is detected as **CALL ME**.

```python
distance_thumb_pinky = ((thumb_x - pinky_x) ** 2 + (thumb_y - pinky_y) ** 2) ** 0.5
if distance_thumb_pinky > 0.1:
    if all(finger_fold_status[1:]):
        print("CALL ME🤙 gesture detected")
```

---

This README section thoroughly covers the logic and how **x** and **y** coordinates are analyzed to detect gestures. Each gesture’s corresponding landmarks are explained, and how those landmarks relate to the **x** and **y** coordinates for recognition.

Let me know if you'd like to add or modify anything further!
