/**
 * Upload Module - Data upload and preprocessing
 */

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('upload-form')) {
        setupUploadHandlers();
    }
});

function setupUploadHandlers() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const dragArea = document.querySelector('.drag-drop-area') || document.querySelector('.upload-area');
    
    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    // Drag and drop
    if (dragArea && fileInput) {
        dragArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dragArea.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
        });
        
        dragArea.addEventListener('dragleave', () => {
            dragArea.style.backgroundColor = '';
        });
        
        dragArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dragArea.style.backgroundColor = '';
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        });
    }
    
    // Form submission
    if (form) {
        form.addEventListener('submit', handleUpload);
    }
}

function handleFileSelect() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (file) {
        console.log('File selected:', file.name);
        appState.uploadedFile = file;
    }
}

async function handleUpload(e) {
    e.preventDefault();
    
    const file = appState.uploadedFile;
    if (!file) {
        showNotification('Please select a file', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        // Upload file
        const formData = new FormData();
        formData.append('file', file);
        
        const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const uploadData = await uploadResponse.json();
        
        if (!uploadResponse.ok) {
            throw new Error(uploadData.error);
        }
        
        showNotification('File uploaded successfully', 'success');
        appState.uploadedFile = uploadData.data;
        
        // Auto-preprocess
        await preprocessData(uploadData.data);
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Upload failed: ${error.message}`, 'error');
    }
}

async function preprocessData(uploadedData) {
    try {
        showLoading();
        
        const dateColumn = document.getElementById('date-column').value || 'date';
        const targetColumn = document.getElementById('target-column').value || 'value';
        
        const preprocessResponse = await apiCall('/preprocess', 'POST', {
            filepath: uploadedData.filepath,
            date_column: dateColumn,
            target_column: targetColumn
        });
        
        appState.processedData = preprocessResponse.data;
        showNotification('Data preprocessing completed', 'success');
        
        // Show status
        const statusDiv = document.getElementById('upload-status');
        statusDiv.style.display = 'block';
        statusDiv.innerHTML = `
            <div class="status-message">
                <p><strong>Data Processed Successfully!</strong></p>
                <p>Shape: ${appState.processedData.shape}</p>
                <p>Date Column: ${appState.processedData.date_column}</p>
                <p>Target Column: ${appState.processedData.target_column}</p>
                <button class="btn btn-primary" onclick="startTraining()">
                    Train Models
                </button>
            </div>
        `;
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Preprocessing failed: ${error.message}`, 'error');
    }
}

async function startTraining() {
    try {
        showLoading();
        
        const trainingResponse = await apiCall('/train', 'POST', {
            filepath: appState.uploadedFile.filepath,
            processed_filepath: appState.processedData.processed_filepath,
            target_column: appState.processedData.target_column,
            seasonal_period: appState.processedData.seasonal_period
        });
        
        appState.trainedModels = trainingResponse.data;
        showNotification('Model training completed!', 'success');
        
        // Navigate to prediction page
        navigateToPage('predict');
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showNotification(`Training failed: ${error.message}`, 'error');
    }
}
