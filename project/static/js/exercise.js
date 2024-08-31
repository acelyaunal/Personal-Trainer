function toggleCamera(exercise) {
    const feedContainer = document.getElementById(exercise + '-feed-container');
    const img = document.getElementById(exercise + '-feed');

    if (feedContainer.classList.contains('off')) {
        img.src = `/video_feed/${exercise}`;
        feedContainer.classList.remove('off');
    } else {
        img.src = '';
        feedContainer.classList.add('off');
    }
}

function updateCount(exercise, count) {
    document.getElementById(`${exercise}-count`).innerText = `Count: ${count}`;
}

const eventSource = new EventSource('/update_counts');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateCount(data.exercise, data.count);
};
