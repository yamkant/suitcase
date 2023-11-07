export function setEventSource(channelName) {
    const es = new ReconnectingEventSource(`/events/${channelName}/`);

    es.addEventListener('stream-reset', function (e) {
        // ... client fell behind, reinitialize ...
    }, false);

    return es
}
