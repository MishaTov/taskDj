const deadlines = Array.from(document.querySelectorAll('.due-to'));

function calculateTime() {
    const now = Math.floor(Date.now() / 1000);
    deadlines.forEach((element) => {
        const value = Number(element.getAttribute('value'));
        const leftTime = value - now;
        const seconds = Math.floor(leftTime % 60);
        const minutes = Math.floor((leftTime / 60) % 60);
        const hours = Math.floor((leftTime / 3600) % 24);
        const days = Math.floor(leftTime / 86400);
        let result = '';
        if (days) {
            result += days !== 1 ? `${days} days` : `${days} day`;
        }
        if (days || hours) {
            result += hours !== 1 ? ` ${hours} hours` : ` ${hours} hour`;
        }
        if (days || hours || minutes) {
            result += minutes !== 1 ? ` ${minutes} minutes` : ` ${minutes} minute`;
        }
        if (days || hours || minutes || seconds) {
            result += seconds !== 1 ? ` ${seconds} seconds` : ` ${seconds} second`;
        }
        element.parentNode.parentNode.querySelector('.time-left').textContent = result;
        if (leftTime <= 0) {
            const ind = deadlines.indexOf(element);
            deadlines.splice(ind, 1);
            if (!deadlines) {
                clearInterval(updateTime);
            }
            element.parentNode.parentNode.querySelector('.time-left').textContent = 'Time is over';
        }
    })
}

const updateTime = setInterval(calculateTime, 1000);