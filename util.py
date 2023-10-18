import filecmp
import logging
import os
import shutil

logger = logging.getLogger(__name__)


def migrate(file_paths, source_string, target_string):
    """
    Migrate list of files from source locations to target folders
    Since the source files to move all share the same file root and is meant to be
    moved to a new root, therefore we only need a source and target string replacement

    Example:
    Moving content files from r'C:/Desktop/UnrealProject' to r'D:/UnrealProject'

    :param file_paths: [str]. list of file paths, make sure it's normalized
    :param source_string: str. name of the shared file root for the source files
    :param target_string: str. name of the new target file root for migration
    :return: [str]. list of the file paths in target folders
    """
    target_files = list()

    for asset_path in file_paths:
        # conform target folder location
        dir_name = os.path.dirname(asset_path)
        target_dir = dir_name.replace(source_string, target_string)

        logging.info('moving %s to %s', asset_path, target_dir)
        copy_file(asset_path, target_dir)
        target_files.append(os.path.join(target_dir, os.path.basename(asset_path)))

    return target_files


def flatten_list(lst):
    """
    Flatten nested (multi-level) list to a list with one level

    :param lst: list.
    :return: list. list flattened
    """
    flattened_list = list()
    for element in lst:
        if isinstance(element, list):
            flattened_list.extend(flatten_list(element))
        else:
            flattened_list.append(element)

    return flattened_list


def copy_file(src_file, dst_folder, do_diff=False, force=True):
    """
    Copy the file from one place to the other

    :param src_file: str. source file full path
    :param dst_folder: str. destination folder full path
    :param do_diff: bool. whether to do file comparison
                    if the file content are the same, the copy operation will be skipped
    :param force: bool. whether to overwrite target file if one already exists
    :return: bool. whether the copy is successful
    """
    if not os.path.isfile(src_file):
        logger.warning('%s not located', src_file)
        return False

    if not os.path.isdir(dst_folder):
        os.makedirs(dst_folder)

    base_name = os.path.basename(src_file)
    target_file = os.path.join(dst_folder, base_name)
    if os.path.exists(target_file):
        # file already already exists we can choose to overwrite
        if not force:
            return False

        if do_diff and filecmp.cmp(src_file, target_file):
            return False

    shutil.copy(src_file, dst_folder)
    return True