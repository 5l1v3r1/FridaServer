import json

import frida

device = frida.get_usb_device()

process_list = """
com.cyjh.gundam
com.cyjh.gundam.service.ScriptService.p
com.cyjh.gundam:channel
com.cyjh.gundam:download_server
com.cyjh.gundam:mqrun
com.cyjh.gundam:remote
""".strip().splitlines()

for process_name in process_list:
    try:
        session = device.attach(process_name)
    except (frida.NotSupportedError, frida.ProcessNotFoundError):
        print("Ignore", process_name)
        continue

    def on_message(message, data):
        print(process_name, json.loads(message["payload"]))

    scr = """
    console.log("$process$ Script initialized")
    Process.enumerateModules()
    .forEach(function(mod) {
        if (mod["path"].startsWith('/system/')) return;
        send(JSON.stringify(mod));
    });
    """.replace(
        "$process$", process_name
    )
    script = session.create_script(scr)
    script.on("message", on_message)
    script.load()
