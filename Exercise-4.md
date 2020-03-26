# Exercise 4 - Arbitrary Command Execution Take 2

## Goals:

The goal of this exercise is to understand how to reverse engineer applications that are using Binder, specifically to look for vulnerabilities.

## Context

Let’s use the same context as Exercise #3, but this time the solution will look different. This will show us another pattern and help us understand Binder.

## Instructions

- [x] Start jadx as described in Exercise #1 and open HonSystemService.apk.

- [x] Use the Manifest to identify interesting components and the bytecode to analyze the code.

```xml
<service android:name="com.honeywell.tools.honsystemservice.SystemOperationService" android:exported="true"/>
<receiver android:name="com.honeywell.tools.honsystemservice.DeviceOwnerReceiver" android:permission="android.permission.BIND_DEVICE_ADMIN" android:enabled="true" android:exported="true">
    <meta-data android:name="android.app.device_admin" android:resource="@xml/device_owner_receiver"/>
    <intent-filter>
        <action android:name="android.app.action.PROFILE_PROVISIONING_COMPLETE"/>
    </intent-filter>
</receiver>
```

```
# egrep -R "exec" *
# The following lines are from a failed decompilation of a function called runtime Exec
sources/com/honeywell/tools/honsystemservice/SystemOperationService.java:                java.lang.Process r11 = r16.exec(r17)     // Catch:{ IOException -> 0x0360, Exception -> 0x034e }
sources/com/honeywell/tools/honsystemservice/SystemOperationService.java:                java.lang.Process r2 = r5.exec(r9)     // Catch:{ IOException -> 0x0058, InterruptedException -> 0x0069 }
sources/com/honeywell/tools/honsystemservice/SystemOperationService.java:            java.lang.Process r7 = r7.exec(r8)     // Catch:{ InterruptedException -> 0x0087, IOException -> 0x008c }
```

```
# egrep -R "runtimeExec" *
sources/com/honeywell/tools/honsystemservice/ISystemOperation.java:    List<String> runtimeExec(String str) throws RemoteException;
sources/com/honeywell/tools/honsystemservice/ISystemOperation.java:        static final int TRANSACTION_runtimeExec = 10;
sources/com/honeywell/tools/honsystemservice/ISystemOperation.java:                    List<String> _result4 = runtimeExec(data.readString());
sources/com/honeywell/tools/honsystemservice/ISystemOperation.java:            public List<String> runtimeExec(String cmd) throws RemoteException {
```

```java
private static final String DESCRIPTOR = "com.honeywell.tools.honsystemservice.ISystemOperation";
static final int TRANSACTION_runtimeExec = 10;

/* ... skip a bunch of lines ... */

public boolean onTransact(int code, Parcel data, Parcel reply, int flags) throws RemoteException {
    Intent _arg0;
    Uri _arg02;
    ContentValues _arg1;
    switch (code) {
        /* ... skip a bunch of lines ... */
        case TRANSACTION_runtimeExec:
            data.enforceInterface(DESCRIPTOR);
            List<String> _result4 = runtimeExec(data.readString());
            reply.writeNoException();
            reply.writeStringList(_result4);
            return true;
    }
}
```

- [x] Find a code path that allows other applications or code on the phone to run arbitrary commands as a privileged user.

There are actually several potential entry points that allow for command execution on this service: `runtimeExec` and `exeCommand`. Both end up passing transaction data straight through to `Runtime.exec`, enabling code execution in the context of the service, which is a `system` level application.
