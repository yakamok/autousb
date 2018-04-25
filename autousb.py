#!/usr/bin/python
import os
import pyudev
import getpass

mount_point = "/mnt/temp/"
rsync_com = "rsync -av "
device_name = "UUID here"
user_name = "username"
context = pyudev.Context()

if os.path.exists('/home/' + user_name + '/.bkpaths') == True:
	for device in context.list_devices():
		if 'ID_FS_UUID' in device:
			if device_name in device['ID_FS_UUID']:
				os.system('cryptsetup luksOpen UUID="' + device_name + '" atbk')
				if not os.path.exists(mount_point):
				    os.makedirs(mount_point)
				os.system('mount -t ext4 /dev/mapper/atbk ' + mount_point)
				with open("/home/" + user_name + "/.bkpaths","r") as handle:
					bkpaths = handle.readlines()
				for x in bkpaths:
					if "|||" not in x:
						if not os.path.exists(mount_point + x.split('/')[-2] + '/'):
						    os.makedirs(mount_point + x.split('/')[-2] + '/')
						os.system(rsync_com + x.replace('\n','') + " " + mount_point + x.replace('\n','').split('/')[-2] + '/')
					elif "|||" in x:
						os.system('cp ' + x.replace('\n','').replace('|||','') + ' ' + mount_point + '/')
				os.system('cp /home/' + user_name + '/.bkpaths ' + mount_point)
				os.system('pip freeze > ' + mount_point + 'python-modules')
				os.system('umount ' + mount_point)
				os.system('cryptsetup luksClose /dev/mapper/atbk')
				os.system('rm -R ' + mount_point)
