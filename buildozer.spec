[app]
# (str) Source directory where your app lives
source.dir = .
# (str) Title of your application
title = John Pet
android.accept_sdk_license = True

# (str) Package name
package.name = johnpet

# (str) Package domain (needed for android packaging)
package.domain = org.johnpet

# (list) Source files to include (let blank to include all files)
source.include_exts = py,png

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (str) Supported orientations (portrait or landscape)
orientation = portrait

# (list) Permissions
android.permissions = SYSTEM_ALERT_WINDOW

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Indicate whether the application is a fullscreen application or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
