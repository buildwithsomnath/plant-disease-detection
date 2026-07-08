
# 🌿 Plant Disease Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

An AI-powered web application that uses **Deep Learning (CNN)** to detect plant diseases from leaf images and provides tailored **fertilizer recommendations** and **treatment guidance** for farmers and agricultural professionals.

## 🎯 Features

- 🔍 **Real-time Disease Detection** - Upload plant images for instant analysis
- 🎯 **High Accuracy** - 81-84% accuracy across 38 plant disease classes
- 💊 **Treatment Recommendations** - Get specific treatment and prevention advice
- 📊 **Prediction History** - Track all past predictions with timestamps
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 🚀 **REST API** - Easy integration with mobile apps and other services
- 🔐 **Secure** - CSRF protection, file validation, and input sanitization

## 🌾 Supported Plants & Diseases

### 38 Disease Classes Across Multiple Crops:

<details>
<summary><strong>🍅 Tomato (10 classes)</strong></summary>

- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-spotted spider mite)
- Target Spot
- Tomato Mosaic Virus
- Yellow Leaf Curl Virus
- Healthy

</details>

<details>
<summary><strong>🥔 Potato (3 classes)</strong></summary>

- Early Blight
- Late Blight
- Healthy

</details>

<details>
<summary><strong>🌽 Corn (4 classes)</strong></summary>

- Common Rust
- Gray Leaf Spot
- Northern Leaf Blight
- Healthy

</details>

<details>
<summary><strong>🌶️ Pepper (2 classes)</strong></summary>

- Bacterial Spot
- Healthy

</details>

<details>
<summary><strong>🍎 Other Crops</strong></summary>
Others Crops (19 classes)

</details>

## 📸 Screenshots

<div align="center">

### Upload Interface
![Upload Interface](screenshots/upload.png)

### Results & Recommendations
![Results](screenshots/disease_result.png)

</div>

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- 4GB+ RAM
- 2GB+ disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/dassomnath99/Plant-Disease-Detection.git
cd Plant-Disease-Detection
```

2. **Create virtual environment**
```bash
# Using venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Download or train the model**

```bash
pip install kagglehub
```
Before downloading the dataset, configure your Kaggle API token.

1. Sign in to your Kaggle account.
2. Go to **Account Settings**.
3. Under **API**, copy your API Token (starts with `KGAT_...`).

**Windows (PowerShell):**

```powershell
$env:KAGGLE_API_TOKEN="KGAT_your_actual_token_here"
```

To make it permanent:

```powershell
setx KAGGLE_API_TOKEN "KGAT_your_actual_token_here"
```

Close and reopen PowerShell after running `setx`.

Now download the PlantVillage dataset:

```bash
python download_data.py
```

Train the model:

```bash
python train_with_evaluate.py
```

Test the model: (optional)

```bash
python test.py test_images/[filename].jpg
```
This will create:

- `models/plant_disease_model.h5`
- `models/plant_disease_model.tflite`
- `models/plant_disease_model.keras`
- `models/class_names.json`
- `models/training_history.png`
- `models/confusion_matrix.png`
- `models/classification_report.txt`

5. **Setup Django**
```bash
# Create necessary directories
mkdir -p media/uploads

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Access the application**

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 📁 Project Structure
```
plant_disease_detection/
│
├── backend/                          # Django project settings
│   ├── __init__.py
│   ├── settings.py                   # Configuration
│   ├── urls.py                       # Main URL routing
│   └── wsgi.py                       # WSGI config
│
├── predictions/                      # Main application
│   ├── migrations                    # Migration
│   ├── templates                     # templates(HTML code)
│   ├── models.py                     # Database models
│   ├── views.py                      # API endpoints
│   ├── urls.py                       # App routing
│   ├── admin.py                      # Admin panel config
│   └── utils.py                      # Helper functions
│
├── models/                           # ML models directory
│   ├── plant_disease_model.h5        # Trained CNN model
│   ├── plant_disease_model.keras     # .keras
│   ├── plant_disease_model.h5        # .h5
│   ├── plant_disease_model.tflite    # .tflite
│   └── class_names.json              # Training plots
│
│
├── media/                            # User uploaded images
│   └── uploads/
│
│
├── requirements.txt                 # Python dependencies
├── manage.py                        # Django management
├── train_with_evaluate.py           # Train and Test for Model Generation
├── test.py                          # Predict and Test
├── download_data.py                 # Download Dataset or change the path for different dataset
└── README.md                        # This file
```

## 🔌 API Usage

### Predict Disease

**Endpoint:** `POST /api/predict/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -F "image=@path/to/plant_leaf.jpg"
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "disease": "Tomato_Late_blight",
    "confidence": 94.32,
    "plant_type": "Tomato",
    "description": "Serious fungal disease that can destroy crops quickly",
    "fertilizer": "Balanced fertilizer with micronutrients",
    "treatment": "Remove infected parts immediately, apply fungicide",
    "prevention": "Avoid wet foliage, ensure good drainage"
  },
  "prediction_id": 123
}
```

### Get Prediction History

**Endpoint:** `GET /api/history/?limit=10`

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "id": 123,
      "disease": "Tomato_Late_blight",
      "confidence": 94.32,
      "plant_type": "Tomato",
      "timestamp": "2025-10-30 14:23:45",
      "image_url": "/media/uploads/2025/10/30/image.jpg"
    }
  ]
}
```

## 🧪 Model Performance

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| **Accuracy** | 82.32% | 77.15% | 68.78% |

### Training Details

- **Dataset**: PlantVillage (54,000+ images)
- **Architecture**: Transfer Learning with MobileNetV2
- **Framework**: TensorFlow 2.15 / Keras
- **Input Size**: 224x224 RGB
- **Training Time**: ~1.5 - 2 hour (GPU)
- **Model Size**: ~13 MB

## 🎓 Model Training

### Training Your Own Model

1. **Prepare dataset**
```bash
# Download PlantVillage dataset
mkdir -p data
kaggle datasets download -d emmarex/plantdisease
unzip plantdisease.zip -d data/

# Or organize your own dataset
# data/plant_disease_data/
#   ├── Disease_Class_1/
#   ├── Disease_Class_2/
#   └── ...
```

2. **Train the model**
```bash
# Simple training (recommended)
python train_with_evaluate.py

# Advanced training with detailed metrics
python train_model.py
```

3. **View results**
```bash
# Check metrics summary
python view_results.py

# Generated files:
# - models/plant_disease_model.h5
# - models/class_names.json
```

## 🛠️ Technology Stack

### Backend
- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **TensorFlow 2.15** - Deep learning framework
- **Keras** - Neural network API
- **Pillow** - Image processing
- **NumPy** - Numerical computing

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling (responsive design)
- **JavaScript** - Interactive functionality
- **Fetch API** - Asynchronous requests

### Machine Learning
- **CNN Architecture** - MobileNetV2 (Transfer Learning)
- **ImageDataGenerator** - Data augmentation
- **Adam Optimizer** - Training optimization
- **Categorical Crossentropy** - Loss function

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
MAX_UPLOAD_SIZE=5242880
MODEL_PATH=models/plant_disease_model.h5
```

### Django Settings

Key configurations in `settings.py`:
```python
# Model settings
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'plant_disease_model.h5')
MAX_UPLOAD_SIZE = 5242880  # 5MB

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS settings (for API access)
CORS_ALLOW_ALL_ORIGINS = True
```

## 📱 Mobile Integration

### React Native Example
```javascript
const uploadImage = async (imageUri) => {
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'plant.jpg',
  });

  const response = await fetch('http://your-server.com/api/predict/', {
    method: 'POST',
    body: formData,
  });

  const result = await response.json();
  return result;
};
```

### Flutter Example
```dart
import 'package:http/http.dart' as http;

Future<void> uploadImage(String imagePath) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://your-server.com/api/predict/'),
  );
  
  request.files.add(await http.MultipartFile.fromPath('image', imagePath));
  var response = await request.send();
  
  // Handle response
}
```

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-app-name
```

4. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

5. **Deploy**
```bash
git push heroku main
```

6. **Run migrations**
```bash
heroku run python manage.py migrate
```

### Docker Deployment
```bash
# Build image
docker build -t plant-disease-detection .

# Run container
docker run -p 8000:8000 plant-disease-detection
```

## 🧪 Testing

### Run Unit Tests
```bash
python manage.py test
```

### Test API Manually
```bash
# Test prediction
curl -X POST http://localhost:8000/api/predict/ \
  -F "image=@test_images/tomato_leaf.jpg"

# Test history
curl http://localhost:8000/api/history/
```

### Test Model Accuracy
```bash
python test_model.py
```

## 🐛 Troubleshooting

### Common Issues

**1. Model not loading**
```bash
# Check if model file exists
ls models/plant_disease_model.h5

# Verify TensorFlow version
python -c "import tensorflow as tf; print(tf.__version__)"
```

**2. Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**3. CORS errors**
```bash
# Add to settings.py
CORS_ALLOW_ALL_ORIGINS = True
```

**4. Memory errors**
```bash
# Reduce batch size in training
BATCH_SIZE = 16  # instead of 32
```


## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Write clean, documented code
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Somnath Das**

- GitHub: [@dassomnath99](https://github.com/buildwithsomnath)
- Email: somnathdas4462@gmail.com

## 🙏 Acknowledgments

- **Kaggle Community Dataset** - For providing the training data
- **TensorFlow Team** - For the amazing deep learning framework
- **Django Community** - For the robust web framework
- **Contributors** - Thanks to all who have contributed!

## 📚 References

- [Kaggle Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)

## 📞 Support

If you have any questions or need help, please:

1. Check the [Issues](https://github.com/dassomnath99/Plant-Disease-Detection/issues) page
2. Open a new issue with detailed description
3. Contact via email

<div align="center">

Made with ❤️ for farmers and agriculture enthusiasts

**[⬆ back to top](#-plant-disease-detection-system)**

</div>
