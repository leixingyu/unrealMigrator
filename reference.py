def get_references_as_list(
    u_registry,
    u_options,
    u_asset,
    search_depth,
    filter_code=True
    ):

    storages = [u_asset]
    references = u_registry.get_referencers(
        package_name=u_asset,
        reference_options=u_options
        )

    if filter_code:
        references = [ref for ref in references
                if not str(ref).startswith('/Script')]

    if references:
        if search_depth == 1:
            storages.append(references)
        else:
            for asset in references:
                # need to go deeper
                storages.append(get_references_as_list(
                    u_registry,
                    u_options,
                    asset,
                    search_depth-1
                    )
                )

    return storages


def get_references(
    u_registry,
    u_options,
    u_asset,
    search_depth=99,
    filter_code=True,
    remove_duplicate=True,
    duplicate_lookups=list()
    ):

    storages = {u_asset: dict()}

    references = u_registry.get_referencers(
        package_name=u_asset,
        reference_options=u_options
        )

    if filter_code:
        references = [ref for ref in references
                if not str(ref).startswith('/Script')]

    if remove_duplicate:
        references = [ref for ref in references
                if ref not in duplicate_lookups]

    if references:
        duplicate_lookups.extend(references)

        if search_depth == 1:
            for asset in references:
                storages[u_asset][asset] = None
        else:
            for asset in references[:]:
                # need to go deeper
                storages[u_asset][asset] = get_references(
                    u_registry,
                    u_options,
                    asset,
                    search_depth-1,
                    filter_code,
                    remove_duplicate,
                    duplicate_lookups
                    )
                references = u_registry.get_referencers(
                    package_name=asset,
                    reference_options=u_options
                    )
                duplicate_lookups.extend(references)

    return storages

def get_dependencies_as_list(
    u_registry,
    u_options,
    u_asset,
    search_depth,
    filter_code=True
    ):

    storages = [u_asset]
    dependencies = u_registry.get_dependencies(
        package_name=u_asset,
        dependency_options=u_options
        )

    if filter_code:
        dependencies = [dep for dep in dependencies
                if not str(dep).startswith('/Script')]

    if dependencies:
        if search_depth == 1:
            storages.append(dependencies)
        else:
            for asset in dependencies:
                # need to go deeper
                storages.append(get_dependencies_as_list(
                    u_registry,
                    u_options,
                    asset,
                    search_depth-1
                    )
                )

    return storages


def get_dependencies(
    u_registry,
    u_options,
    u_asset,
    search_depth=99,
    filter_code=True,
    remove_duplicate=True,
    duplicate_lookups=list()
    ):

    storages = {u_asset: dict()}

    dependencies = u_registry.get_dependencies(
        package_name=u_asset,
        dependency_options=u_options
        )

    if filter_code:
        dependencies = [dep for dep in dependencies
                if not str(dep).startswith('/Script')]

    if remove_duplicate:
        dependencies = [dep for dep in dependencies
                if dep not in duplicate_lookups]

    if dependencies:
        duplicate_lookups.extend(dependencies)

        if search_depth == 1:
            for asset in dependencies:
                storages[u_asset][asset] = None
        else:
            for asset in dependencies[:]:
                # need to go deeper
                storages[u_asset][asset] = get_dependencies(
                    u_registry,
                    u_options,
                    asset,
                    search_depth-1,
                    filter_code,
                    remove_duplicate,
                    duplicate_lookups
                    )
                dependencies = u_registry.get_dependencies(
                    package_name=asset,
                    dependency_options=u_options
                    )
                duplicate_lookups.extend(dependencies)

    return storages
