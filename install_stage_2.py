import os

def append_file(name, append_data):
    with open(name, "a+") as f:

        f.seek(0)
        data = f.read(100)

        if len(data) > 0:
            f.write("\n")

        f.write(append_data)

def configure():
    region = input("Enter your region (for timezone): ")
    city   = input("Enter your city   (for timezone): ")
    os.system("ln -sf /usr/share/zoneinfo/" + region + "/" + city + " /etc/localtime")
    os.system("hwclock --systohc")
    input("Clock configuration complete! Press any key to edit /etc/locale.gen...")
    append_file("nano /etc/locale.gen")
    os.system("locale-gen")
    append_file("/etc/locale.conf", "LANG=en_US.UTF-8")
    keymap2 = input("Enter your keymap once again: ")
    append_file("/etc/vconsole.conf", "KEYMAP=" + keymap2)
    hostname = input("Enter your hostname: ")
    localdom = input("Enter your local domain: ")
    append_file("/etc/hostname", hostname)
    append_file("/etc/hosts", "127.0.0.1    localhost")
    append_file("/etc/hosts", "::1          localhost")
    append_file("/etc/hosts", "127.0.1.1    " + hostname + "." + localdom + "  " + hostname)
    print("Please enter a root user password:")
    os.system("passwd")
    usr = input("Please enter your username: ")
    os.system("useradd -m " + usr)
    os.system("usermod -aG wheel,storage,audio,video,optical " + usr)
    os.system("passwd g98")
    os.system("pacman -S sudo")
    append_file("/etc/sudoers", "%wheel ALL=(ALL) ALL")

def grub():
    os.system("pacman -S grub efibootmgr os-prober networkmanager")
    os.system("mkdir /boot/EFI")
    os.system("lsblk")
    install_disk2 = input("Enter your disk once again: ")
    os.system("mount " + install_disk2 + "1 /boot/EFI")
    os.system("grub-install --target=x86_64-efi --efi-directory=/boot/EFI --bootloader-id=GRUB --recheck")
    os.system("grub-mkconfig -o /boot/grub/grub.cfg")

def finalize():
    os.system("systemctl enable NetworkManager")
    print("IMPORTANT: Please unmount /mnt and reboot, then run stage 3")
    os.system("exit")

configure()
grub()
finalize()
