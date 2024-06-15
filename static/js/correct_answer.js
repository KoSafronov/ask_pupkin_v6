document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.answer-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const answerId = this.dataset.answerId;
            const isChecked = this.checked;

            fetch(correctUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    answer_id: answerId,
                    is_correct: isChecked
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.is_correct) {
                    this.checked = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isChecked;
            });
        });
    });

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
});
