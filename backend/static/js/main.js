function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('imagePreview');
    const uploadForm = document.getElementById('uploadForm');
    const predictBtn = document.getElementById('predictBtn');
    
    // Preview Image on selection
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle Form Submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('image', file);
            predictBtn.textContent = 'Analyzing... 🐱';
            predictBtn.disabled = true;

            try {
                const response = await fetch('/api/predict/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    showResult(data);
                } else {
                    alert('Oops! Something went wrong. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting image.');
            } finally {
                predictBtn.textContent = 'Identify Breed! 🚀';
                predictBtn.disabled = false;
            }
        });
    }
    
    // Close Modal
    const closeModal = document.querySelector('.close-modal');
    if (closeModal) {
        closeModal.addEventListener('click', () => {
             document.getElementById('resultSection').classList.add('hidden');
        });
    }

    // Close modal on outside click
    window.onclick = function(event) {
        const modal = document.getElementById('resultSection');
        if (event.target == modal) {
            modal.classList.add('hidden');
        }
    }
});

function showResult(data) {
    document.getElementById('breedName').textContent = data.breed;
    document.getElementById('confidenceScore').textContent = data.confidence;
    
    // Access details
    const details = data.details || {};
    document.getElementById('breedOrigin').textContent = details.origin || 'Unknown';
    document.getElementById('breedDesc').textContent = details.description || 'No description available.';
    document.getElementById('breedHealth').textContent = details.health || 'No health info available.';
    document.getElementById('breedHabits').textContent = details.habits || 'No habits info available.';
    document.getElementById('breedFood').textContent = details.food || 'No food info available.';
    
    document.getElementById('resultSection').classList.remove('hidden');
}

async function fetchNewFact() {
    try {
        const response = await fetch('/api/fact/');
        const data = await response.json();
        document.getElementById('randomFact').textContent = data.fact;
    } catch (e) {
        console.error("Failed to fetch fact", e);
    }
}
