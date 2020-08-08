Java.perform(function() {
  setImmediate(function() {
    var pointer = Module.findExportByName(
        "libmqm.so",
        "Java_com_cyjh_mqm_MQLanguageStub_Run___3BLjava_lang_String_2Ljava_lang_String_2"
    );
    send("Bind pointer: "+ pointer)
    Interceptor.attach(
      pointer,
      {
        /*
        Java_com_cyjh_mqm_MQLanguageStub_Run__Ljava_lang_String_2Ljava_lang_String_2Ljava_lang_String_2IIJ
        Java_com_cyjh_mqm_MQLanguageStub_Run__Ljava_lang_String_2Ljava_lang_String_2Ljava_lang_String_2Ljava_lang_String_2Ljava_lang_String_2IJ
        Java_com_cyjh_mqm_MQLanguageStub_Run___3BLjava_lang_String_2Ljava_lang_String_2
        Java_com_cyjh_mqm_MQLanguageStub_Run___3BLjava_lang_String_2Ljava_lang_String_2IIJ
         */
        onEnter: function(args) {
          console.log("aaa");
          var env = Java.vm.getEnv();
          var jstrings = env.GetStringUTFChars(args[3]);
          console.log(jstrings);
        },
        onLeave: function(retval) {
          send("return value:" + retval);
        }
      }
    );
  });
});
