## ⭕ **Sign Language Detection with Hand Landmarks** ⛳🔥

This repository provides a method for recognizing sign language gestures using **hand landmarks** provided by the **MediaPipe library**. The **hand landmarks** are used to detect the relative positioning of the fingers in 3D space, which allows for gesture recognition. 

The gestures are detected by comparing the **x** and **y** coordinates of the landmarks and analyzing their relative positions.

### ⭕ **Hand Landmarks:**

The **21 hand landmarks** correspond to the joints and tips of the fingers. The **x** and **y** coordinates are used to determine the relative positions of these landmarks for gesture recognition.

#### ⭕ **Landmark Breakdown:**

![Hand Landmarks](https://github.com/webdevpathiraja/Hand-Gesture-Sign-Detection-Project/blob/main/resources/hand-landmarks.png)
*The image above shows the positions of the 21 hand landmarks on the hand.*

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

---

### ⭕ **Logic for Gesture Detection Using Hand Landmarks**

Here’s a detailed explanation of how gestures are detected based on the relative positions of the hand landmarks, focusing on the **x** and **y** coordinates:

### **1. LIKE (Thumbs-Up) 👍🏽**

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

### **2. DISLIKE (Thumbs-Down) 👎🏻**

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

### **3. OK 👌🏽**

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

### **4. PEACE ✌🏻**

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

### **5. CALL ME 🤙🏽**

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

Here's the updated explanation with a detailed breakdown of the logic, hand landmarks, and how the **x** and **y** coordinates are used to detect the gestures.

---

### **6. STOP ✋🏻**

#### **Key Landmarks:**
- **Thumb (1-4)** and **Other Fingers (5-20)**

#### **Logic:**
To detect the **STOP** gesture, all fingers should be fully extended, which means the **y-coordinate** of each finger’s tip (landmarks 4, 8, 12, 16, 20) must be lower than the previous joint. 
- **Thumb (1-4)**: The **y-coordinate** of the thumb tip (landmark 4) must be lower than landmarks 3 and 2.
- **Index (5-8)**, **Middle (9-12)**, **Ring (13-16)**, and **Pinky (17-20)**: The **y-coordinate** of each finger tip should be lower than its previous joint's **y-coordinate** (ensuring the finger is extended upward).

#### **How it Works:**
- Each of the five fingers (thumb, index, middle, ring, pinky) should be fully extended.
- The **y-coordinates** of each of these tips will be lower than their base joints (e.g., for the index finger, landmark 8’s **y-coordinate** will be lower than landmark 6, and so on for the rest of the fingers).

```python
if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and \
    lm_list[8].y < lm_list[6].y < lm_list[5].y and \
    lm_list[12].y < lm_list[10].y < lm_list[9].y and \
    lm_list[16].y < lm_list[14].y < lm_list[13].y and \
    lm_list[20].y < lm_list[18].y < lm_list[17].y:
    print("Stop✋ gesture detected")
    cv2.putText(frame, "STOP", (100, 120), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
```

---

### **7. FORWARD 👆🏻**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Index Finger (5-8)**, **Middle Finger (9-12)**, **Ring Finger (13-16)**, **Pinky Finger (17-20)**

#### **Logic:**
To detect the **FORWARD** gesture, the **index finger** must be raised upward, while the other fingers should be folded.
- **Index Finger (5-8)**: The **y-coordinate** of landmark 8 (tip) should be higher than landmarks 6 and 5 (showing it is extended).
- **Thumb (1-4)**: The **thumb** should be folded inward, so the **x-coordinate** of the thumb tip (landmark 4) should be less than landmark 3.
- **Middle, Ring, and Pinky Fingers (9-20)**: These should be folded, meaning their **y-coordinates** for the tips (landmarks 12, 16, 20) should be lower than the previous joints (landmarks 11, 15, 19).

#### **How it Works:**
- **Index Finger** is checked for extension (higher **y-coordinate** at the tip).
- **Other fingers** are checked to ensure they are folded by comparing their **y-coordinates**.
- The **thumb** is folded by comparing its **x-coordinates**.

```python
if lm_list[8].y < lm_list[6].y < lm_list[5].y and \
    lm_list[12].y > lm_list[11].y > lm_list[10].y and \
    lm_list[16].y > lm_list[15].y > lm_list[14].y and \
    lm_list[20].y > lm_list[19].y > lm_list[18].y and \
    lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x:
    print("FORWARD✋ gesture detected")
    cv2.putText(frame, "FORWARD", (100, 120), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
```

---

### **8. LEFT 👈🏽**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Index Finger (5-8)**, **Middle Finger (9-12)**, **Ring Finger (13-16)**, **Pinky Finger (17-20)**

#### **Logic:**
To detect the **LEFT** gesture, the **thumb** should be raised upwards, and all fingers should point to the left side.
- **Thumb (1-4)**: The **y-coordinate** of the thumb tip (landmark 4) should be less than landmark 2, indicating the thumb is pointing upward.
- **Index Finger (5-8)**: The **x-coordinate** of the index finger tip (landmark 8) should be less than landmark 6 (pointing to the left).
- **Middle, Ring, and Pinky Fingers (9-20)**: These should all point to the left. Their **x-coordinates** will have specific values compared to each other to check for leftward direction.

#### **How it Works:**
- **Thumb** should be raised (i.e., its **y-coordinate** is smaller than its first joint's **y-coordinate**).
- **Index Finger** should be pointing to the left (i.e., its **x-coordinate** is smaller than the previous joint's **x-coordinate**).
- **Other fingers** (middle, ring, pinky) should also follow a leftward pointing pattern based on their **x-coordinates**.

```python
if lm_list[4].y < lm_list[2].y and \
    lm_list[8].x < lm_list[6].x and \
    lm_list[12].x > lm_list[10].x and \
    lm_list[16].x > lm_list[14].x and \
    lm_list[20].x > lm_list[18].x and \
    lm_list[5].x < lm_list[0].x:
    print("LEFT👈 gesture detected")
    cv2.putText(frame, "LEFT", (100, 120), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
```

---

### **9. RIGHT 👉🏻**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Index Finger (5-8)**, **Middle Finger (9-12)**, **Ring Finger (13-16)**, **Pinky Finger (17-20)**

#### **Logic:**
To detect the **RIGHT** gesture, the **thumb** should be raised upward, and all fingers should point to the right.
- **Thumb (1-4)**: The **y-coordinate** of the thumb tip (landmark 4) should be less than landmark 2, indicating the thumb is raised.
- **Index Finger (5-8)**: The **x-coordinate** of the index finger tip (landmark 8) should be greater than landmark 6 (pointing right).
- **Middle, Ring, and Pinky Fingers (9-20)**: These should be folded or pointing rightward. Their **x-coordinates** will have specific values compared to each other to check for rightward direction.

#### **How it Works:**
- **Thumb** should be raised (i.e., its **y-coordinate** is smaller than its first joint's **y-coordinate**).
- **Index Finger** should be pointing to the right (i.e., its **x-coordinate** is greater than its base joint's **x-coordinate**).
- **Other fingers** should also be pointing rightward, based on their **x-coordinates**.

```python
if lm_list[4].y < lm_list[2].y and \
    lm_list[8].x > lm_list[6].x and \
    lm_list[12].x < lm_list[10].x and \
    lm_list[16].x < lm_list[14].x and \
    lm_list[20].x < lm_list[18].x:
    print("RIGHT👉 gesture detected")
    cv2.putText(frame, "RIGHT", (100, 120), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
```

---

### **10. LOVE YOU 🤟🏽**

#### **Key Landmarks:**
- **Thumb (1-4)**, **Index Finger (5-8)**, **Pinky Finger (17-20)**

#### **Logic:**
To detect the **LOVE YOU** gesture:
- **Thumb (1-4)**: The **thumb** should be extended outward (its **x-coordinate** will be greater than the second joint's **x-coordinate**).
- **Index Finger (5-8)**: The **index finger** should be extended upward.
- **Pinky Finger (17-20)**: The **pinky** should be extended upward.
- **Middle (9-12)** and **Ring Fingers (13-16)**: These should be folded.

#### **How it Works:**
- **Thumb** is extended outward by comparing its **x-coordinates**.
- **Index and Pinky fingers** are raised by comparing their **y-coordinates**.
- **Middle and Ring fingers** should be folded, meaning their **y-coordinates** for the tips should be lower than their base joints.

```python
if lm_list[8].y < lm_list[6].y < lm_list[5].y and \
    lm_list[12].y > lm_list[11].y > lm_list[10].y and \
    lm_list[16].y > lm_list[15].y > lm_list[14].y and \
    lm_list[20].y < lm_list[19].y < lm_list[18].y and \
    lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x:
    print("I love you🤟 gesture detected")
    cv2.putText(frame, "I LOVE YOU", (100, 120), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
```

---

