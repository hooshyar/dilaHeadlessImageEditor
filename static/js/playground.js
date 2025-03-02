document.addEventListener('DOMContentLoaded', function() {
    // Range input value displays
    document.getElementById('fontSize').addEventListener('input', function() {
        document.getElementById('fontSizeValue').textContent = this.value + 'px';
    });
    
    document.getElementById('textOpacity').addEventListener('input', function() {
        const percentage = Math.round(this.value * 100);
        document.getElementById('textOpacityValue').textContent = percentage + '%';
    });
    
    document.getElementById('bgOpacity').addEventListener('input', function() {
        const percentage = Math.round(this.value * 100);
        document.getElementById('bgOpacityValue').textContent = percentage + '%';
    });
    
    document.getElementById('bgCurve').addEventListener('input', function() {
        document.getElementById('bgCurveValue').textContent = this.value + 'px';
    });
    
    document.getElementById('containerWidth').addEventListener('input', function() {
        document.getElementById('containerWidthValue').textContent = this.value + '%';
    });
    
    document.getElementById('containerMargin').addEventListener('input', function() {
        document.getElementById('containerMarginValue').textContent = this.value + 'px';
    });
    
    // Color picker synchronization
    document.getElementById('textColorPicker').addEventListener('input', function() {
        document.getElementById('textColor').value = this.value;
    });
    
    document.getElementById('backgroundColorPicker').addEventListener('input', function() {
        document.getElementById('backgroundColor').value = this.value;
    });
    
    document.getElementById('gradientStartColorPicker').addEventListener('input', function() {
        document.getElementById('gradientStartColor').value = this.value;
    });
    
    document.getElementById('gradientEndColorPicker').addEventListener('input', function() {
        document.getElementById('gradientEndColor').value = this.value;
    });
    
    // Dimension presets
    document.getElementById('preset').addEventListener('change', function() {
        const presetValue = this.value;
        if (presetValue === 'instagram-stories') {
            document.getElementById('outputWidth').value = 1080;
            document.getElementById('outputHeight').value = 1920;
        } else if (presetValue === 'instagram-feed') {
            document.getElementById('outputWidth').value = 1080;
            document.getElementById('outputHeight').value = 1350;
        } else if (presetValue === 'instagram-grid') {
            document.getElementById('outputWidth').value = 1080;
            document.getElementById('outputHeight').value = 1080;
        }
    });
    
    // Gradient presets
    document.querySelectorAll('.gradient-preset').forEach(function(button) {
        button.addEventListener('click', function() {
            const startColor = this.getAttribute('data-start');
            const endColor = this.getAttribute('data-end');
            
            document.getElementById('gradientStartColor').value = startColor;
            document.getElementById('gradientStartColorPicker').value = startColor;
            document.getElementById('gradientEndColor').value = endColor;
            document.getElementById('gradientEndColorPicker').value = endColor;
        });
    });
    
    // Generate preview
    document.getElementById('generatePreview').addEventListener('click', function() {
        const payload = buildPayload();
        const initialMessage = document.getElementById('initialMessage');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const previewImage = document.getElementById('previewImage');
        
        // Show loading spinner
        initialMessage.classList.add('d-none');
        loadingSpinner.classList.remove('d-none');
        previewImage.classList.add('d-none');
        
        // Update code block
        updateCodeBlock(payload);
        
        // Send API request
        fetch('/process_custom', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('API request failed');
            }
            return response.blob();
        })
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            previewImage.src = imageUrl;
            loadingSpinner.classList.add('d-none');
            previewImage.classList.remove('d-none');
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.classList.add('d-none');
            initialMessage.classList.remove('d-none');
            initialMessage.innerHTML = '<p class="text-danger">Error generating preview. Please check your settings.</p>';
        });
    });
    
    // Copy code button
    document.getElementById('copyCodeBtn').addEventListener('click', function() {
        const codeBlock = document.getElementById('codeBlock');
        navigator.clipboard.writeText(codeBlock.textContent)
            .then(() => {
                this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
            });
    });
    
    // Fetch available fonts from API
    fetch('/fonts')
        .then(response => response.json())
        .then(data => {
            const fontSelect = document.getElementById('fontFamily');
            fontSelect.innerHTML = ''; // Clear existing options
            
            // Combine local and Google fonts
            const allFonts = [
                ...data.local_fonts.map(font => ({ name: font, type: 'Local' })),
                ...data.popular_google_fonts.map(font => ({ name: font, type: 'Google' }))
            ].sort((a, b) => a.name.localeCompare(b.name));
            
            // Add option groups
            const localGroup = document.createElement('optgroup');
            localGroup.label = 'Local Fonts';
            
            const googleGroup = document.createElement('optgroup');
            googleGroup.label = 'Google Fonts';
            
            allFonts.forEach(font => {
                const option = document.createElement('option');
                option.value = font.name;
                option.textContent = font.name;
                
                if (font.type === 'Local') {
                    localGroup.appendChild(option);
                } else {
                    googleGroup.appendChild(option);
                }
            });
            
            fontSelect.appendChild(localGroup);
            fontSelect.appendChild(googleGroup);
        })
        .catch(error => console.error('Error fetching fonts:', error));
});

// Build the API payload from form values
function buildPayload() {
    // Get the font weight/style
    let fontFamily = document.getElementById('fontFamily').value;
    const fontWeight = document.getElementById('fontWeight').value;
    if (fontWeight !== '400') {
        fontFamily = `${fontFamily}:${fontWeight}`;
    }
    
    return {
        image_url: document.getElementById('imageUrl').value,
        text: document.getElementById('overlayText').value,
        language: document.getElementById('language').value,
        font_family: fontFamily,
        font_size: parseInt(document.getElementById('fontSize').value),
        text_color: document.getElementById('textColor').value,
        background_color: document.getElementById('backgroundColor').value,
        text_position: null, // Using alignment instead
        alignment: document.getElementById('alignment').value,
        output_dimensions: {
            width: parseInt(document.getElementById('outputWidth').value),
            height: parseInt(document.getElementById('outputHeight').value)
        },
        preset: document.getElementById('preset').value,
        padding: {
            top: parseInt(document.getElementById('paddingTop').value),
            right: parseInt(document.getElementById('paddingRight').value),
            bottom: parseInt(document.getElementById('paddingBottom').value),
            left: parseInt(document.getElementById('paddingLeft').value)
        },
        text_opacity: parseFloat(document.getElementById('textOpacity').value),
        bg_opacity: parseFloat(document.getElementById('bgOpacity').value),
        bg_curve: parseInt(document.getElementById('bgCurve').value),
        container_margin: parseInt(document.getElementById('containerMargin').value),
        container_width_percent: parseInt(document.getElementById('containerWidth').value),
        gradient_start_color: document.getElementById('gradientStartColor').value,
        gradient_end_color: document.getElementById('gradientEndColor').value,
        gradient_direction: document.getElementById('gradientDirection').value
    };
}

// Update the code block with curl command
function updateCodeBlock(payload) {
    const jsonString = JSON.stringify(payload, null, 2);
    const curlCommand = `curl -X POST http://localhost:5001/process_custom \\
-H "Content-Type: application/json" \\
-d '${jsonString}' \\
--output processed_image.png`;
    
    document.getElementById('codeBlock').textContent = curlCommand;
} 