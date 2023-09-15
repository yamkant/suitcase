class MyWebSocket {
    constructor(ws_host, room_name) {
        this.ws_host = ws_host;
        this.ws = new WebSocket(this.ws_host + "/chats/" + room_name + '/');
        this.open(room_name)
    }

    open = (room_name) => {
        this.ws.onopen = () => {
            console.log("Web socket is connected");
            this.ws.send(JSON.stringify({
                'message': room_name + ' 입장'
            }))
        }
        this.ws.onerror = (e) => {
            console.error(e)
        }
    }

    close = (func) => {
        if (func) {
            console.log(clearInterval(func));
            console.log("인터벌 종료");
        }
        this.ws.close();
        console.log("소켓 종료");
    }

    send_message = (event_type) => {
        if (this.ws.OPEN) {
            this.ws.send(JSON.stringify({
                'message': event_type,
            }))
        } else {
            console.log("소켓 종료됨, 인터벌 종료");
        }
    }
    get_interval_send_message_task = (interval, event_type) => {
        const interval_task = setInterval(this.send_message, interval, event_type);
        return interval_task
    }
}
