# House Price Prediction Model

# Vision Price Net 🏠

Predict house prices using images + features with an AI-powered interactive interface.  

This project includes:  
- Drag & Drop house image upload  
- Bedrooms, bathrooms, and area input  
- Animated price counting and confidence meter  
- Soft floating particles background  
- 3D tilting card effect  
- Loader animation while AI predicts  
- Dark/Light mode toggle  
- Gen-Z startup demo aesthetic  

---

## 🔧 Requirements

- Python 3.10+  
- Flask  
- PyTorch  
- Torchvision  
- Pillow  

---

## ⚡ Project Setup

1. **Clone the repository:**

```bash
git clone <repository_url>
cd vision-price-net

2. Create a virtual environment:
    
    python -m venv venv

3. Activate the virtual environment:
    > Windows (PowerShell):
            .\venv\Scripts\Activate
    
    > Mac/Linux:
            .source venv/bin/activate

4. Install dependencies:
    pip install -r requirements.txt

5. Ensure your model is in the correct folder:
            .models/best_model.pth
            .(Replace vision_price_net.pth with your trained model file if necessary.)
        
## 🏃 Running the Application
 
 1. Run Flask app:
        python app.py

2. Open the website in your browser:
        (http://127.0.0.1:5000)

3. Use the website:
        .Drag & drop a house image
        .Enter number of bedrooms, bathrooms, and area
        .Click Predict Price
        .Watch the animated price count and confidence meter

##📁 Project Structure:

 vision-price-net/
│
├─ app.py               # Main Flask app
├─ models/
│   └─ best_model.pth   # Pretrained PyTorch model
├─ src/
│   └─ models.py        # VisionPriceNet model class
├─ static/
│   ├─ style.css        # CSS styles
│   └─ script.js        # JavaScript interactions
└─ templates/
    └─ index.html       # HTML page


##✨ Features
.AI-powered house price prediction
.Animated Gen-Z aesthetic interface
.Loader while predicting
.Price counting animation
.Confidence meter with glow animation
.3D tilt card hover effect
.Drag-drop image glow effect
.Dark/Light mode toggle
.Soft floating particle background

##💡 Notes
.The confidence score is currently mocked at 92%. You can update it to use real model output if available.
.Ensure best_model.pth is compatible with VisionPriceNet class in src/models.py.
.The website is fully interactive — drag-drop, hover, and toggle dark mode included.


---

✅ How to use

Place both files in the root of your project.
Windows: double-click install_and_run.bat.
Linux/macOS: run ./run.sh from terminal.
Your browser will automatically open at http://127.0.0.1:5000.
Everything works immediately — no need to remember commands.