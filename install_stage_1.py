# -- Sarch installer
# -- WARNING: Works only for x64 EFI based systems.

import os

keymap = ""
install_disk = ""

def InternetCheck():
    response = os.system("ping -c 1 google.com")
    if response == 0: return 1
    else:             return 0

def launch_cfdisk():
    os.system("cfdisk " + install_disk)
    if (input("Did you partition your disks correctly? (Y/n)") == "n"):
        launch_cfdisk()

def format_mount_disks():
    # Prepare partitions for mounting
    os.system("mkfs.fat -F32 " + install_disk + "1")
    os.system("mkswap " + install_disk + "2")
    os.system("mkfs.ext4 " + install_disk + "3")

    # Mount all partition aside from /dev/sd*1
    os.system("mount " + install_disk + "3 /mnt")
    os.system("swapon " + install_disk + "2")

def append_file(name, append_data):
    with open(n1ame, "a+") as f:
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
    append_file("/etc/locale.gen", "en_US.UTF-8 UTF-8")
    os.system("locale-gen")
    append_file("/etc/locale.conf", "LANG=en_US.UTF-8")
    append_file("/etc/vconsole.conf", "KEYMAP=" + keymap)
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
    os.system("mount " + install_disk + "1 /boot/EFI")
    os.system("grub-install --target=x86_64-efi --efi-directory=/boot/EFI --bootloader-id=GRUB")
    os.system("grub-mkconfig -o /boot/grub/grub.cfg")
    os.system("systemctl enable NetworkManager")

def finalize():
    os.system("exit")
    os.system("umount -R /mnt")
    print("Installation completed! Rebooting...")
    sleep(5)
    os.system("reboot")

# -- Entry point

if (InternetCheck() != 1):
    print("Installation Failed: You're not connected to internet!")
    return

keymap = input("Enter your keymap: ")
os.system("loadkeys " + keymap)
os.system("timedatectl set-ntp true")
os.system("lsblk")
install_disk = input("Enter the disk you want to install Sarch to: ")
input("Press any key to launch cfdisk on: " + install_disk)
launch_cfdisk()
format_mount_disks()
os.system("pacstrap /mnt base linux linux-firmware") # install linux base system
os.system("genfstab -U /mnt >> /mnt/etc/fstab")
os.system("arch-chroot /mnt")
configure()
grub()
finalize()
