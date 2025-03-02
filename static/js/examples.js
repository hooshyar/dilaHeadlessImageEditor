document.addEventListener('DOMContentLoaded', function() {
    // Example presets for different languages
    const examples = {
        english: [
            {
                name: "Professional Quote",
                text: "Success is not final, failure is not fatal: It is the courage to continue that counts.",
                language: "en",
                font: "Montserrat:700",
                size: 48,
                text_color: "#FFFFFF",
                bg_color: "#1a1a1a",
                bg_opacity: 0.85,
                corner_radius: 15,
                alignment: "center-center",
                gradient_start: "#FF416C",
                gradient_end: "#FF4B2B",
                image_url: "https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?q=80&w=1074&auto=format&fit=crop",
                description: "Elegant professional quote with gradient background"
            },
            {
                name: "Nature Caption",
                text: "Find peace in the beauty of nature's embrace",
                language: "en",
                font: "Roboto:300",
                size: 42,
                text_color: "#FFFFFF",
                bg_color: "#000000",
                bg_opacity: 0.65,
                corner_radius: 8,
                alignment: "bottom-center",
                gradient_start: "#4776E6",
                gradient_end: "#8E54E9",
                image_url: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=1074&auto=format&fit=crop",
                description: "Beautiful nature caption with subtle overlay"
            },
            {
                name: "Creative Inspiration",
                text: "Creativity is intelligence having fun",
                language: "en",
                font: "Open Sans:italic",
                size: 36,
                text_color: "#F8F8F8",
                bg_color: "#181818",
                bg_opacity: 0.75,
                corner_radius: 20,
                alignment: "top-center",
                gradient_start: "#11998e",
                gradient_end: "#38ef7d",
                image_url: "https://images.unsplash.com/photo-1531913764164-f85c52d7e6a9?q=80&w=1074&auto=format&fit=crop",
                description: "Creative inspiration quote with modern styling"
            }
        ],
        arabic: [
            {
                name: "Arabic Wisdom",
                text: "العقل السليم في الجسم السليم",
                language: "ar",
                font: "Cairo:700",
                size: 52,
                text_color: "#FFFFFF",
                bg_color: "#222222",
                bg_opacity: 0.8,
                corner_radius: 12,
                alignment: "center-center",
                gradient_start: "#f953c6",
                gradient_end: "#b91d73",
                image_url: "https://images.unsplash.com/photo-1565902603486-e807b6197c81?q=80&w=1074&auto=format&fit=crop",
                description: "Classic Arabic wisdom quote with elegant styling"
            },
            {
                name: "Arabic Poetry",
                text: "كُن جميلاً ترى الوجود جميلا",
                language: "ar",
                font: "Tajawal:400",
                size: 42,
                text_color: "#FFFFFF",
                bg_color: "#1a1a1a",
                bg_opacity: 0.7,
                corner_radius: 10,
                alignment: "bottom-center",
                gradient_start: "#2193b0",
                gradient_end: "#6dd5ed",
                image_url: "https://images.unsplash.com/photo-1516912481808-3406841bd33c?q=80&w=1074&auto=format&fit=crop",
                description: "Arabic poetry with serene blue gradient"
            },
            {
                name: "Arabic Motivation",
                text: "كن عظيماً في هدفك ، متواضعاً في طموحك",
                language: "ar",
                font: "Almarai:700",
                size: 40,
                text_color: "#FFFFFF",
                bg_color: "#222222",
                bg_opacity: 0.75,
                corner_radius: 15,
                alignment: "top-center",
                gradient_start: "#FF8008",
                gradient_end: "#FFC837",
                image_url: "https://images.unsplash.com/photo-1496449903678-68ddcb189a24?q=80&w=1170&auto=format&fit=crop",
                description: "Motivational Arabic quote with warm gradient"
            }
        ],
        kurdish: [
            {
                name: "Kurdish Wisdom",
                text: "ئەو کەسەی لە هەڵەکانی نەترسێت، سەرکەوتوو دەبێت",
                language: "ckb",
                font: "Tajawal:700",
                size: 46,
                text_color: "#FFFFFF",
                bg_color: "#1a1a1a",
                bg_opacity: 0.85,
                corner_radius: 12,
                alignment: "center-center",
                gradient_start: "#4776E6",
                gradient_end: "#8E54E9",
                image_url: "https://images.unsplash.com/photo-1519677584237-752f8853252e?q=80&w=1074&auto=format&fit=crop",
                description: "Kurdish wisdom with purple gradient background"
            },
            {
                name: "Kurdish Mixed Text",
                text: "توێژینەوەی قوڵی OpenAI: یاریدەدەرێکی شۆڕشگێڕی زیرەکی دەستکرد بۆ توێژینەوە",
                language: "ckb",
                font: "Noto Sans Arabic:700",
                size: 64,
                text_color: "#FFFFFF",
                bg_color: "#1a1a1a",
                bg_opacity: 0.7,
                corner_radius: 0,
                alignment: "center-center",
                gradient_start: "#FF9500",
                gradient_end: "#FF4C00",
                container_width_percent: 100,
                container_margin: 0,
                image_url: "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?q=80&w=1074&auto=format&fit=crop",
                description: "Large Kurdish text with full-width gradient background"
            },
            {
                name: "Kurdish Proverb",
                text: "دەستێک گوڵ نابێت بە بەهار",
                language: "ckb",
                font: "Cairo:400",
                size: 44,
                text_color: "#FFFFFF",
                bg_color: "#222222",
                bg_opacity: 0.7,
                corner_radius: 10,
                alignment: "bottom-center",
                gradient_start: "#11998e",
                gradient_end: "#38ef7d",
                image_url: "https://images.unsplash.com/photo-1528663337188-2aa9d5ba7217?q=80&w=1171&auto=format&fit=crop",
                description: "Kurdish proverb with nature-themed styling"
            },
            {
                name: "Kurdish Inspiration",
                text: "بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت",
                language: "ckb",
                font: "Tajawal:700",
                size: 40,
                text_color: "#FFFFFF",
                bg_color: "#1a1a1a",
                bg_opacity: 0.75,
                corner_radius: 15,
                alignment: "top-center",
                gradient_start: "#FF416C",
                gradient_end: "#FF4B2B",
                image_url: "https://images.unsplash.com/photo-1506617420156-8e4536971650?q=80&w=1074&auto=format&fit=crop",
                description: "Inspirational Kurdish quote with sunrise theme"
            }
        ]
    };

    // Function to apply an example preset to the form
    function applyExample(example) {
        // Update form fields with example values
        document.getElementById('overlayText').value = example.text;
        document.getElementById('language').value = example.language;
        
        // Extract font family and weight
        let fontParts = example.font.split(':');
        document.getElementById('fontFamily').value = fontParts[0];
        if (fontParts.length > 1) {
            document.getElementById('fontWeight').value = fontParts[1];
        } else {
            document.getElementById('fontWeight').value = '400';
        }
        
        document.getElementById('fontSize').value = example.size;
        document.getElementById('fontSizeValue').textContent = example.size + 'px';
        
        document.getElementById('textColor').value = example.text_color;
        document.getElementById('textColorPicker').value = example.text_color;
        
        document.getElementById('backgroundColor').value = example.bg_color;
        document.getElementById('backgroundColorPicker').value = example.bg_color;
        
        document.getElementById('bgOpacity').value = example.bg_opacity;
        document.getElementById('bgOpacityValue').textContent = Math.round(example.bg_opacity * 100) + '%';
        
        document.getElementById('bgCurve').value = example.corner_radius;
        document.getElementById('bgCurveValue').textContent = example.corner_radius + 'px';
        
        document.getElementById('alignment').value = example.alignment;
        
        document.getElementById('gradientStartColor').value = example.gradient_start;
        document.getElementById('gradientStartColorPicker').value = example.gradient_start;
        
        document.getElementById('gradientEndColor').value = example.gradient_end;
        document.getElementById('gradientEndColorPicker').value = example.gradient_end;
        
        document.getElementById('imageUrl').value = example.image_url;
        
        // Set container width and margin if available
        if (example.container_width_percent !== undefined) {
            document.getElementById('containerWidth').value = example.container_width_percent;
            document.getElementById('containerWidthValue').textContent = example.container_width_percent + '%';
        }
        
        if (example.container_margin !== undefined) {
            document.getElementById('containerMargin').value = example.container_margin;
            document.getElementById('containerMarginValue').textContent = example.container_margin + 'px';
        }
        
        // Trigger preview generation
        document.getElementById('generatePreview').click();
    }

    // Function to create the examples section
    function createExamplesSection() {
        // Create examples container
        const examplesContainer = document.createElement('div');
        examplesContainer.className = 'card mb-4';
        
        // Create card header
        const cardHeader = document.createElement('div');
        cardHeader.className = 'card-header';
        cardHeader.innerHTML = '<h5 class="mb-0">Creative Examples</h5>';
        examplesContainer.appendChild(cardHeader);
        
        // Create card body
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        examplesContainer.appendChild(cardBody);
        
        // Create tabs for language selection
        const tabsNav = document.createElement('ul');
        tabsNav.className = 'nav nav-tabs mb-3';
        tabsNav.id = 'examplesTabs';
        tabsNav.setAttribute('role', 'tablist');
        
        // Create tab content container
        const tabContent = document.createElement('div');
        tabContent.className = 'tab-content';
        tabContent.id = 'examplesTabContent';
        
        // Create tabs and content for each language
        const languages = [
            { id: 'english', name: 'English', badgeClass: 'badge-en' },
            { id: 'arabic', name: 'Arabic', badgeClass: 'badge-ar' },
            { id: 'kurdish', name: 'Kurdish', badgeClass: 'badge-ckb' }
        ];
        
        languages.forEach((lang, index) => {
            // Create tab
            const tabItem = document.createElement('li');
            tabItem.className = 'nav-item';
            tabItem.setAttribute('role', 'presentation');
            
            const tabButton = document.createElement('button');
            tabButton.className = `nav-link ${index === 0 ? 'active' : ''}`;
            tabButton.id = `${lang.id}-tab`;
            tabButton.setAttribute('data-bs-toggle', 'tab');
            tabButton.setAttribute('data-bs-target', `#${lang.id}-examples`);
            tabButton.setAttribute('type', 'button');
            tabButton.setAttribute('role', 'tab');
            tabButton.innerHTML = `${lang.name} <span class="badge ${lang.badgeClass} ms-1">${examples[lang.id].length}</span>`;
            
            tabItem.appendChild(tabButton);
            tabsNav.appendChild(tabItem);
            
            // Create tab content panel
            const tabPane = document.createElement('div');
            tabPane.className = `tab-pane fade ${index === 0 ? 'show active' : ''}`;
            tabPane.id = `${lang.id}-examples`;
            tabPane.setAttribute('role', 'tabpanel');
            
            // Create row for examples
            const row = document.createElement('div');
            row.className = 'row g-3';
            
            // Add examples for this language
            examples[lang.id].forEach(example => {
                const col = document.createElement('div');
                col.className = 'col-md-4';
                
                const card = document.createElement('div');
                card.className = 'example-card';
                card.addEventListener('click', () => applyExample(example));
                
                // Card content
                card.innerHTML = `
                    <img src="${example.image_url}" alt="${example.name}" class="example-image">
                    <div class="example-info">
                        <div class="example-title">${example.name}</div>
                        <div class="example-description">${example.description}</div>
                    </div>
                `;
                
                col.appendChild(card);
                row.appendChild(col);
            });
            
            tabPane.appendChild(row);
            tabContent.appendChild(tabPane);
        });
        
        // Add tabs and content to the card body
        cardBody.appendChild(tabsNav);
        cardBody.appendChild(tabContent);
        
        // Insert the examples section before the configuration panel
        const configPanel = document.querySelector('.row');
        configPanel.parentNode.insertBefore(examplesContainer, configPanel);
    }
    
    // Initialize examples section
    createExamplesSection();
}); 