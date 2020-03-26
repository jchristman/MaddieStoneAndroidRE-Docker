# Exercise 5 - Find the Address of the Native Function

## Goals:

The goal of this exercise is to:

1. Identify declared native methods in the DEX bytecode
2. Determine what native libraries are loaded (and thus where the native methods may be implemented)
3. Extract the native library from the APK
4. Load the native library into a disassembler
5. Identify the address (or name) of the function in the native library that is executed when the native method is called

## Instructions

- [x] Open Mediacode.apk in jadx. Refer back to Exercise #1

- [x] This time, if you expand the Resources tab, you will see that this APK has a lib/ directory. The native libraries for this APK are in the default CPU paths.

- [x] Now we need to identify any declared native methods. In jadx, search and list all declared native methods. There should be two.

```
# egrep -R native *

sources/kxrkn/xiukxrkn/xiu/cmbutd/lglx.java:    public static native void a(String str);
sources/com/umeng/common/util/DeltaUpdate.java:    public static native int bspatch(String str, String str2, String str3);
```

- [x] Around the declared native method, see if there is anywhere that a native library is loaded. This will provide guidance of what native library to look in for the function to be implemented.

```java
// sources/kxrkn/xiukxrkn/xiu/cmbutd/lglx.java

public static void tt() {
    d = String.valueOf("tacd");
    System.loadLibrary("rrnad");
}
```

- [x] ~Extract the native library from the APK by creating a new dir and copying the APK into that folder. Then run the command unzip Mediacode.APK. You will see all of the files extracted from APK, which includes the lib/ directory.~

- [x] Select the architecture of the native library you’d like to analyze.

- [x] Start ghidra by running ghidraRun. This will open Ghidra.

- [x] To open the native library for analysis, select “New Project”, “Non-Shared Project”, select a path to save the project to and give it a name. This creates a project that you can then load binary files into.

- [x] Once you’ve created your project, select the dragon icon to open the Code Browser. The go to “File” > “Import File” to load the native library into the tool. You can leave all defaults.

- [x] You will see the following screen. Select “Analyze”. Loading file into Ghidra Code Browser

- [x] Using the linking information above, identify the function in the native library that is executed when the Java-declared native method is called.

The function `native_setAppkey` is registered during the `JNI_OnLoad` function call and will be called any time the `a` function from `lglx.java` is called.
