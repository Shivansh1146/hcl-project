document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('review-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const resultsContainer = document.getElementById('results-container');
    const resultsContent = document.getElementById('results-content');

    // Config: adjust port based on backend
    const API_BASE_URL = 'http://localhost:8000/api';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const repo = document.getElementById('repo').value.trim();
        const prNumber = document.getElementById('pr-number').value.trim();

        if (!repo || !prNumber) return;

        setLoading(true);
        resultsContainer.classList.add('hidden');

        try {
            // Note: Replace with actual PR review endpoint later
            const response = await fetch(`${API_BASE_URL}/info`);

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            // Format mock response to display nicely
            const mockOutput = {
                status: "success",
                repository: repo,
                pull_request: parseInt(prNumber, 10),
                message: "Successfully connected to backend.",
                backend_info: data,
                ai_review_placeholder: "The AI analysis logic would go here."
            };

            resultsContent.textContent = JSON.stringify(mockOutput, null, 2);
            resultsContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error fetching review:', error);
            resultsContent.textContent = `Error: ${error.message}\n\nMake sure the FastAPI backend is running.\nRun: cd backend && uvicorn main:app --reload`;
            resultsContainer.classList.remove('hidden');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.textContent = 'Processing...';
            spinner.classList.remove('hidden');
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Run Review';
            spinner.classList.add('hidden');
        }
    }
});
