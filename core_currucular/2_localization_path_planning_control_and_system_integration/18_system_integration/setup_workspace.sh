git config --global user.email "dhr.bressers@gmail.com"
git config --global user.name "Willem Bressers"
git config --global push.default simple

ssh-keygen -t ed25519 -C "dhr.bressers@gmail.com"
cat /root/.ssh/id_ed25519.pub