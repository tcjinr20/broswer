/*
code:1 保存临时数据 cookie
code:2 获取临时数据 cookie
code:3 保存永久数据
code:4 获取永久数据
code 5 保存文件
code 6 读取文件
*/


(function(win){
    function initWebSocket() {
        var websocket = null;
        var wsUri = "ws://127.0.0.1:1302";
        try {
            if (typeof MozWebSocket == 'function')
                WebSocket = MozWebSocket;
            if ( websocket && websocket.readyState == 1 )
                websocket.close();
            websocket = new WebSocket( wsUri );

            websocket.onopen = function (evt) {
                debug("CONNECTED");
                __on('ready')
            };
            websocket.onclose = function (evt) {
                debug("DISCONNECTED");
            };
            websocket.onmessage = function (evt) {
                __on('message',evt.data);
            };
            websocket.onerror = function (evt) {
                debug('ERROR: ' + evt.data);
            };
        } catch (exception) {
            debug('ERROR: ' + exception);
        }
        return websocket;
    }

    function debug(str){
        document.body.innerHTML += str+"<br/>";
    }
    var sock=initWebSocket()
    var queue = {};
    function __on(event,param){
        if(queue[event])queue[event].call(this,param)
    }

    function pyon(event,back){
        queue[event]=back
    }

    function pyemit(obj){
        sock.send(JSON.stringify(obj))
    }

    function pysetcookie(obj){
        pyemit({'code':1,"mess":JSON.stringify(obj)})
    }
    function pygetcookie(obj){
        pyemit({'code':2,"mess":JSON.stringify(obj)})
    }

    function pysetsession(obj){
        pyemit({'code':3,"mess":JSON.stringify(obj)})
    }
    function pygetsession(obj){
        pyemit({'code':4,"mess":JSON.stringify(obj)})
    }

    function pyfile(path,txt){
        if(txt){
            pyemit({'code':5,"mess":JSON.stringify({'file':path,'content':txt})})
        }else{
            pyemit({'code':6,"mess":JSON.stringify({'file':path})})
        }
    }

    win.pyjs ={
        pyon:pyon,
        pyemit:pyemit,
        pysetcookie:pysetcookie,
        pygetcookie:pygetcookie,
        pysetsession:pysetsession,
        pygetsession:pygetsession,
        pyfile:pyfile,
        debug:debug
    }
})(window)
