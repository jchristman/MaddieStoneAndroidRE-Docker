# Exercise 1

## Goals:

1. Learn to use jadx for reverse engineering APKs
2. Practice identifying class(es) that would be good starting points to begin your revering

## Instructions

- [x] ~Start jadx by opening the terminal in the VM and running the jadx-gui command in the terminal.~ Start the Android RE docker container from the `samples` directory. `cd `ThaiCamera`.
- [x] ~Open ThaiCamera.apk in the jadx GUI. It’s in the VM’s path at ~/samples/ThaiCamera.apk. When you open the application in jadx, you will see the following. Under the Source Code heading, the packages (namespaces for the Java classes) included in the application.~ Execute `jadx ThaiCamera.apk`
- [x] ~By clicking on the expansion tab of “Resources”,~ You can see the contents of the APK by using your favorite editor to look in the `ThaiCamera` folder. Some of the most interesting are the Manifest (AndroidManifest.xml), classes.dex (contains the DEX bytecode that is decompiled under the “Source Code” tab), and the assets/ folder which contains any other files the APK may need to run.
- [x] Open AndroidManifest.xml and identify any of the application entry points described in the Application Entry Points section.

```
# Launcher Activity
<activity android:label="@string/app_name" android:name="com.cp.camera.Loading" android:screenOrientation="portrait">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>

# Exported Receiver
<receiver android:name="com.cp.camera.ReferrerCatcher" android:exported="true">
    <intent-filter>
        <action android:name="com.android.vending.INSTALL_REFERRER"/>
    </intent-filter>
</receiver>

# Exported Receiver
<receiver android:name="com.google.firebase.iid.FirebaseInstanceIdReceiver" android:permission="com.google.android.c2dm.permission.SEND" android:exported="true">
    <intent-filter>
        <action android:name="com.google.android.c2dm.intent.RECEIVE"/>
        <action android:name="com.google.android.c2dm.intent.REGISTRATION"/>
        <category android:name="com.cp.camera"/>
    </intent-filter>
</receiver>

# Exported service
<service android:name="com.google.firebase.iid.FirebaseInstanceIdService" android:exported="true">
    <intent-filter android:priority="-500">
        <action android:name="com.google.firebase.INSTANCE_ID_EVENT"/>
    </intent-filter>
</service>
```

- [x] Using the information gathered in the previous step and the Starting Points for RE section above. Decide on a class or classes, that you think would be classes that you’d begin analyzing when you start your reversing.

`com/cp/camera/Loading.java`

