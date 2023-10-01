class MyEventSource {
    constructor(channelName) {
        this.setEventSource(channelName)


    }

    setEventSource(channelName) {
        this.es = new ReconnectingEventSource('/events/');

    }

}