//
// Playing image sequence hoevering thumbnails
//

const thumbnailContainer = document.getElementById('thumbnailContainer');
const searchInput = document.getElementById('searchInput');
const thumbnail = document.querySelectorAll('[id=thumbnail]');
// const srr = thumbnail.src;
// imgsrc = thumbnail.dataset.imgpath

// framestart = parseInt(thumbnail.dataset.startframe);
// frameend = parseInt(thumbnail.dataset.startend)
const fps = 24; // Set your desired frame rate
const frameDelay = 1000 / fps; // ~41.67ms for 24fps

// Preload images - fixed numbering

let currentFrame = 0;
let animationInterval;
let lastFrameTime = 0;

// Space Bar is not working in search bar so enabling it
searchInput.addEventListener('keydown', function(e) {
    if (e.key === ' ' || e.key === 'Spacebar') {
        e.stopPropagation(); // Only use if event is being blocked by parent
    }
});

// iterate to each thumbnail, load images and preview
thumbnail.forEach(e => {
    const images = [];

    e.addEventListener('mouseenter', () => {
        imgsrc = e.dataset.imgpath

        framestart = parseInt(e.dataset.startframe);
        frameend = parseInt(e.dataset.startend)
        const imageCount = frameend;
        

        for (let i = framestart; i <= imageCount; i++) {
            const img = new Image();
            const frameNum = i.toString().padStart(3, '0');
            img.src = `${imgsrc}_${frameNum}.jpg`
            images.push(img);
        }

        currentFrame = 0;
        lastFrameTime = performance.now();
        updateFrame();

        function animate(currentTime) {
            const elapsed = currentTime - lastFrameTime;
            
            if (elapsed >= frameDelay) {
                currentFrame = (currentFrame + 1) % images.length;
                updateFrame();
                lastFrameTime = currentTime - (elapsed % frameDelay);
            }
            
            animationInterval = requestAnimationFrame(animate);
        }
        
        animationInterval = requestAnimationFrame(animate);
    });

    e.addEventListener('mouseleave', () => {
        cancelAnimationFrame(animationInterval);
        e.src = images[0].src;
     });

     function updateFrame() {
        if (images[currentFrame].complete) {
            e.src = images[currentFrame].src;
        }
    };
});
