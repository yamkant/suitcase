import * as common from './common.js';

export async function start(username) {
    const es = common.setEventSource(username)
    es.addEventListener('message', function (e) {
        // console.log(e.data);
        openPushNotification();
    }, false);
}

const openPushNotification = () => {
    const pushNoti = document.querySelector('.push-notification');
    pushNoti.classList.remove('hidden');
}