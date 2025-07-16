<p align="center">
  <img src="https://github.com/user-attachments/assets/c948d53c-b037-48bc-9aac-98181cdcf569" alt="Banner" width="100%" height="250">
</p>

# 🛒 MindCart 
**Helping Consumers Pause, Reflect, and Shop Smarter — Powered by AI and Behavioral Science**  

---

## ✅ Why This Project Exists  
Consumer confidence is at its **lowest level in 12 years**. Global retailers have seen **billions wiped off their market valuations in a single day** due to shifting spending habits and economic uncertainty.  

### What does this mean for businesses and consumers?  
- Customers are second-guessing purchases → **increasing refund rates**  
- Retailers risk losing billions and triggering **recession-like effects** if confidence doesn’t recover  

The traditional e-commerce model promotes **speed and urgency**:  
> “Add to cart now, deal ends soon!”  

This fuels **impulsive decisions**. But during low-confidence periods, it leads to:  
- ❌ Buyer’s remorse  
- ❌ Abandoned carts  
- ❌ Financial stress  

---

### **Our Hypothesis:**  
Could **AI-driven micro-interventions based on behavioral science** help customers:  
- Feel in control  
- Reduce regret  
- Keep businesses resilient?  

**That’s how MindCart was born.**  

---

## 💡 What is MindCart?  

<img width="1152" height="583" alt="image" src="https://github.com/user-attachments/assets/04008e5b-7966-4da2-a6b3-0a377b63b38b" />

A shopping assistant powered by **Gemini 1.5 Flash** that applies **behavioral psychology** from the book *Thinking, Fast and Slow* to help users:  
✔ Reflect before purchasing  
✔ Reduce impulse buys  
✔ Maintain confidence in spending  
✔ Improve long-term financial habits  

For businesses, it aims to **reduce refund rates** and **stabilize revenue during economic downturns**.  

---

## 🎯 Key Features — Backed by Behavioral Science  

### ✅ 1. **Cart Analysis & Spending Breakdown**  
**What It Does:**  
<img width="1063" height="538" alt="image" src="https://github.com/user-attachments/assets/ce561126-c724-4630-81ca-deda6fba230a" />


- AI scans the user’s cart and provides:  
  - Total spend breakdown (Essentials vs Impulse items)  
  - Smart suggestions for budget alignment  
- Displays **actionable insights** like:  
  > *“You’re about to spend ₹8,500. Essentials: ₹6,000 | Impulse: ₹2,500.”*  

**Psychological Principle:**  
- **Awareness Effect** — Making spending visible improves self-control  
- **Anchoring Bias** — Highlighting impulse cost in context of essentials makes overspending feel larger
- 
### ✅ 2. **10-Second Reflection Pause Before Checkout**  
**What it does:**  

<img width="1130" height="445" alt="image" src="https://github.com/user-attachments/assets/0419413b-8713-4af3-9c88-7a6b763067e1" />

- Based on **Daniel Kahneman’s System 1 vs System 2 thinking**:  
  - System 1 (Fast Thinking): Quick, emotional, impulsive  
  - System 2 (Slow Thinking): Deliberate, rational  
- A **10-second pause** activates System 2 → rational evaluation before checkout  
- Tiny intervention, huge impact in reducing impulsive buying  

---

### ✅ 3. **Item Tagging: Essential | Optional | Impulse**  
**What it does:**  

<img width="730" height="462" alt="image" src="https://github.com/user-attachments/assets/4d9c791c-667b-433b-a5a4-cb74c0f99d73" />

- Uses **Choice Architecture** — structuring choices so people make better decisions without forcing them  
- AI classifies items as:  
  - **Essential:** Daily-use or planned  
  - **Optional:** Nice-to-have  
  - **Impulse:** Emotion-driven, unnecessary  
- When an item is labeled “Impulse,” **cognitive dissonance** kicks in → user reconsiders  

---

### ✅ 4. **Identity Badges for Mindful Shoppers**  
**What it does:**  

<img width="1046" height="381" alt="image" src="https://github.com/user-attachments/assets/20be6afd-e8b5-4d6b-8993-156a382081a5" />

- Based on **Commitment Bias** and **Self-Perception Theory**  
- Awarding badges like **“Mindful Buyer”** creates an identity  
- Users act consistently with self-image → reinforces responsible habits  

---

### ✅ 5. **Savings Awareness Prompts**  
**What it does:**  
- Leverages **Loss Aversion**:  
  > People fear losing ₹500 more than they value gaining ₹500  
- Instead of saying *“Your cart is ₹10,000,”* we show:  
  > *“You can save ₹2,500 by removing impulse items.”*  
- **Framing matters** — shifts decision toward rational saving  

---

### ✅ 6. **“Treat Yourself Later” Suggestions**  
**What it does:**  
- Based on **Delayed Gratification** and **Goal Substitution**  
- Instead of *“Don’t buy,”* we suggest:  
  > *“Add to Treat List for later and reward yourself after reaching goals.”*  
- Satisfies emotional need without harming financial stability  

---

## 🧠 The Science Behind It  
Principles used:  
- **System 1 vs System 2 Thinking** (*Thinking, Fast and Slow*)  
- **Loss Aversion**  
- **Commitment Bias & Self-Perception**  
- **Choice Architecture**  
- **Delayed Gratification**  

> This isn’t random — every feature exists because psychology says it works.  

---

## Demo  
👉 **[Watch Demo Video](your-demo-link)**  

---

## ⚙️ Tech Stack  
- **Gemini 1.5 Flash API** → AI-driven analysis & nudges  
- **Python** → Backend  
- **Streamlit** → UI  
- Behavioral science principles baked into the logic  

---

## 🧩 Example Prompt Design  
```json
You are a mindful shopping advisor.
Analyze this cart: [Cart Items].
Classify items as Essential, Optional, or Impulse.
Generate a short reflection message for the user encouraging mindful decision-making.
Return in JSON format.
