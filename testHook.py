import frida

scr = """
setImmediate(function() {                
    Java.perform(function(){  
        console.log("[*] Starting script");
        var EncryptJni = Java.use("com.cyjh.cjencrypt.EncryptJni");
        EncryptJni.Encrypt.implementation = function(cJEncrypt,context){
            var c = this.Encrypt(cJEncrypt,context);
            send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            send(
                [
                    cJEncrypt.getPurpose(),
                    cJEncrypt.getSource(),
                    cJEncrypt.getCryptType(),
                    cJEncrypt.getIndex(),
                    context,
                    c,
                ]
            );
            return c;
        }
    });
});
"""
"""
      
        var FileEncryptJni = Java.use("com.cyjh.cjfileencrypt.FileEncryptJni");

        // hook 普通方法
        FileEncryptJni.b.implementation = function(a,b,c,d){
            // 修改方法的返回值
            send([a,b,c])
            //console.log("aaaa");
            return this.b(a,b,c,d);
        }
        var ScriptManager = Java.use("com.cyjh.gundam.fengwoscript.script.a.b.ScriptManager");
        ScriptManager.b.overload('int','java.lang.String').implementation = function (a,b) {
            var x = this.b(a,b);
            send(x)
            return x;        
        }
"""

rdev = frida.get_usb_device()

process_list = """
com.cyjh.gundam
com.cyjh.gundam.service.ScriptService.p
com.cyjh.gundam:channel
com.cyjh.gundam:download_server
com.cyjh.gundam:mqrun
com.cyjh.gundam:remote
""".strip().splitlines()

for process in process_list:
    print("Attaching", process)
    session = rdev.attach(process)
    script = session.create_script(scr)

    def on_message(message, data):
        if message.get("type", None) == "send":
            print(process, message["payload"])
        else:
            print(process, message, data)

    script.on("message", on_message)
    script.load()
