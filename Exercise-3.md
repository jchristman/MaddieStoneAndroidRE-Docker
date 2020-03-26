# Exercise 3 - Find the Vulnerability in the Adups OTA Application

## Goals:

The goal of this exercise is to apply our DEX reverse engineering skills to finding a vulnerability in an Android app. This example is a little more complex and will introduce us to reversing across different components of the application.

## Context

You are auditing a set of phones for security issues prior to allowing them onto your enterprise network. You are going through the apps that come pre-installed. For this pre-installed application, you are concerned that there may be a vulnerability that allows it to run arbitrary commands.

## Instructions

- [x] Start jadx as described in Exercise #1 and open FotaProvider.apk.

- [x] Use the Manifest to identify interesting components and the bytecode to analyze the code.

Entry Points of interest:

```
<service android:name="com.adups.fota.sysoper.SysService">
    <intent-filter>
        <action android:name="android.intent.action.AdupsFota.SysService"/>
    </intent-filter>
</service>

<receiver android:label="WriteCommandReceiver" android:name="com.adups.fota.sysoper.WriteCommandReceiver">
    <intent-filter>
        <action android:name="android.intent.action.AdupsFota.WriteCommandReceiver"/>
        <action android:name="android.intent.action.AdupsFota.OperReceiver"/>
    </intent-filter>
</receiver>

<receiver android:name="com.adups.fota.sysoper.TaskReceiver">
    <intent-filter>
        <action android:name="android.net.conn.CONNECTIVITY_CHANGE"/>
        <action android:name="android.intent.action.ACTION_POWER_CONNECTED"/>
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.PACKAGE_ADDED"/>
        <action android:name="android.intent.action.PACKAGE_REMOVED"/>
        <action android:name="android.intent.action.PACKAGE_REPLACED"/>
        <data android:scheme="package"/>
    </intent-filter>
</receiver>

<service android:label="AppService" android:name="com.dataeye.channel.DCAppService" android:persistent="true" android:exported="true" android:process=":de_service">
    <intent-filter android:priority="1000">
        <action android:name="com.dataeye.channel.action.INVOKE_SERVICE"/>
    </intent-filter>
</service>
```

- [x] Find a code path that allows other applications or code on the phone to run arbitrary commands as a privileged user.

WriteCommandReceiver has a function that will execute arbitrary commands if an intent is sent with the action of `android.intent.action.AdupsFota.operReceiver`. If there is an extra string called `cmd`, that string will be executed via `ProcessBuilder`


