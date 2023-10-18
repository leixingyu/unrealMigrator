"""
When we want to get a certain asset/file or a folder in Unreal editor, we also
want to get all the latest dependencies of that asset/file or folder.

This commonly happens if we want to transfer/migrate files from two Unreal project/branch
that lives in separate version control system.
"""

import logging
import unreal

from unrealUtil import reference
from unrealUtil import path

from . import util

logger = logging.getLogger(__name__)


def get_dependencies_from_folder(u_folder_path):
    """
    Get all the downstream dependencies from an Unreal root folder path

    :param u_folder_path: str. Unreal folder path to look for dependencies
    :return: [str]. unique list of Unreal asset dependencies in system path
    """
    dependency_sys_paths = list()

    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    asset_datas = asset_registry.get_assets_by_path(u_folder_path)

    asset_package_paths = [asset_data.get_asset().get_outer().get_path_name()
                           for asset_data in asset_datas]

    for asset_package_path in asset_package_paths:
        dependency_sys_paths.extend(get_dependencies_from_package(asset_package_path))

    seen = set()
    # make it unique
    return [x for x in dependency_sys_paths if x not in seen and not seen.add(x)]


def get_dependencies_from_package(u_package_path):
    """
    Get all the downstream dependencies from an Unreal root asset/package path

    :param u_package_path: str. Unreal package path to look for dependencies
                           we want the outer object path of an asset
                           e.g. ('/Game/Rig/Test' instead of '/Game/Rig/Test.Test')
    :return: [str]. unique list of Unreal asset dependencies in system path
    """
    dependency_sys_paths = list()

    u_reg = unreal.AssetRegistryHelpers.get_asset_registry()

    # soft object reference asset may not exist which will cause issues
    u_options = unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=False,
        include_hard_package_references=True,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False
    )

    dependencies = reference.get_dependencies_as_list(
        u_reg,
        u_options,
        u_package_path
    )
    dependencies = util.flatten_list(dependencies)
    for dependency in dependencies:
        # this converts package path to asset full path which determines
        # if it is a folder or a file on disk
        asset = unreal.EditorAssetLibrary.find_asset_data(dependency).get_asset()
        if asset:
            u_path = asset.get_path_name()
            sys_path = path.to_sys_path(u_path)
            dependency_sys_paths.append(sys_path)
        else:
            # throw out error here
            logger.error("File doesn't exist on disk: %s", u_package_path)

    return dependency_sys_paths


if __name__ == '__main__':
    pass
