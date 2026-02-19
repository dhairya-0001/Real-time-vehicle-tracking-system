document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('video-feed');
    const fpsDisplay = document.getElementById('fps-display');
    const totalCount = document.getElementById('total-count');
    const webcamBtn = document.getElementById('webcam-btn');
    const videoUpload = document.getElementById('video-upload');

    // Counts
    const countCar = document.getElementById('count-car');
    const countTruck = document.getElementById('count-truck');
    const countBus = document.getElementById('count-bus');
    const countMotorcycle = document.getElementById('count-motorcycle');

    // Polling stats
    setInterval(async () => {
        try {
            const response = await fetch('/stats');
            const data = await response.json();

            // Update FPS
            fpsDisplay.innerText = Math.round(data.fps);

            // Update Counts
            totalCount.innerText = data.total;
            countCar.innerText = data.counts['car'] || 0;
            countTruck.innerText = data.counts['truck'] || 0;
            countBus.innerText = data.counts['bus'] || 0;
            countMotorcycle.innerText = data.counts['motorcycle'] || 0;

        } catch (error) {
            console.error('Error fetching stats:', error);
        }
    }, 1000); // Update every second

    // Webcam Button
    webcamBtn.addEventListener('click', () => {
        videoFeed.src = "/video_feed?" + new Date().getTime(); // Force reload
    });

    // File Upload
    videoUpload.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload_video', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            console.log('Upload success:', result);

            // Assuming the backend would return a path or token to convert to a stream URL
            // For this demo, we can just point to the video_feed_file endpoint
            videoFeed.src = `/video_feed_file?filename=${file.name}`;

        } catch (error) {
            console.error('Upload failed:', error);
        }
    });
});
