#从app模块中导入app应用
from app import app

#防止被引用后执行，只有在当前模块中才可以使用
if __name__=='__main__':
    #app.run(host='127.0.0.1',port=80,ssl_context='adhoc')
    app.run(host='127.0.0.1',port=8080, threaded=True)
    #app.run(host='192.168.191.1', port=443, threaded=True,ssl_context='adhoc')
    #app.run(host='192.168.191.1', port=443,debug=True,ssl_context='adhoc')
    #app.run(host='192.168.43.142', port=443,ssl_context='adhoc')