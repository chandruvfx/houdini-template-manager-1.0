document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    // From django get variable value mentioned in the 'json_script'. total bundles
    // passed from the django views context
    const total_bundles = parseInt(JSON.parse(document.getElementById('total_bundles').textContent));
    
    //Iterate through bundles and give per plaback controls
    for(let index=1; index<=total_bundles; ++index){
        const sequenceImage = document.getElementById(`sequence-image-${index}`);
        const frameSlider = document.getElementById(`frame-slider-${index}`);
        const frameInput = document.getElementById(`frame-input-${index}`);
        const frameTotal = document.getElementById(`frame-total-${index}`);
        const playPauseBtn = document.getElementById(`play-pause-${index}`);
        const prevFrameBtn = document.getElementById(`prev-frame-${index}`);
        const nextFrameBtn = document.getElementById(`next-frame-${index}`);
        const reverseToggle = document.getElementById(`reverse-toggle-${index}`);
        const loopToggle = document.getElementById(`loop-toggle-${index}`);
        const fpsInput = document.getElementById(`fps-input-${index}`);
        const rangeStart = document.getElementById(`range-start-${index}`);
        const rangeEnd = document.getElementById(`range-end-${index}`);
        const rangeHighlight = document.getElementById(`range-highlight-${index}`);

        // Player state
        let imageFiles = [];
        let images = [];
        let currentFrame = 0;
        let isPlaying = false;
        let isReversed = false;
        let isLooping = true;
        let fps = 24;
        let playInterval = null;
        let playRange = { start: 0, end: 0 };
        let loadedFrames = new Set(); // Track which frames have been loaded

        imageSrc = sequenceImage.dataset.imgpath;
        framestart = parseInt(sequenceImage.dataset.startframe);
        frameend = parseInt(sequenceImage.dataset.startend);
        
        // Initialize with empty image objects
        for (let i = framestart; i <= frameend; i++) {
            const frameNum = i.toString().padStart(3, '0');
            imageFiles.push(`${imageSrc}_${frameNum}.jpg`);
            images.push({ src: '', loaded: false }); // Placeholder for images
        }

        if (imageFiles.length > 0) {
            resetPlayer();
            playRange.start = 0;
            playRange.end = imageFiles.length - 1;
            updateRangeSliders();
            updateRangeHighlight();
            
            // Load first frame immediately
            loadFrame(0, true);
            
            frameSlider.max = imageFiles.length - 1;
            frameInput.max = imageFiles.length;
            frameTotal.textContent = `/ ${imageFiles.length}`;
            updateFrameCounter();
        } 
        
        // Frame slider control
        frameSlider.addEventListener('input', () => {
            currentFrame = parseInt(frameSlider.value);
            loadFrame(currentFrame);
            updateFrameCounter();
            
        });
        
        // Frame input control
        frameInput.addEventListener('change', () => {
            const frameNum = parseInt(frameInput.value);
            if (!isNaN(frameNum)) {
                const newFrame = Math.min(imageFiles.length, Math.max(1, frameNum)) - 1;
                currentFrame = newFrame;
                updateFrameDisplay();
            }
        });
        
        // Range sliders
        rangeStart.addEventListener('input', () => {
            playRange.start = parseInt(rangeStart.value);
            if (playRange.start > playRange.end) {
                playRange.end = playRange.start;
                rangeEnd.value = playRange.end;
            }
            if (currentFrame < playRange.start) {
                currentFrame = playRange.start;
                updateFrameDisplay();
            }
            updateRangeHighlight();
        });
        
        rangeEnd.addEventListener('input', () => {
            playRange.end = parseInt(rangeEnd.value);
            if (playRange.end < playRange.start) {
                playRange.start = playRange.end;
                rangeStart.value = playRange.start;
            }
            if (currentFrame > playRange.end) {
                currentFrame = playRange.end;
                updateFrameDisplay();
            }
            updateRangeHighlight();
        });
        
        // Play/pause button
        playPauseBtn.addEventListener('click', togglePlayback);
        
        // Previous frame button
        prevFrameBtn.addEventListener('click', () => {
            if (currentFrame > playRange.start) {
                currentFrame--;
                updateFrameDisplay();
            } else if (isLooping) {
                currentFrame = playRange.end;
                updateFrameDisplay();
            }
        });
        
        // Next frame button
        nextFrameBtn.addEventListener('click', () => {
            if (currentFrame < playRange.end) {
                currentFrame++;
                updateFrameDisplay();
            } else if (isLooping) {
                currentFrame = playRange.start;
                updateFrameDisplay();
            }
        });
        
        // Reverse toggle button
        reverseToggle.addEventListener('click', () => {
            isReversed = !isReversed;
            reverseToggle.classList.toggle('active', isReversed);
        });
        
        // Loop toggle button
        loopToggle.addEventListener('click', () => {
            isLooping = !isLooping;
            loopToggle.classList.toggle('active', isLooping);
        });
        
        // FPS input
        fpsInput.addEventListener('change', () => {
            fps = Math.min(120, Math.max(1, parseInt(fpsInput.value) || 24));
            fpsInput.value = fps;
            if (isPlaying) {
                stopPlayback();
                startPlayback();
            }
        });
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case ' ':
                    togglePlayback();
                    e.preventDefault();
                    break;
                case 'ArrowLeft':
                    if (currentFrame > playRange.start) {
                        currentFrame--;
                        updateFrameDisplay();
                    } else if (isLooping) {
                        currentFrame = playRange.end;
                        updateFrameDisplay();
                    }
                    e.preventDefault();
                    break;
                case 'ArrowRight':
                    if (currentFrame < playRange.end) {
                        currentFrame++;
                        updateFrameDisplay();
                    } else if (isLooping) {
                        currentFrame = playRange.start;
                        updateFrameDisplay();
                    }
                    e.preventDefault();
                    break;
                case 'r':
                    isReversed = !isReversed;
                    reverseToggle.classList.toggle('active', isReversed);
                    e.preventDefault();
                    break;
                case 'l':
                    isLooping = !isLooping;
                    loopToggle.classList.toggle('active', isLooping);
                    e.preventDefault();
                    break;
            }
        });
        
        // Functions
        function resetPlayer() {
            stopPlayback();
            currentFrame = 0;
            isPlaying = false;
            isReversed = false;
            isLooping = true;
            reverseToggle.classList.remove('active');
            loopToggle.classList.add('active');
            playPauseBtn.textContent = '⏯';
            frameInput.value = '1';
        }
        
        function loadFrame(frameIndex, forceLoad = false) {
            if (imageFiles.length === 0 || frameIndex < 0 || frameIndex >= imageFiles.length) return;
            
            // If image not loaded yet, load it
            if (!images[frameIndex].loaded || forceLoad) {
                const img = new Image();
                img.onload = () => {
                    images[frameIndex].src = img.src;
                    images[frameIndex].loaded = true;
                    sequenceImage.src = img.src;
                    loadedFrames.add(frameIndex);
                };
                img.src = imageFiles[frameIndex];
            } else {
                sequenceImage.src = images[frameIndex].src;
            }
        }

        
        function updateFrameDisplay() {
        
            frameSlider.value = currentFrame;
            frameInput.value = currentFrame + 1;
            loadFrame(currentFrame);
        }
        
        function updateFrameCounter() {
            frameInput.value = currentFrame + 1;
        }
        
        function updateRangeSliders() {
            rangeStart.max = imageFiles.length - 1;
            rangeEnd.max = imageFiles.length - 1;
            rangeStart.value = playRange.start;
            rangeEnd.value = playRange.end;
        }
        
        function updateRangeHighlight() {
            if (!imageFiles.length) return;
            
            const sliderWidth = frameSlider.offsetWidth;
            const startPos = (playRange.start / (imageFiles.length - 1)) * sliderWidth;
            const endPos = (playRange.end / (imageFiles.length - 1)) * sliderWidth;
            
            rangeHighlight.style.left = `${startPos}px`;
            rangeHighlight.style.width = `${endPos - startPos}px`;
        }
        
        function togglePlayback() {
            if (isPlaying) {
                stopPlayback();
            } else {
                startPlayback();
            }
        }
        
        
        function startPlayback() {
            if (imageFiles.length === 0) return;
            
            isPlaying = true;
            playPauseBtn.textContent = '⏸';
            
            const frameDelay = 1000 / fps;
            
            playInterval = setInterval(() => {
                if (isReversed) {
                    if (currentFrame > playRange.start) {
                        currentFrame--;
                    } else {
                        if (isLooping) {
                            currentFrame = playRange.end;
                        } else {
                            stopPlayback();
                            return;
                        }
                    }
                } else {
                    if (currentFrame < playRange.end) {
                        currentFrame++;
                    } else {
                        if (isLooping) {
                            currentFrame = playRange.start;
                        } else {
                            stopPlayback();
                            return;
                        }
                    }
                }
                
                updateFrameDisplay();
            }, frameDelay);
        }
        
        function stopPlayback() {
            isPlaying = false;
            playPauseBtn.textContent = '⏯';
            
            if (playInterval) {
                clearInterval(playInterval);
                playInterval = null;
            }
        }
        
        // Modal Pan Open and Close Operations
        const playerContainer = document.getElementById(`player-container-${index}`);
        const imageContainer = document.getElementById(`image-container-${index}`);
        const moreViewBtn = document.getElementById(`more-info-${index}`);
        const closeBtn = document.getElementById(`player-close-btn-${index}`);
        const mainContent = document.getElementById('mainContent');
        // Start with fresh values with constants
        moreViewBtn.onclick = () => {
            rangeStart.value = 0;
            rangeEnd.value = imageFiles.length - 1;
            playRange.start = 0;
            playRange.end = imageFiles.length - 1;

            const sliderWidth = 815;
            const startPos = (playRange.start / (imageFiles.length - 1)) * sliderWidth;
            const endPos = (playRange.end / (imageFiles.length - 1)) * sliderWidth;
            
            rangeHighlight.style.left = `${startPos}px`;
            rangeHighlight.style.width = `${endPos - startPos}px`;
            
            playerContainer.style.display= 'block';
            mainContent.style.filter = 'blur(10px)';
            fpsInput.value = '24';
            frameInput.value = "1";
            frameSlider.value = "0";
            //Open in the scrolled position
            playerContainer.style.top = `${window.scrollY}px`;
        };

        closeBtn.addEventListener('click', () => {
            stopPlayback();
            resetPlayer();
            frameSlider.value = "0";
            playerContainer.style.display= 'none';
            mainContent.style.filter = 'blur(0px)';
        });

        // Drag Controls
        let isDragging = false;
        let startX = 0;
        let lastX = 0;
        let animationInterval;
        const baseFrameRate = 1000/ 24;
        let currentFrameRate = baseFrameRate;
        let playbackDirection = 1;

        imageContainer.addEventListener('mouseleave', (e) => {
            if (!isDragging) {
                currentFrame = 0;
                updateFrame();
                e.preventDefault();
            }
        });

        imageContainer.addEventListener('mousedown', (e) => {
            if (e.button !== 0) return;
            
            isDragging = true;
            startX = e.clientX;
            lastX = e.clientX;
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const deltaX = e.clientX - lastX;
            lastX = e.clientX;
            
            const frameChange = Math.round(deltaX / 2);
            
            if (frameChange !== 0) {
                currentFrame += frameChange;
                
                if (currentFrame < 0) currentFrame = images.length - 1;
                if (currentFrame >= images.length) currentFrame = 0;
                
                updateFrame();
                e.preventDefault();
            }
        });

        document.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            
            isDragging = false;
            
            const totalDrag = e.clientX - startX;
            if (Math.abs(totalDrag) > 10) {
                playbackDirection = totalDrag > 0 ? 1 : -1;
            } else {
                playbackDirection = 1;
                e.preventDefault();
            }
        });

        function updateFrame() {
            loadFrame(currentFrame);
        }

        window.addEventListener('resize', () => {
            updateRangeHighlight();
        });
    }
});