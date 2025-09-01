# 🌪️ Enhanced Disaster AI Predictor

## 🚀 Empowering Communities Through Advanced Disaster Prediction

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.11.0-FF4B4B.svg)](https://streamlit.io)

---

## 📚 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Advanced Concepts](#-advanced-concepts)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🌟 About the Project

The Enhanced Disaster AI Predictor is a cutting-edge, AI-powered application designed to revolutionize disaster preparedness and response. By leveraging advanced machine learning algorithms and real-time data analysis, our system provides accurate predictions, timely alerts, and crucial information to help communities and emergency responders prepare for and mitigate the impact of natural disasters.

> "Prediction is better than cure. Our AI doesn't just forecast disasters; it empowers action." - Project Vision

---

## 🔑 Key Features

1. **Multi-Disaster Prediction**: 🌊🌋🔥🌀🌊
   Covers floods, earthquakes, wildfires, hurricanes, and tsunamis.

2. **Real-Time Data Integration**: 📊
   Incorporates live weather data, geological readings, and historical patterns.

3. **Interactive Geospatial Visualization**: 🗺️
   Utilizes Folium for dynamic, interactive disaster mapping.

4. **AI-Powered Severity Analysis**: 🧠
   Employs machine learning to assess and predict disaster severity.

5. **Customizable Alert System**: 🚨
   Provides tailored alerts based on location and disaster type.

6. **Social Media Integration**: 📱
   Aggregates and analyzes disaster-related social media content.

7. **Emergency Resource Locator**: 🏥
   Identifies nearby shelters, hospitals, and emergency services.

8. **Historical Data Analysis**: 📜
   Offers insights from past disasters to improve future preparedness.

9. **Multi-language Support**: 🌐
   Available in multiple languages for global accessibility.

10. **API Integration**: 🔌
    Connects with various weather, geological, and news APIs for comprehensive data.

---

## 💻 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Folium
- **Machine Learning**: Scikit-learn, TensorFlow
- **APIs**: OpenWeatherMap, YouTube, Twitter, News, Gemini-Google
- **Geospatial Analysis**: GeoPy
- **Natural Language Processing**: NLTK, spaCy
- **Alert Messages**:Gmail STMP server
---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/gamerson96/Team_NEXUS.git
   ```

2. Navigate to the project directory:
   ```
   cd Disaster-AI-Predictor
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up API keys:
   - Create a `.streamlit/secrets.toml` file
   - Add your API keys following the structure in `secrets.toml`

5. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

---

## 📘 Usage Guide

1. **Select Disaster Type**: Choose from the available disaster types.
2. **Enter Location**: Input the area you want to analyze.
3. **Set Parameters**: Adjust duration and initial intensity.
4. **Generate Prediction**: Click to run the simulation.
5. **Explore Results**: Analyze the interactive map, charts, and recommendations.
6. **Set Alerts**: Configure custom alerts for your area.
7. **Enquire**: Leverage the power of Gemini to get your answers.
---

## 🧠 Advanced Concepts

### Machine Learning Model
Our core prediction engine uses an ensemble of models:
- Random Forest for pattern recognition
- LSTM networks for time series forecasting
- Gradient Boosting for feature importance

### Data Fusion Algorithm
We employ a novel data fusion algorithm that combines:
- Satellite imagery
- Ground sensor data
- Historical disaster records
- Social media sentiment analysis

This multi-modal approach significantly improves prediction accuracy.

### Scalable Architecture
The application is built on a microservices architecture, allowing for:
- Easy scaling during peak disaster seasons
- Modular updates and improvements
- Regional customization without affecting the core system

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Don't forget to give the project a star! Thanks again!

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

> "In the face of disasters, knowledge is power, and prediction is our strongest shield." - Disaster AI Team
