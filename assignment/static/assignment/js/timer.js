const deadlines = Array.from(document.querySelectorAll('.due-to'));

function calculateTime() {
    const now = Math.floor(Date.now() / 1000);
    deadlines.forEach(element => {
        const value = Number(element.getAttribute('value'));
        const leftTime = value - now;
        if (leftTime <= 0){
            element.parentNode.parentNode.querySelector('.time-left').innerText = 'Time is over';
            return;
        }
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
    })
}

calculateTime();
setInterval(calculateTime, 1000);



// function updateTimeLeft() {
//     const timeLeftElements = document.querySelectorAll('.time-left');
//     timeLeftElements.forEach(el => {
//         const deadline = new Date(el.getAttribute('data-deadline'));
//         const now = new Date();
//         const timeDiff = deadline - now;
//         const taskUid = el.closest('.task-info').getAttribute('id')
//         if (timeDiff > 0) {
//             const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
//             const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//             const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
//             const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);
//
//             let timeParts = [];
//             let foundNonZero = false;
//
//             if (days > 0) {
//                 timeParts.push(`${days} ${days === 1 ? 'day' : 'days'}`);
//                 foundNonZero = true;
//             }
//             if (hours > 0 || foundNonZero) {
//                 timeParts.push(`${hours} ${hours === 1 ? 'hour' : 'hours'}`);
//                 foundNonZero = true;
//             }
//             if (minutes > 0 || foundNonZero) {
//                 timeParts.push(`${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`);
//                 foundNonZero = true;
//             }
//             timeParts.push(`${seconds} ${seconds === 1 ? 'second' : 'seconds'}`);
//
//             el.innerHTML = timeParts.join(' ');
//         } else {
//             el.innerHTML = 'Time is over';
//             socketio.emit('missed deadline', taskUid)
//         }
//     });
// }
// setInterval(updateTimeLeft, 1000);
// document.addEventListener('DOMContentLoaded', updateTimeLeft);
