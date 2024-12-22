pyinstaller password_generator.spec

create-dmg \
  --volname "Password Demon" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Password Demon.app" 175 120 \
  --hide-extension "Password Demon.app" \
  --app-drop-link 425 120 \
  "Password Demon.dmg" \
  "dist/Password Demon.app"

