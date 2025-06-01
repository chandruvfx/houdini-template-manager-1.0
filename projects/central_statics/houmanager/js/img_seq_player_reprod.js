document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const total_bundles = parseInt(JSON.parse(document.getElementById('total_bundles').textContent));

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
        // const imageCount = 138;

        imageSrc = sequenceImage.dataset.imgpath
        framestart = parseInt(sequenceImage.dataset.startframe);
        frameend = parseInt(sequenceImage.dataset.startend)
        

        // Load image sequence
        for (let i = framestart; i <= frameend; i++) {
            const img = new Image();
            const frameNum = i.toString().padStart(3, '0');
            // let seq = `${imageSrc}_${frameNum}.jpg`;
            img.src = `${imageSrc}_${frameNum}.jpg`;
            // imageFiles.push(seq);
            images.push(img);
        }


        if (imageFiles.length > 0) {
            resetPlayer();
            playRange.start = 0;
            playRange.end = imageFiles.length - 1;
            updateRangeSliders();
            updateRangeHighlight();
            loadFrame(0);
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
            // frameTotal.textContent = '/ 0';
        }
        
        function loadFrame(frameIndex) {
            if (imageFiles.length === 0 || frameIndex < 0 || frameIndex >= imageFiles.length) return;
            
            const file = imageFiles[frameIndex];
            sequenceImage.src = file
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
        
        // Modal Pan Open and Close Operations. While Close the player is reseted
        const playerContainer = document.getElementById(`player-container-${index}`);
        const imageContainer = document.getElementById(`image-container-${index}`);
        const moreViewBtn = document.getElementById(`more-info-${index}`);
        const closeBtn = document.getElementById(`player-close-btn-${index}`);
        const mainContent = document.getElementById('mainContent');

        moreViewBtn.onclick = () => {
            
            // Lot of things has to changed while deploy
            rangeStart.value = 0 ;
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
        const baseFrameRate = 1000/ 24; // milliseconds between frames
        let currentFrameRate = baseFrameRate;
        let playbackDirection = 1; // 1 for forward, -1 for backward


        imageContainer.addEventListener('mouseleave', (e) => {
            if (!isDragging) {
                currentFrame = 0;
                updateFrame();
                e.preventDefault();

            }
        });

        // Drag controls
        imageContainer.addEventListener('mousedown', (e) => {
            if (e.button !== 0) return; // Only left mouse button
            
            isDragging = true;
            startX = e.clientX;
            lastX = e.clientX;
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const deltaX = e.clientX - lastX;
            lastX = e.clientX;
            
            // Calculate frame change based on drag distance
            const frameChange = Math.round(deltaX / 2); // Adjust sensitivity
            
            if (frameChange !== 0) {
                currentFrame += frameChange;
                
                // Wrap around if needed
                if (currentFrame < 0) currentFrame = images.length - 1;
                if (currentFrame >= images.length) currentFrame = 0;
                
                updateFrame();
                e.preventDefault();

            }
        });

        document.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            
            isDragging = false;
            
            // Determine if we should play forward or backward based on final drag
            const totalDrag = e.clientX - startX;
            if (Math.abs(totalDrag) > 10) { // Minimum drag threshold
                playbackDirection = totalDrag > 0 ? 1 : -1;
            } else {
                // If just clicked without much drag, play forward
                playbackDirection = 1;
                e.preventDefault();
                
            }
        });


        function updateFrame() {
            sequenceImage.src = images[currentFrame].src;
        }
        // Handle window resize to update range highlight position
        window.addEventListener('resize', () => {
            updateRangeHighlight();
        });

    }
    
});