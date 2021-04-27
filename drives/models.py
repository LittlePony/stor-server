import subprocess
import json


class StorError(Exception):
    pass


class Drive:
    @staticmethod
    def get_fullname(name):
        return f'/dev/{name}'

    @staticmethod
    def get_all():
        result = subprocess.run(['lsblk', '-J', '-e7'], stdout=subprocess.PIPE)
        return json.loads(result.stdout)['blockdevices']

    @classmethod
    def umount(cls, pk):
        fullname = cls.get_fullname(pk)
        result = subprocess.run(
            ['sudo', 'umount', fullname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode:
            raise StorError(result.stderr.decode('utf-8'))

        try:
            result = subprocess.run(['lsblk', '-as', fullname, '-J'], stdout=subprocess.PIPE)
            return json.loads(result.stdout)['blockdevices'][0]
        except Exception:
            raise StorError('Device not found after succesfull umount')

    @classmethod
    def mount(cls, pk, mountpoint):
        fullname = cls.get_fullname(pk)
        result = subprocess.run(
            ['sudo', 'mount', fullname, mountpoint],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode:
            raise StorError(result.stderr.decode('utf-8'))

        try:
            result = subprocess.run(['lsblk', '-as', fullname, '-J'], stdout=subprocess.PIPE)
            return json.loads(result.stdout)['blockdevices'][0]
        except Exception:
            raise StorError('Device not found after succesfull mount')

    @classmethod
    def format(cls, pk):
        fullname = cls.get_fullname(pk)
        result = subprocess.run(
            ['sudo', 'mkfs', '-F', '-t', 'ext4', fullname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode:
            raise StorError(result.stderr.decode('utf-8'))
