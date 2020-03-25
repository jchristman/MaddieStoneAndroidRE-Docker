# Exercise 3 - Find the Vulnerability in the Adups OTA Application

## Goals:

The goal of this exercise is to apply our DEX reverse engineering skills to finding a vulnerability in an Android app. This example is a little more complex and will introduce us to reversing across different components of the application.

## Context

You are auditing a set of phones for security issues prior to allowing them onto your enterprise network. You are going through the apps that come pre-installed. For this pre-installed application, you are concerned that there may be a vulnerability that allows it to run arbitrary commands.

## Instructions

- [x] Start jadx as described in Exercise #1 and open FotaProvider.apk.

- [ ] Use the Manifest to identify interesting components and the bytecode to analyze the code.

Entry Points of interest:

```
<service android:name="com.adups.fota.sysoper.SysService">
    <intent-filter>
        <action android:name="android.intent.action.AdupsFota.SysService"/>
    </intent-filter>
</service>

<service android:label="AppService" android:name="com.dataeye.channel.DCAppService" android:persistent="true" android:exported="true" android:process=":de_service">
    <intent-filter android:priority="1000">
        <action android:name="com.dataeye.channel.action.INVOKE_SERVICE"/>
    </intent-filter>
</service>
```

Source analysis

- [ ] Find a code path that allows other applications or code on the phone to run arbitrary commands as a privileged user.
