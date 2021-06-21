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

# -- Entry point

if (InternetCheck() != 1):
    print("Installation Failed: You're not connected to internet!")
    quit()

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
