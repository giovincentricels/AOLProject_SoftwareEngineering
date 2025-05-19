document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Mencegah reload halaman
    
    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length === 0) {
        alert("Please select an image before uploading.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        }); 

        if (response.ok) {
            const result = await response.json();
            // Memanggil modal untuk menampilkan hasil dari server
            showModal({
                imageUrl: URL.createObjectURL(fileInput.files[0]), // Menampilkan gambar yang di-upload
                foodName: result.foodName,
                caloriesPerGram: result.caloriesPerGram,
                dietSuitability: result.dietSuitability,
                // confidence: result.confidence
            });
        } else {
            alert("Failed to upload the image. Please try again.");
        }        
    } catch (error) {
        console.error("Error uploading file:", error);
        alert("An error occurred. Please try again.");
    }
});

document.querySelectorAll('.sample-image').forEach(image => {
    image.addEventListener('click', function() {
        const imageUrl = this.src; // Get the image URL of the clicked sample
        uploadImageToAI(imageUrl);
    });
});

function uploadImageToAI(imageUrl) {
    // Create a dummy file input element (you could use a real file input if needed)
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';

    // This is where you would typically upload the image to your AI model
    // For example, you might use a fetch request to send the image to the server
    // Since you want to pass the image URL, we simulate the upload

    const formData = new FormData();
    
    // Simulate selecting an image from the sample (this would require actual logic on the backend)
    const fakeFile = dataURLToFile(imageUrl, 'sample-image.jpg'); // Convert the image URL to a File object
    formData.append('file', fakeFile);

    // Example of sending the file to your AI (you should replace the URL with your API endpoint)
    fetch('https://your-ai-endpoint.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('AI Response:', data);
        // Here you can handle the response from the AI, for example, display the calorie count
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
}

// Helper function to convert data URL (image src) to File object
function dataURLToFile(dataUrl, filename) {
    const arr = dataUrl.split(','), mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
}

document.querySelectorAll('.sample-image').forEach(image => {
    image.addEventListener('click', function() {
        const imageUrl = this.src; // Get the image URL of the clicked sample
        uploadImageToAI(imageUrl);
    });
});

function uploadImageToAI(imageUrl) {
    // Create a dummy file input element (you could use a real file input if needed)
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';

    // This is where you would typically upload the image to your AI model
    const formData = new FormData();
    const fakeFile = dataURLToFile(imageUrl, 'sample-image.jpg'); // Convert the image URL to a File object
    formData.append('file', fakeFile);

    // Example of sending the file to your AI (you should replace the URL with your API endpoint)
    fetch('https://your-ai-endpoint.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('AI Response:', data);
        // Display the result in the modal
        showModal(data);
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
}

function dataURLToFile(dataUrl, filename) {
    const arr = dataUrl.split(','), mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
}

function showModal(data) {
    // Fill the modal with AI result
    document.getElementById('foodImage').src = data.imageUrl; // Show the uploaded image
    document.getElementById('foodName').textContent = data.foodName; // AI predicted food name
    document.getElementById('calories').textContent = data.caloriesPerGram; // Calories per gram
    document.getElementById('dietSuitability').textContent = data.dietSuitability; // Diet suitability message
    // const confidencePercent = (data.confidence * 100).toFixed(2); // Convert to percentage and fix 2 decimal points
    // document.getElementById('confidence').textContent = confidencePercent + "%"; // Show confidence as percentage
    // Display the modal
    document.getElementById('resultModal').style.display = 'block';
}

// Function to close the modal
function closeModal() {
    document.getElementById('resultModal').style.display = 'none'; // Hide the modal
}