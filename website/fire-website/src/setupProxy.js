const {createProxyMiddleware} = require('http-proxy-middleware');


module.exports = function (app) {
    const appProxy = createProxyMiddleware('/info/', {
        target: "http://localhost:8000",
        secure: false
    });
    app.use(appProxy);
};
