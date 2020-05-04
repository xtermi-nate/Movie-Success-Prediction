const axios = require("axios").default;

module.exports = class MovieRetriever {
    constructor() {}

    static getMovieData(content) {
        return axios.post("http://127.0.0.1:5000/", { content });
    }

    static showMovieData(content) {
        return axios.get("http://127.0.0.1:5000/", { content });
    }

};
