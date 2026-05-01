name: Build Android APK

on:
  push:
    branches: [ "main" ]
  workflow_dispatch: # This adds a button so you can start the build manually

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          command: buildozer android debug
          buildozer_version: stable

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: my-kivy-app
          path: bin/*.apk
