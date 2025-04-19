
# 🎓 College Recommendation System

A Django-based AI-powered web application that helps students find the best-fit colleges based on academic performance, location, stream, gender, and category.

## 🔍 Features

- ✅ **College Recommendation** using K-Nearest Neighbors (KNN)
- 🤖 **Chatbot Assistant** integrated with pages to help students
- 🏷️ **Filter by Gender, Category, Stream, and State**
- 📊 **Score-based Predictions**
- ⚖️ **Compare Colleges** by cutoffs, location, etc.
- 📍 Clean and responsive user interface

---

## ⚙️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Django (Python)
- **Machine Learning:** Scikit-learn (KNN)
- **Database:** SQLite3
- **APIs:** Optional chatbot integration

---

## 🚀 Getting Started

### 🔧 Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/College-Recommendation-System.git
cd College-Recommendation-System
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

6. **Visit the app in browser**
```
http://127.0.0.1:8000/
```

---

## 👤 User Inputs

| Field        | Description                          |
|--------------|--------------------------------------|
| Name         | Student's full name                  |
| Gender       | Male/Female                          |
| Marks        | Percentage marks (e.g., 85)          |
| Category     | Open/OBC/SC/ST                       |
| Preferred Stream | Engineering/Medical/Commerce/etc. |
| State        | Desired college location             |

---

## 💡 Working Principle

Uses **KNN algorithm** to recommend colleges based on the student profile and similarity with past data.

**Formula Used:**
```
R = (W1 × Normalized_Marks) + (W2 × Stream_Match) + (W3 × Location_Match) + (W4 × Gender_Match) + (W5 × Category_Match)
```

---

## 🧠 Chatbot Integration

A chatbot (`chatbot.html`) is included and rendered on each page to assist students in:
- Understanding how to use the system
- Getting college and stream suggestions
- Answering FAQs

---

## 📌 Future Improvements

- ✅ Web scraping for live cutoffs
- ✅ Ranking by placement data
- ✅ Google Maps integration for location
- ✅ OTP/email login system

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📷 Screenshots (optional)

Add screenshots here using:
```markdown
![Home](screenshots/home.png)
![Recommendation Result](screenshots/result.png)
```

---

## 📬 Contact

**Yash Dilip Sonawane**  
📧 yashsonawane141103@gmail.com 
🔗 [LinkedIn]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/yash-sonawane1411/))
