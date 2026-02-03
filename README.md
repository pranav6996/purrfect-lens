🐈 PurrfectLens: High-Accuracy Cat Breed Classifier

This project features a fully trained and fine-tuned Convolutional Neural Network (CNN) designed to perform fine-grained image classification across 67 distinct cat breeds. The model was rigorously optimized to differentiate between visually similar breeds, achieving high accuracy in real-world testing (5 out of 6 correct in initial testing).

🌟 Project Stack & Technical Scope

This project showcases end-to-end Machine Learning deployment skills:

Model Architecture: Transfer Learning using MobileNetV2 (with $\mathbf{50}$ layers unfrozen for fine-tuning).

Dataset: Over $\mathbf{100,000}$ images across 67 unique breeds.

Frameworks: TensorFlow, Keras, NumPy, PIL.

Skills Demonstrated: Data Integrity Checks, Model Optimization (Low Learning Rate Fine-Tuning), and Command-Line Deployment.

🚀 How to Run the Prediction Script

Step 1: Obtain Model Artifacts

To run this project, you must download the two files that contain the trained intelligence and the labels. These files must be placed in the root directory of your cloned repository.

Trained Model Weights (The Brain): pranav_cat_classifier_new_run.keras

Breed Labels (The Dictionary): breed_labels_new_run.txt

Step 2: Setup the Environment

Clone the Repository:

git clone [YOUR-REPO-URL-HERE]
cd [YOUR-REPO-NAME]


Install Dependencies:
You must create and activate a virtual environment before installing the requirements.

# Create and activate environment (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Install Python libraries
pip install -r requirements.txt


Step 3: Execute Prediction

You will use the predict.py script you uploaded (which utilizes Python's argparse) to run the classification from your terminal.

Example Command (Using your downloaded model and labels):

python predict.py \
    --model pranav_cat_classifier_new_run.keras \
    --labels breed_labels_new_run.txt \
    --image /path/to/your/cat_photo.jpg


Example Prediction Output

When the model successfully classifies an image (like the Persian cat we fixed!), the terminal output will look similar to this: