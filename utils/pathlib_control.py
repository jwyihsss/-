#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023/4/25 16:16
# @Author : 谈林海
import os
import shutil
from pathlib import Path
from typing import Union, List, Tuple


class FileUtils:
    """
    文件操作封装类
    """

    @staticmethod
    def splitall(path: Union[str, Path]) -> List[str]:
        """
        分割文件路径，返回路径各层级的文件夹名和文件名
        :param path: 文件路径
        :return: List[str]
        """
        allparts = []
        path = Path(path)
        while True:
            parts = path.parts
            allparts[:0] = parts
            if path.drive or not path.parent:
                break
            path = path.parent
        return allparts

    @staticmethod
    def is_exist(path: Union[str, Path]) -> bool:
        """
        判断文件/目录是否存在
        :param path: 文件/目录路径
        :return: bool
        """
        return Path(path).exists()

    @staticmethod
    def is_dir(path: Union[str, Path]) -> bool:
        """
        判断路径是否为一个目录
        :param path: 文件/目录路径
        :return: bool
        """
        return Path(path).is_dir()

    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """
        判断路径是否为一个文件
        :param path: 文件路径
        :return: bool
        """
        return Path(path).is_file()

    @staticmethod
    def join(*paths: str) -> str:
        """
        拼接多个路径
        :param paths: 多个路径，可以传递多个参数或将路径作为列表传递
        :return: str
        """
        return os.path.join(*paths)

    @staticmethod
    def create_dir(path: Union[str, Path], exist_ok=True) -> None:
        """
        创建一个目录，如果该目录已经存在则忽略
        :param path: 目录路径
        :param exist_ok: 目录存在是否忽略判断
        :return: None
        """
        Path(path).mkdir(parents=True, exist_ok=exist_ok)

    @staticmethod
    def remove(path: Union[str, Path]) -> None:
        """
        删除一个文件或目录，可以选择是否忽略不存在的文件
        :param path: 文件/目录路径
        :return: None
        """
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            shutil.rmtree(path)
            os.mkdir(path)

    @staticmethod
    def move(src: Union[str, Path], dst: Union[str, Path], overwrite=True) -> None:
        """
        移动文件/目录
        :param src: 源文件/目录路径
        :param dst: 目标文件/目录路径
        :param overwrite: 目标路径存在是否强制覆盖，默认为 True
        :return: None
        """
        src, dst = Path(src), Path(dst)
        if not FileUtils.is_exist(src):
            raise ValueError(f"Source path '{src}' does not exist")
        if dst.exists() and not overwrite:
            raise ValueError(f"Destination path '{dst}' already exists")
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)

    @staticmethod
    def copy_file(src: Union[str, Path], dst: Union[str, Path], overwrite=True) -> None:
        """
        拷贝文件
        :param src: 源文件路径
        :param dst: 目标文件路径
        :param overwrite: 目标路径存在时是否强制覆盖，默认为 True
        :return: None
        """
        src, dst = Path(src), Path(dst)
        if not FileUtils.is_file(src):
            raise ValueError(f"'{src}' is not a file")
        if dst.exists() and not overwrite:
            raise ValueError(f"'{dst}' already exists")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    @staticmethod
    def copy_dir(src: Union[str, Path], dst: Union[str, Path], overwrite=True) -> None:
        """
        拷贝目录
        :param src: 源目录路径
        :param dst: 目标目录路径
        :param overwrite: 目标路径存在时是否强制覆盖，默认为 True
        :return: None
        """
        src, dst = Path(src), Path(dst)
        if not FileUtils.is_dir(src):
            raise ValueError(f"'{src}' is not a directory")
        if dst.exists():
            if not overwrite:
                raise ValueError(f"'{dst}' already exists")
            shutil.rmtree(str(dst))
        shutil.copytree(str(src), str(dst))

    @staticmethod
    def read_file(path: Union[str, Path], encoding="utf8") -> str:
        """
        读取文件内容
        :param path: 文件路径
        :param encoding: 文件编码，默认为utf8
        :return: str
        """
        with open(str(path), "r", encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write_file(path: Union[str, Path], content: str, encoding="utf8") -> None:
        """
        写入文件内容
        :param path: 文件路径
        :param content: 文件内容
        :param encoding: 文件编码，默认为utf8
        :return: None
        """
        with open(str(path), "w", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def append_file(path: Union[str, Path], content: Union[str, List[str]], encoding="utf8") -> None:
        """
        以追加方式写入文件内容
        :param path: 文件路径
        :param content: 追加的内容，可以是字符串或字符串列表
        :param encoding: 文件编码，默认为utf8
        :return: None
        """
        with open(str(path), "a", encoding=encoding) as f:
            if isinstance(content, list):
                for line in content:
                    f.write(line + "\n")
            else:
                f.write(content + "\n")

    @staticmethod
    def read_lines(path: Union[str, Path], strip_lines=True) -> List[str]:
        """
        读取文件所有行内容
        :param path: 文件路径
        :param strip_lines: 是否去除每行开头和结尾的空格和换行符，默认为 True
        :return: List[str]
        """
        with open(str(path), "r") as f:
            lines = f.readlines()
        if strip_lines:
            lines = [line.strip() for line in lines]
        return lines

    @staticmethod
    def write_lines(path: Union[str, Path], lines: List[str], encoding="utf8") -> None:
        """
        将列表内容写入文件，每个元素为一行
        :param path: 文件路径
        :param lines: 写入的行列表
        :param encoding: 文件编码，默认为utf8
        :return: None
        """
        with open(str(path), "w", encoding=encoding) as f:
            f.write("\n".join(lines))

    @staticmethod
    def glob_files(root_dir: Union[str, Path], pattern: str) -> List[Path]:
        """
        获取符合条件的所有文件
        :param root_dir: 目录路径
        :param pattern: 匹配模式，可以使用 * 通配符
        :return: List[Path]
        """
        return [_path for _path in Path(root_dir).rglob(pattern) if _path.is_file()]

    @staticmethod
    def get_size(path: Union[str, Path], human_readable=True) -> Union[int, str]:
        """
        获取文件或目录大小
        :param path: 文件或目录路径
        :param human_readable: 是否以可读格式返回，默认为 True
        :return: 文件大小（int类型）或以可读格式返回的文件大小（str类型）
        """
        size = sum(f.stat().st_size for f in Path(path).glob("**/*") if f.is_file())
        if human_readable:
            return FileUtils._convert_size(size)
        return size

    @staticmethod
    def _convert_size(size, precision=2) -> str:
        """
        将字节数转换为可读的文件大小格式
        :param size: 文件大小（int类型）
        :param precision: 精度，默认为2
        :return: 文件大小的可读格式（str类型）
        """
        suffixes = ["B", "KB", "MB", "GB", "TB"]
        suffix_index = 0
        while size > 1024 and suffix_index < 4:
            suffix_index += 1
            size = size / 1024.0
        return "%.*f%s" % (precision, size, suffixes[suffix_index])

    @staticmethod
    def change_suffix(path: Union[str, Path], suffix: str) -> str:
        """
        更改文件后缀名
        :param path: 文件路径
        :param suffix: 新的文件后缀名
        :return: 新的文件路径
        """
        path = Path(path)
        return path.with_suffix(suffix).as_posix()

    @staticmethod
    def get_file_info(path: Union[str, Path]) -> Tuple[str, str, Union[str, int]]:
        """
        获取文件信息
        :param path: 文件路径
        :return: (文件名称, 文件后缀名, 文件大小)
        """
        path = Path(path)
        return path.name, path.suffix, FileUtils.get_size(path)

