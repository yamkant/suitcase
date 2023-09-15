class APIHandler {
    constructor(csrf_token) {
        this.csrf_token = csrf_token;
    }

    async update_product_api(method, prod_id, data) {
        return axios({
            method: method,
            url: `/api/products/${prod_id}/`,
            headers: {
                "Content-Type": "multipart/form-data",
                'X-CSRFToken': this.csrf_token,
            },
            data: data,
        }).then((res) => {
            return res;
        }).catch(() => {
            alert("ERROR")
        });
    }

    async update_bulk_product_api(method, data) {
        return axios({
            method: method,
            url: `/api/products/bulk/`,
            headers: {
                "Content-Type": "multipart/form-data",
                'X-CSRFToken': this.csrf_token,
            },
            data: data,
        }).then((res) => {
            return res;
        }).catch(() => {
            alert("ERROR")
        });
    }

    async delete_bulk_product_api(method, data) {
        return axios({
            method: method,
            url: `/api/products/bulk/`,
            headers: {
                "Content-Type": "multipart/form-data",
                'X-CSRFToken': this.csrf_token,
            },
            data: data,
        }).then((res) => {
            return res;
        }).catch(() => {
            alert("ERROR")
        });
    }

    async create_product_api(data) {
        return axios({
            url: `/api/products/`,
            method: 'post',
            headers: {
                "Content-Type": "multipart/form-data",
                'X-CSRFToken': this.csrf_token,
            },
            data: data,
        }).then((res) => {
            return res;
        }).catch(() => {
            alert("ERROR")
        });
    }

}